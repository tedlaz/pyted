'''
Module calcmis.py
Calculate Greek Payroll system.
'''
import sys
import os
# PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# if PATH not in sys.path:
#     sys.path.append(PATH)
# print(PATH)
from db_context_manager import Open_sqlite
from dec import dec
from db_sql_create import dic2sql_md


class Calc_exception(Exception):
    pass


sql_paroysies_tmpl = '''
SELECT  m12_pro.id, m12_coy.kad, m12_eid.keid, m12_pro.apod,
sum( case when m12_pard.ptyp_id=1 then  m12_pard.pos end) as ergasimes,
sum( case when m12_pard.ptyp_id=10 then  m12_pard.pos end) as kyriakes,
sum( case when m12_pard.ptyp_id=2 then  m12_pard.pos end) as kanAd,
sum( case when m12_pard.ptyp_id=3 then  m12_pard.pos end) as lapAd,
sum( case when m12_pard.ptyp_id=4 then  m12_pard.pos end) as adikAp,
sum( case when m12_pard.ptyp_id=5 then  m12_pard.pos end) as adXvrisApod,
sum( case when m12_pard.ptyp_id=6 then  m12_pard.pos end) as asles3,
sum( case when m12_pard.ptyp_id=7 then  m12_pard.pos end) as asmor3,
sum( case when m12_pard.ptyp_id=8 then  m12_pard.pos end) as yperor,
sum( case when m12_pard.ptyp_id=9 then  m12_pard.pos end) as ypererg,
sum( case when m12_pard.ptyp_id=11 then  m12_pard.pos end) as nyxtPros,
m12_pro.prod, m12_fpr.epon,m12_fpr.onom,m12_eid.eidp,m12_pard.ptyp_id,
m12_pro.aptyp_id
FROM m12_pard
INNER JOIN m12_par on m12_par.id=m12_pard.par_id
INNER JOIN m12_xrisi on m12_xrisi.id=m12_par.xrisi_id
INNER JOIN m12_period on m12_period.id=m12_par.period_id
INNER JOIN m12_pro on m12_pro.id=m12_pard.pro_id
INNER JOIN m12_fpr on m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_coy on m12_coy.id=m12_pro.coy_id
INNER JOIN m12_eid on m12_eid.id=m12_pro.eid_id
WHERE m12_xrisi.id=%s AND m12_par.period_id between %s and %s
group by  m12_fpr.id
ORDER BY m12_pro.id
'''
mistyp = {'nm': 1, 'dx': 3, 'dp': 4, 'ea': 5}
aptyp = {'minas': 1, 'mera': 2, 'ora': 3}


def get_paroysies(dbf, xrisi_id, period_apo_id, period_eos_id=None):
    if period_eos_id:
        sql = sql_paroysies_tmpl % (xrisi_id, period_apo_id, period_eos_id)
    else:
        sql = sql_paroysies_tmpl % (xrisi_id, period_apo_id, period_apo_id)
    with Open_sqlite(dbf) as db:
        rows = db.select_as_dict(sql)
    return rows


def calc_mis(dbf, xrisi_id, per_id, mis_id, mdate):
    mis_id = int(mis_id)
    md = {'xrisi_id': xrisi_id, 'period_id': per_id, 'mist_id': mis_id,
          'imnia': mdate, 'zlines': []}
    paroysies = []
    if mis_id == mistyp['nm']:
        paroysies = get_paroysies(dbf, xrisi_id, per_id)
    elif mis_id == mistyp['dp']:
        paroysies = get_paroysies(dbf, xrisi_id, 1, 4)
    elif mis_id == mistyp['dx']:
        paroysies = get_paroysies(dbf, xrisi_id, 5, 12)
    elif mis_id == mistyp['ea']:
        paroysies = get_paroysies(dbf, xrisi_id, 1, 12)
    if paroysies == [{}] or not paroysies:  # If not data found return []
        raise Calc_exception('paroysies must have values')

    paroysies = get_par_mtype(dbf, xrisi_id, per_id, mis_id)
    # print(paroysies)
    # m12_misd(mis_id,pro_id,mist_id,mtyp_id,val
    md = {'xrisi_id': xrisi_id, 'period_id': per_id, 'mist_id': mis_id,
          'imnia': mdate, 'zlines': []}
    for pr in paroysies:
        # mdd = {'pro_id': par['id'], 'mist_id': mis_id}
        mt = {}
        print(pr['kad'], pr['keid'], pr['epon'], pr['onom'], pr['meres'])
        if int(pr['aptyp_id']) == aptyp['minas']:
            mt['misthos'] = dec(pr['apod'])
            mt['imsthio'] = dec(0)
            mt['oromist'] = dec(0)
            mt['imsthioc'] = dec(mt['misthos'] / dec(25))
            mt['oromistc'] = dec(mt['imsthioc'] * dec(6) / dec(40))
            # Αποδοχές περιόδου
            mt['apodoxesp'] = dec(mt['misthos'] * pr['meres'] / dec(25))
        elif int(pr['aptyp_id']) == aptyp['mera']:
            mt['misthos'] = dec(0)
            mt['imsthio'] = dec(pr['apod'])
            mt['oromist'] = dec(0)
            mt['imsthioc'] = mt['imsthio']
            mt['oromistc'] = dec(mt['imsthioc'] * dec(6) / dec(40))
            mt['apodoxesp'] = dec(mt['imsthio'] * pr['meres'])
        elif int(par['aptyp_id']) == aptyp['ora']:
            raise Calc_exception('Not implemented yet')
            mt['misthos'] = dec(0)
            mt['imsthio'] = dec(0)
            mt['oromist'] = dec(pr['apod'])
            mt['imsthioc'] = dec(0)
            mt['oromistc'] = mt['oromist']
        else:
            raise Calc_exception('Error in values %s' % pr)
        mt['meres'] = pr['meres']
        if int(mis_id) == mistyp['dxrist'] or int(mis_id) == mistyp['dpasxa']:
            mt['apodoxes'] = dec(mt['apodoxesp'] * dec(1.041666, 6))
        else:
            mt['apodoxes'] = mt['apodoxesp']
        mt['mt'] = pr['merest']
        # At the end
        for el in mt:
            md['zlines'].append({'pro_id': pr['id'], 'mist_id': mis_id,
                                 'mtyp_id': el, 'val': mt[el]})
    return md


def calc_dp(tmeres, apt, apv, tapv=0):
    '''
    tmeres : Total days of period
    apt    : Τύπος αποδοχών (1:Μισθός, 2:Ημερομίσθιο, 3:Ωρομίσθιο)
    apv    : Αποδοχές (μισθός, ημερομίσθιο, ωρομίσθιο)
    '''
    apty = {'minas': 1, 'mera': 2, 'ora': 3}
    apt = int(apt)
    pros = dec(1.0 + 1.0 / 24.0, 6)
    apv = dec(apv)
    dmer = dec(tmeres)
    if apt == apty['minas']:
        # Μισθός Χ ημερολογιακές ημέρες / 240 (4*30*2) Χ 1,04166
        # Μισθός Χ Μέρες ΙΚΑ / 200 (4*25*2) Χ 1,04166
        ex = f"Μισθός({apv}) Χ Μέρες ΙΚΑ({tmeres}) / 200 Χ 1,04166"
        return dec(apv * dmer / dec(200) * pros), ex
    elif apt == apty['mera']:
        #  Ημερομίσθιο Χ εργάσιμες ημέρες / 6,5 Χ 1,04166
        ex = f"Ημερομίσθιο({apv}) Χ εργάσιμες ημέρες({tmeres}) / 6,5 Χ 1,04166"
        return dec(apv * dmer / dec(6.5) * pros), ex
    elif apt == apty['ora']:
        assert tapv > 0
        # αποδοχές από 01-Ιανουαρίου έως 30-Απριλίου / 8 Χ 1,04166
        ex = f"Aποδοχές από 1/1 έως 30/4 ({dec(tapv)}) / 8 Χ 1,04166"
        return dec(tapv / dec(8) * pros), ex
    else:
        raise Calc_exception('Error here !!')


def calc_dx(tmeres, apt, apv, tapv=0):
    '''
    tmeres : Total days of period
    apt    : Τύπος αποδοχών (1:Μισθός, 2:Ημερομίσθιο, 3:Ωρομίσθιο)
    apv    : Αποδοχές (μισθός, ημερομίσθιο, ωρομίσθιο)
    '''
    apty = {'minas': 1, 'mera': 2, 'ora': 3}
    apt = int(apt)
    pros = dec(1.0 + 1.0 / 24.0, 6)
    apv = dec(apv)
    dmer = dec(tmeres)
    if apt == apty['minas']:
        # Μισθός Χ ημερολογιακές ημέρες / 237,5 (25*19/2) Χ 1,04166
        # Μισθός Χ Μέρες ΙΚΑ / 200 (8*25) Χ 1,04166
        ex = f"Μισθός({apv}) Χ Μέρες ΙΚΑ({tmeres}) / 200 Χ 1,04166"
        return dec(apv * dmer / dec(200) * pros), ex
    elif apt == apty['mera']:
        # Ημερομίσθιο Χ εργάσιμες ημέρες / 8 Χ 1,04166
        ex = f"Ημερομίσθιο({apv}) Χ εργάσιμες ημέρες({tmeres}) / 8 Χ 1,04166"
        return dec(apv * dmer / dec(8) * pros), ex
    elif apt == apty['ora']:
        assert tapv > 0
        # αποδοχές από 01-Mαΐου έως 31-Δεκεμβρίου / 8 Χ 1,04166
        ex = f"Aποδοχές από 1/5 έως 31/12 ({dec(tapv)}) / 8 Χ 1,04166"
        return dec(tapv / dec(8) * pros), ex
    else:
        raise Calc_exception('Error here !!')


def calc_ea(tmeres, apt, apv, tapv=0):
    '''
    tmeres : Total days of period
    apt    : Τύπος αποδοχών (1:Μισθός, 2:Ημερομίσθιο, 3:Ωρομίσθιο)
    apv    : Αποδοχές (μισθός, ημερομίσθιο, ωρομίσθιο)
    '''
    apty = {'minas': 1, 'mera': 2, 'ora': 3}
    apt = int(apt)
    apv = dec(apv)
    dmer = dec(tmeres)
    if apt == apty['minas']:
        # Μέρες ΙΚΑ / 25 * Μισθός / 25
        meresea = dec(dmer / dec(12.5), 6)
        if meresea > 12.5:
            meresea = dec(12.5)
        ex = f"Μισθός({apv}) * Μέρες Επίδ({meresea}) / 25"
        return dec(meresea * apv / dec(25)), ex
    elif apt == apty['mera']:
        # Μέρες εργάσιμες / 26 * 2
        meresea = dec(dmer / dec(12.5), 6)
        if meresea > 13:
            meresea = dec(13)
        ex = f"Ημερομίσθιο({apv}) * Μέρες Επίδ({meresea})"
        return dec(meresea * apv), ex
    elif apt == apty['ora']:
        raise Calc_exception('Not implemented yet')
        assert tapv > 0
        # αποδοχές από 01-Mαΐου έως 31-Δεκεμβρίου / 8 Χ 1,04166
        ex = f"Aποδοχές από 1/5 έως 31/12 ({dec(tapv)}) / 8 Χ 1,04166"
        return dec(tapv / dec(8) * pros), ex
    else:
        raise Calc_exception('Error here !!')


def calc_nm(tmeres, apt, apv, tores=0):
    '''
    tmeres : Total days of period
    apt    : Τύπος αποδοχών (1:Μισθός, 2:Ημερομίσθιο, 3:Ωρομίσθιο)
    apv    : Αποδοχές (μισθός, ημερομίσθιο, ωρομίσθιο)
    '''
    apty = {'minas': 1, 'mera': 2, 'ora': 3}
    apt = int(apt)
    apv = dec(apv)
    dmer = dec(tmeres)
    if apt == apty['minas']:
        # Μισθός Χ Μέρες ΙΚΑ / 25
        ex = f"Μισθός({apv}) Χ Μέρες ΙΚΑ({tmeres}) / 25"
        return dec(apv * dmer / dec(25)), ex
    elif apt == apty['mera']:
        # Ημερομίσθιο Χ εργάσιμες ημέρες
        ex = f"Ημερομίσθιο({apv}) Χ εργάσιμες ημέρες({tmeres})"
        return dec(apv * dmer), ex
    elif apt == apty['ora']:
        assert tapv == 0
        assert tores > 0
        # Ωρες Χ ωρομίσθιο
        ex = f"Ωρες({dec(tores)}) Χ Ωρομίσθιο({apv})"
        return dec(tapv * dec(tores)), ex
    else:
        raise Calc_exception('Error here !!')


if __name__ == '__main__':
    db = '/home/tedlaz/Documents/mistst.m13'
    # par = calc_mis(db, 6, 4, 4, '2017-04-30')
    # print(dic2sql_md('m12_mis', 'm12_misd', par))
    print(calc_dp(26.5, 1, 337.74))
    print(calc_dp(1, 2, 55))
    print(calc_dp(5, 3, 11, 55))
    print(calc_dx(200, 1, 337.74))
    print(calc_dx(1, 2, 55))
    print(calc_dx(5, 3, 11, 55))
    print(calc_ea(25, 1, 337.74))
    print(calc_ea(250, 2, 55))
    print(calc_nm(25, 1, 337.74))
    print(calc_nm(2, 2, 55))
