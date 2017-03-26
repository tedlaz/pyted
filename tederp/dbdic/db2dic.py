# -*- coding: utf-8 -*-
import sqlite3


def db2dic(dbf, idv, tablemaster, tabledetail=None, key=None,
           remove_parent_id=True, id_at_end=True):
    '''
    Επιστρέφει από την sqlite3 βάση δεδομένων db και από τον πίνακα tablemaster
    την εγγραφή με id = id εισόδου. Εάν έχει τιμή και το tabledetail τότε
    επιστρέφει και τις τιμές από το tabledetail που έχουν πεδίο
    tablemaster_id = id εισόδου. Σε αυτή την περίπτωση αν θέλουμε να αφαιρέσουμε
    τις επαναλαμβανόμενες τιμές του id δίνουμε remove_parent_id=True
    key : Το πεδίο που συνδέει τον tablemaster με τον tabledetail
    Η default τιμή του είναι mastertable_id και υπολογίζεται αυτόματα όταν key=None
    εκτός εάν του δώσουμε άλλη τιμή.
    remove_parent_id : Όταν είναι True αφαιρεί από τις αναλυτικές γραμμές το πεδίο σύνδεσης key
    '''
    if id_at_end:
        fkeytemplate = '%s_id'
    else:
        fkeytemplate = 'id_%s'
    if key:
        id_field = key
    else:
        id_field = fkeytemplate % tablemaster
    sql1 = "SELECT * FROM %s WHERE id='%s'" % (tablemaster, idv)
    sql2 = "SELECT * FROM %s WHERE %s='%s'" % (tabledetail, id_field, idv)
    con = sqlite3.connect(dbf)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql1)
    rows = cur.fetchall()
    dic = dict(zip(rows[0].keys(), rows[0]))
    if tabledetail:
        cur.execute(sql2)
        rows = cur.fetchall()
        dic['zlines'] = []
        for i, row in enumerate(rows):
            dic['zlines'].append(dict(zip(row.keys(), row)))
            if (id_field in dic['zlines'][i]) and remove_parent_id:
                del dic['zlines'][i][id_field]
    cur.close()
    con.close()
    return dic


if __name__ == '__main__':
    DBFILE = '/home/tedlaz/pyted/tederp/tst.db'
    print(db2dic(DBFILE, 1, 'ki', 'kid'))
