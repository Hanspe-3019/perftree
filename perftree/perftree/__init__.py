''' imports 
decorator @time_it to monitor execution of functions
Context Manager  TimeIt to monitor block of statements
function print_it to dump the performance tree to stdout

Usage: see code in test_it.py – Run it with:
    % python -c 'from perftree.test_it import test_it as t; t()'
'''
from .perfrec import time_it
from .perfrec import print_it
from .perfrec import TimeIt
from .perfrec import reset
__all__ = ('time_it', 'print_it', 'TimeIt', 'reset')
