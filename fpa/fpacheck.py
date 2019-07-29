# -*- coding: utf-8 -*-
from dbsqlite import Db
ACCOUNT_SPLITTER = '.'
ACCOUNT_FPA = '54.00'


def checkvat(lines, dfpa={}, threshold=0.2):
    '''
    Δίνουμε dictionary με εγγραφές λογιστικής και ελέγχει και βρίσκει
    τα άρθρα που έχουν διαφορές στο φπα με κατώφλι διαφοράς οριζόμενο
    '''
    def eql(vala, valb, fthres):
        '''Υπολογισμός αν η διαφορά δύο αριθμών υπερβαίνει ένα κατώφλι'''
        return round(abs(vala - valb), 2) <= fthres
    # Μετατροπή των γραμμών σε άρθρα
    # Γραμμές της μορφής :
    # id     lmo           val      dat
    #  1  53.98.00.080  -15.12   2016-01-01
    #  1  62.03.00.123   12.29   2016-01-01
    #  1  54.00.29.023    2.83   2016-01-01
    #
    # Γίνονται : {1: {'53.98.00.080': -15.12,
    #                 '62.03.00.123': 12.29,
    #                 '54.00.29.023': 2.83}}
    dvals = {}
    for ele in lines:
        _id = ele['id']
        dvals[_id] = dvals.get(_id, {})
        dvals[_id][ele['lmo']] = ele['val']
    log = u''
    logok = u'Όλα τα άρθρα είναι οκ'
    loger = u'Άρθρα λογιστικής με διαφορά στο ΦΠΑ :\n'
    ignored = 0
    for arth in dvals:
        lenArth = len(dvals[arth])  # Εδώ βρίσκουμε τον αριθμό γραμμών
        assert lenArth > 1  # Δεν γίνεται να υπάρχει άρθρο με γραμμές < 2
        if lenArth == 2:  # Αποκλείουμε τα συμψηφιστικά άρθρα (με 2 γραμμές)
            continue
        lmopair = {}
        lmorev = []
        for lmo in dvals[arth]:
            if lmo.startswith(ACCOUNT_FPA):  # Ο λογαριασμός είναι φπα 54.00*
                # Έυρεση συντελεστή φπα
                # 1. Από λίστα και
                # 2. Aπό τελευταία ψηφία
                dk = list(dvals[arth].keys())
                dkf = []
                for el in dk:
                    if el[0] in '1267':
                        dkf.append(el)
                simil = accountSimilar(lmo, dkf)
                synt = dfpa.get(lmo, int(lmo[-2:]))
                rev = round(dvals[arth][lmo] * 100.0 / synt, 2)
                # print(lmo, synt, dvals[arth][lmo], rev)
                for elmo in simil:
                    if elmo in lmorev:
                        # print('%s already exists' % elmo)
                        continue
                    if eql(dvals[arth][elmo],
                           rev,
                           threshold * 100.0 / float(synt)):
                        lmopair[lmo] = elmo
                        lmorev.append(elmo)
                        break
                if lmo not in lmopair:
                    log += '%s : %s ~> %s %s\n' % (arth, dvals[arth], lmo, rev)
        if lmopair:
            ignored += 1
            print(lmopair)
    print('')
    print(u'Συνολικές εγγραφές : %s' % len(dvals))
    print(u'Eγγραφές χωρίς φπα : %s' % ignored)
    if log:
        return loger + log
    else:
        return logok


def accountSimilar(acc, acclist):
    '''
    Προσπαθούμε να εντοπίσουμε τον πιο κοντινό λογαριασμό σε μορφή
    '''
    lenaf = len(ACCOUNT_FPA) + 1
    # print('acc->', acc, acclist, acc[lenaf:])
    accparts = acc[lenaf:].split(ACCOUNT_SPLITTER)
    # print('accparts->', accparts)
    accparts.pop()
    accparts.append(acc[-2:])  # Προσθέτουμε και τα τελευταία δύο ψηφία
    # print('accparts2->', accparts)
    # print(accparts)
    rating = {}
    for el in acclist:
        rating[el] = 0
    for par in accparts:
        for oth in acclist:
            if par in oth:
                rating[oth] += 1
    # print('rating->', rating)
    return sorted(rating, key=rating.get, reverse=True)


def is_idio_prosimo(val1, val2):
    return val1 * val2 >= 0


# Δεν χρησιμοποιείται πουθενά ...
def find_similarities(lines, omosimoi=False, threshold=0):
    '''Μετατροπή των γραμμών σε άρθρα'''
    dvals = {}
    for el in lines:
        _id = el['id']
        dvals[_id] = dvals.get(_id, {})
        dvals[_id][el['lmo']] = el['val']

    tog = {}
    app = {}
    for arth in dvals:
        for lmo in dvals[arth]:
            app[lmo] = app.get(lmo, 0) + 1
            tog[lmo] = tog.get(lmo, {})
            for lmo2 in dvals[arth]:
                if lmo != lmo2:
                    if omosimoi:
                        if is_idio_prosimo(dvals[arth][lmo],
                                           dvals[arth][lmo2]):
                            tog[lmo][lmo2] = tog[lmo].get(lmo2, 0)
                            tog[lmo][lmo2] += 1
                    else:
                        tog[lmo][lmo2] = tog[lmo].get(lmo2, 0)
                        tog[lmo][lmo2] += 1
                    if lmo2[:5] == '54.00' and lmo[0] in '1267':
                        print(arth,
                              lmo2,
                              lmo,
                              dvals[arth][lmo2] / dvals[arth][lmo])
    ds = {}
    for lmo in tog:
        ds[lmo] = {}
        for lm2 in tog[lmo]:
            rank = (tog[lmo][lm2] / app[lm2]) * (tog[lmo][lm2] / app[lmo])
            if rank > threshold:
                ds[lmo][lm2] = round(rank, 3)
    return(ds, app)


def main(dbpath):
    sql = ("SELECT tr.id, lmo.lmo, trd.xr - trd.pi as val, tr.dat "
           "FROM tr "
           "INNER JOIN trd ON tr.id=trd.id_tr "
           "INNER JOIN lmo ON lmo.id=trd.id_lmo;")
    dbcon = Db(dbpath)
    print(checkvat(dbcon.rowsd(sql), {}, 0.5))


if __name__ == '__main__':
    dbpath = '/home/ted/Documents/pelates/samaras/2019b/el2019b.sql3'
    main(dbpath)
    # print(accountSimilar('64.02.06.024', ['54.00.29.024', '54.00.29.025']))
