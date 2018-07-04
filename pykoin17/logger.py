# -*- coding: utf-8 -*-

"""
 author Ted Lazaros <tedlaz@gmail.com>
"""

import logging


frm = "%(asctime)s  %(module)s : %(levelname)s %(message)s"
# Initialize logging module, give basic formats and level we want to report
logging.basicConfig(format=frm,
                    datefmt='%H:%M:%S',
                    level=logging.INFO,
                    filename='koinoxrista.log')
# logging.basicConfig(filename='koinoxrista.log',level=logging.DEBUG)
# Get OpenShot logger and set log level
log = logging.getLogger('Koinoxrista')
log.setLevel(logging.DEBUG)
# log.setLevel(logging.CRITICAL)
