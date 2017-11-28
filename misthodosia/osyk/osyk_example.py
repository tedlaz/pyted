# -*- coding: utf-8 -*-


def print_arr(arr):
    txt = u''
    for line in arr:
        for col in line:
            txt += '%s ' % col
        txt += '\n'
    print(txt)

if __name__ == "__main__":
    import os
    import osyk as ok
    # import sys
    # python_version = sys.version[0]
    # if python_version == '2':
    #     reload(sys)
    #     sys.setdefaultencoding("utf-8")
    per = '201605'
    print_arr(ok.eid_kad_list('5540', per))
    print_arr([ok.kpk_find('101', per), ])
    print(ok.kadeidkpk_find('5540', '744020', per))
    print(ok.kad_find('5540'))
    print(ok.eid_find('913230'))
    print(ok.kad_find('5540'))
    # print(ok.kads('this|is|it'))
    print(ok.kadeidkpk_find('5530', '913240', per))
    sa = ok.kpk_find(ok.kadeidkpk_find('5540', '913230', per), per)
    # for e in sa:
    #     for i in e:
    #         print('%s' % i)
    #     print('')
    a = ok.kad_list('335')
    for l in a:
        print('%s %s' % (l[0], l[1]))
    # gg = ok.eid_kad_listFilteredDouble('5530')
    # for el in gg:
    #     print('%s %s' % (el[0], el[1]))
    # for el in ika_list():
    #    print el[0],el[1]
    print(os.path.dirname(os.path.realpath(__file__)))
    dirfile = os.path.dirname(__file__)
    print(os.path.exists(os.path.join(dirfile, 'osyk.zip')))
