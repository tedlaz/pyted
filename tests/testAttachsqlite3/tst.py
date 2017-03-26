# -*- coding: utf-8 -*-


to_19 = ('Μηδέν', 'Ένα', 'Δύο', 'Τρία', 'Τέσσερα', 'Πέντε', 'Έξι',
         'Επτά', 'Οκτώ', 'Εννέα', 'Δέκα', 'Έντεκα', 'Δώδεκα',
         'Δεκατρία', 'Δεκατέσσερα', 'Δεκαπέντε', 'Δεκαέξι', 'Δεκαεπτά',
         'Δεκαοκτώ', 'Δεκαεννέα')
tens = ('Είκοσι', 'Τριάντα', 'Σαράντα', 'Πενήντα', 'Εξήντα',
        'Εβδομήντα', 'Ογδόντα', 'Ενενήντα')
huns = ('', 'Εκατόν', 'Διακόσια', 'Τριακόσια', 'Τετρακόσια', 'Πεντακόσια',
        'Εξακόσια', 'Επτακόσια', 'Οκτακόσια', 'Εννιακόσια')
denom = ('', 'Χίλια', 'Million', 'Billion', 'Trillion',
         'Quadrillion', 'Quintillion', 'Sextillion', 'Septillion',
         'Octillion', 'Nonillion', 'Decillion', 'Undecillion',
         'Duodecillion', 'Tredecillion', 'Quattuordecillion',
         'Sexdecillion', 'Septendecillion', 'Octodecillion',
         'Novemdecillion', 'Vigintillion')

def _convert_nn(val):
    """convert a value < 100 to English.
    """
    if val < 20:
        return to_19[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens)):
        if dval + 10 > val:
            if val % 10:
                return dcap + '-' + to_19[val % 10]
            return dcap

def _convert_nnn(val):
    """
        convert a value < 1000 to english, special cased because it is the level that kicks
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    word = ''
    (mod, rem) = (val % 100, val // 100)
    print(mod, rem)
    if val == 100:
        return 'Εκατό'
    if rem > 0:
        word = huns[rem]
        if mod > 0:
            word += ' '
    if mod > 0:
        word += _convert_nn(mod)
    return word

def greek_number(val):
    if val < 100:
        return _convert_nn(val)
    if val < 1000:
         return _convert_nnn(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            ret = _convert_nnn(l) + ' ' + denom[didx]
            if r > 0:
                ret = ret + ', ' + greek_number(r)
            return ret

if __name__ == '__main__':
    print(greek_number(2526))

