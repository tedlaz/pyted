# -*- coding: utf-8 -*-

from pymiles.sqlite import db_select as dbs

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
print(dbs.columnames('tst.sql3', 'SELECT * FROM tss'))
rws = dbs.selectd('tst.sql3', 'SELECT * FROM ej')
for row in rws:
    print('%s %s' % (row['id'], row['ej']))

for row in rws:
    stra = ''
    for col in row:
        stra += '%s ' % col
    print(stra)
