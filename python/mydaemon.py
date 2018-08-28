#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from time import sleep
import lockfile
import daemon
import daemon.pidfile
import os

def do_main():
    while True:
        sleep(0.5)

if __name__ == '__main__':
    with daemon.DaemonContext(
        uid=131,
        gid=136,
        umask=0o022,
        chroot_directory=None,
        working_directory=os.getcwd(),
        pidfile=daemon.pidfile.PIDLockFile('/var/run/binance/bncpump.pid')):
        do_main()
