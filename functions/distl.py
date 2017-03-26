# -*- coding: utf-8 -*-
from dec import dec


def distl(val, distl, decimals=2):
    """
    Συνάρτηση κατανομής της val με βάση μια λίστα κατανομής
    input parameters:
    val       : Decimal value for distribution
    distl     : Distribution List (eg [10, 20, 30, 40])
    decimals  : Number of decimal digits
    """
    tmpl = []
    val = dec(val, decimals)
    try:
        tar = dec(sum(distl), decimals)
    except:
        return tmpl
    for el in distl:
        tmpl.append(dec(val * dec(el, decimals) / tar, decimals))
    nval = sum(tmpl)
    dif = val - nval  # Get the possible difference to fix round problem
    if dif == 0:
        pass
    else:
        # Max value Element gets the difference
        tmpl[tmpl.index(max(tmpl))] += dif
    return tmpl
