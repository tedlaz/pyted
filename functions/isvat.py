# -*- coding: utf-8 -*-


def isvat(a):
    '''
    Αλγοριθμικός έλεγχος Ελληνικού ΑΦΜ
    '''
    assert len(a) == 9
    b = int(a[0]) * 256 + int(a[1]) * 128 + int(a[2]) * 64 + int(a[3]) * 32 + \
        int(a[4]) * 16 + int(a[5]) * 8 + int(a[6]) * 4 + int(a[7]) * 2
    c = b % 11
    d = c % 10
    # print(d)
    return d == int(a[8])


if __name__ == '__main__':
    print(isvat('800315534'))