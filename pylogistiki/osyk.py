"""
Class to  manage osyk
"""
import os
import zipfile
import utils as ul
ENC = 'CP1253'  # Εναλλακτικά 'ISO8859-7'
SPL = '|'  # Splitter πεδίων
LIN = '\r\n'  # Splitter γραμμών
OSYKFILE = os.path.join(os.path.dirname(__file__), 'osyk.zip')


class Exception_Osyk(Exception):
    pass


class Osyk():
    """Osyk class"""
    def __init__(self, osyk_zip_file=OSYKFILE):
        with zipfile.ZipFile(osyk_zip_file) as osyk:
            with osyk.open('dn_eid.txt') as eidf:
                self._eid = eidf.read().decode(ENC)
            with osyk.open('dn_kad.txt') as kadf:
                self._kad = kadf.read().decode(ENC)
            with osyk.open('dn_kpk.txt') as kpkf:
                self._kpk = kpkf.read().decode(ENC)
            with osyk.open('dn_kadeidkpk.txt') as kekf:
                self._kek = kekf.read().decode(ENC)

    def index_kek(self):
        fkek = {}
        for line in self._kek.split(LIN):
            try:
                kad, eid, kpk, apo, eos = line.split(SPL)
                fkek[kad] = fkek.get(kad, {})
                fkek[kad][eid] = fkek.get(fkek[kad].get(eid), )
            except ValueError:
                pass

    def index_eid(self):
        feid = {}
        for line in self._eid.split(LIN):
            try:
                eid, eidp = line.split(SPL)
                feid[eid] = eidp
            except ValueError:
                pass
        return feid

    def index_kad(self):
        self._kadi = {}
        for line in self._kad.split(LIN):
            try:
                kad, kadp = line.split(SPL)
                self._kadi[kad] = kadp
            except ValueError:
                raise Exception_Osyk('Error in line %s' % line)

    def index_kpk(self, period):
        pers = int(period)
        kpkd = {}
        for line in self._kpk.split(LIN):
            try:
                kpk, kpkp, pen, pet, ptt, per = line.split(SPL)
                if int(per) <= pers:
                    if kpk not in kpkd.keys():
                        kpkd[kpk] = {'kpk': kpk,
                                     'kpkp': kpkp,
                                     'penos': pen,
                                     'petis': pet,
                                     'ptotal': ptt,
                                     'perapo': per}
            except ValueError:
                pass
        return kpkd

    def find_kad(self, per):
        """Find kad by description"""
        tli = []
        for line in self._kad.split(LIN):
            if len(line) < 6:
                continue
            if ul.grup(per) in ul.grup(line):
                kad, kadp = line.split(SPL)
                tli.append({'kad': kad, 'kadp': kadp})
        return tli

    def find_eid(self, per):
        """Find eid by description"""
        tli = []
        for line in self._eid.split(LIN):
            if len(line) < 8:
                continue
            if ul.grup(per) in ul.grup(line):
                eid, eidp = line.split(SPL)
                tli.append({'eid': eid, 'eidp': eidp})
        return tli

    def find_kad_eids(self, kad, period):
        """Get a list of eid by kad"""
        kads = [str(i) for i in kad]
        pers = int(period)
        eids = self.index_eid()
        kpks = self.index_kpk(period)
        kdic = {}
        for line in self._kek.split(LIN):
            if len(line) < 13:
                continue
            try:
                kadl, eidl, kpkl, apo, eos = line.split(SPL)
            except:
                raise Exception_Osyk('Error in line %s' % line)
            if  kadl in kads and int(apo) <= pers <= int(eos):
                kdic[kadl] = kdic.get(kadl, {})
                kdic[kadl][eidl] = {'eidp': eids[eidl],
                                    'period_anazitisis': pers,
                                    'apo': apo,
                                    'eos': eos,
                                    'kpk': kpks[kpkl]}
                # tlist.append({'kad': kads,
                #               'eid': eidl,
                #               'eidp': eids[eidl],
                #               'period_anazitisis': pers,
                #               'kpk': kpkl,
                #               'kpkv': kpks[kpkl],
                #               'apo': apo,
                #               'eos': eos})
        return kdic

    def find_kpk_periodou(self, kad, eid, period):
        """Get kpk by kad eid period"""
        kads = str(kad)
        eids = str(eid)
        pers = int(period)
        for line in self._kek.split(LIN):
            if len(line) < 13:
                continue
            try:
                kadl, eidl, kpkl, apo, eos = line.split(SPL)
            except:
                raise Exception_Osyk('Error in line %s' % line)
            if kads == kadl and eids == eidl and int(apo) <= pers <= int(eos):
                return {'kad': kads,
                        'eid': eids,
                        'period_anazitisis': pers,
                        'kpk': kpkl,
                        'apo': apo,
                        'eos': eos}
        return {'kad': kads,
                'eid': eids,
                'period_anazitisis': pers,
                'kpk': None,
                'apo': None,
                'eos': None}

    def find_kpk_pososta(self, kpk, period):
        kpks = str(kpk)
        pers = int(period)
        for line in self._kpk.split(LIN):
            if len(line) < 1:
                continue
            try:
                kpkl, perl, pel, ptl, psl, per = line.split(SPL)
            except:
                raise Exception_Osyk('Error in line %s' % line)
            if kpks == kpkl and int(per) <= pers:
                return {'kpk': kpks,
                        'kpkp': perl,
                        'per': pel,
                        'peti': ptl,
                        'ptotal': psl,
                        'period_anazitisis': pers,
                        'period_apo': per}
        return {'kpk': kpks,
                'kpkp': None,
                'per': None,
                'peti': None,
                'ptotal': None,
                'period_anazitisis': pers,
                'period_apo': None}


def pprint(list_of_dicts):
    for el in list_of_dicts:
        for key in el.keys():
            print(key, el[key])
        print('=' * 80)


def tst():
    ast = {'0110': {'22345': {'201001': {'201012': 'tst'}}}}


if __name__ == '__main__':
    osyk = Osyk()
    per1 = 201606
    kad1 = 1120
    eid1 = 411410
    # print(osyk._kad)
    # print(osyk.find_kad('5540'))print(kpkper['5540']['913230'])
    # print(osyk.find_eid('724070'))
    # print(osyk._kadi['5540'])
    # print(osyk._kpk)
    kpk1 = osyk.find_kpk_periodou(kad1, eid1, per1)
    kpka = osyk.find_kpk_pososta(kpk1['kpk'], per1)
    # print(kpk1, kpka)
    # pprint(osyk.find_kad('5540'))
    kpkper = osyk.find_kad_eids(['5540', '5530'], 201711)
    print(kpkper['5540']['913230'])
    print(kpkper['5530']['913230'])
    # Με ένα διάβασμα του αρχείου δημιουργούμε ένα dictionary της μορφής
    # {kad1: {eid1: {kpk, ...}}, kad2: {eid2:kpk}}
    # di[kad1][eid1][kpk]
    # print(osyk._kek)
