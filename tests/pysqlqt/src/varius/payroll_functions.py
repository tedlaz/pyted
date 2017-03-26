# Analogia epidomatos adeias se dora :
# (1/2 epidoma adeias) / 12 misthoi = 1/24 i analogia ~ 0.04166 
pros_epidomatos = 1.04166


def calc_dpasxa_misthotoi(misthos, meres):
    '''
    imeres: imerologiakes imeres
    misthos: eite kanonikos eite meiomenos i ek peritropis
    orio o misos misthos
    synolikes imeres : 31 + 28 + 31 + 30 = 120
    '''
    if meres > 120:
        meres = 120
    result = misthos * meres / 240.0 * pros_epidomatos
    return round(result, 2)


def calc_dpasxa_imeromisthioi(imeromisthio, meres):
    '''
    Dyo imeromisthia gia kathe 13 meres ergasias
    (meres / 13) * 2 = meres / 6.5
    orio oi 15 meres
    '''
    a1 = meres / 6.5
    if a1 > 15:
        a1 = 15
    result = imeromisthio * a1 * pros_epidomatos
    return round(result, 2)


def calc_dxristoygenon_misthotoi(misthos, meres):
    '''
    2/25 gia kathe 19 meres (meres/19) * 2 / 25 =
    meres / (25 * 19 / 2) = meres / 237.5
    orio enas misthos
    '''
    if meres > 237.5:
        meres = 237.5
    result = misthos * meres / 237.5 * pros_epidomatos
    return round(result, 2)


def calc_dxristoygenon_imeromisthioi(imeromisthio, meres):
    '''
    1 imeromisthio kathe 8 meres ergasias
    orio oi 25 meres
    '''
    meres_doroy = meres / 8.0
    if meres_doroy > 25:
       meres_doroy = 25
    result = imeromisthio * meres_doroy * pros_epidomatos
    return round(result, 2)

def calc_meres_adeias_ek_peritropis(meres):
    pass


def calc_apozimiosi_apolysis_misthotoi(misthos, eti):
    orio_basikis_apozimiosis = 5385.6
    orio_epipleon_apozimiosis = 1714.286
    apozimiosi = 0
    if misthos > orio_basikis_apozimiosis:
        misthos_apolysis = orio_basikis_apozimiosis * 14 / 12.0
    else:
        misthos_apolysis = misthos * 14 / 12.0
    if eti < 1:
        apozimiosi = 0
    elif eti < 4:
        apozimiosi = misthos_apolysis * 2
    elif eti < 6:
        apozimiosi = misthos_apolysis * 3
    elif eti < 8:
        apozimiosi = misthos_apolysis * 4     
    elif eti < 10:
        apozimiosi = misthos_apolysis * 5 
    elif eti < 11:
        apozimiosi = misthos_apolysis * 6 
    elif eti < 12:
        apozimiosi = misthos_apolysis * 7
    elif eti < 13:
        apozimiosi = misthos_apolysis * 8     
    elif eti < 14:
        apozimiosi = misthos_apolysis * 9 
    elif eti < 15:
        apozimiosi = misthos_apolysis * 10
    elif eti < 16:
        apozimiosi = misthos_apolysis * 11
    elif eti >= 16:
        apozimiosi = misthos_apolysis * 12
    else:
        apozimiosi = 0
    return round(apozimiosi,2)

        
if __name__ == '__main__':
    print calc_dpasxa_misthotoi(568.45, 30)
    print calc_dpasxa_imeromisthioi(40, 10)
    print calc_dxristoygenon_misthotoi(568.45, 30)
    print calc_dxristoygenon_imeromisthioi(40, 11)
    print calc_apozimiosi_apolysis_misthotoi(1000, 20)