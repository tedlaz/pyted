import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from utils import info


class StreamToLogger(object):
    """Custom class to log all stdout and stderr streams"""

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

    def errors(self):
        pass

# Initialize logging module, give basic formats and level we want to report
logging.basicConfig(format="%(module)12s:%(levelname)s %(message)s",
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(module)12s:%(levelname)s %(message)s')

# Get logger instance & set level
log = logging.getLogger('pymiles')

#  Log Levels
# ------------
# CRITICAL  50
# ERROR     40
# WARNING   30
# INFO      20
# DEBUG     10
# NOTSET     0

log.setLevel(logging.INFO)

# Add rotation file handler
fh = RotatingFileHandler(os.path.join(info.USER_PATH, 'pymiles.log'),
                         encoding="utf-8",
                         maxBytes=25*1024*1024,
                         backupCount=3)
fh.setFormatter(formatter)
log.addHandler(fh)

# Route stdout and stderr to logger (custom handler)
if not getattr(sys, 'frozen', False):
    so = StreamToLogger(log, logging.INFO)
    sys.stdout = so

    se = StreamToLogger(log, logging.ERROR)
    sys.stderr = se
