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


def batch_check(afile, delays=5):
    alist = []
    fdic = {}
    algorithmic_errors = 0
    with open(afile) as openedfile:
        for line in openedfile:
            afm = line.split()[0].replace('"', '')
            assert len(afm) == 9
            if not isvat(afm):
                print('AFM: %s is not valid' % afm)
                algorithmic_errors += 1
            alist.append(afm)
    if algorithmic_errors > 0:
        print('Before you continue please correct the errors')
        return
    print('%s afm for check ...' % len(alist))
    for j, afm in enumerate(alist):
        if j > 0:
            delay(delays)
        for i in range(30):  # 30 φορές προσπάθεια για έλεγχο στο site
            fdic[afm] = vatol(afm)
            if 'conError' not in fdic[afm]:
                break
            print('Error %s during verification of AFM: %s' % (i + 1, afm))
            delay(30 + (i * 30))
        print(fdic[afm])
    return alist


if __name__ == '__main__':
    import os
    CPATH = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(CPATH, 'afm.csv')
    print(file)
    print(batch_check(file))
