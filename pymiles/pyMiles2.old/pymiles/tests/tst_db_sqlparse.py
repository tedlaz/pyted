from pymiles.sqlite import db_sqlparse as sqp
from pymiles.sqlite.db_meta import Metadb


def compare_db_meta(db):
    tbls = sqp.return_meta(db)
    meta = Metadb()
    add_tables = []
    for table in meta._tables:
        if table not in tbls.keys():
            print(table)
            add_tables.append(table)
    return add_tables


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    db = 'tst.sql3'
    print(compare_db_meta(db))
