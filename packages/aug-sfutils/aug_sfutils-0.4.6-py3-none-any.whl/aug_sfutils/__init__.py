#!/usr/bin/env python

"""Shotfile reading with pure python

https://www.aug.ipp.mpg.de/aug/manuals/aug_sfutils

"""
__author__  = 'Giovanni Tardini (Tel. 1898)'
__version__ = '0.4.6'
__date__    = '27.10.2021'

import sys, logging

fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%H:%M:%S')
hnd = logging.StreamHandler()
hnd.setFormatter(fmt)
logger = logging.getLogger('aug_sfutils')
logger.addHandler(hnd)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

logger.info('Using version %s', __version__)

try: # wrapper classes, available only with afs-client and kerberos access
    from .ww import *
except:
    logger.warning('ww not loaded')
    pass
try:
    from .sfh import *
except:
    logger.warning('sfh not loaded')
    pass
try:
    from .journal import *
except:
    logger.warning('journal not loaded')
    pass

from .sfread import *
from .sf2equ import *
from .libddc import ddcshotnr, previousshot
from .mapeq import *

import encodings.utf_8
