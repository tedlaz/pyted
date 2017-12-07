"""
   Υπολογισμός ΑΜΚΑ, αντικειμενικής αξίας ακινήτων.
"""
# Times zonis / foros ana tetragoniko
KLI = [500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
FRK = [2.0, 2.8, 2.9, 3.7, 4.5, 6.0, 7.6, 9.2, 9.5, 11.1, 11.3, 13.0]
# Syntelestis palaiotita ktismatos eti/ syntelestis
SPK = [4, 9, 14, 19, 25]
SPV = [1.25, 1.2, 1.15, 1.1, 1.05, 1.0]
# Syntelestis apomeiosis epiganeias metra/syntelestis
SAE = [500, 1500, 3000, 5000, 10000, 25000, 50000]
SAV = [1.0, 0.8, 0.75, 0.65, 0.55, 0.45, 0.35, 0.25]
# Syntelestis orofou orofos/syntelestis
SOA = [-1, 1, 3, 5]
SOB = [0.98, 1.0, 1.01, 1.02, 1.03]
# Syntelestis monokatoikias 0: nai 1: oxi
MOA = [0]
MOB = [1.0, 1.02]
# Syntelestis prosopsis
PRA = [0, 1]
PRB = [1.0, 1.01, 1.02]
# Syntelestis epikarpoti
EPA = [19, 29, 39, 49, 59, 69, 79]
EPB = [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]


def calcp(val, kli, frk):
    assert len(kli) + 1 == len(frk)
    for i, elm in enumerate(kli):
        if val <= elm:
            return frk[i]
    return frk[i + 1]


def calcaj(aki):
    vls = {}
    vls['xronia'] = 2017 - aki['etos']
    vls['spalio'] = calcp(vls['xronia'], SPK, SPV)
    vls['sapom'] = calcp(aki['tetragonika'], SAE, SAV)
    vls['sorof'] = calcp(aki['orofos'], SOA, SOB)
    vls['smono'] = calcp(aki['monokatoikia'], MOA, MOB)
    vls['spros'] = calcp(aki['prosopsi'], PRA, PRB)
    vls['forostm'] = calcp(aki['timizonis'], KLI, FRK)
    vls['foros'] = vls['forostm'] * aki['tetragonika'] * vls['spalio'] * vls['sapom'] * vls['sorof'] * vls['smono'] * vls['spros'] * aki['analogia']
    return vls


def calc_antikeimeniki(aki):
    vls = {}
    vls['timizonis'] = aki['timizonis']
    vls['tetragonika'] = aki['tetragonika']
    vls['orofos'] = aki['orofos']
    vls['etos'] = aki['etos']
    vls['xronia'] = 2017 - aki['etos']
    vls['prosopsi'] = aki['prosopsi']
    vls['se'] = aki['se']
    vls['analogia'] = aki['analogia']
    sorofou = 1.0
    if aki['orofos'] == -1:
        sorofou = 0.6
    elif aki['orofos'] == 0:
        if aki['se'] == 1:
            sorofou = 0.9
        elif aki['se'] == 2:
            sorofou = 1.2
        elif aki['se'] == 3:
            sorofou = 1.25
        elif aki['se'] == 4:
            sorofou = 1.3
    elif aki['orofos'] == 1:
        if aki['se'] == 1:
            sorofou = 1.0
        elif aki['se'] == 2:
            sorofou = 1.1
        elif aki['se'] == 3:
            sorofou = 1.15
        elif aki['se'] == 4:
            sorofou = 1.2
    elif aki['orofos'] == 2:
        sorofou = 1.05
        if aki['se'] == 3:
            sorofou = 1.1
        elif aki['se'] == 4:
            sorofou = 1.15
    elif aki['orofos'] == 3:
        sorofou = 1.1
        if aki['se'] == 4:
            sorofou = 1.15
    elif aki['orofos'] == 4:
        sorofou = 1.15
    elif aki['orofos'] == 5:
        sorofou = 1.2
    elif aki['orofos'] == 6:
        sorofou = 1.25
    vls['syntelestis_orofou'] = sorofou
    # Syntelestis Palaiotitas
    palaiotita = 1.0
    if 1 <= vls['xronia'] <= 5:
        palaiotita = 0.9
    elif vls['xronia'] <= 10:
        palaiotita = 0.8
    elif vls['xronia'] <= 15:
        palaiotita = 0.75
    elif vls['xronia'] <= 20:
        palaiotita = 0.7
    elif vls['xronia'] <= 25:
        palaiotita = 0.65
    elif vls['xronia'] > 25:
        palaiotita = 0.6
    vls['syntelestisPalaiotitas'] = palaiotita
    tetr = aki['tetragonika']
    tzon = aki['timizonis']
    pro = aki['prosopsi']
    if vls['analogia'] == 1.0:
        smany = 1.0
        pososto = 1.0
    else:
        smany = 0.9
        pososto = vls['analogia']
    antik = tetr * tzon * palaiotita * sorofou * smany
    if pro in [2, 3]:
        antik = antik * 1.05
    elif pro == 0:
        antik = antik * 0.8
    if tetr <= 25:
        antik = antik * 1.05
    elif tetr <= 100:
        pass
    elif tetr <= 200:
        antik = antik * 1.05
    elif tetr <= 300:
        antik = antik * 1.1
    elif tetr <= 500:
        antik = antik * 1.2
    else:
        antik = antik * 1.3

    vls['antikeimeniki'] = antik * pososto
    return vls


def calc_all(dta):
    print(calcaj(dta)['foros'])
    print(calc_antikeimeniki(dta)['antikeimeniki'])


if __name__ == '__main__':
    ddd = {'timizonis': 1250,
           'tetragonika': 53.01,
           'orofos': 5,
           'etos': 1959,
           'prosopsi': 1,
           'se': 1,
           'monokatoikia': 0,
           'analogia': 0.5  # An 100% enas idioktitis allios parapano
           }
    calc_all(ddd)
