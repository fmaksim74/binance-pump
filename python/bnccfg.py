#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import encodings
import json
import logging

CONFIG = None
# Config sections
CONFIG_SECTION_DAEMON          = "DAEMON_OPTIONS"
CONFIG_SECTION_DATABASE        = "DATABASE_OPTIONS"
CONFIG_SECTION_ACTIONS         = "STARTUP_ACTIONS"
CONFIG_SECTION_DATA_TO_COLLECT = "DATA_TO_COLLECT"
# Config fields
CONFIG_FIELD_USER              = "user"
CONFIG_FIELD_PASSWORD          = "password"
CONFIG_FIELD_PID_FILE          = "pid_file"
CONFIG_FIELD_LOG_FILE          = "log_file"
CONFIG_FIELD_LOG_LEVEL         = "log_level"
CONFIG_FIELD_HOST              = "host"
CONFIG_FIELD_PORT              = "port"
CONFIG_FILED_DATABASE          = "database"
CONFIG_FIELD_UPDATE_DB_SCHEMA  = "update_db_schema"
CONFIG_FIELD_DEFAULT           = "default"
# Config default values
DEFAULT_VALUE_CONFIG_FILE      = "/etc/bncpump.conf"
DEFAULT_VALUE_USER             = "binance" 
DEFAULT_VALUE_PASSWORD         = "" 
DEFAULT_VALUE_PID_FILE         = "/run/binance/bncpumpd.pid"
DEFAULT_VALUE_LOG_FILE         = "/var/log/binance/bncpumpd.log"
DEFAULT_VALUE_LOG_LEVEL_NAME   = "WARNING"
DEFAULT_VALUE_LOG_LEVEL        = getattr(logging, DEFAULT_LOG_LEVEL_NAME)
DEFAULT_VALUE_HOST             = "localhost"
DEFAULT_VALUE_PORT             = "5432"
DEFAULT_VALUE_DATABASE         = "binancedb"
DEFAULT_VALUE_UPDATE_DB_SCHEMA = True

def load_config(fn=None):
    
    """
    Load config from file to json object
    """
    global CONFIG

    _log = logging.getLogger()  # get current log provider

    if not (isinstance(fn, str) and len(fn) != 0):  # check file name
        fn = DEFAULT_CONFIG_FILE
    
    try:
        f = open(fn)
        CONFIG = json.load(f)
        f.close()
    except Exception as e:
        _log.exception('Failed to load config file {filename}. {error}'.format(filename=fn,error=e))
        _log.warning('Failed to load config file {filename}. Default values will be used.'.format(filename=fn))

def get_config_field(sname, fname, defval=None):
    """
    Exctract a value from config.
    """
    _log = logging.getLogger()
    r = defval

    if not (sname and fname): return None

    try:
        r = CONFIG[sname][fname].strip()
    except:
        s = 'No value for the option {option}.'.format(option=sname+'/'+pname)
        if defval:
            s += 'The default value "{defval}" will be used'.format(defval=defval)
        _log.warning(s)
    finally:
        return r

def get_daemon_user():
    
    """
    Get daemon service user name
    """
    return get_config_field(CONFIG_SECTION_DAEMON,CONFIG_FIELD_USER,DEFAULT_VALUE_USER)

def get_daemon_pid_file_name():
    """
    Get daemon pid file name
    """
    return get_config_field(CONFIG_SECTION_DAEMON,CONFIG_FIELD_PID_FILE,DEFAULT_VALUE_PID_FILE)

def get_daemon_log_file_name():
    """
    Get daemon log file name
    """
    return get_config_field(CONFIG_SECTION_DAEMON,CONFIG_FIELD_LOG_FILE,DEFAULT_VALUE_LOG_FILE)
    
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
    load_config()
    print(get_daemon_user())
    print(get_daemon_pid_file_name())
    print(get_daemon_log_file_name())
    print(get_daemon_log_level_name())
    print(get_daemon_log_level_value())
#   print(CONFIG)
