# -*- coding: utf-8 -*-
from report_viewer import view_html_report
import greek_str as gs

html_tabl = '''<table width="100%%" border="1" cellpadding="4" cellspacing="0">
 <tbody>
%s </tbody>
</table>'''

html_tabll = '  <tr>\n%s  </tr>\n'
html_title = '   <td><center><b>%s</b></center></td>\n'
html_val = '   <td align="right">%s</td>\n'
html_tot = '   <td align="right"><b>%s</b></td>\n'
html_text = '   <td>%s</td>\n'


def create_html_table(columns, rows):
    # create table headers here
    htmlh = html_text % ''
    ctot = []
    for col in columns:
        htmlh += html_title % col
        ctot.append(0)
    htmlh += html_title % u'Σύνολα'

    htmlr = html_tabll % htmlh
    for row in rows:
        htmll = ''
        rowt = 0
        for i, col in enumerate(row):
            if i == 0:
                htmll += html_text % col
            else:
                htmll += html_val % gs.greek_num_str(col)
                rowt += col
                ctot[i-1] += col
        htmll += html_tot % gs.greek_num_str(rowt)
        htmlr += html_tabll % htmll

    # create totals row here
    htmlt = html_title % u'Σύνολα'
    for i, col in enumerate(columns):
        htmlt += html_tot % gs.greek_num_str(ctot[i])
    htmlt += html_tot % gs.greek_num_str(sum(ctot))
    htmlr += html_tabll % htmlt
    final = html_tabl % htmlr
    return final


if __name__ == '__main__':
    html_h = u'<p><center>'
    html_h += u'<span style="font-size:12pt; text-decoration:underline;">'
    html_h += u'<b>ΚΟΙΝΟΧΡΗΣΤΑ ΑΝΑ ΔΙΑΜΕΡΙΣΜΑ</b></span>'
    html_h += u'</center><p>'
    html_h += u'Περίοδος : 3ο Τετράμηνο 2015<br>'
    html_h += u'Ημ/νία έκδοσης : 13/12/2015<br>'
    cols = [u'Θέρμανση', u'Ασανσέρ', u'Καθαριότητα']
    ros = [[u'Διαμέρισμα 1', 12, 13, 10],
           [u'Διαμέρισμά 2', 11, 7, 5],
           [u'Διαμέρισμά 3', 1, 2, 3],
           [u'Διαμέρισμά 4', 4, 5, 6],
           [u'Διαμέρισμά 5', 7, 8, 9],
           [u'Διαμέρισμά 6', 10, 11, 12]
           ]
    html = html_h + create_html_table(cols, ros)
    view_html_report(html)
