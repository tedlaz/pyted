#!/home/ted/.venv/sofos/bin/python3
# pip install pycrypto
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from getpass import getpass
CHUNKSIZE = 64 * 1024
EXTENSION = ".ted"
LEN_EXTENSION = len(EXTENSION)
ISIZE = 16


def encrypt(filename, outputfile=None):
    if not outputfile:
        outputfile = filename + EXTENSION
    if os.path.isfile(outputfile):
        print('File : %s already exists. Encryption Canceled' % outputfile)
        return
    key = get_key(getpass())
    filesize = str(os.path.getsize(filename)).zfill(ISIZE)
    rnd = Random.new()
    ivv = rnd.read(16)
    # for _ in range(ISIZE):
    #     ivv += chr(random.randint(0, 0xFF))
    encryptor = AES.new(key, AES.MODE_CBC, ivv)
    with open(filename, 'rb') as infile:
        with open(outputfile, 'wb') as outfile:
            outfile.write(filesize.encode())
            outfile.write(ivv)
            while True:
                chunk = infile.read(CHUNKSIZE)
                lchunk = len(chunk)
                modchunk = lchunk % ISIZE
                if lchunk == 0:
                    break
                elif modchunk != 0:
                    stra = ' ' * (ISIZE - modchunk)
                    chunk += stra.encode()
                outfile.write(encryptor.encrypt(chunk))
    print("[Done] Created encrypted file: %s" % outputfile)


def get_key(password):
    hasher = SHA256.new(password.encode())
    return hasher.digest()


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Encrypt a file")
    parser.add_argument('file', help='file to encrypt')
    parser.add_argument('-o', '--out', help='Encrypted filename', default=None)
    parser.add_argument('-v', '--version', action='version', version='1.0')
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        print('No such file : %s' % args.file)
        return
    encrypt(args.file, args.out)


if __name__ == "__main__":
    main()
