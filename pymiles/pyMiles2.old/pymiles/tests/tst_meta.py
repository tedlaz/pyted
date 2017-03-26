# -*- coding: utf-8 -*-

from pymiles.sqlite.db_meta import Metadb

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    meta = Metadb()
    '''
    print(meta._flbl['epo'])
    print(meta.labels_from_fields(['epo', 'id', 'ono']))
    print(meta.sql_all('pros'))
    print(meta.table_fields('ika'))
    print(meta._ftyp['epo'])
    print(meta.sql_all('erg'))
    print(meta.sql_rpr('pros'))
    '''
    print(meta.rpr('trd'))
