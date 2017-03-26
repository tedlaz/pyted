# -*- coding: utf-8 -*-

import decimal


def dec(poso=0, decimals=2):
    """ use : Given a number, it returns a decimal with a specific number
        of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or
                int ..)
            2.decimals : The number of decimals (default 2)
        output: A decimal number
        """
    def isNum(value):  # Einai to value arithmos, i den einai ?
        try:
            float(value)
        except ValueError:
            return False
        else:
            return True

    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')

    return tmp.quantize(PLACES)
