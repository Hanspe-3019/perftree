'''Singleton Module.
'''
import time
import weakref
from dataclasses import dataclass, field

from perftree import perfout

def time_it(func):
    ''' Decorator to collect start and stop timing of decorated functions
    
    Not useful for generator functions. Decorating a generator function
    will only measure building of the generator object. Use context manager to
    monitor the generator, simple example:

    def demo():
        for i in range(1000):
            with perftree.TimeIt('yielding'):
                # do some work
                time.sleep(.1)

            yield str(i * i)
    
    '''
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

def print_it(header='\n', footer=None):
    ''' print performance measurements collected,
    wraps "real" print_it with optional heaader and footer'''
    print(header)
    if PerfRec.ROOT is None:
        return
    perfout.print_it(PerfRec.ROOT)
    if footer is not None:
        print(footer)

def reset():
    ' reinitialize the tree, returns previous tree'
    previous = PerfRec.ROOT
    PerfRec.init()
    return previous

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

    @staticmethod
    def start(name):
        ' starts measurment, initializes the tree if necessary '
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
        ''' stops the measurement and sets CURR to current node's parent  
        '''
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
        ' class var ROOT gets initialized with dummy node, CURR is set to ROOT '
        PerfRec.ROOT = PerfRec(name='**main**')
        PerfRec.CURR = PerfRec.ROOT

class TimeIt():
    ''' Context manager to monitor a block of statements
        with TimeIt('a code block'):
            func1()
            func2()
        func3('not measured')
    '''
    def __init__(self, name):
        self.name = str(name)
    def __enter__(self):
        PerfRec.start(self.name)
    def __exit__(self, exc_type, exc_value, exc_tb):
        PerfRec.stop(exception=exc_type is not None)
