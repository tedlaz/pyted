# -*- coding: utf-8 -*-


def iszerol(alist):
    '''
    If all elements of list are equal to zero returns True otherwise False
    '''
    for el in alist:
        if el != 0:
            return False
    return True
