# -*- coding: utf-8 -*-
from distl import distl


def distd(val, distd, decimals=2):
    """
    Συνάρτηση κατανομής της val με βάση ένα dictionary κατανομής distd
    input parameters:
    val       : Decimal value for distribution
    distl     : Distribution Dictionary
    decimals  : Number of decimal digits
    """
    dist = {}
    sorted_keys = sorted(distd)
    print(sorted_keys)
    tmpdist_list = []
    # Create a list with distribution values
    for el in sorted_keys:
        tmpdist_list.append(distd[el])
    dist_list = distl(val, tmpdist_list, decimals)
    for i, el in enumerate(sorted_keys):
        dist[el] = dist_list[i]
    return dist

if __name__ == '__main__':
    f = {'k': 20, 'b': 10, 'c': 30, 'd': 40}
    print(distd(100, f))
