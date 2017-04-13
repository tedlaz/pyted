# -*- coding: utf-8 -*-
'''
Created on 11 Δεκ 2012

@author: tedlaz

Συνάρτηση για να κατεβάζουμε από το Internet αρχεία
που δεν υπάρχουν τοπικά.

'''
import sys
import os
import hashlib
python_version = sys.version[0]


def fsha1(file):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def download(url, directory=None):
    if not directory:
        directory = os.path.dirname(__file__)
    filename = url.split('/')[-1]
    *front, last = filename.split('.')
    oldfront = '.'.join(front) + '.' + 'old'
    oldfilename = '.'.join([oldfront, last])
    olddirfile = os.path.join(directory, oldfilename)
    dirfile = os.path.join(directory, filename)
    if os.path.exists(dirfile):
        os.rename(dirfile, olddirfile)
        print(fsha1(olddirfile))
    if python_version == '2':
        import urllib as ur
    else:
        import urllib.request as ur
    ur.urlretrieve(url, dirfile)
    print(fsha1(dirfile))


if __name__ == '__main__':
    urlfile = "http://www.ika.gr/gr/infopages/downloads/osyk.zip"
    download(urlfile)
    print('file Downloaded')
