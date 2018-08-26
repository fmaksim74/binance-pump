#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import arparse,errno,json,os,sys
from time import sleep,time

CONFIG_FILE = 'bncpump.conf'
ACTION_START = 'start'
ACTION_STOP = 'stop'
ACTION_RELOAD = 'reload'
ACTION_RESTART = 'restart'
ACTION_STATUS = 'status'
TERMINATE = False

def load_config():
    try:
        r = json.load(open(os.sep.join((os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))),CONFIG_FILE))))
    except:
        print('Binance Pump: Fatal Error: Configuration not found.')
        r = None
    finally:
        return r

def parse_command_line():
    if len(sys.argv) == 2:
        r = sys.argv[1]
        if r not in (ACTION_START,ACTION_STOP,ACTION_RELOAD,ACTION_RESTART,ACTION_STATUS):
            print('Uknown action.')
            r = None
    else:
        print('No action specified. Default action get status.')
        r = ACTION_STATUS
    return r

def signal_handler():
    global TERMINATE


    pass

if __name__ == '__main__':

    CONFIG = load_config()
    if CONFIG is None:
        exit(2)

    ACTION = parse_command_line()
    if ACTION is None:
        exit(2)

    if ACTION == ACTION_START:
        new_id = os.fork()
        if new_id == 0:
            print('Exit as parent')
            exit()
        if new_id < 0:
            print('FATAL: Daemon start failed')
            exit(2)
        if new_id > 0:

            print('Start as daemon')
            while not TERMINATE:
                sleep(0.100)
            print('Exit as daemon')

    if ACTION == ACTION_STOP:
        pass
    
    if ACTION == ACTION_START:
        pass

    if ACTION == ACTION_START:
        pass
