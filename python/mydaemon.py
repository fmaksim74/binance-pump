#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# The Python v3.5 or later required

import logging


if __name__ == '__main__':
    print(hasattr(logging, 'FATAL'))
    print(getattr(logging, 'FATAL'))
#   logger = logging.getLogger('myapp')
#   logger.setLevel(logging.DEBUG)

#   sh = logging.StreamHandler()
#   sh.setLevel(logging.DEBUG)

#   fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#   sh.setFormatter(fmt)

#   logger.addHandler(sh)

#   logger.debug('debug message')
#   logger.info('info message')
#   logger.warn('warn message')
#   logger.error('error message')
#   logger.critical('critical message')
