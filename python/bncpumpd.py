#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import argparse,encodings,errno,json,logging,os,signal,sys
from logging import getLogger,Logger,Formatter
from logging.handlers import RotatingFileHandler
from pwd import getpwnam
from time import sleep,time
from daemon import DaemonContext,pidfile

TERMINATE = False

MESSAGES = {
            'CONFIG_LOAD_ERROR' : 'bncpumpd: Error: Failed to load config file {filename}. {error}',
            'GET_USER_INFO_ERROR' : 'bncpumpd: Error: Failed to read properties of user {user}. {error}',
            'CREATE_DIRECTORY_ERROR' : 'bncpumpd: Error: Failed to create directory for file {filename}. {error}',
            'DAEMON_START' : 'Binance Exchange data collector services starting ....'
           }

DAEMON_INFO = { 'prog': 'bncpumpd',
                'description': 'Binance Exchange data collector',
                'notice': 'NOTICE: This software is provided "as is" and any expressed or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.'
              }

ACTIONS = ('initdb','start','status','reload','stop')
LOG_LEVELS = ('notset','debug','info','warning','error','fatal')


def parse_args():
    parser = argparse.ArgumentParser(prog=DAEMON_INFO['prog'],
                                     description=DAEMON_INFO['description'],
                                     epilog=DAEMON_INFO['notice'])
    parser.add_argument('-a','--action',dest='action',default=ACTIONS[2],
                        choices=ACTIONS,
                        help="Control daemon. Deafult get status")
    parser.add_argument('-c','--config',dest='config',
                        default="/etc/bncpump.conf",
                        help='Full name of configuration file. Default /etc/bncpump.conf')
    parser.add_argument('-l','--log-level',dest='log_level',
                        choices=LOG_LEVELS[1:],
                        default=LOG_LEVELS[3],
                        help='Log detalization level. Default WARNING')
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

def make_directory(fn, uid, gid):
    r = True
    try:
        p = os.path.dirname(fn)
        os.mkdir(p)
    except Exception as e:
        if hasattr(e, 'errno') and e.errno == errno.EEXIST:
            os.chown(p, uid, gid)
        else:
            msg = MESSAGES['CREATE_DIRECTORY_ERROR'].format(filename=fn)
            r = False
    if not r:
        print(msg)
    return r

def init_daemon_log(name, fn, level):

    l = getattr(logging, level.upper())
    r = getLogger(name)
    r.setLevel(l)

    fh = RotatingFileHandler(fn,maxBytes=1024**2,backupCount=100,encoding=encodings.utf_8.getregentry().name)
    fh.setLevel(l)

    fmt = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)

    r.addHandler(fh)
    r.fatal('Log level', level, l)
    return r

def signal_handler(signum, frame):
    global TERMINATE
    if signum == signal.SIGTERM:
        LOG.info('SIGTERM signal recieved. Stopping...')
        TERMINATE = True

def DO_MAIN():
    while not TERMINATE:
        LOG.debug("I'm working")
        sleep(1)

if __name__ == '__main__':
    
    ARGS = parse_args()

    CONFIG = load_config(ARGS.config)
    if CONFIG is None:
        exit(2)

    if getattr(logging, ARGS.log_level.upper()) < getattr(logging, CONFIG['DAEMON_OPTIONS']['log_level'].upper()):
        CONFIG['DAEMON_OPTIONS']['log_level'] = ARGS.log_level

    pw = get_user_info(CONFIG['DAEMON_OPTIONS']['user'])
    if pw is not None:
        CONFIG['DAEMON_OPTIONS']['user_id'] = pw.pw_uid
        CONFIG['DAEMON_OPTIONS']['group_id'] = pw.pw_gid
    else:
        exit(2)

    if not make_directory(CONFIG['DAEMON_OPTIONS']['pid_file'],CONFIG['DAEMON_OPTIONS']['user_id'],CONFIG['DAEMON_OPTIONS']['group_id']):
        exit(2)

    with DaemonContext(uid=CONFIG['DAEMON_OPTIONS']['user_id'],
                       gid=CONFIG['DAEMON_OPTIONS']['group_id'],
                       pidfile=pidfile.PIDLockFile(CONFIG['DAEMON_OPTIONS']['pid_file']),
                       signal_map= {
                           signal.SIGTERM: signal_handler
                       }):

        if not make_directory(CONFIG['DAEMON_OPTIONS']['log_file'],CONFIG['DAEMON_OPTIONS']['user_id'],CONFIG['DAEMON_OPTIONS']['group_id']):
            exit(2)

        LOG = init_daemon_log(DAEMON_INFO['prog'],CONFIG['DAEMON_OPTIONS']['log_file'],CONFIG['DAEMON_OPTIONS']['log_level'])
        if LOG is None:
            exit(2)

        LOG.warn('Binance Exchange data collector service started')
        LOG.info('PID file {fname} created successfully.'.format(fname=CONFIG['DAEMON_OPTIONS']['pid_file']))
        LOG.info('Current process id {pid}.'.format(pid=str(os.getpid())))
        LOG.info('Log file {fname} created successfully.'.format(fname=CONFIG['DAEMON_OPTIONS']['log_file']))
        LOG.warn('Log level {l}'.format(l=CONFIG['DAEMON_OPTIONS']['log_level']))

        DO_MAIN()
        
        LOG.info('Main worker stoped.')
        try:
            os.remove(CONFIG['DAEMON_OPTIONS']['pid_file'])
        except:
            LOG.error('Cannot remove PID file {fname}'.format(fname=CONFIG['DAEMON_OPTIONS']['pid_file']))

        LOG.info('Exit')






