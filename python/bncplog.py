# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

from logging import getLogger,Logger,Formatter
from logging.handlers import RotatingFileHandler

LOG = None
DEFAULT_LOG_FILE = "/var/log/bncpump.log"

def init_log(lname = None, fname = None, level = loggin.WARNING):
    global LOG

    if LOG: return LOG

    if not fname: fname = DEFAULT_LOG_FILE

    l = getattr(logging, level.upper())
    LOG = getLogger(name)
    LOG.setLevel(l)

    fh = RotatingFileHandler(fname,maxBytes=1024**2,backupCount=100,encoding=encodings.utf_8.getregentry().name)
    fh.setLevel(l)

    fmt = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)

    LOG.addHandler(fh)

    return LOG
