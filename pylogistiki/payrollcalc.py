import utils as ul


dva = {}
dva['meresMina'] = ul.dec(25, 0)
dva['meresWeek'] = ul.dec(6, 0)
dva['oresWeek'] = ul.dec(40, 0)
dva['pNyxta'] = ul.dec(0.25)
dva['pArgia'] = ul.dec(0.75)
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
    ooo['yperorArgia'] = erg.get('yperorArgia', 1)
    if erg['typ'] == 'misthos':
        ooo['apod'] = ooo['apodoxes'] * ooo['meres'] / dva['meresMina']
        ooo['imeromisthio'] = ooo['apodoxes'] / dva['meresMina']
        ooo['imeromisthion'] = ooo['apodoxesn'] / dva['meresMina']
        ooo['oromisthio'] = ooo['imeromisthio'] * dva['meresWeek'] / dva['oresWeek']
        ooo['oromisthion'] = ooo['imeromisthion']\
                             * dva['meresWeek']\
                             / dva['oresWeek']
    elif erg['typ'] == 'imeromisthio':
        ooo['apod'] = ooo['apodoxes'] * ooo['meres']
        ooo['imeromisthio'] = ooo['apodoxes']
        ooo['imeromisthion'] = ooo['apodoxesn']
        ooo['oromisthio'] = ooo['imeromisthio'] * \
                                dva['meresWeek'] / dva['oresWeek']
        ooo['oromisthion'] = ooo['imeromisthion'] * \
                                dva['meresWeek'] / dva['oresWeek']
    elif erg['typ'] == 'oromisthio':
        ooo['apod'] = ooo['apodoxes'] * ooo['ores']
        ooo['oromisthio'] = ooo['apodoxes']
        ooo['oromisthion'] = ooo['apodoxesn']
    ooo['apodoxest'] = ooo['apod']
    # Υπολογισμός προσαύξησης νυχτερινών
    if 'oresNyxta' in erg:
        ooo['apodNyxta'] = ooo['oresNyxta'] * ooo['oromisthion'] * \
                            dva['pNyxta']
        ooo['apodoxest'] += ooo['apodNyxta']
    # Υπολογισμός προσαύξησης αργιών σε μέρες
    if 'argiesm' in erg:
        ooo['apodArgiam'] = ooo['argiesm'] * ooo['imeromisthion'] * \
                                dva['pArgia']
        ooo['apodoxest'] += ooo['apodArgiam']
    # Υπολογισμός προσαύξησης αργιών σε ώρες
    if 'argieso' in erg:
        ooo['apodArgiao'] = ooo['argieso'] * ooo['oromisthion'] * dva['pArgia']
        ooo['apodoxest'] += ooo['apodArgiao']
    # Υπολογισμός υπερωριών
    if 'yperor' in erg:
        ooo['apodYperor'] = ooo['yperor'] * ooo['oromisthio']
        ooo['apodoxest'] += ooo['apodYperor']
        ooo['yperorPros'] = ooo['yperor'] * ooo['oromisthion'] * \
                                dva['pYperoria']
        ooo['apodoxest'] += ooo['apodYperorPros']
    if 'yperorArgia' in erg:
        ooo['apodYperorArgia'] = ooo['yperorArgia'] * ooo['oromisthio']
        ooo['apodoxest'] += ooo['apodYperorArgia']
        ooo['apodYperorArgiaPros'] = ooo['yperorArgia'] * \
                                        ooo['oromisthion'] * dva['pArgia']
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


if __name__ == '__main__':
    serg = {'typ': 'imeromisthio',
            'pika': .45,
            'pikaErgazomenoy': .15,
            'apodoxes': 70,
            'apodoxesn': 50,
            'meres': 1,
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
    print(ul.print_dic(aaa))
