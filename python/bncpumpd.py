#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import argparse,errno,json,os,sys
from pwd import getpwnam
from time import sleep,time
from daemon import DaemonContext,pidfile

TERMINATE = False

MESSAGES = {
            'CONFIG_LOAD_ERROR' : 'bncpumpd: Error: Failed to load config file {filename}. {error}',
            'GET_USER_INFO_ERROR' : 'bncpumpd: Error: Failed to read properties of user {user}. {error}',
            'PID_DIRECTORY_ERROR' : 'bncpumpd: Error: Failed to create directory for pid file {filename}. {error}'
           }

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

def load_config(fn):
    if isinstance(fn, str):
        try:
            r = json.load(open(fn))
        except Exception as e:
            print(MESSAGES['CONFIG_LOAD_ERROR'].format(filename=fn,error=e))
            r = None
        finally:
            return r

def get_user_info(user):
    try:
        return getpwnam(user)
    except Exception as e:
        print(MESSAGES['GET_USER_INFO_ERROR'].format(user=user,error=e))
        return None

def make_pid_directory(fn, uid, gid):
    r = True
    try:
        p = os.path.dirname(fn)
        os.mkdir(p)
    except Exception as e:
        if hasattr(e, 'errno') and e.errno == errno.EEXIST:
            os.chown(p, uid, gid)
        else:
            msg = MESSAGES['PID_DIRECTORY_ERROR'].format(filename=fn)
            r = False
    if not r:
        print(msg)
    return r

def signal_handler():
    global TERMINATE


    pass

def do_main():
    while True:
        sleep(0.5)

if __name__ == '__main__':
    
    ARGS = parse_args()

    CONFIG = load_config(ARGS.config)
    if CONFIG is None:
        exit(2)

    pw = get_user_info(CONFIG['DAEMON_OPTIONS']['user'])
    if pw is not None:
        CONFIG['DAEMON_OPTIONS']['user_id'] = pw.pw_uid
        CONFIG['DAEMON_OPTIONS']['group_id'] = pw.pw_gid
    else:
        exit(2)

    if not make_pid_directory(CONFIG['DAEMON_OPTIONS']['pid_file'],CONFIG['DAEMON_OPTIONS']['user_id'],CONFIG['DAEMON_OPTIONS']['group_id']):
        exit(2)
                            
    with DaemonContext(uid=CONFIG['DAEMON_OPTIONS']['user_id'],
                       gid=CONFIG['DAEMON_OPTIONS']['group_id'],
                       pidfile=pidfile.PIDLockFile(CONFIG['DAEMON_OPTIONS']['pid_file'])):
        do_main()
