# -*- coding: utf-8 -*-

import ted_util as tu
from ted_util import dec
import ted_sqlite as ts
fil = 'tdf.sql3'

sqlc = "create table mis(id INTEGER PRIMARY KEY, xr, per, typ, erg, js, jse);"
sqli = "insert into mis values (null, ?, ?, ?, ?, ?, ?);"
sqls = '''select xr, per, typ, erg, p0(js, 'forol') as sk, p0(jse, 'mert') as kl
from mis'''
# ts.script_on_new_db(fil, sqlc)

par = {'mer': 2,
       'mad': 0,
       'apousia': 0,
       'ony': 0,
       'mky': 0,
       'oky': 0,
       'oyp': 0,
       'astheneia': [
                      {'apo': '2014-02-10',
                       'eos': '2014-02-12',
                       'meres3': 3,
                       'meresm3': 0,
                       'ika_apozimiosi': 0,
                       },
                      {'apo': '2014-02-16',
                       'eos': '2014-02-26',
                       'meres3': 0,
                       'meresm3': 6,
                       'ika_apozimiosi': 132.34
                      }
                    ]
       }

def dictojs(dic):
    js = {}
    for key in dic.keys():
        try:
            js[key] = float(dic[key])
        except:
            js[key] = dic[key]
    return js


def parousies(xrisi, period, typos):
    return [{'er': 'nikos', 'mer': 15, 'ka': 3},
            {'er': 'aleka', 'mer': 13}]


def erdata(er):
    return {'ty': 0, 'apod': 23.46, 'ddays': 25}


def miscalc(pa, edata):
    da = {}  # Αποτελέσματα μισθοδοσίας
    ex = {}  # Εξήγηση υπολογισμού
    for key in pa.keys():
        da[key] = pa[key]
    for key in edata.keys():
        da[key] = edata[key]
    mer = pa.get('mer', 0)
    ka = pa.get('ka', 0)
    da['mert'] = dec(mer + ka)
    ex['mert'] = "Εργάσιμες(%s) + καν.αδεία(%s) = %s" % (mer, ka, da['mert'])

    if edata['ty'] == 0:  # imeromisthios
        da['mapo'] = dec(da['mert'] * dec(edata['apod']))
        ex['mapo'] = u"Μέρες(%s) Χ Ημερομίσθιο(%s) = %s" % (da['mert'], edata['apod'], da['mapo'])
    elif edata['ty'] == 1:  # misthotos
        da['mapo'] = dec(da['mert'] / edata['ddays'] * edata['apod'])
        ex['mapo'] = u"To fix"
    else:
        da['mapo'] = dec(0)
        ex['mapo'] = u"To fix"

    da['ika'] = dec(da['mapo'] * dec(.4))
    ex['ika'] = u"To fix"
    da['ikaen'] = dec(da['mapo'] * dec(.15))
    ex['ikaen'] = u"to fix"
    da['ikaet'] = da['ika'] - da['ikaen']
    ex['ikaet'] = u"to fix"
    da['forol'] = da['mapo'] - da['ikaen']
    ex['forol'] = u"to fix"
    return dictojs(da), ex


def mis(xrisi, period, typos):
    par = parousies(xrisi, period, typos)
    for i in range(1):
        for line in par:
            erg = line['er']
            edata = erdata(erg)
            da, ex = miscalc(line, edata)
            ts.insertp(fil, sqli, ('2015', '04', '01', da['er'], ts.jd(da), ts.jd(ex)))
    vls = ts.select_with_functions(fil, sqls)
    for li in vls:
        print("{xr} {per} {typ} {erg} {sk} {kl}".format(**li))


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    mis(1, 1, 1)
