"""
 @file
 @brief This file sets the default logging settings
 @author Ted Lazaros <tedlaz@gmail.com>
 """

import logging

# Initialize logging module, give basic formats and level we want to report
logging.basicConfig(format="%(module)12s:%(levelname)s %(message)s",
                    datefmt='%H:%M:%S', level=logging.INFO)

# Get OpenShot logger and set log level
log = logging.getLogger('MyApp')
log.setLevel(logging.DEBUG)
