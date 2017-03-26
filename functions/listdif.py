# -*- coding: utf-8 -*-
from dec import dec
from listdim import listdim


def listdif(list1, list2):
    '''
    Επιστρέφει τη διαφορά ανάμεσα στους όρους των δύο λιστών.
    '''
    'Πρώτα τις μετατρέπει σε ισοδιάστατες με τη συνάρτηση listdim'
    list1, list2 = listdim(list1, list2)
    return [dec(list1[i]) - dec(list2[i]) for i in range(len(list1))]


if __name__ == '__main__':
    print('Testing function listdif ...')
    print(listdif([10, 11, 12, 'a'], [10,11,8, 7]))
    print(listdif(20, [12, 13, 14, 15]))
    print(listdif([12, 13, 14, 15], 7))
