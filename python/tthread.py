#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import threading

class TerminatableThread(threading.Thread):

    terminate = False

if __name__ == '__main__':
    exit()
