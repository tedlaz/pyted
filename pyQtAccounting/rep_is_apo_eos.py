# -*- coding: utf-8 -*-
'''
Ισοζύγιο περιόδου από έως
'''
import classReport as cr

def isozygioApoEos(hmapo,hmeos,db=None,pdfFile=None):
    sqlBefore="""
    select logistiki_lmo.code, sum(xr),sum(pi) 
    from logistiki_tran 
    inner join logistiki_tran_d on logistiki_tran.id=logistiki_tran_d.tran_id
    inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id
    where imnia<'%s' 
    group by logistiki_tran_d.lmos_id
    order by logistiki_lmo.code
    """ % hmapo 
    sqlMain="""
    select logistiki_lmo.code, sum(xr),sum(pi) 
    from logistiki_tran 
    inner join logistiki_tran_d on logistiki_tran.id=logistiki_tran_d.tran_id
    inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id
    where imnia between '%s' and '%s'
    group by logistiki_tran_d.lmos_id
    order by logistiki_lmo.code
    """ % (hmapo,hmeos)
    sqlLogsx = "select code,per from logistiki_lmo order by code"    
    #and logistiki_lmo.code like '50%% 
   
    vbefore = cr.getData(sqlBefore,db)
    vmain   = cr.getData(sqlMain,db)
    logsxed = cr.getData(sqlLogsx,db)
    fbefore = {}
    fmain   = {}
    for lmo in logsxed:
        fbefore[lmo[0]] = 0
        fmain[lmo[0]]   = 0
    for el in vbefore:
        fbefore[el[0]] = el[1]-el[2]
    for el in vmain:
        fmain[el[0]] = el[1]-el[2]
    vFinal = []
    omBefore = {}
    omMain   = {}
    omAfter  = {}
    prot50   = [0,0,0]
    for i in range(10):
        omBefore[i] = 0
        omMain[i]   = 0
        omAfter[i]  = 0
    rp = cr.pdfReport(10,True)
    o = int(logsxed[0][0][0])
    for lmo in logsxed:
        y = fbefore[lmo[0]] + fmain[lmo[0]]
        if abs(y) > 0.004 or abs(fbefore[lmo[0]]) > 0.004 or abs(fmain[lmo[0]]) > 0.004:
            omNo = int(lmo[0][0])
            omBefore[omNo] += fbefore[lmo[0]]
            omMain[omNo]   += fmain[lmo[0]]
            omAfter[omNo]  += y
            if o <> omNo:
                vFinal.append([rp.pb('%s' % o),rp.pb('Σύνολο ομάδας %s' % o),rp.rb(cr.gr(omBefore[o])),rp.rb(cr.gr(omMain[o])),rp.rb(cr.gr(omAfter[o]))])
                o = omNo
            vFinal.append([rp.c(lmo[0]),rp.p(lmo[1]),rp.r(cr.gr(fbefore[lmo[0]])),rp.r(cr.gr(fmain[lmo[0]])),rp.r(cr.gr(y))])
            #print lmo[0][:1]
            if int(lmo[0][:2]) == 50:
                prot50[0] += fbefore[lmo[0]]
                prot50[1] += fmain[lmo[0]]
                prot50[2] += y
    vFinal.append([rp.pb('%s' % o),rp.pb('Σύνολο ομάδας %s' % o),rp.rb(cr.gr(omBefore[o])),rp.rb(cr.gr(omMain[o])),rp.rb(cr.gr(omAfter[o]))])
    #vFinal.append([rp.pb('%s' % o),rp.pb('Σύνολο ομάδας %s' % o),rp.rb(cr.gr(omBefore[o])),rp.rb(cr.gr(omMain[o])),rp.rb(cr.gr(omAfter[o]))])
    apB = omBefore[2]+omBefore[6]+omBefore[7]+omBefore[8]
    apM = omMain[2]+omMain[6]+omMain[7]+omMain[8]
    apA = omAfter[2]+omAfter[6]+omAfter[7]+omAfter[8]
    vFinal.append([rp.pb(''),rp.pb('(2)+(6)+(7)+(8)'),rp.rb(cr.gr(apB)),rp.rb(cr.gr(apM)),rp.rb(cr.gr(apA))])
    vFinal.append([rp.pb(''),rp.pb('50 '),rp.rb(cr.gr(prot50[0])),rp.rb(cr.gr(prot50[1])),rp.rb(cr.gr(prot50[2]))])
    yea, mon, da = hmapo.split('-')
    yea1,mon1,da1= hmeos.split('-')
    
    pageTitle   = u'Ισοζύγιο από %s/%s/%s έως %s/%s/%s' % (da,mon,yea,da1,mon1,yea1)
    titles      = ['Λογαριασμός','Επωνυμία','Από μεταφ.','Περίοδος','Υπόλοιπο']
    colwidths   = [80,250,70,70,70]
    #pdfFileName = 'i%s%s%s-%s%s%s.pdf' % (yea, mon, da,yea1,mon1,da1)
    if vFinal:
        rp.makepdf(pageTitle,titles,vFinal,colwidths, '%s' % pdfFile)
        print 'isozygioApoEos is ok'
if __name__ == '__main__':
    import sys
    if   len(sys.argv) == 4:
        isozygioApoEos(sys.argv[1],sys.argv[2],sys.argv[3])
    elif len(sys.argv) == 3:
        isozygioApoEos(sys.argv[1],sys.argv[2])
    else:
        isozygioApoEos('2011-10-01','2011-12-31')
    