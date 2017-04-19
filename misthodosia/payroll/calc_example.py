# -*- coding: utf-8 -*-
"""Module calc_example.py"""


if __name__ == '__main__':
    import calc as c
    B105 = c.Erg(50, 45.66, 18.95, False)
    B101 = c.Erg(40, 40.06, 15.5, False)

    # -----------------------------------------------
    # Nea pososta IKA
    #
    # Perigrafi        ergazomenos  Ergodotis  Synolo
    # ===============================================
    # Syntaksi             6.67       13.33     20.00
    # Perilthapsi          2.15        4.30      6.45
    # Se eidos             0.40        0.25      0.65
    # ===============================================
    # Synola               9.22       17.88     27.10
    # Epikoyriko           3.50        3.50      7.00
    # ===============================================
    # Synolo & epikoyriko 12.72       21.38     34.10
    # -----------------------------------------------
    # bnew = Erg(40, 27.1, 9.22, False)
    # print(doro_pasxa(20, 38, False))
    # par = Parousies(10)
    # prncalc(par.calc(bnew))
    # print('%s|' % fmt('ted laza', 30, 't'))
    # print('%s|' % fmt('120.836,23.15', 10, 'n'))
    c.printfor(8000, 71000, 1000, True)
    # print(foros_ak(55000))
    # print(foros_ea(23000))
    # print(oaee_etisio(24000))
    c.ek_ee(200000, 0, 0, 0, True)
    print(c.foros_eis(15052.8, 0, True))
    print(c.foros_eispar(15052.8, 0, True))
