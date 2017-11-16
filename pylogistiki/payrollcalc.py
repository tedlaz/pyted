import utils as ul


dva = {}
dva['meresMina'] = ul.dec(25, 0)
dva['meresWeek'] = ul.dec(6, 0)
dva['oresWeek'] = ul.dec(40, 0)
dva['pNyxta'] = ul.dec(0.25)
dva['pArgia'] = ul.dec(0.75, 3)
dva['pYperoria'] = ul.dec(0.50)
print(dva)


def calcmis(erg):
    '''erg : {}
    '''
    ooo = ul.DicDec()
    ooo['meres'] = erg['meres']
    ooo['apodoxes'] = erg['apodoxes']
    ooo['apodoxesn'] = erg['apodoxesn']
    ooo['pika'] = erg['pika']
    ooo['pikaErgazomenoy'] = erg['pikaErgazomenoy']
    ooo['oresNyxta'] = erg.get('oresNyxta', 0)
    ooo['argiesm'] = erg.get('argiesm', 0)
    ooo['argieso'] = erg.get('argieso', 0)
    ooo['yperor'] = erg.get('yperor', 1)
    ooo['yperorNyxta'] = erg.get('yperorNyxta', 1)
    ooo['yperorArgia'] = erg.get('yperorArgia', 1)
    ooo['yperorArgiaNyxta'] = erg.get('yperorArgiaNyxta', 1)
    if erg['typ'] == 'misthos':
        ooo['apod'] = ooo['apodoxes'] * ooo['meres'] / dva['meresMina']
        ooo['imeromisthio'] = ooo['apodoxes'] / dva['meresMina']
        ooo['imeromisthion'] = ooo['apodoxesn'] / dva['meresMina']
        ooo['oromisthio'] = ooo['imeromisthio'] * dva['meresWeek'] / dva['oresWeek']
        ooo['oromisthion'] = ooo['imeromisthion'] * dva['meresWeek'] / dva['oresWeek']
    elif erg['typ'] == 'imeromisthio':
        ooo['apod'] = ooo['apodoxes'] * ooo['meres']
        ooo['imeromisthio'] = ooo['apodoxes']
        ooo['imeromisthion'] = ooo['apodoxesn']
        ooo['oromisthio'] = ooo['imeromisthio'] * dva['meresWeek'] / dva['oresWeek']
        ooo['oromisthion'] = ooo['imeromisthion'] * dva['meresWeek'] / dva['oresWeek']
    elif erg['typ'] == 'oromisthio':
        ooo['apod'] = ooo['apodoxes'] * ooo['ores']
        ooo['oromisthio'] = ooo['apodoxes']
        ooo['oromisthion'] = ooo['apodoxesn']
    ooo['apodoxest'] = ooo['apod']
    # Υπολογισμός προσαύξησης νυχτερινών
    if 'oresNyxta' in erg:
        ooo['apodNyxta'] = ooo['oresNyxta'] * ooo['oromisthion'] * dva['pNyxta']
        ooo['apodoxest'] += ooo['apodNyxta']
    # Υπολογισμός προσαύξησης αργιών σε μέρες
    if 'argiesm' in erg:
        ooo['apodArgiam'] = ooo['argiesm'] * ooo['imeromisthion'] * dva['pArgia']
        ooo['apodoxest'] += ooo['apodArgiam']
    # Υπολογισμός προσαύξησης αργιών σε ώρες
    if 'argieso' in erg:
        ooo['apodArgiao'] = ooo['argieso'] * ooo['oromisthion'] * dva['pArgia']
        ooo['apodoxest'] += ooo['apodArgiao']
    # Υπολογισμός υπερωριών
    if 'yperor' in erg:
        ooo['apodYperor'] = ooo['yperor'] * ooo['oromisthio']
        ooo['apodoxest'] += ooo['apodYperor']
        ooo['yperorPros'] = ooo['yperor'] * ooo['oromisthion'] * dva['pYperoria']
        ooo['apodoxest'] += ooo['apodYperorPros']
    if 'yperorArgia' in erg:
        ooo['apodYperorArgia'] = ooo['yperorArgia'] * ooo['oromisthio']
        ooo['apodoxest'] += ooo['apodYperorArgia']
        ooo['apodYperorArgiaPros'] = ooo['yperorArgia'] * ooo['oromisthion'] * dva['pArgia']
        ooo['apodoxest'] += ooo['apodYperorArgiaPros']
        ooo['apodYperorArgPros'] = (ooo['apodYperorArgia'] +
            ooo['apodYperorArgiaPros']) * dva['pYperoria']
        ooo['apodoxest'] += ooo['apodYperorArgPros']
    ooo['ika'] = ooo['apodoxest'] * ooo['pika']
    ooo['ikaErgazomenoy'] = ooo['apodoxest'] * ooo['pikaErgazomenoy']
    ooo['ikaErgodoti'] = ooo['ika'] - ooo['ikaErgazomenoy']
    ooo['forologiteo'] = ooo['apodoxest'] - ooo['ikaErgazomenoy']
    ooo['foros'] = 10
    ooo['epidoma'] = 5
    ooo['kratiseisErgazomenoy'] = ooo['ikaErgazomenoy'] + ooo['foros'] + ooo['epidoma']
    ooo['kratiseisErgodoti'] = ooo['ikaErgodoti']
    ooo['pliroteo'] = ooo['apodoxest'] - ooo['kratiseisErgazomenoy']
    return ooo


def calc_normal(erg):
    ooo = ul.DicDec()
    des = {}
    ooo['apo'] = erg['apodoxes']
    des['apo'] = 'Τακτικές Αποδοχές'
    ooo['apon'] = erg.get('apodoxesNomimes', erg['apodoxes'])
    des['apon'] = 'Νόμιμες Αποδοχές'
    ooo['meres'] = erg['meres']
    des['meres'] = 'Ημέρες εργάσίας'
    ooo['argiam'] = erg.get('argiam', 0)
    des['argiam'] = 'Ημέρες Αργίας'
    ooo['nyxtao'] = erg.get('nyxtao', 0)
    des['nyxtao'] = 'Ώρες νυχτερινής εργασίας'
    ooo['argiao'] = erg.get('argiao', 0)
    des['argiao'] = 'Ώρες Αργίας'
    if erg['typ'] == 'misthos':
        ooo['typ'] = 1
        des['typ'] = 'Μισθοτοί'
        ooo['isthio'] = ooo['apo'] / dva['meresMina']
        ooo['isthion'] = ooo['apon'] / dva['meresMina']
        ooo['oro'] = ooo['isthio'] * dva['meresWeek'] / dva['oresWeek']
        ooo['oron'] = ooo['isthion'] * dva['meresWeek'] / dva['oresWeek']
        ooo['apop'] = ooo['apo'] * ooo['meres'] / dva['meresMina']
    elif erg['typ'] == 'imeromisthio':
        ooo['typ'] = 2
        des['typ'] = 'Ημερομίσθιοι'
        ooo['isthio'] = ooo['apo']
        ooo['isthion'] = ooo['apon']
        ooo['oro'] = ooo['isthio'] * dva['meresWeek'] / dva['oresWeek']
        ooo['oron'] = ooo['isthion'] * dva['meresWeek'] / dva['oresWeek']
        ooo['apop'] = ooo['apo'] * ooo['meres']
    elif erg['typ'] == 'oromisthio':
        ooo['typ'] = 3
        des['typ'] = 'Ωρομίσθιοι'
        ooo['oro'] = ooo['apo']
        ooo['oron'] = ooo['apon']
        ooo['apop'] = ooo['apodoxes'] * ooo['ores']
    des['isthio'] = 'Ημερομίσθιο'
    des['isthion'] = 'Νόμιμο ημερομίσθιο'
    des['oro'] = 'Ωρομίσθιο'
    des['oron'] = 'Νόμιμο ωρομίσθιο'
    des['apop'] = 'Αποδοχές εργάσιμων ημερών'
    ooo['apodoxes'] = ooo['apop']
    des['apodoxes'] = 'Αποδοχές περιόδου'
    # Υπολογισμός προσαύξησης νυχτερινών
    if 'nyxtao' in erg:
        ooo['apodn'] = ooo['nyxtao'] * ooo['oron'] * dva['pNyxta']
        des['apodn'] = 'Προσαύξηση νυχτερινών ωρών'
        ooo['apodoxes'] += ooo['apodn']
    # Υπολογισμός προσαύξησης αργιών σε μέρες
    if 'argiam' in erg:
        ooo['apoam'] = ooo['argiam'] * ooo['isthion'] * dva['pArgia']
        des['apoam'] = 'Προσαύξηση ημερών αργίας'
        ooo['apodoxes'] += ooo['apoam']
    # Υπολογισμός προσαύξησης αργιών σε ώρες
    if 'argiao' in erg:
        ooo['apoao'] = ooo['argiao'] * ooo['oron'] * dva['pArgia']
        des['apoao'] = 'Προσαύξηση ωρών αργίας'
        ooo['apodoxes'] += ooo['apoao']
    return ooo, des


def calc_yperories(erg):
    pass


def calc_astheneia(erg):
    pass


def calc_ika(erg):
    cio = ul.DicDec()
    ilb = {}
    cio['poso'] = erg['poso']
    ilb['poso'] = 'Ποσό για ΙΚΑ'
    cio['pika'] = erg['pika']
    ilb['pika'] = 'Ποσοστό ΙΚΑ'
    cio['pikae'] = erg['pikae']
    ilb['pikae'] = 'Ποσοστό ΙΚΑ εργαζομένου'
    cio['pikar'] = cio['pika'] - cio['pikae']
    ilb['pikar'] = 'Ποσοστό ΙΚΑ εργoδότη'
    cio['ika'] = cio['poso'] * cio['pika']
    ilb['ika'] = 'ΙΚΑ'
    cio['ikae'] = cio['poso'] * cio['pikae']
    ilb['ikae'] = 'ΙΚΑ εργαζόμενου'
    cio['ikar'] = cio['ika'] - cio['ikae']
    ilb['ikar'] = 'ΙΚΑ εργοδότη'
    return cio, ilb


class misth():
    def __init__(self):
        pass

    def calc_normal(self):
        pass


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
    aaa = calcmis(ser2)
    ul.print_dic(aaa)

    ter1 = {'typ': 'imeromisthio',
            'apodoxes': 21.19,
            # 'apodoxesNomimes': 50,
            'meres': 25,
            # 'argiam': 1,
            # 'nyxtao': 6,
            # 'argiao': 1,
            'poso': 100.36,
            'pika': .45,
            'pikae': .15,
            }
    c01 = calc_normal(ter1)
    ul.print_dicl(c01)
    ul.print_dicl(calc_ika(ter1))
