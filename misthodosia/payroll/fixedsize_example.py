# -*- coding: utf-8 -*-

import fixedsize as fs


def main():
    t = (('1', 'i2', 'i2', 't8', 'i2', 'i2', 'i3', 't50', 't80', 't30', 't30',
          'i10', 'i9', 't50', 't10', 'i5', 't30', 'i2', 'i4', 'i2', 'i4',
          'i8', 'n12', 'n12', 'd8', 'd8', 't30'
          ),
         ('2', 'i9', 'i11', 't50', 't30', 't30', 't30', 'd8', 'i9'),
         ('3', 'n10', 't30'),
         ('EOF',)
         )
    ft = fs.Fixedtext(t)
    l = []
    l.append(('1', 1, 1, 'CSL01', 1, 1, 21, u'ΠΑΡΟΥ', u'ΑΚΤΗ ΕΠΕ', u'', u'',
              123123123, 1231, u'ΑΜΑΝ', u'34', 1442, u'ΑΝΑΦΗ', 1, 2002, 1, 220,
              12, 110.32, 34.21, '31012015', '', ''))
    for i in range(10):
        l.append(('2', 1398526, 25016702869, u'ΦΑΡΜAΚΙΔΟΥ', u'ΜΑΡΙΑ',
                  u'ΒΑΣΙΛΕΙΟΣ', u'ΑΜΑΛΙΑ', '25011967', 42856965))
    l.append(('3', 89.78, 'Kala Krasia'))
    l.append(('EOF', ))
    # txt = ft.data2text(l)
    ft.data2file(l, 'tst.txt')
    val = ft.file2data('tst.txt')
    print(val[0][8])
    # print('')
    # print(txt)
    # print('')
    # print(ft.text2data(txt))

if __name__ == '__main__':
    main()
