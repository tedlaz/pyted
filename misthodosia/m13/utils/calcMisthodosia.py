# -*- coding: utf-8 -*-

import sqlite3
import decimal
from osyk import osyk
import fmy as fmyp1
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

def d(poso , dekadika=2 ):
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
    return d(g.replace(",","."))
    
sql = '''
SELECT  m12_pro.id, m12_coy.kad, m12_eid.keid, m12_pro.apod, sum(m12_parf.kerg) as s, m12_pro.prod, m12_fpr.epon,m12_fpr.onom,m12_eid.eidp
FROM m12_parf
INNER JOIN m12_xrisi on m12_xrisi.id=m12_parf.xrisi_id
INNER JOIN m12_period on m12_period.id=m12_parf.period_id
INNER JOIN m12_pro on m12_pro.id=m12_parf.pro_id
INNER JOIN m12_fpr on m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_coy on m12_coy.id=m12_pro.coy_id
INNER JOIN m12_eid on m12_eid.id=m12_pro.eid_id
WHERE m12_xrisi.id=%s AND m12_parf.period_id between %s and %s
group by  m12_pro.id
ORDER BY m12_parf.id
'''
sql2 = '''
SELECT  m12_pro.id, m12_coy.kad, m12_eid.keid, m12_pro.apod, 
sum( case when m12_pard.ptyp_id=1 then  m12_pard.pos end) as taktApod,
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
m12_pro.prod, m12_fpr.epon,m12_fpr.onom,m12_eid.eidp,m12_pard.ptyp_id
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
ORDER BY m12_fpr.id
'''
#DB = 'mis.sql3'

#sa = osyk.kpk_find(osyk.kadeidkpk_find(self.coy.kad,self.eid.kad),'201210')
def getParousies(xr,per,db,pereos=None):
    if pereos:
        sq = sql2 % (xr,per,pereos)
    else:
        sq = sql2 % (xr,per,per)
    con = sqlite3.connect(db) 
    cur = con.cursor()
    cur.execute(sq)
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows

def getSingleVal(sql,db):
    con = sqlite3.connect(db) 
    cur = con.cursor()
    cur.execute(sql)
    val = cur.fetchone()
    cur.close()
    con.close()
    return val[0]

def nullToZero(val):
    if val:
        return val
    else:
        return 0
    
def makeMis(xrid,perid,mistid,dat,db):
    from collections import OrderedDict
    xrisip  = getSingleVal("SELECT xrisi from m12_xrisi WHERE id=%s" % xrid,db)
    perno   = getSingleVal("SELECT period from m12_period WHERE id=%s" % perid,db)
    
    perid = int(perid)
    mistid = int(mistid)
    bar = 1
    if mistid == 1:
        par     = getParousies(xrid,perid,db)
    elif mistid == 4: # Δώρο Πάσχα
        par   = getParousies(xrid,1,db,4)
        bar = 2
    elif mistid == 5: # Επίδομα Αδείας
        par   = getParousies(xrid,1,db,12)
        bar = 2
    elif mistid == 3: # Δώρο Χριστουγέννων
        par   = getParousies(xrid,5,db,12)
    else:
        par   = getParousies(xrid,1,db,12)
    if not par:
        return False
            
    xrisiper= xrisip + perno
    
    sql1 = "INSERT INTO m12_mis(xrisi_id,period_id,mist_id,imnia) VALUES (%s,%s,%s,'%s')" % (xrid,perid,mistid,dat)
    sql2 = "INSERT INTO m12_misd(mis_id,pro_id,mist_id,mtyp_id,val) VALUES(%s,%s,%s,%s,%s)" 
    
    con  = sqlite3.connect(db) 
    cur  = con.cursor()
    curd = con.cursor()
    cur.execute(sql1)
    mis_id = cur.lastrowid
    for col in par:
        vals = OrderedDict()
        pro_id = col[0]
        kpk = osyk.kpk_find(osyk.kadeidkpk_find(col[1],col[2],xrisiper),xrisiper)[0]
        penos,pika,kpkno = d(kpk[2]),d(kpk[4]),kpk[0]
        misim = d(col[3])
        #meres = 0
        if mistid == 1:
            meres = nullToZero(col[4])#+nullToZero(col[5]))
            kyriakes = nullToZero(col[5])
        elif mistid == 4:  # Δώρο Πάσχα
            meres = d(d(col[4]) / d(6.5),2)
        elif mistid == 5:  # Επίδομα Αδείας
            meres = d( d(col[4]) / d(12.5), 2) #Mesos oros imeron mexri maio kai meta dia dyo
            if meres > 13:
                meres = 13
        elif mistid == 3:  # Δώρο Χριστουγέννων
            meres = d(d(col[4]) / d(8),2)
        else:
            meres = d(0)

        vals[100] = misim
        vals[101] = d(0) # Μισθός
        vals[109] = meres
        if mistid == 1:
            vals[110] = meres
            vals[111] = kyriakes
        else:
            vals[110] = d(0)

        apod  = misim * meres
        
        if mistid == 1:
            prosKyr = d(kyriakes * misim * d(0.75))
            apod = apod + prosKyr
            
        if mistid == 4:
            pros = d(1.041666,6)
            apod = d(apod * pros)
            
        if mistid == 3:
            pros = d(1.041666,6)
            apod = d(apod * pros) 
                   
        vals[200] = d(apod,2)
        ikaer = d(apod * penos / d(100))
        vals[500] = ikaer
        ika   = d(apod * pika  / d(100))
        vals[502] = ika
        ikaet = ika - ikaer
        vals[501] = ikaet
        
        forol = apod - ikaer
        
        vals[503] = mistid  
                
        vals[504]  = kpkno
        vals[505]  = penos
        vals[506]  = pika
        
        vals[599] = forol
        
        fmy   = d(0)
        fpar  = d(0)
        fmy, fpar = fmyp1.fpXrisis(forol, bar, int(xrisip))
        vals[600] = fpar
        vals[601] = fmy
        eea   = fmyp1.eeaXrisis(forol, bar, int(xrisip))
        vals[610] = eea
        tker  = ikaer + fpar + eea
        vals[700] = tker
        plir  = apod - tker
        vals[900] = plir
        for k in vals:
            curd.execute(sql2 % (mis_id,pro_id,mistid,k,vals[k]))
    con.commit()
    cur.close()
    curd.close()
    con.close()
    return True

def getTotals(xr,per,typ):
    sql = '''
            SELECT sum(meres) ,sum(apod),sum(ikaer),sum(ikaet),sum(fmy), sum(ika), sum(plir)
            FROM m12_misdf
            GROUP BY mis_id
            ORDER BY mis_id
          '''
    print sql
    pass

def tst():
    par = getParousies(2,12,'e:/tmp/mistst.m13',12)
    for row in par:
        for col in row:
            print col,
        print ''   
if __name__ == "__main__":
    #print makeMis(2,12)
    tst()