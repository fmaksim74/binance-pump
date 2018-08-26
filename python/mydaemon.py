#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from time import sleep
import daemon
import lockfile

def do_main():
    while True:
        sleep(0.5)

if __name__ == '__main__':
    with daemon.DaemonContext():
        pid_file = lockfile.PIDLockFile('/var/mydaemon/mydaemon.pid')
        pid_file.acquire(timeout=10)
        do_main()
