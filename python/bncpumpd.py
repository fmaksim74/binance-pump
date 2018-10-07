#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import argparse,encodings,errno,json,logging,os,signal,sys
from logging import getLogger,Logger,Formatter
from logging.handlers import RotatingFileHandler
from pwd import getpwnam
from time import sleep,time
from daemon import DaemonContext,pidfile
from binance.client import Client
from binance.websockets import BinanceSocketManager
from bncenums import enum_kline_intervals
from bncpgdb import BinanceDB

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

EXCHANGE_INFO = None

AGGTRADES = list()
TRADES = list()
KLINES = list()
MINITICKERS = list()
TICKERS = list()

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
    return r

def signal_handler(signum, frame):
    global TERMINATE
    if signum == signal.SIGTERM:
        LOG.info('SIGTERM recieved. Stopping...')
        TERMINATE = True

def SymbolIsTrading(symbol, data):  # data - exchange info
    for s in data['symbols']:
        if s['symbol'] == symbol and s['status'] == SYMBOL_STATUS_TRADING:
            return True
    return False

def make_wss_list():
    
    if ('symbols' in CONFIG['DATA_TO_COLLECT']) and (len(CONFIG['DATA_TO_COLLECT']['symbols']) != 0):

        for symbol in CONFIG['DATA_TO_COLLECT']['symbols']: 

            if 'symbol' in symbol and SymbolIsTrading(symbol['symbol'], EXCHANGE_INFO):

                if 'aggTrades' in symbol and symbol['aggTrades']:
                    s_name = '{s}@aggTrade'.format(s=symbol['symbol'].lower())
                    AGGTRADES.append(s_name)

                if 'trades' in symbol and symbol['trades']:
                    s_name = '{s}@trade'.format(s=symbol['symbol'].lower())
                    TRADES.append(s_name)

                if 'klines' in symbol and symbol['klines']:

                    if 'kline_intervals' in symbol:
                        _intervals = symbol['kline_intervals']

                        for i in _intervals:
                            if not i in enum_kline_intervals:
                                LOG.warning('KLine interval {i} for symbol {s} is incorrect. Skipped.'.format(i=i.lower(),s=symbol['symbol']))
                                _intervals.remove(i)

                    else:
                        _intervals = enum_kline_intervals

                    for i in _intervals:
                        s_name = '{s}@kline_{i}'.format(s=symbol['symbol'].lower(),i=i.lower())
                        KLINES.append(s_name)

                if 'miniTickers' in symbol and symbol['miniTicker']:
                    s_name = '{s}@miniTicker'.format(s=symbol['symbol'].lower())
                    MINITICKERS.append(s_name)

                if 'tickers' in symbol and symbol['ticker']:
                    s_name = '{s}@ticker'.format(s=symbol['symbol'].lower())
                    TICKERS.append(s_name)

            else:
                LOG.warning('Symbol {s} is not trading. Skipped.'.format(s=symbol['symbol']))

    else:

        if 'default' in CONFIG['DATA_TO_COLLECT']:

            _load_agg_trades = 'aggTrades' in CONFIG['DATA_TO_COLLECT']['default'] and CONFIG['DATA_TO_COLLECT']['default']['aggTrades']

            _load_trades = 'trades' in CONFIG['DATA_TO_COLLECT']['default'] and CONFIG['DATA_TO_COLLECT']['default']['trades']

            _load_klines = 'klines' in CONFIG['DATA_TO_COLLECT']['default'] and CONFIG['DATA_TO_COLLECT']['default']['klines']

            if 'kline_intervals' in CONFIG['DATA_TO_COLLECT']['default']:
                _intervals = CONFIG['DATA_TO_COLLECT']['default']['kline_intervals']

                for i in _intervals:
                    if not i in enum_kline_intervals:
                        LOG.warning('KLine interval {i} incorrect. Skipped.'.format(i=i.lower()))
                        _intervals.remove(i)
            else:
                 _intervals = enum_kline_intervals

            for symbol in EXCHANGE_INFO['symbols']: 

                if _load_agg_trades:
                    s_name = '{s}@aggTrade'.format(s=symbol['symbol'].lower())
                    AGGTRADES.append(s_name)

                if _load_trades:
                    s_name = '{s}@trade'.format(s=symbol['symbol'].lower())
                    TRADES.append(s_name)

                if _load_klines:

                    if 'kline_intervals' in symbol:
                        _intervals = symbol['kline_intervals']

                        for i in _intervals:
                            if not i in enum_kline_intervals:
                                LOG.warning('KLine interval {i} in default options is incorrect. Skipped.'.format(i=i.lower()))
                                _intervals.remove(kl)
                    else:
                        _intervals = enum_kline_intervals

                    for i in enum_kline_intervals:
                        s_name = '{s}@kline_{i}'.format(s=symbol['symbol'].lower(),i=i.lower())
                        KLINES.append(s_name)

            if 'miniTickers' in CONFIG['DATA_TO_COLLECT']['default'] and CONFIG['DATA_TO_COLLECT']['default']['miniTickers']:
                s_name = '!miniTicker@arr'
                MINITICKERS.append(s_name)

            if 'tickers' in CONFIG['DATA_TO_COLLECT']['default'] and CONFIG['DATA_TO_COLLECT']['default']['tickers']:
                s_name = '!ticker@arr'
                TICKERS.append(s_name)

#   return [data for data in [AGGTRADES, TRADES, KLINES, MINITICKERS, TICKERS] if len(data) > 0]
    return [data for data in [TICKERS, ] if len(data) > 0]
    

def DO_MAIN():
    
    global EXCHANGE_INFO

    try:
        fail_msg = "Exception occurred at database engine initialization\n"
        bncdb = BinanceDB()
        bncdb.Connect(**CONFIG['DATABASE_CONNECTION'])

        fail_msg = "Exception occurred at exchange client engine initialization\n"
        bnccli = Client('','')

        fail_msg = "Exception occurred at exchangeInfo request\n"
        EXCHANGE_INFO = bnccli.get_exchange_info()


        fail_msg = "Exception occurred at common schema update\n"
        bncdb.UpdateCommonSchema(EXCHANGE_INFO)

        fail_msg = "Exception occurred at symbols schema update\n"
        bncdb.UpdateSymbolSchema(EXCHANGE_INFO)

        fail_msg = "Exception occurred at binance socket manager initialization\n"
        bncwsm = BinanceSocketManager(bnccli)

        fail_msg = "Exception occurred at WSS streams names generation\n"
        wss_data = make_wss_list()
        LOG.debug(wss_data)

        fail_msg = "Exception occurred at WSS streams open.\n"
        conns = [ bncwsm.start_multiplex_socket(data, bncdb.wssSaveMsg) for data in wss_data ]
        bncwsm.daemon = True

        fail_msg = "Exception occurred at socket manager start"
        bncwsm.start()

        while not TERMINATE: sleep(1)

        LOG.debug("Terminating")
        fail_msg = "Exception occurred at connections close\n"
        for conn in conns: bncwsm.stop_socket(conn)
        LOG.debug("Stopping connection manager")
        bncwsm.close()

    except:
        LOG.exception(fail_msg)

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
    
        LOG.info('Binance Exchange data collector service started')
        LOG.info('PID file {fname} created successfully.'.format(fname=CONFIG['DAEMON_OPTIONS']['pid_file']))
        LOG.info('Current process id {pid}.'.format(pid=str(os.getpid())))
        LOG.info('Log file {fname} created successfully.'.format(fname=CONFIG['DAEMON_OPTIONS']['log_file']))
        LOG.info('Log level {l}'.format(l=CONFIG['DAEMON_OPTIONS']['log_level']))
    
        DO_MAIN()
        
        LOG.info('Main worker stoped.')
        try:
            os.remove(CONFIG['DAEMON_OPTIONS']['pid_file'])
        except:
            LOG.error('Cannot remove PID file {fname}'.format(fname=CONFIG['DAEMON_OPTIONS']['pid_file']))
    
        LOG.info('Exit')
