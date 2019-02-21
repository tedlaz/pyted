# -*- coding: utf-8 -*-

import random as r
import linecache


class krypto():
    def __init__(self, fkey='key', keyLength=5000):
        self.chars = u'''αβγδεζηθικλμνξοπρσςτυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩάΆέΈύΎίΊόΌήΉώΏ 1234567890!@#$%^&*()_+-=[]{}<>?,./|'":;qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'''
        self.cArray = []
        self.fkey = '%s' % fkey
        for c in self.chars:
            self.cArray.append(c)
        r.shuffle(self.cArray)
        self.keyLineLength = len(self.fkey)
        self.keyLines = 0
        try:
            fk = open(self.fkey, 'r')
        except:
            self.makeKey(self.fkey, keyLength)
            fk = open(self.fkey, 'r')
        try:
            i = 0
            for l in fk:
                i += 1
            self.keyLines = i
        finally:
            fk.close()

    def newKeyLine(self):
        str = u''
        r.shuffle(self.cArray)
        for c in self.cArray:
            str += c
        return str

    def makeKey(self, filekey, lines=5000):
        fkey = open(filekey, 'w', encoding="utf-8")
        for _ in range(lines):
            fkey.write(self.newKeyLine()+'\n')
        fkey.close()
        self.fkey = '%s' % filekey
        self.keyLines = lines
        print('Key created with filename %s' % filekey)
        return True

    def krypto(self, finput):
        message = open(finput)
        out = finput + '.msg'
        wf = open(out, 'w')
        # wf.write(self.fkey + '\n')
        for line in message:
            coded = ''
            uline = line[:-1].decode('utf-8')
            for c in uline:
                a = r.randint(1, self.keyLines)
                lin = linecache.getline(self.fkey, a).decode('utf-8')
                b = lin.find(c)
                coded += '%s %s ' % (a, b)
                # print 'coded,lin,a,b',coded,lin,a,b
            coded += '\n'
            wf.write(coded)
        message.close()
        wf.close()
        print('File %s coded succesfully with filename %s' % (finput, out))

    def kryptoLines(self, lines, finput):
        message = lines
        out = finput + '.msg'
        wf = open(out, 'w', encoding="utf-8")
        # wf.write(self.fkey.split('/')[-1] + '\n')
        for line in message:
            coded = ''
            uline = '%s' % line  # .decode('utf-8')
            for c in uline:
                a = r.randint(1, self.keyLines)
                lin = linecache.getline(self.fkey, a)
                b = lin.find(c)
                coded += '%s %s ' % (a, b)
                # print 'coded,lin,a,b',coded,lin,a,b
            coded += '\n'
            wf.write(coded)
        wf.close()
        print('File %s coded succesfully with filename %s' % (finput, out))

    def dekrypto(self, encryptedFile):
        with open(encryptedFile, 'r', encoding="utf-8") as ef:
            msg = ''
            for line in ef:
                d = line[:-1].split(' ')
                ln = len(d) // 2
                for idx in range(ln):
                    a = int(d[idx*2])
                    b = int(d[idx*2+1])
                    lin = linecache.getline(self.fkey, a)
                    msg += lin[b]
                msg += '\n'
        return msg

    def dekryptoToFile(self, message, fout='dekrypted.txt'):
        ef = open(message, 'r', encoding="utf-8")
        # a = self.dekrypto(message)
        fw = open(fout, 'w', encoding="utf-8")
        # fw.write(a)
        j = 0
        for line in ef:
            msg = u''
            d = line[:-1].split(' ')
            ln = len(d)/2
            for i in range(ln):
                a = int(d[i*2])
                b = int(d[i*2+1])
                lin = linecache.getline(self.fkey, a)
                msg += lin[b]
            msg += '\n'
            if j > 0:
                fw.write(msg.encode('utf-8'))
            j += 1
        ef.close()
        fw.close()
        print('Dekrypted file %s created' % fout)

if __name__ == "__main__":
    # k = krypto()
    # k.krypto('a.txt')
    # print k.dekrypto('tst.msg')
    print("pyKrypto ...")