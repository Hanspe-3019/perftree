# perftree
## Test

Run `python -m perftree`

See `perftree/__main__.py` 


**Expected Output**:
```
Test Run with Monitoring disabled
Pauline catched 'str' object cannot be interpreted as an integer
Overhead when monitoring is disabled: ~ 0.15 µs/call

Test finished after 2.75 secs.

Small test using/demonstrating decorator @timeit and context manager TimeIt(name)
Run time approx. 5 seconds.

Pauline catched 'str' object cannot be interpreted as an integer
Overhead when monitoring is enabled: ~ 3.27 µs/call
                                   count      elaps       /call      cpu   busy
pauline                       :       1       0.4 ms               0.4 ms   91%
    hans                      :       2 *   101.0 ms    50.5 ms    0.1 ms    0%
    peter                     :       9     383.3 ms    42.6 ms    0.4 ms    0%
    karin                     :       1     100.1 ms               0.1 ms    0%
        auguste               :       1     500.3 ms               0.1 ms    0%
inline-timer                  :       1    1876.5 ms            1839.6 ms   98%
    do_nothing                :   1.00M    1390.9 ms     1.4 µs 1422.1 ms  100%
    inline-nested             :       1    1502.6 ms               0.1 ms    0%
******************************:            5855.1 ms

Test finished after 5.86 secs.
```
