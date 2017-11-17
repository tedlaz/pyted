import utils as ul


class Mis_exception(Exception):
    pass


dva = {}
dva['meresMina'] = ul.dec(25, 0)
dva['meresWeek'] = ul.dec(6, 0)
dva['oresWeek'] = ul.dec(40, 0)
dva['pNyxta'] = ul.dec(0.25)
dva['pArgia'] = ul.dec(0.75, 3)
dva['pYperoria'] = ul.dec(0.50)
# print(dva)


def normal(erg):
    ooo = ul.DicDec()
    des = {}
    ooo['t_mtyp'] = 'Αποδοχές περιόδου'
    des['t_mtyp'] = 'Τύπος μισθοδοσίας'
    ooo['apo'] = erg['apo']
    des['apo'] = 'Τακτικές Αποδοχές'
    ooo['apon'] = erg.get('apon', erg['apo'])
    des['apon'] = 'Νόμιμες Αποδοχές'
    ooo['meres'] = erg.get('meres', 0)
    des['meres'] = 'Ημέρες εργάσίας'
    ooo['ores'] = erg.get('ores', 0)
    des['ores'] = 'Ώρες εργάσίας (Για ωρομίσθιους)'
    ooo['argiam'] = erg.get('argiam', 0)
    des['argiam'] = 'Ημέρες Αργίας'
    ooo['nyxtao'] = erg.get('nyxtao', 0)
    des['nyxtao'] = 'Ώρες νυχτερινής εργασίας'
    ooo['argiao'] = erg.get('argiao', 0)
    des['argiao'] = 'Ώρες Αργίας'
    if erg['typ'] == 'misthos':
        ooo['t_typ'] = 'Μισθωτός'
        ooo['isthio'] = ooo['apo'] / dva['meresMina']
        ooo['isthion'] = ooo['apon'] / dva['meresMina']
        ooo['oro'] = ooo['isthio'] * dva['meresWeek'] / dva['oresWeek']
        ooo['oron'] = ooo['isthion'] * dva['meresWeek'] / dva['oresWeek']
        ooo['apop'] = ooo['apo'] * ooo['meres'] / dva['meresMina']
    elif erg['typ'] == 'imeromisthio':
        ooo['t_typ'] = 'Ημερομίσθιος'
        ooo['isthio'] = ooo['apo']
        ooo['isthion'] = ooo['apon']
        ooo['oro'] = ooo['isthio'] * dva['meresWeek'] / dva['oresWeek']
        ooo['oron'] = ooo['isthion'] * dva['meresWeek'] / dva['oresWeek']
        ooo['apop'] = ooo['apo'] * ooo['meres']
    elif erg['typ'] == 'oromisthio':
        ooo['typ'] = 'Ωρομίσθιος'
        ooo['oro'] = ooo['apo']
        ooo['oron'] = ooo['apon']
        ooo['apop'] = ooo['apo'] * ooo['ores']
    des['t_typ'] = 'Τύπος εργαζομένου'
    des['isthio'] = 'Ημερομίσθιο'
    des['isthion'] = 'Νόμιμο ημερομίσθιο'
    des['oro'] = 'Ωρομίσθιο'
    des['oron'] = 'Νόμιμο ωρομίσθιο'
    des['apop'] = 'Αποδοχές εργάσιμων ημερών'
    ooo['apot'] = ooo['apop']
    des['apot'] = 'Αποδοχές περιόδου'
    # Υπολογισμός προσαύξησης νυχτερινών
    if 'nyxtao' in erg:
        ooo['apodn'] = ooo['nyxtao'] * ooo['oron'] * dva['pNyxta']
        des['apodn'] = 'Προσαύξηση νυχτερινών ωρών'
        ooo['apot'] += ooo['apodn']
    # Υπολογισμός προσαύξησης αργιών σε μέρες
    if 'argiam' in erg:
        ooo['apoam'] = ooo['argiam'] * ooo['isthion'] * dva['pArgia']
        des['apoam'] = 'Προσαύξηση ημερών αργίας'
        ooo['apot'] += ooo['apoam']
    # Υπολογισμός προσαύξησης αργιών σε ώρες
    if 'argiao' in erg:
        ooo['apoao'] = ooo['argiao'] * ooo['oron'] * dva['pArgia']
        des['apoao'] = 'Προσαύξηση ωρών αργίας'
        ooo['apot'] += ooo['apoao']
    return ooo, des


def yperories(erg):
    cyp = ul.DicDec()
    ylb = {}
    cyp['t_mtyp'] = 'Υπερωρίες'
    ylb['t_mtyp'] = 'Τύπος μισθοδοσίας'
    cyp['oro'] = erg['oro']
    ylb['oro'] = 'Ωρομίσθιο'
    cyp['oron'] = erg.get('oron', erg['oro'])
    ylb['oron'] = 'Νόμιμο ωρομίσθιο'
    cyp['ype'] = erg['ype']
    ylb['ype'] = 'Υπερωρίες (ώρες)'
    cyp['ypen'] = erg.get('ypen', 0)
    ylb['ypen'] = 'Υπερωρίες για νυχτερινή προσαύξηση'
    cyp['ypea'] = erg.get('ypea', 0)
    ylb['ypea'] = 'Υπερωρίες για προσαύξηση αργιών'
    # Υπολογισμός εδώ
    cyp['ayp'] = cyp['ype'] * cyp['oro']
    ylb['ayp'] = 'Αμοιβή υπερωριών'
    cyp['aypn'] = cyp['ypen'] * cyp['oron'] * dva['pNyxta']
    ylb['aypn'] = 'Προσαύξηση λόγω νυχτερινής απασχόλησης'
    cyp['aypa'] = cyp['ypea'] * cyp['oron'] * dva['pArgia']
    ylb['aypa'] = 'Προσαύξηση λόγω αργίας'
    cyp['gaya'] = cyp['ayp'] + cyp['aypn'] + cyp['aypa']
    ylb['gaya'] = 'Σύνολο για προσαύξηση υπερωρίας'
    cyp['aypp'] = cyp['gaya'] * dva['pYperoria']
    ylb['aypp'] = 'Προσαύξηση υπερωριακής απασχόλησης'
    cyp['aypt'] = cyp['ayp'] + cyp['aypn'] + cyp['aypa'] + cyp['aypp']
    ylb['aypt'] = 'Συνολικές αποδοχές υπερωριών'
    return cyp, ylb


def astheneia(erg):
    cas = ul.DicDec()
    alb = {}
    cas['t_mtyp'] = 'Αποδοχές ασθένειας'
    alb['t_mtyp'] = 'Τύπος μισθοδοσίας'
    cas['isthio'] = erg['isthio']
    alb['isthio'] = 'Ημερομίσθιο'
    cas['ml3'] = erg.get('ml3', 0)
    alb['ml3'] = 'Ημέρες ασθένειας <= 3'
    cas['mm3'] = erg.get('mm3', 0)
    alb['mm3'] = 'Ημέρες ασθένειας > 3'
    cas['epi'] = erg.get('epi', 0)
    alb['epi'] = 'Επίδομα ΙΚΑ'
    # Υπολογισμός εδώ
    cas['asl3'] = cas['isthio'] * cas['ml3'] / ul.dec(2)
    alb['asl3'] = 'Αποδοχές ασθένειας <= 3'
    cas['asm3'] = cas['isthio'] * cas['mm3']
    alb['asm3'] = 'Αποδοχές ασθένειας > 3'
    cas['asti'] = cas['asl3'] + cas['asm3']
    alb['asti'] = 'Αποδοχές για ΙΚΑ'
    return cas, alb


def ika(erg):
    cio = ul.DicDec()
    ilb = {}
    cio['poso'] = erg['poso']
    ilb['poso'] = 'Ποσό για ΙΚΑ'
    cio['pika'] = erg['pika'] if erg['pika'] < 1 else erg['pika'] / 100.0
    ilb['pika'] = 'Ποσοστό ΙΚΑ'
    cio['pikae'] = erg['pikae'] if erg['pikae'] < 1 else erg['pikae'] / 100.0
    ilb['pikae'] = 'Ποσοστό ΙΚΑ εργαζομένου'
    # Calculate here ...
    cio['pikar'] = cio['pika'] - cio['pikae']
    ilb['pikar'] = 'Ποσοστό ΙΚΑ εργoδότη'
    cio['ika'] = cio['poso'] * cio['pika']
    ilb['ika'] = 'ΙΚΑ'
    cio['ikae'] = cio['poso'] * cio['pikae']
    ilb['ikae'] = 'ΙΚΑ εργαζόμενου'
    cio['ikar'] = cio['ika'] - cio['ikae']
    ilb['ikar'] = 'ΙΚΑ εργοδότη'
    return cio, ilb


def doro_pasxa(erg):  # tmeres, apt, apv, tapv=0):
    '''
    tmeres : Total days of period
    apt    : Τύπος αποδοχών (1:Μισθός, 2:Ημερομίσθιο, 3:Ωρομίσθιο)
    apv    : Αποδοχές (μισθός, ημερομίσθιο, ωρομίσθιο)
    '''
    cdp = ul.DicDec()
    ldp = {}
    cdp['t_mtyp'] = 'Δώρο Πάσχα'
    ldp['t_mtyp'] = 'Τύπος μισθοδοσίας'
    cdp['merest'] = erg['merest'] if erg['merest'] <= 100 else 100
    ldp['merest'] = 'Ημέρες εργασίας 1/1-30/4'
    cdp['apo'] = erg['apo']  # Μισθός/ημερομίσθιο/συνολικές αποδοχές(ωρομισθ)
    ldp['apo'] = 'Αποδοχές'
    pros = ul.dec(1.0 + 1.0 / 24.0, 6)  # Συντελεστής 1,04166
    if erg['typ'] == 'misthos':
        cdp['t_typ'] = 'Μισθωτός'
        # Μισθός Χ ημερολογιακές ημέρες / 240 (4*30*2) Χ 1,04166
        # Μισθός Χ Μέρες ΙΚΑ / 200 (4*25*2) Χ 1,04166
        exp = (f"Μισθός({cdp['apo']}) Χ Μέρες ΙΚΑ({cdp['merest']})"
               " / 200 Χ 1,04166")
        cdp['dpas'] = cdp['apo'] * cdp['merest'] / ul.dec(200) * pros
    elif erg['typ'] == 'imeromisthio':
        cdp['t_typ'] = 'Ημερομίσθιος'
        #  Ημερομίσθιο Χ εργάσιμες ημέρες / 6,5 Χ 1,04166
        exp = (f"Ημερομίσθιο({cdp['apo']}) Χ εργάσιμες ημέρες"
               f"({cdp['merest']}) / 6,5 Χ 1,04166")
        meresDoroy = cdp['merest'] / ul.dec(6.5)
        if meresDoroy > 15:
            meresDoroy = ul.dec(15)
        cdp['dpas'] = cdp['apo'] * meresDoroy * pros
    elif erg['typ'] == 'oromisthio':
        cdp['t_typ'] = 'Ωρομίσθιος'
        # αποδοχές από 01-Ιανουαρίου έως 30-Απριλίου / 8 Χ 1,04166
        exp = f"Aποδοχές από 1/1 έως 30/4 ({cdp['apo']}) / 8 Χ 1,04166"
        cdp['dpas'] = cdp['apo'] / ul.dec(8) * pros
    else:
        raise Mis_exception('function doro_pasxa Error !!')
    ldp['t_typ'] = 'Τύπος εργαζομένου'
    ldp['dpas'] = 'Δώρο Πάσχα'
    print(exp)
    return cdp, ldp


def doro_xristoygena(erg):
    '''
    tmeres : Total days of period
    apt    : Τύπος αποδοχών (1:Μισθός, 2:Ημερομίσθιο, 3:Ωρομίσθιο)
    apv    : Αποδοχές (μισθός, ημερομίσθιο, ωρομίσθιο)
    '''
    cdx = ul.DicDec()
    ldx = {}
    cdx['t_mtyp'] = 'Δώρο Χριστουγέννων'
    ldx['t_mtyp'] = 'Τύπος μισθοδοσίας'
    cdx['merest'] = erg['merest'] if erg['merest'] <= 200 else 200
    ldx['merest'] = 'Ημέρες εργασίας 1/5-31/12'
    cdx['apo'] = erg['apo']  # Μισθός/ημερομίσθιο/συνολικές αποδοχές(ωρομισθ)
    ldx['apo'] = 'Αποδοχές'
    pros = ul.dec(1.0 + 1.0 / 24.0, 6)
    if erg['typ'] == 'misthos':
        cdx['t_typ'] = 'Μισθωτός'
        # Μισθός Χ ημερολογιακές ημέρες / 237,5 (25*19/2) Χ 1,04166
        # Μισθός Χ Μέρες ΙΚΑ / 200 (8*25) Χ 1,04166
        exp = (f"Μισθός({cdx['apo']}) Χ Μέρες ΙΚΑ({cdx['merest']}) "
               "/ 200 Χ 1,04166")
        cdx['dxri'] = cdx['apo'] * cdx['merest'] / ul.dec(200) * pros
    elif erg['typ'] == 'imeromisthio':
        cdx['t_typ'] = 'Ημερομίσθιος'
        # Ημερομίσθιο Χ εργάσιμες ημέρες / 8 Χ 1,04166
        exp = (f"Ημερομίσθιο({cdx['apo']}) Χ εργάσιμες ημέρες"
               f"({cdx['merest']}) / 8 Χ 1,04166")
        meresDoroy = cdx['merest'] / ul.dec(8)
        if meresDoroy > 25:
            meresDoroy = ul.dec(25)
        cdx['dxri'] = cdx['apo'] * cdx['merest'] / ul.dec(8) * pros
    elif erg['typ'] == 'oromisthio':
        cdx['t_typ'] = 'Ωρομίσθιος'
        # αποδοχές από 01-Mαΐου έως 31-Δεκεμβρίου / 8 Χ 1,04166
        exp = f"Aποδοχές από 1/5 έως 31/12 ({cdx['apo']}) / 8 Χ 1,04166"
        cdx['dxri'] = cdx['apo'] / ul.dec(8) * pros
    else:
        raise Mis_exception('function doro_xristoygena Error!!')
    ldx['t_typ'] = 'Τύπος εργαζομένου'
    ldx['dxri'] = 'Δώρο Χριστουγέννων'
    print(exp)
    return cdx, ldx


def epidoma_adeias(erg):
    '''
    tmeres : Total days of period
    apt    : Τύπος αποδοχών (1:Μισθός, 2:Ημερομίσθιο, 3:Ωρομίσθιο)
    apv    : Αποδοχές (μισθός, ημερομίσθιο, ωρομίσθιο)
    '''
    cea = ul.DicDec()
    lea = {}
    cea['t_mtyp'] = 'Επίδομα αδείας'
    lea['t_mtyp'] = 'Τύπος μισθοδοσίας'
    cea['merest'] = erg['merest'] if erg['merest'] <= 200 else 200
    lea['merest'] = 'Ημέρες εργασίας'
    cea['apo'] = erg['apo']  # Μισθός/ημερομίσθιο/συνολικές αποδοχές(ωρομισθ)
    lea['apo'] = 'Αποδοχές'
    if erg['typ'] == 'misthos':
        # Μέρες ΙΚΑ / 25 * Μισθός / 25
        meresea = ul.dec(cea['merest'] / ul.dec(12.5), 6)
        if meresea > 12.5:
            meresea = ul.dec(12.5)
        exp = f"Μισθός({cea['apo']}) * Μέρες Επίδ({meresea}) / 25"
        cea['aea'] = meresea * cea['apo'] / ul.dec(25)
    elif erg['typ'] == 'imeromisthio':
        # Μέρες εργάσιμες / 26 * 2
        meresea = ul.dec(cea['merest'] / ul.dec(12.5), 6)
        if meresea > 13:
            meresea = ul.dec(13)
        exp = f"Ημερομίσθιο({cea['apo']}) * Μέρες Επίδ({meresea})"
        cea['aea'] = meresea * cea['apo']
    elif erg['typ'] == 'oromisthio':
        raise Mis_exception('Not implemented yet')
        exp = f"To be fixed"
        cea['aea'] = cea['apo'] / ul.dec(8)
    else:
        raise Mis_exception('Error here !!')
    lea['aea'] = 'Επίδομα Αδείας'
    print(exp)
    return cea, lea


def doro_pasxa_test(erg):  # tmeres, apt, apv, tapv=0):
    '''
    tmeres : Total days of period
    apt    : Τύπος αποδοχών (1:Μισθός, 2:Ημερομίσθιο, 3:Ωρομίσθιο)
    apv    : Αποδοχές (μισθός, ημερομίσθιο, ωρομίσθιο)
    '''
    cdp = ul.DicDec()
    ldp = {}
    cdp['t_mtyp'] = 'Δώρο Πάσχα'
    ldp['t_mtyp'] = 'Τύπος μισθοδοσίας'
    cdp['apot'] = erg['apot']  # Μισθός/ημερομίσθιο/συνολικές αποδοχές(ωρομισθ)
    ldp['apot'] = 'Σύνολο Αποδοχών από 1/1 - 30/4'
    pros = ul.dec(1.0 + 1.0 / 24.0, 6)  # Συντελεστής 1,04166
    if erg['typ'] == 'misthos':
        # Μισθός Χ ημερολογιακές ημέρες / 240 (4*30*2) Χ 1,04166
        # Μισθός Χ Μέρες ΙΚΑ / 200 (4*25*2) Χ 1,04166
        cdp['t_typ'] = 'Μισθωτός'
        cdp['dpas'] = cdp['apot'] / ul.dec(8) * pros
    elif erg['typ'] == 'imeromisthio':
        cdp['t_typ'] = 'Ημερομίσθιος'
        #  Ημερομίσθιο Χ εργάσιμες ημέρες / 6,5 Χ 1,04166
        cdp['dpas'] = cdp['apot'] * ul.dec(0.15384, 5) * pros
    elif erg['typ'] == 'oromisthio':
        cdp['t_typ'] = 'Ωρομίσθιος'
        # αποδοχές από 01-Ιανουαρίου έως 30-Απριλίου / 8 Χ 1,04166
        cdp['dpas'] = cdp['apo'] / ul.dec(8) * pros
    else:
        raise Mis_exception('function doro_pasxa Error !!')
    ldp['t_typ'] = 'Τύπος εργαζομένου'
    ldp['dpas'] = 'Δώρο Πάσχα'
    return cdp, ldp


if __name__ == '__main__':
    serg = {'typ': 'imeromisthio',
            'pika': .45,
            'pikaErgazomenoy': .15,
            'apodoxes': 70,
            'apodoxesn': 50,
            'meres': 1,
            'paroysies': [5, 0, 0, 0],
            'oresNyxta': 4,
            'argiesm': 1,
            'yperorArgia': 2}
    ser2 = {'typ': 'misthos',
            'pika': .45,
            'pikaErgazomenoy': .15,
            'apodoxes': 3200,
            'apodoxesn': 2400,
            'meres': 1,
            'oresNyxta': 8,
            'argieso': 5,
            'yperorArgia': 4}

    ter1 = {'typ': 'imeromisthio',
            'apodoxes': 21.19,
            'apodoxesNomimes': 17,
            'meres': 25,
            # 'argiam': 1,
            # 'nyxtao': 6,
            # 'argiao': 1,
            'poso': 100.36,
            'pika': 45,
            'pikae': 15,
            }
    c01 = normal(ter1)
    ul.print_dicl(c01)
    ul.print_dicl(ika(ter1))
    ffb = {'ype': 2, 'oro': 10.5, 'oron': 7.5, 'ypen': 0, 'ypea': 2}
    ffc = {'ype': 4, 'oro': 19.2, 'oron': 14.4, 'ypen': 1, 'ypea': 4}
    ul.print_dicl(yperories(ffb))
    ast = {'isthio': 80, 'ml3': 3, 'mm3': 6, 'epi': 350}
    ul.print_dicl(astheneia(ast))
    dps1 = {'typ': 'misthos', 'merest': 26, 'apo': 600}
    dps2 = {'typ': 'imeromisthio', 'merest': 25, 'apo': 38}
    dps3 = {'typ': 'oromisthio', 'merest': 360, 'apo': 600}
    ul.print_dicl(doro_pasxa(dps1))
    ul.print_dicl(doro_xristoygena(dps3))
    # dp21 = {'typ': 'imeromisthio', 'apot': 750}
    # ul.print_dicl(doro_pasxa_test(dp21))
    dea01 = {'typ': 'misthos', 'merest': 25, 'apo': 600}
    dea02 = {'typ': 'imeromisthio', 'merest': 200, 'apo': 30}
    ul.print_dicl(epidoma_adeias(dea01))
