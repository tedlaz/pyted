import sqlite3


def _d2sql(adic, table, masterfld=None, masterid=None):
    '''
    Creates insert or update sql from a dictionary
    table : Table name
    adic  : Dictionary with keys corresponding to table's fields
    Returns update or insert sql according id
    if (id = 0 or id = '' or id = None) returns insert sql
    if id <> 0 returns update sql
    '''
    fields = []  #
    values = []
    ufldva = []
    adic['id'] = adic.get('id', 0)
    for el in adic.keys():
        if el == 'id':
            continue
        if el == 'zlines':
            # Το κλειδί zlines παραβλέπεται γιατί εάν υπάρχει, αναφέρεται
            # σε πίνακα details
            continue
        fields.append(el)
        # Εδώ γίνεται η εισαγωγή του parent κλειδιού την ώρα της εγγραφής
        if '(SELECT MAX(id) FROM' in ('%s' % adic[el]):
            values.append("%s" % adic[el])
        else:
            values.append("'%s'" % adic[el])
        ufldva.append("%s='%s'" % (el, adic[el]))

    if (adic['id'] == 0) or (adic['id'] == '') or (adic['id'] is None):
        sql = "INSERT INTO %s (%%s) VALUES (%%s);" % table
        return sql % (', '.join(fields), ', '.join(values))
    else:
        if masterfld:
            sql = "UPDATE %s SET %s WHERE id='%s' AND %s='%s';"
            return sql % (table, ', '.join(ufldva), adic['id'], masterfld, masterid)
        else:
            sql = "UPDATE %s SET %s WHERE id='%s';"
            return sql % (table, ', '.join(ufldva), adic['id'])


def _md2sql(adic, tmaster, tdetail=None):
    '''
    Master-Detail to sql
    '''
    if not tdetail:
        return _d2sql(adic, tmaster)
    sql = _d2sql(adic, tmaster) + '\n'
    for el in adic['zlines']:
        if (adic['id'] == 0) or (adic['id'] == '') or (adic['id'] is None):
            el['%s_id' % tmaster] = ('(SELECT MAX(id) FROM %s)' % tmaster)
            sql += _d2sql(el, tdetail) + '\n'
        else:
            masterfld = '%s_id' % tmaster
            masterid = adic['id']
            el[masterfld] = masterid
            sql += _d2sql(el, tdetail, masterfld, masterid) + '\n'
    return 'BEGIN TRANSACTION;\n' + sql + 'COMMIT;\n'


def confsql(adic, tmaster):
    '''
    Returns back data from tables just to make sure everything is ok
    '''
    asql = 'SELECT * FROM %s WHERE %%s;' % tmaster
    aval = []
    for ele in adic.keys():
        if ele == 'id':
            continue
        if ele == 'zlines':
            continue
        aval.append("%s='%s'" % (ele, adic[ele]))
    return asql % ' and '.join(aval)


def _execute_script(sqlscript, dbf, confirmsql):
    con = sqlite3.connect(dbf)
    con.row_factory = sqlite3.Row
    con.executescript(sqlscript)
    cur = con.cursor()
    cur.execute(confirmsql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    return dict(zip(rows[0].keys(), rows[0]))


def dic2db(dbf, adic, tmaster, tdetail=None):
    '''
    Create master and/or detail sql in a transaction and run it
    against database dbf
    '''
    csql = confsql(adic, tmaster)
    return _execute_script(_md2sql(adic, tmaster, tdetail), dbf, csql)


def db2dic(dbf, idv, tablemaster, tabledetail=None, key=None, remove_parent_id=True):
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
    sql1 = "SELECT * FROM %s WHERE id='%s'" % (tablemaster, idv)
    sql2 = "SELECT * FROM %s WHERE %s_id='%s'" % (tabledetail, tablemaster, idv)
    if key:
        master_id_field = key
    else:
        master_id_field = '%s_id' % tablemaster
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
            if (master_id_field in dic['zlines'][i]):
                del dic['zlines'][i][master_id_field]
    cur.close()
    con.close()
    return dic


class Dbdic():
    '''
    Record administration via dictionaries
    '''
    def __init__(self, dbf, tmaster, tdetail=None, key=None):
        self.dbf = dbf
        self.tmaster = tmaster
        self.tdetail = tdetail
        self.key = key

    def save_one(self, ddata):
        '''
        Save or update one record of data as dictionary to Database
        '''
        return dic2db(self.dbf, ddata, self.tmaster, self.tdetail)

    def get_one_by_id(self, idno):
        '''
        Get data from Database by id as dictionary
        '''
        return db2dic(self.dbf, idno, self.tmaster, self.tdetail, self.key)


if __name__ == '__main__':
    DBFILE = '/home/tedlaz/pyted/tederp/tst.db'
    dbdic = Dbdic(DBFILE, 'lm')
    adi = dbdic.get_one_by_id('70.01.82')
    print(adi)
    adi['par'] = 'Z456'
    # print('----------------\n')
    # print(dbdic.save_one(adi))
