# -*- coding: utf-8 -*-

import sqlite3
import decimal

debug = True
if debug:
    DB = "tedtst.sql3"

#######################################################################
#  Utility Functions
#######################################################################

def isNum(value): # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters : 
            1.value : the value to check against.
        output: True or False
    """
    if not value:
        return False
    try: float(value)
    except ValueError: return False
    else: return True

def dec(poso , dekadika=2 ):
    """ 
    use : Given a number, it returns a decimal with a specific number of decimal digits
    input Parameters:
          1.poso     : The number for conversion in any format (e.g. string or int ..)
          2.dekadika : The number of decimals (default 2)
    output: A decimal number     
    """
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)

def makeDecimalFromString(strNumber):
    g = "".join(strNumber.split())
    return dec(g.replace(",","."))


def runSQL(sqlArr,db=DB):
    con = sqlite3.connect(db) 
    cur = con.cursor()
    for sql in sqlArr:
        cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
    
def initDB():
    '''
    lmo    : πίνακας λογαριασμών λογιστικής
    syb    : πίνακας με τα στοιχεία συναλλασσομένων (Πελατών - Προμηθευτών κλπ)
    pak    : πίνακας με τα πακέτα εγγραφών
    tran   : πίνακας με τις επικεφαλίδες εγγραφών λογιστικής
    tran_d : πίνακας με τις γραμμές των εγγραφών λογιστικής
    '''
    sqAr = []
    sqAr.append("create table if not exists logistiki_lmo(id INTEGER PRIMARY KEY NOT NULL, code TEXT, per TEXT)")
    sqAr.append("create unique index if not exists idx_cod on logistiki_lmo(code)")
    sqAr.append("create table if not exists syn(afm TEXT PRIMARY KEY NOT NULL, eponymia TEXT, address TEXT, doy TEXT)")
    sqAr.append("create table if not exists pak(pn INTEGER PRIMARY KEY NOT NULL, imnia TEXT, per TEXT, user TEXT)")
    sqAr.append("create table if not exists logistiki_tran(id INTEGER PRIMARY KEY NOT NULL, imnia TEXT,par TEXT, per TEXT)")
    #sqAr.append("create unique index if not exists idx_par on logistiki_tran(imnia, par)")
    sqAr.append("create table if not exists logistiki_tran_d(id INTEGER PRIMARY KEY NOT NULL,\
                 tran_id INTEGER NOT NULL, lmos_id INTEGER NOT NULL,\
                 per2 TEXT, xr DECIMAL NOT NULL, pi DECIMAL NOT NULL)")
    runSQL(sqAr)

#initDB()

class lmos():

    def __init__(self,_cod,_per='',db=DB):
        self.aa = 0
        self.cod = _cod
        self.per = _per.decode('utf-8')
        self.db = db
        self.saveToDB()
        
    def saveToDB(self):
        con = sqlite3.connect(self.db) 
        cur = con.cursor()
        cur.execute("SELECT id,per FROM logistiki_lmo WHERE code='%s'" % self.cod)
        tmpaa = cur.fetchone()
        if not tmpaa:
            cur.execute("INSERT INTO logistiki_lmo(code,per) VALUES('%s','%s')" %(self.cod,self.per))
            self.aa = cur.lastrowid
        else:
            self.aa  = tmpaa[0]
            self.per = tmpaa[1]
        con.commit()
        cur.close()
        con.close()
        #print self

    def __str__(self):
        tstr = "%s %s %s : %s" % (self.aa, self.cod, self.per, ypol(self.cod))  
        return tstr.encode('utf-8')
    
class syn():
    def __init__(self, _afm,db):
        self.afm = _afm
        self.db  = db
    def saveToDB(self):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute("SELECT afm FROM syn WHERE afm='%s'" % self.afm)
        tmpAFM = cur.fetchone()
        if not tmpAFM:
            cur.execute("INSERT INTO syn(afm) VALUES('%s')" % self.afm)
        else:
            print 'Already saved.'
        con.commit()
        cur.close()
        con.close()
        
def returnOrCreate(cod,db=DB):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("SELECT id, per FROM logistiki_lmo WHERE code='%s'" % cod)
    tmpaa = cur.fetchone()
    idr = 0
    if not tmpaa:
        per = 'Νέος Λογαριασμός'
        cur.execute("INSERT INTO logistiki_lmo(code,per) VALUES('%s','%s')" %(cod,per))
        idr = cur.lastrowid
    else:
        idr = tmpaa[0]
        per  = tmpaa[1]
    con.commit()
    cur.close()
    return idr ,cod , per

def returnId(cod,db=DB):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("SELECT id, per FROM logistiki_lmo WHERE code='%s'" % cod)
    tmpaa = cur.fetchone()
    idr = 0
    if not tmpaa:
        per = ''
    else:
        idr = tmpaa[0]
        per  = tmpaa[1]
    con.commit()
    cur.close()
    return idr , per

def returnFromId(idr,db=DB):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("SELECT code , per FROM logistiki_lmo WHERE id='%s'" % idr)
    tmpaa = cur.fetchone()
    if not tmpaa:
        return 0
    else:
        code = tmpaa[0]
        per  = tmpaa[1]
    con.commit()
    cur.close()
    #print code , per
    return code , per

class tran():
    # Logistiki eggrafi gia apothikefsi se database 
    def __init__(self,imnia,par, per, db=DB):
        self.no = 0
        self.imnia = imnia
        self.par = par
        self.per = per
        self.lines = []
        self.lineNo = 0
        self.txr = dec(0)
        self.tpi = dec(0)
        self.td  = dec(0)
        self.isSaved = False
        self.db = db

    def ln(self,lmos,xr=0,pi=0, per2=''):
        # ln : line : Nea analytiki grammi
        if xr == '':
            xr = 0
        if pi == '':
            pi = 0    
        if (dec(xr) == 0) and (dec(pi) == 0):
            return
        no = self.lineNo + 1
        self.lines.append([no,returnOrCreate(lmos,self.db)[0],per2,dec(xr),dec(pi)])
        self.lineNo = no
        self.txr += dec(xr)
        self.tpi += dec(pi)
        self.td = self.txr - self.tpi

    def fl(self,lmos):
        # fl:final line : Teliki analytiki grammi
        if self.td > 0:
            self.ln(lmos,0,self.td)
        elif self.td < 0:
            self.ln(lmos,self.td * -1,0)

    def tr(self,lxr,lpi,poson):
        # Metafora posoy apo logariasmo se logariasmo
        self.ln(lxr,poson)
        self.ln(lpi,0,poson)

    def isOk(self):
        if ((self.lineNo >= 2) and ( self.td == 0)): # and ( self.txr <> 0)):
            return True
        return False
     
    def saveToDB(self):
        if self.isSaved:
            return 0
        if self.isOk() and self.no == 0:
            con = sqlite3.connect(self.db)      
            cur = con.cursor()
            cur_d = con.cursor()
        try:
            cur.execute("insert into logistiki_tran(imnia, par, per) values ('%s','%s', '%s')" % (self.imnia,self.par,self.per))
            master = cur.lastrowid
            for col in self.lines:
                cur_d.execute("insert into logistiki_tran_d(tran_id,lmos_id, per2, xr, pi) values(%s,%s,'%s',%s,%s)" % (master,col[1],col[2],col[3],col[4]))
        except sqlite3.Error, e:
            print 'Error during saveToDB of object '
            return 0
        con.commit()
        self.no = master
        self.isSaved = True
        cur.close()
        cur_d.close()
        con.close()
        return self.no
    
def findLmo(lmo='',per='',db=DB):
    con = sqlite3.connect(db)
    cur = con.cursor()
    if lmo == '':
        if per == '':
            sql = "select code, per from logistiki_lmo order by code"
        else:
            fper = per + '%'
            sql = "select code, per from logistiki_lmo where per like '%s' order by per" % fper
    else:
        ftext = lmo + '%'
        sql = "select code, per from logistiki_lmo where code like '%s' order by code" % ftext
    cur.execute(sql)
    v1 = cur.fetchall()
    cur.close()
    con.close()
    return v1
    
class trans():
    '''
        Antikeimeno xeirismou ton eggrafon tis basis dedomenon
    '''
    def __init__(self, _db = DB):
        self.db = _db

    def bs(self):
        # Isozygio
        con = sqlite3.connect(self.db)
        c = con.cursor()
        c.execute("SELECT code,per, sum(xr), sum(pi),sum(xr)-sum(pi) as ypol FROM logistiki_tran_d inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id group by lmos_id order by code")
        v1 = c.fetchall()
        #for col in v1:
        #    print "%-13s %-50s %10s %10s %10s" % (col[0],col[1],dec(col[2]),dec(col[3]), dec(col[2]-col[3]))
        c.close()
        con.close()
        return v1
    def im(self):
        con = sqlite3.connect(self.db)
        c = con.cursor()
        c.execute("""SELECT logistiki_tran.id,imnia,par,per,sum(xr) as tot FROM logistiki_tran
                    INNER JOIN logistiki_tran_d on logistiki_tran.id=logistiki_tran_d.tran_id
                    group by logistiki_tran.id 
                    order by imnia desc,  logistiki_tran.id desc""")
        v1 = c.fetchall()
        c.close()
        con.close()
        return v1
    def bsPrn(self):
        pass
    
    def findNotBalanced(self):
        con = sqlite3.connect(self.db)
        c = con.cursor()
        c.execute("SELECT logistiki_tran.id, sum(xr) , sum(pi) FROM logistiki_tran inner join logistiki_tran_d on logistiki_tran.id = logistiki_tran_d.tran_id group by logistiki_tran.id")
        v1 = c.fetchall()
        c.close()
        con.close()
        print "From findNotBalanced ..."
        for col in v1:
            if dec(col[1]) <> dec(col[2]):
                print "Error on %s ----> %s , %s " % (col[0],col[1],col[2])
        
    def __str__(self):
        con = sqlite3.connect(self.db)
        c = con.cursor()
        d = con.cursor()
        c.execute("SELECT * FROM logistiki_tran ")
        v1 = c.fetchall()
        tstr = u''
        for col in v1:
            for row in col:
                tstr += '%s ' % row
            tstr += '\n'
            d.execute("SELECT * FROM logistiki_tran_d WHERE tran_id='%s'" % col[0])
            v2 = d.fetchall()
            tXr = dec(0)
            tPi = dec(0)
            for col2 in v2:
                lmo, per = returnFromId(col2[2])
                tstr += '> %-15s %-40s %-40s %12s %12s \n' % (lmo, per,col2[3],dec(col2[4]),dec(col2[5]))
                tXr += dec(col2[4])
                tPi += dec(col2[5])
            tstr += '> %-15s %-40s %-40s %12s %12s \n' %('','','Synolo',tXr,tPi)
            tstr += '\n'
        c.close()
        d.close()
        con.close()
        return tstr.encode('utf-8')
 
def utilTr(date = '2010-01-01',par='Log.Eggr',per = 'test',lxr = '38.00',lpi='40.00',val = 100):
    t = tran(date,par,per)
    t.tr(lxr,lpi,val)
    t.saveToDB()

def ypol(lmos):
    con = sqlite3.connect(DB)
    c = con.cursor()
    c.execute("SELECT lmos FROM logistiki_tran_d WHERE lmos='%s'" % lmos)
    tmp = c.fetchone()
    v = 0
    if not tmp:
        pass
    else:
        c.execute("SELECT SUM(xr)-SUM(pi) FROM logistiki_tran_d WHERE lmos='%s'" % lmos)
        v = dec(c.fetchone()[0])
    c.close()
    con.close()
    return dec(v)

def kinisi(lmos,db=DB):
    con = sqlite3.connect(db)
    c = con.cursor()
    c.execute("SELECT imnia, par, per , xr, pi, logistiki_tran_d.tran_id FROM logistiki_tran_d inner join logistiki_tran on logistiki_tran_d.tran_id=logistiki_tran.id WHERE lmos_id='%s' order by imnia" % lmos)
    tmp = c.fetchall()
    kinList = []
    c.close()
    con.close()
    a = 0
    for line in tmp:
        #print line
        a += line[3]-line[4]
        kinList.append((line[0],line[1],line[2],line[3],line[4],a,line[5]))
    return kinList
    #for ln in kinList:    
    #    print '%-10s %-25s %-50s %12s %12s %12s ' % ln
    
def totalBalance(lmos,apo,eos,db=DB):
    sqlb = '''SELECT sum(xr)-sum(pi) as d
            from logistiki_lmo
            inner join logistiki_tran_d on logistiki_lmo.id=logistiki_tran_d.lmos_id
            inner join logistiki_tran on logistiki_tran_d.tran_id = logistiki_tran.id
            where code like '%s%%' and imnia < '%s';'''
    sql = '''SELECT sum(xr)-sum(pi) as d
            from logistiki_lmo
            inner join logistiki_tran_d on logistiki_lmo.id=logistiki_tran_d.lmos_id
            inner join logistiki_tran on logistiki_tran_d.tran_id = logistiki_tran.id
            where code like '%s%%' and imnia between '%s' and '%s';'''
    sqla = '''SELECT sum(xr)-sum(pi) as d
            from logistiki_lmo
            inner join logistiki_tran_d on logistiki_lmo.id=logistiki_tran_d.lmos_id
            inner join logistiki_tran on logistiki_tran_d.tran_id = logistiki_tran.id
            where code like '%s%%' and imnia > '%s';'''          
    con  = sqlite3.connect(DB)
    c    = con.cursor()
    
    sqr = sql % (lmos,apo,eos)
    c.execute(sqr)
    res_c = dec(c.fetchone()[0])
    
    sqr = sqlb % (lmos,apo)
    c.execute(sqr)
    res_b = dec(c.fetchone()[0])
    
    sqr = sqla % (lmos,eos)
    c.execute(sqr)
    res_a = dec(c.fetchone()[0])
        
    c.close()
    con.close()
    #print res_b, res_c, res_a
    return [res_b, res_c, res_a]
    
def apotelesma(apo,eos,db=DB):
    result = []
    result.append([apo,eos])
    
    profit  = dec('0')
    pr_b    = dec('0')
    pr_a    = dec('0') 
             
    b2, a2, c2 = totalBalance('2',apo,eos)
    pr_b   += b2
    profit += a2
    pr_a   += c2
    result.append(['2',b2,a2,c2])
    
    b6, a6, c6 = totalBalance('6',apo,eos)
    pr_b   += b6
    profit += a6
    pr_a   += c6
    result.append(['6',b6,a6,c6])
    
    b7, a7, c7 = totalBalance('7',apo,eos)
    pr_b   += b7
    profit += a7
    pr_a   += c7
    result.append(['7',b7,a7,c7])
    
    if b7 <> dec(0):
        b7p = dec(b2 / b7 * 100)
    else:
        b7p = dec(0)
        
    if a7 <> dec(0): 
        a7p = dec(a2 / a7 * 100)
    else:
        a7p = dec(0)
    
    if c7 <> dec(0):
        c7p = dec(c2 / c7 * 100)
    else:
        c7p = dec(0)
    result.append(['p',b7p,a7p,c7p])
    result.append(['8',pr_b,profit,pr_a])    
    return result
    
def apotelesmaMina(minas,etos='2010'):
    apo = '%s-%s-01' % (etos,minas)
    eos = '%s-%s-31' % (etos,minas)
    return apotelesma(apo,eos)
    
def apMinaPrn(minas,etos):
    ar = apotelesmaMina(minas,etos)
    for row in ar:
        for col in row:
            print '%14s' % col,
        print ''
    print ''
    
def apMines():
    for mina in ['09','10','11','12']:
        apMinaPrn(mina,'2010') 
         
def tst():
    #utilTr('2010-12-01','Λογ.Εγγρ.1','Κεφάλαιο σε ταμείο', '38.00.00.0000','40.00.00.0000',6000)
    #utilTr('2010-12-01','Λογ.Εγγρ.3','Δοκιμή', '38.00','40.00',1250)
    #aPagia('2010-12-02','ΤΔΑ5678', 1000,'50.00.00.0000')
    #utilTr('2010-12-10','ΑΠ001','Πληρωμή Προμηθευτή', '50.00','38.00',7872)
    #aEmp('2010-05-05','ΤΔΑ131',2000,'50.00.00.0000')
    #utilTr('2010-12-14','ΑΠ003','Πληρωμή Προμηθευτή', '50.00','38.00',123.3)
    #aEmp('2010-05-06','ΤΔΑ523',1000.34,'50.00')
    #utilTr('2010-12-14','ΑΠ004','Πληρωμή Προμηθευτή', '50.00','38.00',1230.42)
    #pLian('2010-10-01','Ζ001',2000,1000)
    #pLian('2010-10-02','Ζ002',1341.21,122.79)
    #pLian('2010-10-02','Ζ003',114.89,0)
    tr = trans()
    #print tr 
    tr.findNotBalanced()
    #tr.bs()
    #kinisi('1')
    #print findLmo('5','')
    #print apotelesma('2011-01-01','2011-12-31')
    #print apotelesmaMina('12')
    #apMinaPrn('12','2010')
    #print totalBalance('7','2010-12-01','2010-12-31')
    #apMines()
    
if __name__ == "__main__":
    #tst()
    t = tran('2011-10-10','test','ssfddf')
    t.ln('38.00.00.0000',0,-10)
    t.ln('52.00.00.0000',0,10)
    print t.tpi, t.txr,t.td
    print t.isOk()

