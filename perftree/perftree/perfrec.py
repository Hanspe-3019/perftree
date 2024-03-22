'''Singleton Module.
'''
import time
import weakref
from dataclasses import dataclass, field

from perftree import perfout

def time_it(func):
    ''' Wrapper '''
    def wrapper(*args, **kwargs):
        PerfRec.start(func.__name__)
        try:
            rc = func(*args, **kwargs)
        except Exception as error:
            PerfRec.stop(exception=True)
            raise error

        PerfRec.stop()
        return rc

    return wrapper

def print_it(header='===', footer=None):
    ' - '
    print(header)
    if PerfRec.ROOT is None:
        return
    perfout.print_it(PerfRec.ROOT)
    if footer is not None:
        print(footer)


@dataclass
class PerfRec():
    ' - '
    # pylint: disable=too-many-instance-attributes
    name: str
    elaps: float = .0
    cpu: float = .0
    count: int = 0
    children: dict = field(default_factory=dict, repr=False)
    parent: object = field(default=None)
    started_at: float = .0
    cpu_at_start: float = .0
    exceptions: int = 0

    ROOT = None
    CURR = ROOT

    def __repr__(self):
        childrens_elaps = sum(
            child.elaps for child in self.children.values()
        )
        own_pct = 1 - (
            self.elaps - childrens_elaps
            ) / self.elaps if self.elaps > 0 else 1

        return (
            f'{self.name:20s}: '
            f'elaps={self.elaps*1000:.0f} ms ({own_pct:.1%}) '
            f'count={self.count} '
            f'num_childs={len(self.children)} '
        )
    @staticmethod
    def start(name):
        ' - '
        cls = PerfRec # Tipparbeit sparen
        if cls.ROOT is None:
            cls.init()
        # Suche `name` in `children
        try:
            perfrec = cls.CURR.children[name]
        except KeyError:
            new_rec = PerfRec(
                name=name,
                parent=weakref.ref(cls.CURR),
                started_at=time.perf_counter(),
                cpu_at_start=time.process_time()
            )
            cls.CURR.children[name] = new_rec
            cls.CURR = new_rec
        else:
            cls.CURR = perfrec
            cls.CURR.started_at = time.perf_counter()
            cls.CURR.cpu_at_start = time.process_time()

    @staticmethod
    def stop(exception=False):
        ' - '
        PerfRec.CURR.elaps += (
            time.perf_counter() - PerfRec.CURR.started_at
        )
        PerfRec.CURR.cpu += (
            time.process_time() - PerfRec.CURR.cpu_at_start
        )
        PerfRec.CURR.count += 1
        if exception:
            PerfRec.CURR.exceptions += 1

        try:
            PerfRec.CURR = PerfRec.CURR.parent()
        except TypeError:
            pass

    @staticmethod
    def init():
        ' - '
        PerfRec.ROOT = PerfRec(name='**main**')
        PerfRec.CURR = PerfRec.ROOT

class TimeIt():
    ' context manager '
    def __init__(self, name):
        self.name = str(name)
    def __enter__(self):
        PerfRec.start(self.name)
    def __exit__(self, exc_type, exc_value, exc_tb):
        PerfRec.stop(exception=exc_type is not None)
