# -*- coding: utf-8 -*-


def file2txt(afile):
    txt = ''
    try:
        with open(afile) as fl:
            txt = fl.read()
    except:
        pass
    return txt


if __name__ == '__main__':
    print('Testing function file2txt ...')
    print(file2txt('vatalg.py'))
