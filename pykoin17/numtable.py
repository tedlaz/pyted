# -*- coding: utf-8 -*-
import decimal


def isNum(value):  # Einai to value arithmos, i den einai ?
    """
    use: Returns False if value is not a number , True otherwise
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
    """ use : Given a number, it returns a decimal with a specific number
        of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or
                int ..)
            2.decimals : The number of decimals (default 2)
        output: A decimal number
        """
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


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


def dist_d(val, dist_dic, decimals=2):
    dist = {}
    sorted_keys = sorted(dist_dic)
    tmpdist_list = []
    # Create a list with distribution values
    for el in sorted_keys:
        tmpdist_list.append(dist_dic[el])
    if sum(tmpdist_list) != 1000:
        print("Distribution total is not 1000")
    dist_list = distribute(val, tmpdist_list, decimals)
    for i, el in enumerate(sorted_keys):
        dist[el] = dist_list[i]
    return dist


class ntable():

    def __init__(self):
        self.title = u'Κοινόχρηστα'
        self.subtitle = u'3ο Τετράμηνο 2015'
        self.column_headers = {1: u'Θέρμανση',
                               2: u'Ασανσέρ',
                               3: u'Καθαριότητα',
                               4: u'Αποχέτευση'}
        self.row_headers = {1: u'Φροντιστήριο',
                            2: u'Νικολόπουλος-Μάρδα',
                            3: u'Καλυβιώτης',
                            4: u'Νεοπούλου',
                            5: u'Αχλάδη',
                            6: u'Λάζαρος'}
        self.xiliosta = {1: {2: 204, 3: 159, 4: 243, 5: 120, 6: 274},
                         2: {2: 139, 3: 108, 4: 249, 5: 122, 6: 382},
                         3: {2: 204, 3: 159, 4: 243, 5: 120, 6: 274},
                         4: {1: 270, 2: 150, 3: 115, 4: 178, 5: 87, 6: 200}
                         }
        self.posa = {1: 800, 2: 100}
        self.distribution = {}

    def get_dist(self, y, x):
        if y in self.distribution.keys():
            ydist = self.distribution[y]
            if x in ydist.keys():
                return ydist[x]
        return dec(0)

    def row_list(self):
        return sorted(self.row_headers.keys())

    def row_titles(self):
        lst = []
        for key in self.row_list():
            lst.append(self.row_headers[key])
        return lst

    def column_list(self):
        return sorted(self.column_headers.keys())

    def col_titles(self):
        lst = []
        for key in self.column_list():
            lst.append(self.column_headers[key])
        return lst

    def distribute(self):
        self.distribution = {}
        for key in self.posa.keys():
            self.distribution[key] = dist_d(self.posa[key], self.xiliosta[key])

    def print_dist(self):
        self.distribute()
        print(', '.join(self.column_headers.values()))
        for col in self.column_list():
            pass


if __name__ == '__main__':
    a = ntable()
    a.print_dist()
    print(a.get_dist(10, 23))
