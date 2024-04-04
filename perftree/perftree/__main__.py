'''
Small test using/demonstrating decorator @timeit and context manager TimeIt(name)
Run time approx. 5 seconds.
'''
import time
from timeit import timeit as timeit_sys
from perftree import time_it
from perftree import print_it
from perftree import TimeIt
from perftree import enable, is_enabled

def test_it():
    ' kleine Test-Routine '
    if is_enabled():
        print(__doc__)
    else:
        print('Test Run with Monitoring disabled')

    started_at = time.time()
    pauline()

    with TimeIt('inline-timer'):
        overhead = timeit_sys(do_nothing, number=10**6)

        with TimeIt('inline-nested'):
            time.sleep(1.5)

    overhead_txt = f'{"enabled" if is_enabled() else "disabled"}'
    print_it(
        header=f'Overhead when monitoring is {overhead_txt}: ~ {overhead:.2f} µs/call',
        footer=f'\nTest finished after {time.time()-started_at:.2f} secs.',
    )

# Testroutines

@time_it
def do_nothing():
    ' - '

@time_it
def hans(wait=.1):
    ' - '
    time.sleep(wait)
@time_it
def peter(wait=.1):
    ' - '
    time.sleep(wait)
@time_it
def karin(wait=.1):
    ' - '
    auguste(wait=.5)
    time.sleep(wait)
@time_it
def auguste(wait=.1):
    ' - '
    time.sleep(wait)
@time_it
def pauline(wait=.1):
    ' - '
    hans()
    for i in range(9):
        peter(wait=i*.01)
    karin()
    try:
        hans('ojeh')    # will raise TypeError
    except TypeError as exception :
        print(f'Pauline catched {exception}')
    else:
        time.sleep(wait)

if __name__ == '__main__':
    test_it()
    enable()
    test_it()
