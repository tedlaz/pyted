# -*- coding: utf-8 -*-
from f_seq import Fsequencial
'''
from f_seqm import Fseqm
from f_grid import Fgrid
from f_mdet import Fmdet
from f_find import Ffind
from f_findgrid import Ffindgrid
from f_ftree import Ftree


def newform(type, pars):
    # pars : {'table': '', 'id': 1, 'table2': '', 'parent': None, }
    # table, rid=None, dbname=None, parent=None
    if type == 'seq':
        frm = Fseq(tbl_or_sql, parent)
    elif type == 'seqm':
        frm = Fseqm(tbl_or_sql, parent)
    elif type == 'grid':
        frm = Fgrid(tbl_or_sql, parent)
    elif type == 'mdet':
        frm = Fmdet(tbl_or_sql, parent, det)
    elif type == 'find':
        frm = Ffind(tbl_or_sql, parent)
    elif type == 'findgrid':
        frm = Ffindgrid(tbl_or_sql, parent)
    elif type == 'tree':
        frm = Ftree(tbl_or_sql, parent)
    else:
        frm = None
    return frm
'''


class Wtype():
    SEQ = 1
    SEQM = 2
    GRID = 3
    MDET = 4
    FIND = 5
    FINDGRID = 6
    TREE = 7

if __name__ == '__main__':
    print(Wtype.GRID)
