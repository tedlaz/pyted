# -*- coding: utf-8 -*-
from pymiles.sqlite import db_select as dbs
import greek_str as gs
import distribute2 as dis

sqlej = 'select ej_id, sum(poso) as total from koi_d where koi_id=%s group by koi_id, ej_id order by koi_id, ej_id'

sqlkat = 'SELECT dia_id, ej_id, xil FROM dia_ej'
sqlen = "SELECT * FROM ej ORDER BY id"
sqldi = "SELECT * FROM dia ORDER BY id"


def html_katanomi(idp, dbf):
    dapanes = dbs.select(dbf, sqlej % idp)['rows']
    katan = dbs.select(dbf, sqlkat, False)['rows']
    ej = dbs.select(dbf, sqlen)['rows']
    dia = dbs.select(dbf, sqldi)['rows']
    dej = []
    dejp = []
    ddi = []
    ddip = []
    dapd = {}
    dap = []
    print(dapanes)
    for el in dapanes:
        dapd[el['ej_id']] = el['total']
    for row in ej:
        dej.append(row['id'])
        dejp.append(row['ej'])
        if row['id'] in dapd.keys():
            dap.append(dapd[row['id']])
        else:
            dap.append(0)
    for row in dia:
        ddi.append(row['id'])
        ddip.append('%s %s' % (row['dno'], row['user']))
    dist = dis.Distribution(ddi, ddip, dej, dejp, katan)
    return dist.dist_html(dap, True, True)

if __name__ == '__main__':
    from report_viewer import view_html_report
    view_html_report(html_katanomi(51, 'tst.sql3'))
