#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import encodings

CONFIG = None
DEFAULT_CONFIG_FILE = "/etc/bncpump.conf"

def del_comments(s):
    """
    
    """
    if s[1] == '#': return ''
    for c in s:
        if c == '#':
            c = ''
            del_c = True
        if not del_c:

def load_config(fname=None):
    global CONFIG

    if not fname:
        fname = DEFAULT_CONFIG_FILE
    
    with open(fname, mode='rt', encoding=encodings.utf_8.getregentry().name) as f:
        content = [l.strip() for l in f]

    print(content)

if __name__ == '__main__':
    load_config()
