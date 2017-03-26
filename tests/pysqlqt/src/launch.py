#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
 @file
 @brief This file is used to launch application
 @author Ted Lazaros <tedlaz@gmail.com>

 @mainpage My application documentation
 Δοκιμαστικό κείμενο εδώ στα Ελληνικά
"""

import sys
from classes.logger import log
from classes import info
from classes.app import Qmain


def main():
    """Initialize settings and create main application window"""
    # Display version and exit (if requested)
    if "--version" in sys.argv:
        print("Application version : %s" % info.VERSION)
        exit()

    log.info("--------------------------------")
    log.info("    %s (version %s)" % (info.NAME, info.VERSION))
    log.info("--------------------------------")

    # Create Qt application
    app = Qmain(sys.argv)
    sys.exit(app.run())


if __name__ == '__main__':
    main()
