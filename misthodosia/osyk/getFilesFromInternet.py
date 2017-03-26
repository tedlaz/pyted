# -*- coding: utf-8 -*-
'''
Created on 11 Δεκ 2012

@author: tedlaz

Συνάρτηση για να κατεβάζουμε από το Internet αρχεία
που δεν υπάρχουν τοπικά.

'''
import sys
python_version = sys.version[0]


def download(url):
    filename = url.split('/')[-1]
    print(filename)
    if python_version == '2':
        import urllib as ur
    else:
        import urllib.request as ur
    ur.urlretrieve(url, filename)


if __name__ == '__main__':
    urlfile = "http://www.ika.gr/gr/infopages/downloads/osyk.zip"
    download(urlfile)
    print('file Downloaded')
