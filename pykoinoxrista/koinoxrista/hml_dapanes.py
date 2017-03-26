# -*- coding: utf-8 -*-

from pymiles.sqlite import db_select as dbs
import greek_str as gs


def html_dapanes(ida, dbf):
    sql_koi = "SELECT * FROM koi WHERE id=%s" % ida
    sql_koid = "SELECT * FROM koi_d WHERE koi_id=%s ORDER BY pdate" % ida
    sql_ej = "SELECT * FROM ej ORDER BY id"
    head = dbs.select(dbf, sql_koi)['rows'][0]
    lines = dbs.select(dbf, sql_koid)['rows']
    ej = dbs.select(dbf, sql_ej)['rows']

    ht = u'<p><center><span style="font-size:14pt">'
    ht += u'<b>ΚΟΙΝΟΧΡΗΣΤΕΣ ΔΑΠΑΝΕΣ (%s)</b></span></center></p>\n' % head['koip']
    ht += u'Ημ/νία έκδοσης : %s\n' % gs.gr_date_str(head['kdat'])
    ht += u'%s' % head['sxol']
    ht += u'<table width="100%" border="0.5" cellpadding="4" cellspacing="0" style="font-size:10pt"><tbody>'
    # Create Headers
    ht += u'<tr>\n'
    ht += u' <th>Ημ/νία</th>\n'
    ht += u' <th>Παρ/κό</th>\n'
    ht += u' <th>Περιγραφή</th>\n'
    lej = len(ej)
    arej = {}
    ejt = {}
    for i, el in enumerate(ej):
        ht += u' <th>%s</th>\n' % el['ej']
        arej[el['id']] = i
        ejt[i] = 0
    ht += u'</tr>\n'

    # Fill lines
    for line in lines:
        ht += u'<tr>\n'
        ht += ' <td>%s</td>\n' % gs.gr_date_str(line['pdate'])
        ht += ' <td>%s</td>\n' % line['par']
        ht += ' <td>%s</td>\n' % line['parp']
        for el in range(lej):
            if arej[line['ej_id']] == el:
                ht += ' <td align="right">%s</td>\n' % gs.gr_num_str(line['poso'])
                ejt[el] += line['poso']
            else:
                ht += ' <td></td>\n'
        ht += u'</tr>\n'

    # Create Footer
    total = 0
    ht += u'<tr>\n'
    ht += u' <td colspan=3><center><b>Σύνολα</b></center></td>\n'
    for el in range(lej):
        ht += ' <td align="right"><b>%s</b></td>\n' % gs.gr_num_str(ejt[el])
        total += ejt[el]
    ht += u'</tr>\n'
    ht += u'<tr>\n'
    stotal = gs.gr_num_str(total)
    ht += u' <td colspan=3><center><b>ΓΕΝΙΚΟ ΣΥΝΟΛΟ</b></center></td>\n'
    ht += u' <td colspan=%s><center><b>%s</b></center></td>\n' % (lej, stotal)
    ht += u'</tr>\n'
    ht += '</tbody></table>\n'
    return ht

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    from report_viewer import view_html_report
    from html_katanomi import html_katanomi
    num = 47
    db = 'tst.sql3'
    html_brake = '<p style="page-break-after:always;">'
    h1 = html_dapanes(num, db)
    h2 = html_katanomi(num, db)

    view_html_report(h1+h2)

