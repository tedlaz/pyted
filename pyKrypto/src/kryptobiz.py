# -*- coding: utf-8 -*-
'''
Created on 01 Φεβ 2011

@author: tedlaz
'''
import random as r

stClassicEn = u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
stClassicGr = u'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
stBasis = u'''aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ αάΑΆβΒγΓδΔεέΕΈζΖηήΗΉθΘιίϊΙΊΪκΚλΛμΜνΝξΞοόΟΌπΠρΡσςΣτΤυύΥΎφΦχΧψΨωώΩΏ1234567890.,<>?/«»\|':;¨[]{}~`!@#$%^&*()-=_+'''


def makeBizArray(str='abcd'):
    l = len(str)
    basicAlphabet = str
    ar = []
    for i in range(l):
        ar.append(basicAlphabet[i:] + basicAlphabet[:i])
    return ar


def encode(basis, key, msg):
    key_len = len(key)
    txt_len = len(msg)
    visArr = makeBizArray(basis)
    msgCoded = ''
    for i in range(txt_len):
        j = i
        if i >= key_len:
            j = i % key_len
        codeLine = key[j]
        txt_c = msg[i]
        l1 = basis.find(txt_c)
        k = visArr[0].find(codeLine)
        msgCoded += visArr[k][l1]
    return msgCoded


def decode(basis, key, msgCoded):
    key_len = len(key)
    msg_len = len(msgCoded)
    visArr = makeBizArray(basis)
    msg = ''
    for i in range(msg_len):
        j = i
        if i >= key_len:
            j = i % key_len
        codeLine = key[j]
        msg_c = msgCoded[i]
        l1 = basis.find(codeLine)
        k = visArr[l1].find(msg_c)
        msg += basis[k]
    return msg


def shuffle(stringArray):
    cArray = []
    keytxt = u''
    for c in stringArray:
        cArray.append(c)
    r.shuffle(cArray)
    for el in cArray:
        keytxt += el
    return keytxt


def makeArrayFromUnicode(siz=5000):
    a = u''
    for i in range(0, siz):
        a += (unichr(i))
    return a


def makeMessage(msg, size=5000): # size for strbasis and key
    strBasis = makeArrayFromUnicode(size)
    key = shuffle(strBasis)
    msgCoded = encode(strBasis, key, msg)
    final = key + msgCoded
    return final


def makeFileMessage(msg, fname, size=5000):
    coded = makeMessage(msg, size)
    f = open(fname, 'w')
    f.write(coded.encode('utf-8'))
    f.close()


def readMessage(msgCoded, size=5000):
    strBasis = makeArrayFromUnicode(size)
    key = msgCoded[:5000]
    msg = decode(strBasis, key, msgCoded[5000:])
    return msg


def readFileMessage(fname, size=5000):
    f = open(fname)
    coded = f.read()
    f.close()
    return readMessage(coded.decode('utf-8'), size)


if __name__ == "__main__":
    #strBasis = shuffle(makeArrayFromUnicode()) #stBasis
    #key = shuffle(strBasis)
    #print('Testing kryptobiz')
    #print('-----------------')
    #key = u'S34^&@rTRΔόκιμος cxazy:"|_-=+8965'
    #print(key.encode('utf-8'))
    #coded = encode(strBasis, key, u'2,7182818 hghj και το κρασί δωρεάν ρε φίλε')
    #print('coded message   : ' + coded)
    #print('Message Decoded : ' + decode(strBasis, key, coded))
    cm = makeMessage(u'ted εδώ είναι ωραία')
    #print(cm.encode('utf-8'))
    fm = readMessage(cm)
    #print(fm.encode('utf-8'))
    makeFileMessage(u'Με λένε θοδωρή και όλα είναι μια χαρά \n και για να δούμε τι θα πούμε ρε παιδιά εδώ σε όλους ...1234 English', 'aa.txt')
    print(readFileMessage('aa.txt'))
