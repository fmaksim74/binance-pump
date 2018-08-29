#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import errno
from time import sleep
import lockfile
import daemon
import daemon.pidfile
import os
from pwd import getpwnam
import signal

def do_main():
    while True:
        sleep(0.5)

if __name__ == '__main__':
    with daemon.DaemonContext():
        do_main()
