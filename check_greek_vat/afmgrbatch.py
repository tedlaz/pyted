"""
Validate many vat numbers at once !!!
Just pass a file with a row per vat number
"""
import time
from afmgr import isvat, vatol


def delay(counter, step=1):
    '''
    if step=1 counter = seconds
    '''
    for i in range(counter):
        print(i + step, end=" ", flush=True)
        time.sleep(step)
    print('')


def log2file(filename, line):
    with open(filename, 'a') as wfile:
        wfile.write('%s\n' % line)


def batch_check(afile, delays=5):
    alist = []
    fdic = {}
    with open(afile) as openedfile:
        for line in openedfile:
            afm = line.split()[0].replace('"', '')
            assert len(afm) == 9
            if not isvat(afm):
                log2file('log.txt', '%s algorithmic err' % afm)
                print('AFM: %s has algorithmic err' % afm)
            else:
                alist.append(afm)
    total_afms = len(alist)
    print('%s afm for online check ...' % total_afms)
    for j, afm in enumerate(alist):
        if j > 0:
            delay(delays)
        for i in range(30):  # 30 φορές προσπάθεια για έλεγχο στο site
            fdic[afm] = vatol(afm)
            if 'conError' not in fdic[afm]:
                break
            print('Error %s during verification of AFM: %s' % (i + 1, afm))
            delay(30 + (i * 30))
        if fdic[afm]['valid'] is False:
            log2file('log.txt', '%s Not Valid err' % afm)
        else:
            log2file('log.txt', '%s %s' % (afm, fdic[afm]['name']))
        print('%s/%s ->' % (j + 1, total_afms), fdic[afm])
    return True


if __name__ == '__main__':
    import os
    CPATH = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(CPATH, 'afm.txt')
    print(file)
    print(batch_check(file))
