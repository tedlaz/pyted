# -*- coding: utf-8 -*-
'''
Ισοζύγιο περιόδου
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

fn, fni, fb, fbi = 'fn', 'fni','fb','fbi'

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
        canvas.drawString(208, PAGE_HEIGHT-56, Title)
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

def valuesForPrintInGrid(db,pdfFileName):
    sqlMain="""
    select logistiki_lmo.code,logistiki_lmo.per, sum(xr),sum(pi) 
    from logistiki_tran 
    inner join logistiki_tran_d on logistiki_tran.id=logistiki_tran_d.tran_id
    inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id
    where logistiki_lmo.code like '50%%'
    group by logistiki_tran_d.lmos_id
    order by logistiki_lmo.code
    """
    #and logistiki_lmo.code like '50%%'
    titles = ['Λογαριασμός','Επωνυμία','Χρέωση','Πίστωση','Υπόλοιπο']
    vFinal = []
    v = getData(sqlMain,db)
    tx ,tp, x1 ,p1 = 0,0,0,0
    lmos1 = ''
    f={}
    for i in range(10):
        f[i] = 0
    for l in v:
        if lmos1 <> l[0][0]:
            if lmos1 <> '':
                vFinal.append([pb(lmos1),pb(u'Σύνολο ομάδας %s' % lmos1),rb(gr(x1)),rb(gr(p1)),rb(gr(x1-p1))])
                f[int(lmos1)] = x1-p1
                x1 = 0
                p1 = 0
            lmos1 = l[0][0]

        delta = l[2] - l[3]
        if abs(delta) <= 0.004:
            pass
        else:
            vFinal.append([c(l[0]),p(l[1]),r(gr(l[2])),r(gr(l[3])),r(gr(l[2]-l[3]))])
            tx += l[2]
            tp += l[3]
            x1 += l[2]
            p1 += l[3]
    vFinal.append([pb(lmos1),pb(u'Σύνολο ομάδας %s' % lmos1),rb(gr(x1)),rb(gr(p1)),rb(gr(x1-p1))])
    f[int(lmos1)] = x1-p1
    #pdfFileName = 'isTot50.pdf'
    pageTitle = u'Ισοζύγιο προμηθευτών' 
    if vFinal:
        vFinal.append([c(''),pb(u'Σύνολα'),rb(gr(tx)),rb(gr(tp)),rb(gr(tx-tp))])
        #vFinal.append([c(''),pb(u'(2)+(6)+(7)+(8)'),rb(''),rb(''),rb(gr(f[2]+f[6]+f[7]+f[8]))])
        makepdf(vFinal,titles,pageTitle,[80,250,80,80,80],pdfFileName)
        
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
    
def ConfigSectionMap(section,Config):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
    
def runReport(db,pdfFileName):
    valuesForPrintInGrid(db,pdfFileName)
    from subprocess import call
    
    import ConfigParser
    import os
    Config = ConfigParser.ConfigParser()
    if not os.path.isfile('tst.ini'):
        inifile = open("tst.ini",'w')
        Config.add_section('pdf')
        Config.set('pdf','pdf_program','C:/Program Files (x86)/SumatraPDF/SumatraPDF.exe')
        Config.write(inifile)
        inifile.close()
    Config.read("tst.ini")
    pdfProgram = ConfigSectionMap("pdf",Config)['pdf_program']
    call([pdfProgram, '%s' % pdfFileName])
        
if __name__ == '__main__':        
    runReport('gasbah1.sql3','isTot50.pdf')