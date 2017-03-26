# -*- coding: utf-8 -*-

from pymiles.sqlite.db_create import create_user_db

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    create_user_db('tst.sql3')
