# -*- coding: utf-8 -*-

import decimal


def isNum(value):  # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters :
            1.value : the value to check against.
        output: True or False
        """
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """
    Always returns a decimal number. If poso is not a number or None
    returns dec(0)

    :param poso: Mumber in any format (string, float, int, ...)
    :param decimals: Number of decimals (default 2)
    :return: A decimal number rounded to decimals parameter
    """
    if poso is None:
        poso = 0
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(poso)
    else:
        tmp = decimal.Decimal('0')
    # in case of tmp = -0.00 to remove negative sign
    if tmp == decimal.Decimal(0):
        tmp = decimal.Decimal(0)
    return tmp.quantize(PLACES)


def multiply(num, alist, decim=2):
    return [dec(dec(num, decim) * dec(i, decim), decim) for i in alist]


def asum(arr1, arr2, decimals=2):
    return [dec(x + y, decimals) for x, y in zip(arr1, arr2)]


def distribute(val, distArray, decimals=2):
    """
    input parameters:
    val       : Decimal value for distribution
    distArray : Distribution Array
    decimals  : Number of decimal digits
    """
    tmpArr = []
    val = dec(val, decimals)
    try:
        tar = dec(sum(distArray), decimals)
    except Exception:
        return tmpArr
    for el in distArray:
        tmpArr.append(dec(val * dec(el, decimals) / tar, decimals))
    nval = sum(tmpArr)
    dif = val - nval  # Get the possible difference to fix round problem
    if dif == 0:
        pass
    else:
        # Max value Element gets the difference
        tmpArr[tmpArr.index(max(tmpArr))] += dif
    return tmpArr


def dic_to_lists(adic):
    return adic.keys(), adic.values()


def distribute_per_cent(array, decimals=2):
    return distribute(1, array, decimals)


def dis_round(alist, decimals=2):
    tar = dec(sum(alist), decimals)
    return distribute(tar, alist, decimals)


def dist_to_dict(val, dist_dic, decimals=2):
    """
    input parameters:
    val       : Decimal value for distribution
    dist_dic  : Distribution Dictionary
    decimals  : Number of decimal digits
    """
    keys = dist_dic.keys()
    vals = [dist_dic[key] for key in keys]
    katanomi = distribute(val, vals, decimals)
    return dict(zip(keys, katanomi))


def distxy(valdic, xyarr, flds=['x', 'y', 'val'], decimals=2):
    '''
    Distribute multiple values
    valdic : Dictionary holding values to distribute eg {'th': 230, 2: 120}
    xyarr : List of dicts holding distribution data
              eg [{'x': 'd1', 'y': 'th', 'val': 204}, κλπ]
    flds : names for x, y, val keys
    '''
    f_x = flds[0]
    f_y = flds[1]
    f_v = flds[2]
    dicv = {}  # List of dicts holding distribution arrays
    dicx = {}  # List of dicts holding x names arrays
    dicd = {}  # distributed values
    for el in xyarr:
        tv = dicv.get(el[f_y], [])
        tx = dicx.get(el[f_y], [])
        tv.append(el[f_v])
        tx.append(el[f_x])
        dicv[el[f_y]] = tv
        dicx[el[f_y]] = tx
    for vkey in valdic.keys():
        if vkey in dicx.keys():
            dicd[vkey] = distribute(valdic[vkey], dicv[vkey])
    fardic = []  # final list of dicts for return
    for dkey in dicd.keys():
        for i, el in enumerate(dicd[dkey]):
            dica = {}
            dica[f_x] = dicx[dkey][i]
            dica[f_y] = dkey
            dica[f_v] = dicd[dkey][i]
            fardic.append(dica)
    return fardic


def sumdic(key, skey, dicarr):
    '''
    key : Με βάση αυτό το κλειδί κάνουμε το άθροισμα
    skey: Το κλειδί που βρίσκονται οι τιμές που θα αθροιστούν
    dicarr : List of dictionary με τις τιμές
    '''
    fdic = {}
    for dic in dicarr:
        if (key not in dic.keys()) or (skey not in dic.keys()):
            continue
        fdic[dic[key]] = dic[skey] + fdic.get(dic[key], 0)
    return fdic


def str(dicarr):
    pass


if __name__ == '__main__':
    print(distribute(100, [10, 20, 30, 0]))
    print('\n\n')
    print(dist_to_dict(100, {'ted': 10, 'popi': 20, 'kon': 70}))
    print('\n\n')
    d = [{'x': 'd1', 'y': 'th', 'val': 204},
         {'x': 'd2', 'y': 'th', 'val': 159},
         {'x': 'd3', 'y': 'th', 'val': 243},
         {'x': 'd4', 'y': 'th', 'val': 120},
         {'x': 'd5', 'y': 'th', 'val': 274},
         {'x': 'd1', 'y': 'as', 'val': 139},
         {'x': 'd2', 'y': 'as', 'val': 108},
         {'x': 'd3', 'y': 'as', 'val': 249},
         {'x': 'd4', 'y': 'as', 'val': 122},
         {'x': 'd5', 'y': 'as', 'val': 382}
         ]
    disa = distxy({'th': 255.6, 'as': 233}, d)
    print('\ndisa')
    print(disa)
    print('\n\n')
    print(sumdic('y', 'val', disa))
    print('\n\n')
    print(sumdic('x', 'val', disa))
