# -*- coding: utf-8 -*-
from dec import dec
from listdim import listdim


def listadd(list1, list2):
    '''
    Επιστρέφει το άθροισμα ανάμεσα στους όρους των δύο λιστών.
    '''
    'Πρώτα τις μετατρέπει σε ισοδιάστατες με τη συνάρτηση listdim'
    list1, list2 = listdim(list1, list2)
    return [dec(list1[i]) + dec(list2[i]) for i in range(len(list1))]
