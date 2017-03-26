#!/usr/bin/env python3

import sys

try:
    from utils import info
    print("Loaded modules from current directory: %s" % info.PATH)
except ImportError:
    from pymiles.utils import info
    sys.path.append(info.PATH)
    print("Loaded modules from installed directory: %s" % info.PATH)

from utils.app import PyMilesApp
from utils.logger import log


def main():
    """"Initialize settings and create main window application."""

    # Display version and exit (if requested)
    if "--version" in sys.argv:
        print("pymiles version %s" % info.SETUP['version'])
        exit()

    log.info("------------------------------------------------")
    log.info("   pymiles (version %s)" % info.SETUP['version'])
    log.info("------------------------------------------------")

    # Create pymiles application
    app = PyMilesApp(sys.argv)

    # Run and return result
    sys.exit(app.run())


if __name__ == "__main__":
    main()
