# -*- coding: utf-8 -*-
# Υπολογισμός μισθοδοσίας


def getpar(xrisi, period, apo, eos):
    e1 = {'id': 1, 'aptyp': 1, 'pika': 40.06, 'pikan': 15.5, 'ap': 32.35}
    e2 = {'id': 2, 'aptyp': 1, 'pika': 40.06, 'pikan': 15.5, 'ap': 46}
    vals = [[1, e1, {'mer': 15}], [2, e2, {'mer': 22}]]
    return vals


def miscalc(xrisi, period, type=1):
    data = getpar(xrisi, period, apo, eos)
    res = []
    for el in data:
        rd = {}
        e
