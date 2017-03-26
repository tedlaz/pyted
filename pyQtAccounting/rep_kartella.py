# -*- coding: utf-8 -*-
'''
Ισοζύγιο περιόδου από έως
'''
from classReport import *

def kartellaLmoyApoEos(lmos,apo,eos,db=None,pdfName=None):
    sqlBefore="""
    select sum(xr),sum(pi) 
    from logistiki_tran 
    inner join logistiki_tran_d on logistiki_tran.id=logistiki_tran_d.tran_id
    inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id
    where imnia<'%s' and logistiki_lmo.code='%s'
    """ % (apo,lmos) 
    sqlMain="""
    select logistiki_tran.imnia,logistiki_tran.id, logistiki_tran_d.id,logistiki_tran.par,logistiki_tran.per,logistiki_lmo.code,logistiki_lmo.per,per2, xr,pi 
    from logistiki_tran 
    inner join logistiki_tran_d on logistiki_tran.id=logistiki_tran_d.tran_id
    inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id
    where logistiki_lmo.code='%s' and logistiki_tran.imnia between '%s' and '%s'
    order by imnia, logistiki_tran.id, logistiki_tran_d.id
    """ % (lmos,apo,eos)   
    lm = getData("select code,per from logistiki_lmo where code='%s'" % lmos,db)
    if lm:
        lmostr = '%s ( %s )' % (lm[0][1],lm[0][0])
    else:
        print 'Not a valid account'
        return
    vbefore = getData(sqlBefore,db)
    vmain   = getData(sqlMain,db)
    try:
        if vbefore[0][0] > vbefore[0][1] :
            bxr = vbefore[0][0] - vbefore[0][1]
            bpi = 0
        else:
            bxr = 0
            bpi = vbefore[0][1] - vbefore[0][0]
    except:
        bxr = bpi = 0
    rsum = bxr - bpi
    txr = 0
    tpi = 0
    rp = pdfReport(10,True)
    titles      = ['Ημνία','Παρ/κό','Περιγραφή','Χρέωση','Πίστωση','Υπόλοιπο']
    v = []
    v.append([rp.p(''),rp.p(''),rp.p('Από μεταφορά'),rp.r(gr(bxr)),rp.r(gr(bpi)),rp.r(gr(rsum))])
    for l in vmain:
        rsum = rsum + l[8] - l[9]
        txr += l[8]
        tpi += l[9]
        v.append([rp.p(grd(l[0])),rp.p(l[3]),rp.p(l[4]),rp.r(gr(l[8])),rp.r(gr(l[9])),rp.r(gr(rsum))])
    pageTitle   = u'%s' % lmostr
    ptitle2     = u'%s έως %s' % (grd(apo),grd(eos))
    colwidths   = [50,60,250,60,60,60]
    sapo = apo.replace('-','')
    seos = eos.replace('-','')

    if v:
        v.append([rp.p(''),rp.p(''),rp.pb('Σύνολο περιόδου'),rp.rb(gr(txr)),rp.rb(gr(tpi)),rp.rb(gr(txr-tpi))])
        v.append([rp.p(''),rp.p(''),rp.pb('Γενικό σύνολο'),rp.rb(gr(txr+bxr)),rp.rb(gr(tpi+bpi)),rp.rb(gr(txr-tpi+bxr-bpi))])
        rp.makepdf(pageTitle,titles,v,colwidths,'%s' % pdfName,ptitle2)
        print 'kartella is ok'  
if __name__ == '__main__':
    pass
    