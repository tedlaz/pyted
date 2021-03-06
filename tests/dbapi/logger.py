# -*- coding: utf-8 -*-

"""
 author Ted Lazaros <tedlaz@gmail.com>
"""

import logging

#  Log Levels
# ------------
# CRITICAL  50
# ERROR     40
# WARNING   30
# INFO      20
# DEBUG     10
# NOTSET     0

frm = "%(asctime)s  %(module)s : %(levelname)s %(message)s"
# Initialize logging module, give basic formats and level we want to report
logging.basicConfig(format=frm,
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
#                    filename='koinoxrista.log')
# logging.basicConfig(filename='koinoxrista.log',level=logging.DEBUG)
# Get OpenShot logger and set log level
log = logging.getLogger('Koinoxrista')
log.setLevel(logging.DEBUG)
