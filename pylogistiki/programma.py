"""
Module Programma
"""
from utils import dec
MO, TU, WE, TH, FR, SA, SU = range(7)
DE, TR, TE, PE, PA, SA, KY = range(7)
GRD = ['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη', 'Παρασκευή', 'Σάββατο',
       'Κυριακή']


class DubbleApoException(Exception):
    pass


def nextday(weekday):
    return (weekday + 1) % 7


def h2str(ores):
    """
    ores : Ώρα σε δεκαδική μορφή (πχ 10.5)
    Επιστρέφει string της μορφής 'ΗΗ:ΜΜ' (πχ '10:30')
    """
    hh = int(ores // 1)
    mm = int((ores % 1) * 60)
    return '{:02}:{:02}'.format(hh, mm)


def idxless(val, alist):
    """
    Επιστρέφει το index της alist για το οποίο ισχύει ότι val < τιμήalist
    Διαφορετικά (εφ όσον η τιμή είναι μεγαλύτερη από την τελευταία τιμή)
      επιστρέφει το μήκος του πεδίου + 1
    val: μια τιμή
    alist: Λίστα με τιμές
    """
    for i, elm in enumerate(alist):
        if val < elm:
            return i
    return len(alist)


def split2vals(apo, eos, kli, vals):
    """
    apo <= eos
    kli : [k1, k2, .. kn] : k1 < k2 < ... < kn
    vals: [v1, v2, .. vn, v(n+1)]
    ----k1----k2----    ---kn------
      v1 |  v2 |         vn | vn+1

    """
    assert len(kli) + 1 == len(vals)
    assert apo <= eos
    ca0 = set([apo, eos] + kli)
    ca1 = list(ca0)
    ca1.sort()
    sta = ca1.index(apo)
    end = ca1.index(eos) + 1
    ford = ca1[sta:end]
    delta = []
    theta = []
    for i, elm in enumerate(ford):
        if i == 0:
            continue
        vala = elm - ford[i - 1]
        delta.append(vala)
        theta.append(vals[idxless(ford[i - 1], kli)])
    fdic = {}
    for i, el2 in enumerate(theta):
        fdic[el2] = fdic.get(el2, 0) + delta[i]
    return fdic


def split2days(day, apo, duration):
    """
    Split hours to two days if necessary
    day : number of day (0:Δευτέρα, .. 5:Σάββατο 6:Κυριακή)
    apo : 'hh:mm'
    duration: ώρες εργασίας
    """
    tapoh, tapom = apo.split(':')
    apoh = int(tapoh)
    apom = int(tapom)
    apo1 = apoh + (apom / 60)
    eos1 = apo1 + duration
    or1 = eos1 - apo1
    if eos1 > 24:
        day2 = nextday(day)
        apo2 = 0
        eos2 = eos1 - 24
        eos1 = 24
        or1 = eos1 - apo1
        or2 = eos2 - apo2
        apof = h2str(apo1)
        apof2 = h2str(apo2)
        return {day: {apof: {
                      'd': day,
                      'napo': apo1,
                      # 'apo': apof,
                      'neos': eos1,
                      'eos': h2str(eos1),
                      'h': dec(or1, 1)}},
                day2: {apof2: {
                       'd': day,
                       'napo': apo2,
                       # 'apo': apof2,
                       'neos': eos2,
                       'eos': h2str(eos2),
                       'h': dec(or2, 1)}}}
    return {day: {h2str(apo1): {
                  'd': day,
                  'napo': apo1,
                  # 'apo': h2str(apo1),
                  'neos': eos1,
                  'eos': h2str(eos1),
                  'h': dec(or1, 1)}}}


def orario_by_day_night(day, apo, duration):
    res = split2days(day, apo, duration)
    for day in res:
        for eapo in res[day]:
            vapo = res[day][eapo]['napo']
            veos = res[day][eapo]['neos']
            mern = split2vals(vapo, veos, [6, 22], ['nyxta', 'mera', 'nyxta'])
            res[day][eapo]['mera'] = dec(mern.get('mera', 0), 1)
            res[day][eapo]['nyxta'] = dec(mern.get('nyxta', 0), 1)
    return res


def endtim(start, duration):
    hhh, mmm = start.split(':')
    nhh = int(hhh)
    imm = int(mmm)
    zstart = nhh + (imm / 60)
    zend = zstart + duration
    hh = int(zend // 1) % 24
    mm = int((zend % 1) * 60)
    return '{:02}:{:02}'.format(hh, mm)


class Programma():
    def __init__(self, prg):
        """
        {0: {'10:00': 4, '20:00': 4}, 1: {'10:00': 8}}
        """
        self._prg = prg

    @property
    def week_ores_meres(self):
        _, val = self.orario_analytika
        val['imeres'] = len(self._prg)
        return val

    @property
    def orario_analytika(self):
        """
        {0: {'22:00': {'eos': '24:00', 'd': 0, 'omer': 2, 'onyx': 0, 'ot': 2},
             '10:00': {'eos': '12:00', 'd': 0, 'omer': 2, 'onyx': 0, 'ot': 2}},
         1: {'10:00': {'eos': '14:00', 'd': 1, 'omer': 4, 'onyx': 0, 'ot': 4},
             '21:00': {'eos': '24:00', 'd': 1, 'omer': 1, 'onyx': 2, 'ot': 3}},
         2: {'00:00': {'eos': '03:00', 'd': 1, 'omer': 0, 'onyx': 3, 'ot': 3}}}
        """
        fdi = {}
        fto = {'mera': dec(0, 1), 'nyxta': dec(0, 1), 'total': dec(0, 1)}
        for day in self._prg:
            for apo in self._prg[day]:
                adi = orario_by_day_night(day, apo, self._prg[day][apo])
                for dday in adi:
                    fdi[dday] = fdi.get(dday, {})
                    for dapo in adi[dday]:
                        if dapo in fdi[dday]:
                            raise DubbleApoException('Υπαρχει ήδη %s' % dapo)
                        fdi[dday][dapo] = adi[dday][dapo]
                        fto['mera'] += adi[dday][dapo]['mera']
                        fto['nyxta'] += adi[dday][dapo]['nyxta']
                        fto['total'] += adi[dday][dapo]['h']
        return fdi, fto

    @property
    def orario_synoptika(self):
        ttt = []
        for day in self._prg:
            mer = GRD[day]
            tvl = []
            for apo in self._prg[day]:
                dur = self._prg[day][apo]
                stt = '%s-%s(%s ώρα)' if dur == 1 else '%s-%s(%s ώρες)'
                tvl.append(stt % (apo, endtim(apo, dur), dur))
            ttt.append('%s ' % mer + ' και '.join(tvl))
        return ',\n'.join(ttt)

    def __repr__(self):
        tml = '%-10s %-10s %5s %5s %10s %10s %10s\n'
        sep = '-' * 66 + '\n'
        rst = tml % ('Ημέρα',
                     'Συνέχεια..',
                     'Από',
                     'Έως', 'Ημερήσιες', 'Νυχτερινές', 'Σύνολο')
        rst += sep
        ora, tts = self.orario_analytika
        for day in ora:
            for apo in ora[day]:
                sday = GRD[day]
                sdap = '' if day == ora[day][apo]['d'] else GRD[ora[day][apo]['d']]
                eos = ora[day][apo]['eos']
                mer = ora[day][apo]['mera']
                nyx = ora[day][apo]['nyxta']
                tot = ora[day][apo]['h']
                rst += tml % (sday, sdap, apo, eos, mer, nyx, tot)
        rst += sep
        rst += tml % ('', '', '',  '', tts['mera'], tts['nyxta'], tts['total'])
        return rst


if __name__ == '__main__':
    pr1 = Programma({DE: {'21:00': 8},
                     TR: {'10:30': 8},
                     TE: {'08:00': 8},
                     PA: {'08:00': 4, '23:00': 4}})
    print(pr1.week_ores_meres)
    # print(orario_by_day_night(0, '22:00', 8))
    # print(pr1.orario_analytika)
    print(pr1.orario_synoptika)
