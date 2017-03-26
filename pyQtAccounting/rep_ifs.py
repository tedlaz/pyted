# -*- coding: utf-8 -*-
'''
Ημερήσιο Φύλλο Συναλλαγών
'''
from classReport import *
def valuesForPrintInGrid(hmnia='2011-11-28',db=None,fdir=None,tameio=None):
    sqlMain="""
    select logistiki_tran.id, logistiki_tran_d.id,logistiki_tran.par,logistiki_lmo.code,logistiki_lmo.per, xr,pi 
    from logistiki_tran 
    inner join logistiki_tran_d on logistiki_tran.id=logistiki_tran_d.tran_id
    inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id
    where imnia='%s'
    """ % hmnia
    
    sqlTotal="""
    select sum(xr),sum(pi) 
    from logistiki_tran 
    inner join logistiki_tran_d on logistiki_tran.id=logistiki_tran_d.tran_id
    inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id
    where imnia<'%s' and logistiki_lmo.code='%s'
    group by logistiki_tran_d.lmos_id
    """ % (hmnia,tameio)    
    
    titles = ['Παραστατικό','Λογαριασμός','Επωνυμία','Εισπράξεις','Πληρωμές','Χρέωση','Πίστωση']
    vFinal = []
    v = getData(sqlMain,db)
    totalsBefore = getData(sqlTotal,db)
    arthraTameioy = []
    tx ,tp, dx ,dp = 0,0,0,0
    rp = pdfReport(10,False)
    for l in v:
        if l[3] == tameio:
            arthraTameioy.append(l[0])
    for l in v:
        if l[0] in arthraTameioy:
            if l[3] == tameio:
                pass
            else:
                vFinal.append([rp.p(l[2]),rp.c(l[3]),rp.p(l[4]),rp.r(gr(l[6])),rp.r(gr(l[5])),rp.r(gr(0)),rp.r(gr(0))])
                tx += l[6]
                tp += l[5]
        else:
            vFinal.append([rp.p(l[2]),rp.c(l[3]),rp.p(l[4]),rp.r(gr(0)),rp.r(gr(0)),rp.r(gr(l[5])),rp.r(gr(l[6]))])
            dx += l[5]
            dp += l[6]
            
    yea, mon, da = hmnia.split('-')
    pdfFileName = 'ifs%s%s%s.pdf' % (yea,mon,da)
    if fdir:
        pdfFileName = '%s/%s' % (fdir,pdfFileName)
    pageTitle = u'Ημερήσιο Φύλλο Συναλλαγών της %s/%s/%s' % (da,mon,yea)
    if vFinal:
        try:
            ypol_old = totalsBefore[0][0]-totalsBefore[0][1]
        except:
            ypol_old = 0
        esMinusEj= tx-tp 
        ypol_new = ypol_old + esMinusEj
        vFinal.append([rp.p(''),rp.c(''),rp.pb(u'Σύνολα'),rp.rb(gr(tx)),rp.rb(gr(tp)),rp.rb(gr(dx)),rp.rb(gr(dp))])
        vFinal.append([rp.p(''),rp.c(''),rp.pb(u'Προηγούμενο υπόλοιπο'),rp.rb(gr(ypol_old)),rp.p(''),rp.p(''),rp.p('')])
        vFinal.append([rp.p(''),rp.c(''),rp.pb(u'Εισπράξεις - Πληρωμές'),rp.rb(gr(esMinusEj)),rp.p(''),rp.p(''),rp.p('')])
        vFinal.append([rp.p(''),rp.c(''),rp.pb(u'Υπόλοιπο σε Νέο'),rp.rb(gr(ypol_new)),rp.p(''),rp.p(''),rp.p('')])
        rp.makepdf(pageTitle,titles,vFinal,[100,80,250,80,80,80,80],pdfFileName)

def makePdf(apo,eos='',db=None,fdir=None,tameio=None):
    if eos == '' : 
        valuesForPrintInGrid(apo,db,fdir,tameio)
        print apo
        return
    def tx(no,size=2):
        s = '%s' % no
        d = size - len(s)
        if d > 0:
            s = ('0' * d)+s
        return s
    ya,ma,da = apo.split('-')
    ye,me,de = eos.split('-')
    pdfDates = []
    tmpYear = int(ya)
    tmpMonth= int(ma)
    tmpDay  = int(da)
    finalDay = int('%s%s%s' % (ye,me,de))
    while (True) :
        if tmpDay <= 31:
            pass
        else:
            tmpDay    = 1
            tmpMonth += 1
        if tmpMonth <= 12:
            pass
        else:
            tmpMonth  = 1
            tmpYear  += 1
        a = '%s%s%s' % (tx(tmpYear),tx(tmpMonth),tx(tmpDay))
        ia = int(a)
        if ia <= finalDay:
            dat = '%s-%s-%s' %(tx(tmpYear),tx(tmpMonth),tx(tmpDay))
            pdfDates.append(dat)
            tmpDay += 1
        else:
            break
    for el in pdfDates:
        print el
        valuesForPrintInGrid(el,db,fdir,tameio)
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        makePdf(sys.argv[1],sys.argv[2])
    elif len(sys.argv) == 2:    
        makePdf(sys.argv[1])
    else:
        makePdf('2010-12-31','','C:/prg/MyApplications/tedlogistiki/ted.sql3','C:/tmp','38.00.00.0000')