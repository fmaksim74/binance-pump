#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import bncenums
from time import time
from time import sleep
from math import floor

def interval_to_milliseconds(interval):
    seconds_per_unit = {
        "s": 1,
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60,
    }
    try:
        return int(interval[:-1]) * seconds_per_unit[interval[-1]] * 1000
    except (ValueError, KeyError):
        return None

if __name__ == '__main__':
    kli = [ v // 1000 for v in [interval_to_milliseconds(v) for v in bncenums.task_intervals] if v is not None]
    print(kli)
    while True:
        m = int(0)
        t = int(time())
        for i,vs in enumerate(kli):
            if t - (t // vs) * vs == 0:
                m += 1 << i
        if m > 0:
            print('Result: {:#016b}'.format(m))
        sleep(1)
#   for i,v in enumerate(v for v in bncenums.task_intervals if ):
#       print('Index {} value {} = {}'.format(i,v, interval_to_milliseconds(v)))
