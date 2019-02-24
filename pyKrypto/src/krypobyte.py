import random as rnd
CHUNKSIZE = 4096


def bisenet(filename, keyfile, outfile):
    key = ''
    msg = ''
    cip = []
    with open(keyfile, 'br') as kfil:
        key = kfil.read()
    key_lengh = len(key)
    with open(filename, 'br') as mfil:
        msg = mfil.read()
    for i, abyt in enumerate(msg):
        keypos = i % key_lengh
        cip.append((abyt + key[keypos]) % 256)
    with open(outfile, 'bw') as ofil:
        ofil.write(bytes(cip))


def debisenet(cipherfile, keyfile, messagefile):
    key = ''
    cip = ''
    msg = []
    with open(keyfile, 'br') as kfil:
        key = kfil.read()
    key_lengh = len(key)
    with open(cipherfile, 'br') as mfil:
        cip = mfil.read()
    for i, abyt in enumerate(cip):
        keypos = i % key_lengh
        msg.append((abyt - key[keypos]) % 256)
    with open(messagefile, 'bw') as ofil:
        ofil.write(bytes(msg))    

def crypto_byte(filename, key=220):
    fil = open(filename, 'br')
    fsave = "%s.enc" % filename
    fsa = open(fsave, 'wb')
    try:
        bytes_read = fil.read(CHUNKSIZE)
        while bytes_read:
            for abyte in bytes_read:
                encoded = (abyte + key) % 256
                print(abyte, encoded)
                fsa.write(bytes([encoded])) 
            bytes_read = fil.read(CHUNKSIZE)
    finally:
        fil.close()
        fsa.close()


def derypto_byte(filename, key=220):
    fil = open(filename, 'br')
    fsave = "%s.dec" % filename
    fsa = open(fsave, 'wb')
    try:
        bytes_read = fil.read(CHUNKSIZE)
        while bytes_read:
            for abyte in bytes_read:
                encoded = (abyte - key) % 256
                print(abyte, encoded)
                fsa.write(bytes([encoded])) 
            bytes_read = fil.read(CHUNKSIZE)
    finally:
        fil.close()
        fsa.close()


def readkey(filename):
    """Returns a dict of {0: [pos1, pos2, ...], ...,255: [posa,posb, ...]}
    """
    fbyts = ''
    fdi = {i: [] for i in range(256)}  # actual key
    fds = {i: 0 for i in range(256)}  # sizes
    fdc = {i: 0 for i in range(256)}  # current position
    with open(filename, 'br') as fil:
        fbyts = fil.read()
    for i, val in enumerate(fbyts):
        fdi[val].append(i)
    for akey in fdi.keys():
        rnd.shuffle(fdi[akey])  # position is random
        fds[akey] = len(fdi[akey])
    return fdi, fds, fdc


def create_random_key(nbytes, filename):
    arr = [i % 256 for i in range(nbytes * 256)]
    rnd.shuffle(arr)
    with open(filename, 'bw') as fil:
        fil.write(bytes(arr))


def encrypt(filename, keyfile, outfile):
    """
    keydic : The dictionary with val positions
    keysizes: Dictionary with number of values per bytenumber
    keycp: Dictionary with current index position
    """
    keydic, keysizes, keycp = readkey(keyfile)
    fbyts = ""
    fval = []
    with open(filename, 'br') as fil:
        fbyts = fil.read()
    for abyt in fbyts:
        pos = keycp[abyt]
        fval.append(str(keydic[abyt][pos]))
        keycp[abyt] = (keycp[abyt] + 1) % keysizes[abyt]
    with open(outfile, "w") as ofil:
        ofil.write(' '.join(fval))


def decrypt(filename, keyfile, outfile):
    txt = ''
    with open(filename, 'r') as ifi:
        txt = ifi.read()
    fbyt = []
    pos = []
    with open(keyfile, "br") as keyf:
        pos = keyf.read()
    for val in txt.split():
        ival = int(val)
        fbyt.append(pos[ival])
    with open(outfile, 'bw') as ofi:
        ofi.write(bytes(fbyt))


def is_good_key(keyfile, atleast=2):
    _, keysizes, _ = readkey(keyfile)
    for _, val in keysizes.items():
        if val < atleast:
            print("File %s can not be used as crypto key" % keyfile)
            return False
    print("file %s can be used as crypto key" % keyfile)
    return True


if __name__ == "__main__":
    afile = "/home/ted/sofos.png"
    dfile = '%s.enc' % afile
    # crypto_byte(afile)
    # derypto_byte(dfile)
    # aaa = readkey(afile)
    # print([len(aaa[i]) for i in aaa.keys()])
    # print(aaa)
    # create_random_key(100, '/home/ted/keya')
    # aaa = readkey('/home/ted/keya')
    # print([len(aaa[i]) for i in aaa.keys()])
    # encrypt("/home/ted/aaa.txt", '/home/ted/keya', "/home/ted/aaa.enc")
    # print(is_good_key('/home/ted/keya'))
    # decrypt("/home/ted/aaa.enc", '/home/ted/keya', "/home/ted/aaa1.txt")
    # bisenet("/home/ted/aaa.txt", '/home/ted/keya', '/home/ted/aaa.biz')
    debisenet("/home/ted/aaa.biz", '/home/ted/keya', '/home/ted/aaa1.txt')
