#!/usr/bin/python
# *- coding: utf-8 -*
import decimal
import locale
locale.setlocale(locale.LC_ALL, '')


def isNum(value):  # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters :
            1.value : the value to check against.
        output: True or False
        """
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """ use : Given a number, it returns a decimal with a specific number
        of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or
                int ..)
            2.decimals : The number of decimals (default 2)
        output: A decimal number
        """
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


def f2(pin):
    f = {}
    f[301] = dec(pin.get(301, 0))
    f[302] = dec(pin.get(302, 0))
    f[303] = dec(pin.get(303, 0))
    f[304] = dec(pin.get(304, 0))
    f[305] = dec(pin.get(305, 0))
    f[306] = dec(pin.get(306, 0))
    f[307] = f[301] + f[302] + f[303] + f[304] + f[305] + f[306]
    f[308] = dec(pin.get(308, 0))
    f[309] = dec(pin.get(309, 0))
    f[310] = dec(pin.get(310, 0))
    f[311] = f[307] + f[308] + f[309] + f[310]
    f[331] = dec(f[301] * dec(0.13))
    f[332] = dec(f[302] * dec(0.065, 3))
    f[333] = dec(f[303] * dec(0.23))
    f[334] = dec(f[304] * dec(0.09))
    f[335] = dec(f[305] * dec(0.05))
    f[336] = dec(f[306] * dec(0.16))
    f[337] = f[331] + f[332] + f[333] + f[334] + f[335] + f[336]
    f[341] = dec(pin.get(341, 0))
    f[342] = dec(pin.get(342, 0))
    f[343] = dec(pin.get(343, 0))
    f[344] = dec(pin.get(344, 0))
    f[345] = dec(pin.get(345, 0))
    f[346] = dec(pin.get(346, 0))
    f[351] = dec(pin.get(351, 0))
    f[352] = dec(pin.get(352, 0))
    f[353] = dec(pin.get(353, 0))
    f[354] = dec(pin.get(354, 0))
    f[355] = dec(pin.get(355, 0))
    f[356] = dec(pin.get(356, 0))
    f[357] = dec(pin.get(357, 0))
    f[358] = f[351] + f[352] + f[353] + f[354] + f[355] + f[356] + f[357]
    f[371] = dec(f[351] * dec(0.13))
    f[372] = dec(f[352] * dec(0.065, 3))
    f[373] = dec(f[353] * dec(0.23))
    f[374] = dec(f[354] * dec(0.09))
    f[375] = dec(f[355] * dec(0.05))
    f[376] = dec(f[356] * dec(0.16))
    f[377] = dec(pin.get(377, 0))
    f[378] = f[371] + f[372] + f[373] + f[374] + f[375] + f[376] + f[377]
    f[400] = dec(pin.get(400, 0))
    f[401] = dec(pin.get(401, 0))
    f[402] = dec(pin.get(402, 0))
    f[403] = dec(pin.get(403, 0))
    f[404] = f[400] + f[401] + f[402] + f[403]
    f[411] = dec(pin.get(411, 0))
    f[412] = dec(pin.get(412, 0))
    f[413] = f[411] + f[412]
    f[420] = f[378] + f[404] - f[413]
    f[501] = dec(0)
    f[502] = dec(0)
    f[503] = dec(0)
    f[511] = dec(0)
    f[512] = dec(0)
    f[513] = dec(0)
    f[514] = dec(0)
    f[521] = dec(0)
    f[522] = dec(0)
    f[105] = dec(pin.get(105, 0))  # pistotiko ypoloipo apo isozygio 54.00
    f[115] = dec(pin.get(115, 0))  # xreostiko ypoloipo apo isozygio 54.00
    if f[420] > f[337]:
        f[501] = f[420] - f[337]
    else:
        f[511] = f[337] - f[420]
    return f


def str_f2(f):
    for key in f:
        f[key] = locale.format("%0.2f", f[key], grouping=True)
    f[100] = ''
    k = {}
    for key in f:
        k['%s' % key] = f[key]
    st = ''
    st += '301:%(301)13s 331:%(331)12s 351:%(351)13s 371:%(371)12s\n'
    st += '302:%(302)13s 332:%(332)12s 352:%(352)13s 372:%(372)12s\n'
    st += '303:%(303)13s 333:%(333)12s 353:%(353)13s 373:%(373)12s\n'
    st += '304:%(304)13s 334:%(334)12s 354:%(354)13s 374:%(374)12s\n'
    st += '305:%(305)13s 335:%(335)12s 355:%(355)13s 375:%(375)12s\n'
    st += '306:%(306)13s 336:%(336)12s 356:%(356)13s 376:%(376)12s\n'
    st += '307:%(307)13s 337:%(337)12s 357:%(357)13s 377:%(377)12s\n'
    st += '308:%(308)13s     %(100)12s 358:%(358)13s 378:%(378)12s\n'
    st += '309:%(309)13s\n'
    st += '310:%(310)13s     %(100)12s 400:%(400)13s\n'
    st += '311:%(311)13s     %(100)12s 401:%(401)13s\n'
    st += '    %(100)13s     %(100)12s 402:%(402)13s\n'
    st += '341:%(341)13s 344:%(344)12s 403:%(403)13s 404:%(404)12s\n'
    st += '342:%(342)13s 345:%(345)12s 411:%(411)13s\n'
    st += '343:%(343)13s 346:%(346)12s 412:%(412)13s 413:%(413)12s\n\n'
    st += '    %(100)13s     %(100)12s     %(100)13s 420:%(420)12s\n\n'
    st += '501:%(501)13s     %(100)12s 511:%(511)13s\n'
    return st % k


def render_to_html(data, filename='f2_tst.html'):
    with open('f2.html') as html_template:
        html_text = html_template.read().decode('utf-8')
    dat = f2(data)
    fdict = {}
    for key in dat:
        fdict['i%s' % key] = dat[key]
    fdict['etos'] = '2015'
    fdict['tr'] = u'Α Τρίμηνο'
    fdict['epon'] = u'Μαλακόπουλος'
    fdict['onom'] = u'Γεώργιος'
    fdict['patr'] = u'Σπυρίδων'
    fdict['afm'] = u'044568974'
    final = html_text.format(**fdict)
    with open(filename, 'w') as fout:
        fout.write(final.encode('utf-8'))


if __name__ == '__main__':
    pik = {353: 9679.79,
           303: 18316.08,
           306: 3052.91,
           342: 5811.88,
           357: 4297.08,
           377: 779.45
           }
    ap = f2(pik)
    print(str_f2(ap))
    render_to_html(pik)
