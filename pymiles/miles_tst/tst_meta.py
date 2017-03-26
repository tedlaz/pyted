# -*- coding: utf-8 -*-

from pymiles import u_db_meta as u_meta

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    db = 'tst1.sql3'
    tmeta = u_meta.Metadb(db)
    print(tmeta.trpr('lmo'))
    print(tmeta.db)
    print(tmeta.zf_exists)
    print(tmeta.pars('programmer'))
    print(tmeta.flbl('tr_id'))
    print(tmeta.ftype('tr_id'))
