# -*- coding: utf-8 -*-
from dbsqlite import Db


def checkvat(lines, dfpa={}, threshold=0.2, lfpa='54.00'):
    '''
    Δίνουμε dictionary με εγγραφές λογιστικής και ελέγχει και βρίσκει
    τα άρθρα που έχουν διαφορές στο φπα με κατώφλι διαφοράς οριζόμενο
    '''
    def eql(vala, valb, fthres):
        '''Υπολογισμός αν η διαφορά δύο αριθμών υπερβαίνει ένα κατώφλι'''
        if round(abs(vala - valb), 2) <= fthres:
            return True
        else:
            return False
    # Μετατροπή των γραμμών σε άρθρα
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
        lmopair = {}
        lmorev = []
        for lmo in dvals[arth]:
            if lenArth == 2: # Αποκλείουμε τα συμψηφιστικά άρθρα (με 2 γραμμές)
                continue
            if lmo[:len(lfpa)] == lfpa:  # Ο λογαριασμός είναι φπα 54.00
                # Έυρεση συντελεστή φπα 1.Απο λίστα και 2. απο τελευταία ψηφία
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
                    if eql(dvals[arth][elmo], rev, threshold * 100.0 / float(synt)):
                        lmopair[lmo] = elmo
                        lmorev.append(elmo)
                        break

                        # print(elmo, dvals[arth][elmo], lmorev)
                if lmo not in lmopair:
                    log += '%s : %s ~> %s\n' % (arth, dvals[arth], lmo)

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

def accountSimilar(acc, acclist, aaf='54.00', splitp='.'):
    '''
    Προσπαθούμε να εντοπίσουμε τον πιο κοντινό λογαριασμό σε μορφή
    '''
    lenaf = len(aaf) + 1
    # print(acc[lenaf:])
    accparts = acc[lenaf:].split(splitp)
    accparts.pop()
    accparts.append(acc[-2:])  # Προσθέτουμε και τα τελευταία δύο ψηφία
    # print(accparts)
    rating = {}
    for el in acclist:
        rating[el] = 0
    for par in accparts:
        for oth in acclist:
            if par in oth:
                rating[oth] += 1
    # print(rating)
    return sorted(rating, key=rating.get, reverse=True)


def is_idio_prosimo(val1, val2):
    if val1 * val2 >= 0:
        return True
    else:
        return False


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
                        if is_idio_prosimo(dvals[arth][lmo], dvals[arth][lmo2]):
                            tog[lmo][lmo2] = tog[lmo].get(lmo2, 0)
                            tog[lmo][lmo2] += 1
                    else:
                        tog[lmo][lmo2] = tog[lmo].get(lmo2, 0)
                        tog[lmo][lmo2] += 1
                    if lmo2[:5] == '54.00' and lmo[0] in '1267':
                        print(arth, lmo2, lmo, dvals[arth][lmo2] / dvals[arth][lmo])
    ds = {}
    for lmo in tog:
        ds[lmo] = {}
        for lm2 in tog[lmo]:
            rank = (tog[lmo][lm2] / app[lm2]) * (tog[lmo][lm2] / app[lmo])
            if rank > threshold:
                ds[lmo][lm2] = round(rank, 3)
    return(ds, app)


if __name__ == '__main__':
    dbpath = '/home/tedlaz/tedfiles/prj/samaras2016d/2016.sql3'
    sql = ("SELECT tr.id, lmo.lmo, trd.xr - trd.pi as val, tr.dat "
           "FROM tr "
           "INNER JOIN trd ON tr.id=trd.id_tr "
           "INNER JOIN lmo ON lmo.id=trd.id_lmo;")
    dbcon = Db(dbpath)
    # print('\n'.join(map(str,dbcon.rowsd(sql))))
    print(checkvat(dbcon.rowsd(sql), {}, 0.5))
    #res , app = find_similarities(dbcon.rowsd(sql), True)
    #for el in sorted(res):
    #    print(el, app[el], res[el])
