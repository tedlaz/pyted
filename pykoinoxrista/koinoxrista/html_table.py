# -*- coding: utf-8 -*-

t1 = '<table width="100%" border="1" cellpadding="4" cellspacing="0"><tbody>\n'


def make_labels(labels):
    html = '<tr>\n'
    for lbl in labels:
        html += ' <th>%s</th>\n' % lbl
    html += '</tr>\n'
    return html


def make_line(line):
    html = '<tr>\n'
    for col in line:
        html += ' <td>%s</td>\n' % col
    html += '</tr>\n'
    return html


def make_lines(lines):
    html = ''
    for lin in lines:
        html += make_line(lin)
    return html


def make_footer(footer):
    html = '<tr>\n'
    for el in footer:
        html += ' <td><b>%s</b></td>' % el
    html = '</tr>\n'
    return html


def table(lbls, lines, footers):
    html = t1
    html += make_labels(lbls)
    html += make_lines(lines)
    html += make_footer(footers)
    html += '</tbody></table>'
    return html


if __name__ == '__main__':
    lb = ['epo', 'ono', 'pat']
    ln = [['ted', 'lazaros', 'konnos'], ['popi', 'dazea', 'nikos']]
    ft = ['', '', '']
    print(table(lb, ln, ft))
