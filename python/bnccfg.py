#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import encodings
import json
import logging

CONFIG = None
DEFAULT_DAEMON_USER    = "binance" 
DEFAULT_CONFIG_FILE    = "/etc/bncpump.conf"
DEFAULT_PID_FILE       = "/run/binance/bncpumpd.pid"
DEFAULT_LOG_FILE       = "/var/log/binance/bncpumpd.log"
DEFAULT_LOG_LEVEL_NAME = "WARNING"
DEFAULT_LOG_LEVEL      = getattr(logging, DEFAULT_LOG_LEVEL_NAME)

def load_config(fn=None):
    
    """
    Load config from file to json object
    """
    global CONFIG

    _log = logging.getLogger()  # get current log provider

    if not (isinstance(fn, str) and len(fn) != 0):  # check file name
        fn = DEFAULT_CONFIG_FILE
    
    try:
        CONFIG = json.load(open(fn))
    except Exception as e:
        _log.exception('Failed to load config file {filename}. {error}'.format(filename=fn,error=e))
        _log.warning('Failed to load config file {filename}. Default values will be used.'.format(filename=fn))

def get_daemon_parm(pname, defval=None):
    """
    Extract a parm value from the daemon's config.
    Return defval if parm is not specified.
    """

    _log = logging.getLogger()  # get current log provider

    try:
        r = CONFIG['DAEMON_OPTIONS'][pname].strip()
    except:
        s = 'No value for the option {option}.'.format(option='DAEMON_OPTIONS/'+pname)
        if defval:
            s += 'The default value {defval} will be used'.format(defval=defval)
        _log.warning(s)
    finally:
        if not r: r = defval
        return r
    
def get_daemon_user():
    
    """
    Get daemon service user name
    """
    return get_daemon_parm('user',DEFAULT_DAEMON_USER)

def get_daemon_pid_file_name():
    """
    Get daemon pid file name
    """
    return get_daemon_parm('pid_file',DEFAULT_PID_FILE)

def get_daemon_log_file_name():
    """
    Get daemon log file name
    """
    return get_daemon_parm('log_file',DEFAULT_LOG_FILE)
    
def get_daemon_log_level_name():
    """
    Get daemon log level name
    """
    return get_daemon_parm('log_level',DEFAULT_LOG_LEVEL_NAME).upper()
    
def get_daemon_log_level_value():
    """
    Get daemon log level value
    """
    return getattr(logging, get_daemon_log_level_name())


if __name__ == '__main__':
    CONFIG = load_config()
    print(get_daemon_user())
    print(get_daemon_pid_file_name())
    print(get_daemon_log_file_name())
    print(get_daemon_log_level_name())
    print(get_daemon_log_level_value())
#   print(CONFIG)
