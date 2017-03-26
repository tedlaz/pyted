# -*- coding: utf-8 -*-


def file2dic(afile):
    lines = ''
    dic = {}
    with open(afile) as fl:
        lines = fl.readlines()
    # Η πρώτη γραμμή περιέχει τα ονόματα των πεδίων
    for line in lines[1:]:
        if len(line) < 4:  # αποκλείουμε γραμμές με μέγεθος < 4
            continue
        alist = line.split()
        key = alist.pop(0)
        dic[key] = [i for i in alist]
    return dic


if __name__ == '__main__':
    print('Testing function file2txt ...')
    print(file2dic('xtst.txt'))
