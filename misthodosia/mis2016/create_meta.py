# -*- coding: utf-8 -*-

from pymiles.sqlite.db_create import createmeta

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    createmeta()
