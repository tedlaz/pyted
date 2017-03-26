# -*- coding: utf-8 -*-
from math import sqrt
from listdim import listdim


def eucdist(list1, list2):
    '''
    Ευκλείδια απόσταση ανάμεσα σε δύο λίστες.
    '''
    l1, l2 = listdim(list1, list2)
    tval = 0.0
    for i in range(len(l1)):
        tval += (l1[i] - l2[i]) ** 2
    return sqrt(tval)
