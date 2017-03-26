# -*- coding: utf-8 -*-
from dec import dec


class Distribution():
    def __init__(self, distd):
        self.distd = distd

    def calc(self, val, decimals=2):
        sorted_keys = sorted(self.distd)
        distlist = []
        for el in sorted_keys:
            distlist.append(dec(self.distd[el], decimals))
        tmpl = []
        val = dec(val, decimals)
        tar = dec(sum(distlist), decimals)
        for el in distlist:
            tmpl.append(dec(val * el / tar , decimals))
        nval = sum(tmpl)
        dif = val - nval
        if dif != 0:
            tmpl[tmpl.index(max(tmpl))] += dif

        dist = {}
        for i, el in enumerate(sorted_keys):
            dist[el] = tmpl[i]
        return dist

    def check(self, val, decimals=2):
        ad = self.calc(val, decimals)
        tmp = dec(0)
        for el in ad.keys():
            tmp += ad[el]
        return (dec(val, decimals) == tmp)

    @property
    def xiliosta(self):
        return self.calc(1000, 0)

    @property
    def xiliostast(self):
        dic = self.xiliosta
        st = ''
        for key in sorted(dic.keys()):
            st += '%20s : %20s\n' % (key, dic[key])
        return st


if __name__ == '__main__':
    asanser = {'a': 204, 'b': 159, 'c': 243, 'd': 120, 'e': 274}
    disasans = Distribution(asanser)
    print(disasans.xiliostast)
    print(disasans.calc(34.467, 3))
    print(disasans.check(34.467, 3))

