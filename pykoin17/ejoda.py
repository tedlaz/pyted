from collections import defaultdict
import math

tmpl = """<!DOCTYPE html>
<html>
<head>
  <link href="tbl.css" rel="stylesheet"
</head>
<body>
<h1><center><span style="font-size:18pt; text-decoration:underline;"><b>{title}</b></span></center></h1>
Ημ/νία έκδοσης : {date}<br>
<table width="100%" border="1" cellpadding="1" cellspacing="0">
  <tbody>{val}  </tbody>
</table>
</body>
</html>
"""


def grnum(num, decimals=2):
    return f'{num:,.2f}'.replace(',', '|').replace('.', ',').replace('|', '.')


def create_head(headers):
    tvl = '    <tr>\n{headlines}    </tr>\n'
    tmptd = '      <th><center>{val}</center></th>\n'
    headv = ''
    for header in headers:
        headv += tmptd.format(val=header)
    return tvl.format(headlines=headv)


def create_line(line):
    tvl = '    <tr>\n{headlines}    </tr>\n'
    tleft = '      <td>{val}</td>\n'
    tcenter = '      <td><center>{val}</center></td>\n'
    tright = '      <td align="right">{val}</td>\n'
    headv = tleft.format(val=line[0])  # Ημερομηνία
    headv += tleft.format(val=line[1])  # Παραστατικό
    headv += tleft.format(val=line[2])  # Περιγραφή
    tline = grnum(line[4])
    if line[3] == 1:
        headv += tright.format(val=tline)
        headv += tright.format(val='')
        headv += tright.format(val='')
        headv += tright.format(val='')
    elif line[3] == 2:
        headv += tright.format(val='')
        headv += tright.format(val=tline)
        headv += tright.format(val='')
        headv += tright.format(val='')
    elif line[3] == 3:
        headv += tright.format(val='')
        headv += tright.format(val='')
        headv += tright.format(val=tline)
        headv += tright.format(val='')
    elif line[3] == 4:
        headv += tright.format(val='')
        headv += tright.format(val='')
        headv += tright.format(val='')
        headv += tright.format(val=tline)
    else:
        pass
    return tvl.format(headlines=headv)


def create_lines(lines):
    ftxt = ''
    dsums = defaultdict(float)
    for line in lines:
        ftxt += create_line(line)
        dsums[line[3]] += line[4]
    return ftxt, dsums


def create_total(sums):
    tvl = '    <tr>\n{headlines}    </tr>\n'
    tright = '      <td align="right"><b>{val}</b></td>\n'
    headv = '      <td colspan=3><center><b>Σύνολα</b></center></td>\n'
    headv += tright.format(val=grnum(sums[1]))
    headv += tright.format(val=grnum(sums[2]))
    headv += tright.format(val=grnum(sums[3]))
    headv += tright.format(val=grnum(sums[4]))
    return tvl.format(headlines=headv)


if __name__ == '__main__':
    par = ['Ημ/νία', 'Παρ/κό', 'Περιγραφή']
    cat = {1: 'Θέρμανση', 2: 'Ασανσέρ', 3: 'Καθαριότητα', 4: 'Λοιπά'}
    flist = par + list(cat.values())
    dat = [['2019-01-01', 'ΤΠΥ1', 'Ασανσέρ', 2, 15.45],
           ['2019-02-01', 'ΤΠΥ2', 'Ασανσέρ', 2, 16],
           ['2019-02-02', 'ΤΙΜ34', 'Πετρέλαιο', 1, 540.23],
           ['2019-01-31', 'ΑΠ14', 'Καθαριότητα Ιανουάριος 2019', 3, 50],
           ['2019-02-28', 'ΑΠ15', 'Καθαριότητα Φεβρουάριος 2019', 3, 50],
           ['2019-01-15', 'ΤΠΥ234', 'Κήπος καθαρισμός', 4, 230.45],
           ['2019-02-01', 'ΤΠΥ2', 'Ασανσέρ', 2, 16],
           ['2019-01-03', 'ΤΙΜ34', 'Πετρέλαιο', 1, 1240],
           ['2019-04-30', 'ΑΠ14', 'Καθαριότητα Απρίλιος 2019', 3, 50],
           ['2019-03-31', 'ΑΠ15', 'Καθαριότητα Μάρτιος 2019', 3, 50]]
    dat.sort(key=lambda x: x[0])
    fst = create_head(par + list(cat.values()))
    lines, sums = create_lines(dat)
    fst += lines
    fst += create_total(sums)
    title = 'ΚΟΙΝΟΧΡΗΣΤΑ 12/11/2019'
    print(tmpl.format(val=fst, title=title, date='12/11/2019'))
