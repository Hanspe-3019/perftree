' Small test using @timeit und Context Manager TimeIt'
import time
from perftree import time_it
from perftree import print_it
from perftree import TimeIt

def test_it():
    ' kleine Test-Routine '
    elaps, cpu = time.perf_counter(), time.process_time()

    pauline()

    with TimeIt('inline-timer'):
        print(
            f'elaps ={time.perf_counter()-elaps:9.3f}'
            f'  cpu ={time.process_time()-cpu:9.3f}'
        )
        with TimeIt('inline-nested'):
            time.sleep(1.5)


    print_it()

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
        peter(wait=i*.1)
    karin()
    try:
        hans('ojeh')
    except TypeError as exception :
        print(f'Pauline catched {exception}')
    else:
        time.sleep(wait)
