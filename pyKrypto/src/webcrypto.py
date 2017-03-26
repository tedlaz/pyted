# -*- coding: utf-8 -*-
# Symmetric cryptography using a web page as a key
# The two sides deside on what web page to use as a key
# The sender encrypts the message and sends
# The receiver gives as parameters for decryption the web page and the message
# If key web page gets updated the message is useless.
# κρυπτογραφούμε το μύνημα
# Στέλνουμε το μύνημα
# Αν χρησιμοποιηθούν ιστοσελίδες με συχνή ενημέρωση θα χρειαστεί συντονισμός
# μεταξύ των επικοινωνούντων ώστε να κατεβάσουν το ίδιο κλειδί, διαφορετικά
# το μύνημα θα είναι απροσπέλαστο


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from random import choice


def get_page(url):
    response = urlopen(url, timeout=5)
    atext = response.read()
    return atext


def get_from_file(filename):
    with open(filename) as fle:
        atext = fle.read()
    return atext


def get_key_text(fileurl):
    if fileurl.startswith('http'):
        txt_key = get_page(fileurl)
    else:
        txt_key = get_from_file(fileurl)
    return txt_key.decode('utf-8')


def create_dict_of_keys(fileurl):
    txt_key = get_key_text(fileurl)
    dic_char = {}
    for i, char in enumerate(txt_key):
        tdic = []
        tdic = dic_char.get(char, [])
        tdic.append(i)
        dic_char[char] = tdic

    # Έλεγχος κατανομής χαρακτήρων
    # for key in sorted(dic_char.keys()):
    #     print('%s -> %s' % (key, len(dic_char[key])))
    return dic_char


def encrypt(urlortextfile, txt):
    dic_char = create_dict_of_keys(urlortextfile)
    encoded = ''
    for char in txt:
        if char in dic_char:
            encoded += '%s ' % choice(dic_char[char])
    return encoded


def encrypt_file(urlortextfile, afile):
    text_to_encode = get_from_file(afile)
    encrypted = encrypt(urlortextfile, text_to_encode)
    encfile = '%s.enc' % afile
    with open(encfile, 'w') as efile:
        efile.write(encrypted)


def decrypt(fileurl, encoded):
    txt_key = get_key_text(fileurl)
    lstEncoded = encoded.split()
    decoded = ''
    for el in lstEncoded:
        decoded += '%s' % txt_key[int(el)]
    return decoded


def decrypt_file(fileurl, afile):
    text_to_decrypt = get_from_file(afile)
    # print(text_to_decode)
    decrypted = decrypt(fileurl, text_to_decrypt)
    # print('edo dec', decoded)
    decfile = '%s.txt' % afile
    with open(decfile, 'w') as wfile:
        wfile.write(decrypted)


def makeArrayFromUnicode(siz=55000):
    a = u''
    for i in range(0, siz):
        a += (unichr(i))
    return a

if __name__ == '__main__':
    urlfile = 'http://dimitriskazakis.blogspot.gr'
    # urlfile = 'ttt.txt'
    # text = 'aaaaa is my name \nand i am ok'
    # encoded = encode(url, text)
    # print(encoded)
    # print(decode(urlfile, encoded))
    encrypt_file(urlfile, 'tst.txt')
    decrypt_file(urlfile, 'tst.txt.enc')
    # print(makeArrayFromUnicode())
