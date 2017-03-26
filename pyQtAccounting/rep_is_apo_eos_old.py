# -*- coding: utf-8 -*-
'''
Ισοζύγιο περιόδου από έως
'''
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, doctemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape, portrait 
from reportlab.platypus.tables import GRID_STYLE, LongTable
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

import sqlite3

pdfmetrics.registerFont(TTFont('fn',"Alkaios.ttf"))
pdfmetrics.registerFont(TTFont('fni',"Alkaios-Italic.ttf"))
pdfmetrics.registerFont(TTFont('fb',"Alkaios-Bold.ttf"))
pdfmetrics.registerFont(TTFont('fbi',"Alkaios-BoldItalic.ttf"))
'''
pdfmetrics.registerFont(TTFont('fcn',"FreeMono.ttf"))
pdfmetrics.registerFont(TTFont('fcni',"FreeMonoOblique.ttf"))
pdfmetrics.registerFont(TTFont('fcb',"FreeMonoBold.ttf"))
pdfmetrics.registerFont(TTFont('fcbi',"FreeMonoBoldOblique.ttf"))
'''
fn, fni, fb, fbi = 'fn', 'fni','fb','fbi'
#fcn, fcni, fcb, fcbi = 'fcn', 'fcni','fcb','fcbi'

def getData(sql,DB):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(sql)
    v1 = cur.fetchall()
    cur.close()
    con.close()
    return v1

def stylesAdd(styleSheet,fSize=12):
    styleSheet.add(ParagraphStyle(name='normalStyle',fontName=fn,alignment=TA_LEFT,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='normalCenterStyle',fontName=fn,alignment=TA_CENTER,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='numStyle',fontName=fni,alignment=TA_RIGHT,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='numStyleBold',fontName=fbi,alignment=TA_RIGHT,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='boldCenterStyle',fontName=fb,alignment=TA_CENTER,fontSize=fSize+2,leading=fSize+3))
style_sheet = getSampleStyleSheet()
stylesAdd(style_sheet,10)

def pb(txt):
    return Paragraph(txt, style=style_sheet["boldCenterStyle"])
def p(txt):
    return Paragraph(txt,style=style_sheet["normalStyle"])
def r(txt):
    return Paragraph(txt,style=style_sheet["numStyle"])
def rb(txt):
    return Paragraph(txt,style=style_sheet["numStyleBold"])
def c(txt):
    return Paragraph(txt,style=style_sheet["normalCenterStyle"])
    
def makepdf(vals,titles,pageTitle,colwidths=[25,200,50,40,60,60,60,60,60,60,60,40],filename='test'):
    top_margin = 60 #distance from top edge
    bottom_margin = 30 #distance from bottom edge
    left_margin = 30 #distance from left edge
    right_margin = 30 #distance from right edge
    top_title = A4[1] - top_margin #Distance from bottom edge
    right_title = A4[0] - left_margin #Distance from left edge
    frame_width = right_title - left_margin
    doct = doctemplate.SimpleDocTemplate(filename,rightMargin=right_margin, leftMargin=left_margin, topMargin=top_margin, bottomMargin=bottom_margin)#,pagesize=landscape(A4))
    PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
    Title = pageTitle #u"Δοκιμαστική Εκτύπωση Μισθοδοσίας"
    company = u"Ακτή Φάραγγα Πάρου ΕΠΕ"
    URL = "http://users.otenet.gr/~tedlaz"
    email = "nicopolise@gmail.com"
    addr  = u"Αγαθημέρου 3 Αθήνα"
    afm   = u"999249820"
    pageinfo = u"%s , %s , ΑΦΜ:%s / %s /" % (company, addr,afm, Title)
     
    def myFirstPage(canvas, doc):
        canvas.saveState()
        canvas.setFont(fb,20)
        canvas.drawString(100, PAGE_HEIGHT-56, Title)
        canvas.setFont(fni,9)
        canvas.drawString(inch-60, inch-60, u"%s , %s , ΑΦΜ:%s / %s / Σελίδα %s" % (company, addr,afm, Title,canvas.getPageNumber()))
        canvas.restoreState()
        
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont(fni,9)
        canvas.line(left_margin, top_title, right_title, top_title)
        canvas.drawString(left_margin+4, top_title + 4, Title)
        canvas.setFont(fb,9)
        canvas.drawRightString(right_title-8, top_title + 4, '%s' % canvas.getPageNumber())
        canvas.line(left_margin, bottom_margin, right_title, bottom_margin)
        canvas.restoreState()    
    data = []
    rr = []
    for e in titles:
        rr.append(pb(e))
    data.append(rr)
    for val in vals:
        data.append(val)
    style = GRID_STYLE
    style.add(*('VALIGN', (0,0), (-1,-1), 'MIDDLE'))
    style.add(*('LEFTPADDING', (0,0), (-1,-1), 3))
    style.add(*('TOPPADDING', (0,0), (-1,-1), 1))
    #style.add(*('BOTTOMPADDING', (0, 0), (-1, -1), 0))
    style.add(*('RIGHTPADDING', (0,0), (-1,-1), 3))
    table = LongTable(data, colWidths=colwidths, rowHeights=17, style=style,repeatRows=True)
    a = []
    a.append(table)
    page_flowables = [table]
    doct._doSave = 0
    doct.build(a,onFirstPage=myFirstPage, onLaterPages=myFirstPage)
    canvas = doct.canv
    canvas.setTitle("Some title")
    canvas.save()

def valuesForPrintInGrid(hmapo='2011-11-28',hmeos='2011-12-31'):
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
    #and logistiki_lmo.code like '50%%'
    titles = ['Λογαριασμός','Επωνυμία','Πρίν','Περίοδος','Υπόλοιπο']
   
    vbefore = getData(sqlBefore,'aktiFaragga.sql3')
    vmain   = getData(sqlMain,'aktiFaragga.sql3')
    logsxed = getData(sqlLogsx,'aktiFaragga.sql3')
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
    for lmo in logsxed:
        y = fbefore[lmo[0]] + fmain[lmo[0]]
        if abs(y) > 0.004 or abs(fbefore[lmo[0]]) > 0.004 or abs(fmain[lmo[0]]) > 0.004:
            vFinal.append([c(lmo[0]),p(lmo[1]),r(gr(fbefore[lmo[0]])),r(gr(fmain[lmo[0]])),r(gr(y))])
    
    yea, mon, da = hmapo.split('-')
    yea1,mon1,da1= hmeos.split('-')
    pdfFileName = 'i%s%s%s-%s%s%s.pdf' % (yea, mon, da,yea1,mon1,da1)
    pageTitle = u'Ισοζύγιο από %s/%s/%s έως %s/%s/%s' % (da,mon,yea,da1,mon1,yea1)
    if vFinal:
        #vFinal.append([c(''),pb(u'Σύνολα'),rb(gr(tx)),rb(gr(tp)),rb(gr(tx-tp))])
        #vFinal.append([c(''),pb(u'(2)+(6)+(7)+(8)'),rb(''),rb(''),rb(gr(f[2]+f[6]+f[7]+f[8]))])
        makepdf(vFinal,titles,pageTitle,[80,250,70,70,70],pdfFileName)
        
def gr(number):
    if abs(number) <= 0.004:
        return ''
    s = '%.2f' % number
    a,d = s.split('.')
    groups = []
    while a and a[-1].isdigit():
        groups.append(a[-3:])
        a = a[:-3]
    return a + '.'.join(reversed(groups)) +','+d

def makePdf(apo,eos=''): 
    valuesForPrintInGrid(apo)
if __name__ == '__main__':
    makePdf('2011-09-30')
    #makePdf('2010-12-30','2010-12-31')
    #test()