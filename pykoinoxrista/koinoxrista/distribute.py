# -*- coding: utf-8 -*-

from pymiles.utils.txt_num import dec


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
    except:
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


def dist_to_dict(val, dist_dic, decimals=2):
    """
    input parameters:
    val       : Decimal value for distribution
    dist_dic  : Distribution Dictionary
    decimals  : Number of decimal digits
    """
    keys = dist_dic.keys()
    arr = []
    farr = []  # For distributed values temporary store
    fdic = {}
    for key in keys:
        arr.append(dist_dic[key])
    farr = distribute(val, arr, decimals)
    for i, val in enumerate(farr):
        fdic[keys[i]] = val
    return fdic


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
    print(dist_to_dict(100, {'ted': 10, 'popi': 20, 'kon': 30}))
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
