# -*- coding: utf-8 -*-
'''
Κλάση για δημιουργία grid reports
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

import ted_utils as tu

import os
pdfmetrics.registerFont(TTFont('fn',os.path.join(os.path.dirname(__file__), 'Alkaios.ttf')))
pdfmetrics.registerFont(TTFont('fni',os.path.join(os.path.dirname(__file__), 'Alkaios-Italic.ttf')))
pdfmetrics.registerFont(TTFont('fb',os.path.join(os.path.dirname(__file__), 'Alkaios-Bold.ttf')))
pdfmetrics.registerFont(TTFont('fbi',os.path.join(os.path.dirname(__file__), 'Alkaios-BoldItalic.ttf')))

fn, fni, fb, fbi = 'fn', 'fni','fb','fbi'

   
def gr(number):
    number = tu.dec(number)
    if abs(number) <= 0.004:
        return ''
    s = '%.2f' % number
    a,d = s.split('.')
    groups = []
    while a and a[-1].isdigit():
        groups.append(a[-3:])
        a = a[:-3]
    return a + '.'.join(reversed(groups)) +','+d

def grint(number):
    number = tu.dec(number)
    if abs(number) <= 0.004:
        return ''
    s = '%.1f' % number
    a,d = s.split('.')
    groups = []
    while a and a[-1].isdigit():
        groups.append(a[-3:])
        a = a[:-3]
    return a + '.'.join(reversed(groups)) +','+d

def grd(imnia):
    y,m,d = imnia.split('-')
    return '%s/%s/%s' % (d,m,y)

def customStyleSheet(fSize):
    styleSheet = getSampleStyleSheet()
    styleSheet.add(ParagraphStyle(name='normalStyle',fontName=fn,alignment=TA_LEFT,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='normalCenterStyle',fontName=fn,alignment=TA_CENTER,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='numStyle',fontName=fni,alignment=TA_RIGHT,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='numStyleBold',fontName=fbi,alignment=TA_RIGHT,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='boldCenterStyle',fontName=fb,alignment=TA_CENTER,fontSize=fSize+2,leading=fSize+3))
    styleSheet.add(ParagraphStyle(name='boldCenterStyleSmall',fontName=fb,alignment=TA_CENTER,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='intboldCenterStyle',fontName=fb,alignment=TA_CENTER,fontSize=fSize,leading=fSize))
    return styleSheet

def gridStyle():
    style = GRID_STYLE
    style.add(*('VALIGN', (0,0), (-1,-1), 'MIDDLE'))
    style.add(*('LEFTPADDING', (0,0), (-1,-1), 3))
    style.add(*('TOPPADDING', (0,0), (-1,-1), 1))
    #style.add(*('BOTTOMPADDING', (0, 0), (-1, -1), 0))
    style.add(*('RIGHTPADDING', (0,0), (-1,-1), 3))
    return style

class paragraph():
    def __init__(self,fontSize=10):
        self.styleSheet = customStyleSheet(fontSize)
        
    def t(self,txt): #Text Left normal
        return Paragraph(txt,style=self.styleSheet["normalStyle"])
        
    def tc(self,txt):#Text center normal
        return Paragraph(txt,style=self.styleSheet["normalCenterStyle"])
        
    def tcb(self,txt): # Text Center Bold
        return Paragraph(txt, style=self.styleSheet["boldCenterStyle"])
        
    def n(self,txt): #Number right
        txt = gr(txt)
        return Paragraph(txt,style=self.styleSheet["numStyle"])
        
    def i(self,txt): #Number right
        txt = grint(txt)
        return Paragraph(txt,style=self.styleSheet["normalCenterStyle"])
        
    def ib(self,txt): #Number right
        txt = grint(txt)
        return Paragraph(txt,style=self.styleSheet["intboldCenterStyle"])
        
    def nb(self,txt): #Number right bold
        txt = gr(txt)
        return Paragraph(txt,style=self.styleSheet["numStyleBold"])
        
    def d(self,txt): #Date left
        txt = grd(txt)
        return Paragraph(txt,style=self.styleSheet["normalStyle"])
        
    def dc(self,txt): #Date center
        txt = grd(txt)
        return Paragraph(txt,style=self.styleSheet["normalCenterStyle"])
        
    def dcb(self,txt): #Date center bold
        txt = grd(txt)
        return Paragraph(txt,style=self.styleSheet["boldCenterStyle"])
    
    def f(self,val,typ):
        if   typ == 't'  : return self.t(val)
        elif typ == 'tc' : return self.tc(val)
        elif typ == 'tcb': return self.tcb(val)
        elif typ == 'n'  : return self.n(val)
        elif typ == 'i'  : return self.i(val)
        elif typ == 'ib' : return self.ib(val)
        elif typ == 'nb' : return self.nb(val)
        elif typ == 'd'  : return self.d(val)
        elif typ == 'dc' : return self.dc(val)
        elif typ == 'dcb': return self.dcb(val)
        else             : return self.t(val)
        
def makePrintTable(vals,typeArr,sumArr,hasAA = True):
    v1 = vals # [['test',100,20],['lin2',5,4]]
    ta = typeArr #['t','n','n']
    sa = sumArr #[ 0 , 1 , 1 ]
    v = []
    t = []
    cols = len(v1[0])
    pr = paragraph()
    aaNo = 1
    for i in range(cols):
        if sa[i] == 0:
            t.append(pr.tc(''))
        else:
            t.append(0)
    for lin in v1:
        l=[]
        if hasAA:
            l.append(aaNo)
            aaNo += 1
        for i in range(cols):
            l.append(pr.f(lin[i],ta[i]))    
            if sa[i] == 1 :
                t[i] += lin[i]
        v.append(l) 
    for i in range(cols):
        if sa[i] == 1:
            t[i] = pr.nb(t[i])
    if hasAA:
        k = []
        k.append(pr.tc(''))
        for el in t:
            k.append(el)
        v.append(k)
    else:
        v.append(t)
    return v    
class pdfReport():
    def __init__(self,fontSize=10,portrait=True):
        self.styleSheet = customStyleSheet(fontSize)
        self.portrait = portrait
        self.fontSize = fontSize
    def pb(self,txt):
        return Paragraph(txt, style=self.styleSheet["boldCenterStyleSmall"])
    def p(self,txt):
        return Paragraph(txt,style=self.styleSheet["normalStyle"])
    def r(self,txt):
        txt = gr(txt)
        return Paragraph(txt,style=self.styleSheet["numStyle"]) # Number style
    def rb(self,txt):
        txt = gr(txt)
        return Paragraph(txt,style=self.styleSheet["numStyleBold"]) # Bold Number style
    def c(self,txt):
        return Paragraph(txt,style=self.styleSheet["normalCenterStyle"])
    
    def makepdf(self,pageTitle,titles,vals,colwidths,filename,ptitle2='',footer=''):
        top_margin = 60 #distance from top edge
        bottom_margin = 30 #distance from bottom edge
        left_margin = 30 #distance from left edge
        right_margin = 30 #distance from right edge
        top_title = A4[1] - top_margin #Distance from bottom edge
        right_title = A4[0] - left_margin #Distance from left edge
        frame_width = right_title - left_margin
        if self.portrait:
            doct = doctemplate.SimpleDocTemplate(filename,rightMargin=right_margin, leftMargin=left_margin, topMargin=top_margin, bottomMargin=bottom_margin)
            PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
        else:
            doct = doctemplate.SimpleDocTemplate(filename,rightMargin=right_margin, leftMargin=left_margin, topMargin=top_margin, bottomMargin=bottom_margin,pagesize=landscape(A4))
            PAGE_HEIGHT=defaultPageSize[0]; PAGE_WIDTH=defaultPageSize[1]
        #company = u"Ακτή Φάραγγα Πάρου ΕΠΕ"
        #URL = "http://users.otenet.gr/~tedlaz"
        #email = "nicopolise@gmail.com"
        #addr  = u"Αγαθημέρου 3 Αθήνα"
        #afm   = u"999249820"
        #pageinfo = u"%s , %s , ΑΦΜ:%s / %s /" % (company, addr,afm, pageTitle)
         
        tableData = []
        headerData = []
        for e in titles:
            headerData.append(self.pb(e))
        tableData.append(headerData)
        for val in vals:
            tableData.append(val)
        table = LongTable(tableData, colWidths=colwidths, rowHeights=self.fontSize+12, style=gridStyle(),repeatRows=True)
        a = []
        a.append(table)
        doct._doSave = 0

        def myFirstPage(canvas, doc):
            canvas.saveState()
            canvas.setFont(fb,self.fontSize+6)
            canvas.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT-45, pageTitle)
            if len(ptitle2) > 0:
                canvas.setFont(fb,self.fontSize)
                canvas.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT-58, ptitle2)
            canvas.setFont(fni,9)
            canvas.drawString(inch-60, inch-60, u"%s   Σελίδα: %s" % (footer,canvas.getPageNumber()))
            canvas.restoreState()
 
        doct.build(a,onFirstPage=myFirstPage, onLaterPages=myFirstPage)
        canvas = doct.canv
        canvas.setTitle(pageTitle)
        canvas.save()
    