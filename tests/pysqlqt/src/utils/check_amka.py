# -*- coding: utf-8 -*-

'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''


def Validate_amka(amka):
    if len(amka) != 11 or (amka.isdigit() is False):
        return False

    tsum = int(amka[10])
    i = 0
    for s in amka[0:10]:
        if (i % 2) != 0:
            if int(s) * 2 > 9:
                tsum += int(str(int(s) * 2)[0]) + int(str(int(s) * 2)[1])
            else:
                tsum += int(s)* 2
        else:
            tsum += int(s)
            i = i + 1
    if tsum % 10 == 0:
        return True
    else:
        return False

if __name__ == '__main__':
    print(Validate_amka('04068915026'))
