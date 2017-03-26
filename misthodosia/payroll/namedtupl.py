# -*- coding: utf-8 -*-
# How to use namedtuple

from collections import namedtuple as nt


class Erg():
    def __init__(self):
        self.epo = ''
        self.ono = ''
        self.pat = ''
        self.mit = ''
        self.klp = ''

    def save(self):
        pass


def test():
    '''A short description Here ...

    input parameters
      put pars here

    returns
      returns here
    '''
    Erg = nt('Erg', 'epo, ono, pat, mit')
    ted = Erg('Laz', 'Ted', 'Kon', 'Stav')
    print(ted)
    print(ted.epo)


if __name__ == '__main__':
    test()
