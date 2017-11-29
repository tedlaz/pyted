"""
Class to  manage osyk
"""
import os
import zipfile
ENC = 'CP1253'  # Εναλλακτικά 'ISO8859-7'
SPL = '|'  # Splitter πεδίων
LIN = '\r\n'  # Splitter γραμμών
OSYKFILE = os.path.join(os.path.dirname(__file__), 'osyk.zip')


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
            self.index_kad()

    def index_kad(self):
        self._kadi = {}
        for line in self._kad.split(LIN):
            try:
                kad, kadp = line.split(SPL)
                self._kadi[kad] = kadp
            except Exception:
                pass

    def find_kad(self, per):
        """Find kad by description"""
        tli = []
        for line in self._kad.split(LIN):
            if per in line:
                kad, kadp = line.split(SPL)
                tli.append({'kad': kad, 'kadp': kadp})
        return tli

    def find_eid(self, per):
        """Find eid by description"""
        tli = []
        for line in self._eid.split(LIN):
            if per in line:
                eid, eidp = line.split(SPL)
                tli.append({'eid': eid, 'eidp': eidp})
        return tli

    def find_kad_eids(self, kad):
        """Get a list of eid by kad"""
        pass

    def find_kpk(self, kad, eid, period):
        """Get kpk by kad eid period"""
        kads = str(kad)
        eids = str(eid)
        pers = int(period)
        for line in self._kek.split(LIN):
            try:
                kadl, eidl, kpkl, apo, eos = line.split(SPL)
            except Exception:
                return None
            if kads == kadl and eids == eidl and int(apo) <= pers <= int(eos):
                return kpkl
        return None

    def find_kpk_pososta(self, kpk, period):
        kpks = str(kpk)
        pers = int(period)
        for line in self._kpk.split(LIN):
            try:
                kpkl, perl, pel, ptl, psl, per = line.split(SPL)
            except Exception:
                return None
            if kpks == kpkl and int(per) <= pers:
                return line

if __name__ == '__main__':
    osyk = Osyk()
    per1 = 201710
    # print(osyk._kad)
    # print(osyk.find_kad('5540'))
    # print(osyk.find_eid('724070'))
    # print(osyk._kadi['5540'])
    # print(osyk._kpk)
    kpk = osyk.find_kpk(1120, 411410, per1)
    kpkl = osyk.find_kpk_pososta(kpk, per1)
    print(kpk, kpkl)
