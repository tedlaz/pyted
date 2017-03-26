# -*- coding: utf-8 -*-

from pymiles.utils.txt_num import dec


def distribute(val, distArray, decimals=2):
    """
    input parameters:
    val       : Decimal value for distribution
    distArray : Distribution Array
    decimals  : Number of decimal digits
    """
    tmpArr = []
    val = dec(val, decimals)
    try:
        tar = dec(sum(distArray), decimals)
    except:
        return tmpArr
    for el in distArray:
        tmpArr.append(dec(val * dec(el, decimals) / tar, decimals))
    nval = sum(tmpArr)
    dif = val - nval  # Get the possible difference to fix round problem
    if dif == 0:
        pass
    else:
        # Max value Element gets the difference
        # tmpArr[tmpArr.index(max(tmpArr))] += dif
        tmpArr[distArray.index(max(distArray))] += dif
    return tmpArr


def distribute2d(vals, distArrays, decimals=2, totals=True):
    assert len(vals) == len(distArrays)
    clen = len(distArrays[0])
    # be sure we have same number of elements to distribute
    for el in distArrays:
        assert clen == len(el)
    matrix = []
    for i, val in enumerate(vals):
        disted = distribute(val, distArrays[i])
        sdisted = sum(disted)
        assert sdisted == dec(vals[i])
        if totals:
            disted.append(sdisted)
        matrix.append(disted)
    fdist = list(zip(*matrix))
    finalv = []
    for row in fdist:
        trow = []
        for col in row:
            trow.append(col)
        if totals:
            trow.append(sum(row))
        finalv.append(trow)
    return finalv


def pretty_print_matrix(matrix):
    stra = ''
    for row in matrix:
        for col in row:
            stra += '%12s ' % col
        stra += '\n'
    print(stra)


class Xydata():

    def __init__(self, data):
        for el in data:
            assert len(el) == 3
        self.datas = data

    def val(self, x, y):
        for row in self.datas:
            if (x == row[0]) and (y == row[1]):
                    return row[2]
        return 0


h_tbl = '''<table width="100%%" border="1" cellpadding="4" cellspacing="0">
 <tbody>
%s </tbody>
</table>'''
h_tbll = '  <tr>\n%s  </tr>\n'
h_title = '   <td><center><b>%s</b></center></td>\n'
h_val = '   <td align="right">%s</td>\n'
h_tot = '   <td align="right"><b>%s</b></td>\n'
h_txt = '   <td>%s</td>\n'


class Distribution():

    '''
    Class to make easier distribution
    '''

    def __init__(self, rows, rowh, cols, colh, distdata):
        self.rows = rows
        self.rowheaders = rowh
        self.cols = cols
        self.colheaders = colh
        self.fixdata(distdata)

    def fixdata(self, distdata):
        self.dista = []
        self.ddata = Xydata(distdata)
        for col in self.cols:
            tmpa = []
            for row in self.rows:
                tmpa.append(self.ddata.val(row, col))
            self.dista.append(tmpa)

    def dist(self, vals, atotals=False):
        return distribute2d(vals, self.dista, totals=atotals)

    def run_str(self, vals, atotals=False):
        dist = self.dist(vals, atotals)
        colsize = '%10s '
        rowheadsize = '%14s '
        stra = rowheadsize % 'Διαμερίσματα'
        for col in self.colheaders:
            stra += colsize % col
        if atotals:
            stra += colsize % 'Σύνολο'
        stra += '\n'
        for i, row in enumerate(self.rowheaders):
            stra += rowheadsize % row
            for col in dist[i]:
                stra += colsize % col
            stra += '\n'
        if atotals:
            tlineno = len(dist) - 1
            stra += rowheadsize % 'Totals'
            for col in dist[tlineno]:
                stra += colsize % col
            stra += '\n'
        return stra

    def dist_html(self, vals, atotals=False, indist=False):
        tr = u'<tr>\n'
        trs = u'</tr>\n'
        th = u' <th>%s</th>\n'
        tha = u' <th colspan=2>%s</th>\n'
        thb = u' <th rowspan=2>%s</th>\n'
        td = u' <td>%s</td>\n'
        tdb = u' <td><b>%s</b></td>\n'
        tdbc = u' <td><center><b>%s</b></center></td>\n'
        tdr = u' <td align="right">%s</td>\n'
        tdrb = u' <td align="right"><b>%s</b></td>\n'

        html = u'<table width="100%" border="0.5" cellpadding="4" cellspacing="0" style="font-size:10pt"><tbody>'
        dist = self.dist(vals, atotals)

        html += tr
        html += thb % u'Διαμερίσματα'
        for col in self.colheaders:
            if indist:
                html += tha % col
            else:
                html += th % col
        if atotals:
            html += thb % u'Σύνολο'
        html += trs

        if indist:
            html += tr
            for col in self.colheaders:
                html += th % u'Χιλιοστά'
                html += th % u'Ποσό'
            html += trs

        for i, row in enumerate(self.rowheaders):
            html += tr
            html += td % row
            lendi = len(dist[i])
            for j, col in enumerate(dist[i]):
                if atotals:
                    if j == lendi-1:
                        html += tdrb % col
                    else:
                        html += tdr % self.dista[j][i]
                        html += tdr % col
                else:
                    html += tdr % self.dista[i][j]
                    html += tdr % col
            html += trs

        if atotals:
            tlineno = len(dist) - 1
            html += tr
            html += tdbc % u'Σύνολα'
            for i, col in enumerate(dist[tlineno]):
                if indist:
                    if i < lendi-1:
                        html += tdrb % ''
                    html += tdrb % col
                else:
                    html += tdrb % col
            html += trs
        return html + '</tbody></table>'

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    rws = [1, 2, 3, 4, 5, 6]
    rwh = ['fro', 'd1', 'd2', 'd3', 'd4', 'laz']
    clm = [1, 2, 3, 4]
    clh = ['thermansi', 'asanser', 'kipos', 'Loipa']
    dd = [[2, 1, 204],
          [3, 1, 159],
          [4, 1, 243],
          [5, 1, 120],
          [6, 1, 274],
          [2, 2, 139],
          [3, 2, 108],
          [4, 2, 249],
          [5, 2, 122],
          [6, 2, 382],
          [2, 3, 204],
          [3, 3, 159],
          [4, 3, 243],
          [5, 3, 120],
          [6, 3, 274],
          [1, 4, 270],
          [2, 4, 150],
          [3, 4, 115],
          [4, 4, 178],
          [5, 4, 87],
          [6, 4, 200]
          ]
    dis = Distribution(rws, rwh, clm, clh, dd)
    print(dis.dist_html([-20, 0.01, 222.79, 0.01], True))
