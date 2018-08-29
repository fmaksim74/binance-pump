#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import argparse
from time import sleep

DAEMON_INFO = { 'prog': 'bncpumpd.py',
                'description': 'Binance Exchange data collector',
                'notice': 'NOTICE: This software is provided "as is" and any expressed or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.'
              }

def parse_args():
    parser = argparse.ArgumentParser(prog=DAEMON_INFO['prog'],
                                     description=DAEMON_INFO['description'],
                                     epilog=DAEMON_INFO['notice'])
    parser.add_argument('-a','--action',dest='action',default="status",
                        choices=('initdb','start','status','reload','stop'),
                        help="Control daemon. Deafult get status")
    parser.add_argument('-c','--config',dest='config',
                        default="/etc/bncpump.conf",
                        help='Full name of configuration file. Default /etc/bncpump.conf')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print(args.config)
    print(args.action)
    while True:
       sleep(1) 
