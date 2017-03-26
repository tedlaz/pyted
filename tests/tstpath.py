import os
import sys
# Connect my path here
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from functions import dbsqlite

dbsqlite.test()
