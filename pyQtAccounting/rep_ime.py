# -*- coding: utf-8 -*-
'''
Ημερολόγιο Κινήσεων
'''
from classReport import *
def imerologioData(apo='2011-01-01',eos='2011-12-31',db='aktiFaragga.sql3'):
    sqlMain="""
    select logistiki_tran.imnia,logistiki_tran.id, logistiki_tran_d.id,logistiki_tran.par,logistiki_tran.per,logistiki_lmo.code,logistiki_lmo.per,per2, xr,pi 
    from logistiki_tran 
    inner join logistiki_tran_d on logistiki_tran.id=logistiki_tran_d.tran_id
    inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id
    where logistiki_tran.imnia between '%s' and '%s'
    order by imnia, logistiki_tran.id, logistiki_tran_d.id
    """ % (apo,eos)
      
    titles = ['Ημ/νία','Νο','Παρ/κό','Περιγραφή','Περ2','Χρέωση','Πίστωση']
    vFinal = []
    v = getData(sqlMain,db)
    arthra = []
    rp = pdfReport(10,False)
    arthroNo = 0
    vf = []
    for l in v:
        if arthroNo <> l[1]:
            arthroNo = l[1]
            vf.append([rp.p(grd(l[0])),rp.p('%s' % l[1]),rp.p(l[3]),rp.p(l[4]),rp.p(''),rp.c(''),rp.c('')])
        vf.append([rp.p(''),rp.p(''),rp.p(l[5]),rp.p(l[6]),rp.p(l[7]),rp.r(gr(l[8])),rp.r(gr(l[9]))])

    pdfFileName = 'im%s%s.pdf' % (apo,eos)

    pageTitle = u'Ημερολόγιο Εγγραφών από %s έως %s' % (grd(apo),grd(eos))
    if vf:
        rp.makepdf(pageTitle,titles,vf,[55,30,80,250,150,80,80],pdfFileName)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        imerologioData(sys.argv[1],sys.argv[2])
    elif len(sys.argv) == 2:    
        imerologioData(sys.argv[1],sys.argv[1])
    else:
        imerologioData('2000-01-01','2300-12-31')