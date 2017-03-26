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
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER,TA_JUSTIFY

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
    styleSheet.add(ParagraphStyle(name='justStyle',fontName=fn,alignment=TA_JUSTIFY,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='normalCenterStyle',fontName=fn,alignment=TA_CENTER,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='numStyle',fontName=fni,alignment=TA_RIGHT,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='numStyleBold',fontName=fbi,alignment=TA_RIGHT,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='boldCenterStyle',fontName=fb,alignment=TA_CENTER,fontSize=fSize+2,leading=fSize+3))
    styleSheet.add(ParagraphStyle(name='boldCenterStyleSmall',fontName=fb,alignment=TA_CENTER,fontSize=fSize,leading=fSize))
    styleSheet.add(ParagraphStyle(name='intboldCenterStyle',fontName=fb,alignment=TA_CENTER,fontSize=fSize,leading=fSize))
    return styleSheet

story = []
styles =  customStyleSheet(15)

top_margin = 60 #distance from top edge
bottom_margin = 30 #distance from bottom edge
left_margin = 50 #distance from left edge
right_margin = 30 #distance from right edge
top_title = A4[1] - top_margin #Distance from bottom edge
right_title = A4[0] - left_margin #Distance from left edge
frame_width = right_title - left_margin
filename = 'test.pdf'
doc = doctemplate.SimpleDocTemplate(filename,
                                     rightMargin=right_margin, 
                                     leftMargin=left_margin, 
                                     topMargin=top_margin, 
                                     bottomMargin=bottom_margin)
def add(size=10,style='n',text=''):
    if text == '':
        story.append(Spacer(0,size))
        return
    if style == 'n':
        story.append(Paragraph(u'<font size=%s>%s</font>' % (size,text),styles['justStyle']))
    elif style == 't': # titlos
        story.append(Paragraph(u'<font size=%s>%s</font>' % (size,text),styles['boldCenterStyle']))
    elif style == 'r': # deksia
        story.append(Paragraph(u'<font size=%s>%s</font>' % (size,text),styles['numStyle']))
    
add(16,'t',u'ΑΤΟΜΙΚΗ ΣΥΜΒΑΣΗ ΕΡΓΑΣΙΑΣ ΜΕΡΙΚΗΣ ΑΠΑΣΧΟΛΗΣΗΣ')        
add(30)
add(12,'t',u'Ο ΕΡΓΟΔΟΤΗΣ')
add(10)
add(11,'n',u'Επωνυμία          :  ΑΚΤΗ ΦΑΡΑΓΓΑ ΠΑΡΟΥ ΕΠΕ')
add(11,'n',u'Δραστηριότητα     : Εστιατόριο - Μπάρ')
add(11,'n',u'Διεύθυνση         : Αγαθημέρου 3')
add(11,'n',u'Ον/μο εκπροσώπου  : Αθερίνης - Σπαρτιώτης Μιχάλης')
add(30)
add(12,'t',u'Ο ΕΡΓΑΖΟΜΕΝΟΣ')
add(11)
add(11,'n',u'Ονοματεπώνυμο : Μαυράκης Νικόλαος του Κωνσταντίνου')
add(11,'n',u'Διευθυνση κατοικίας : Κεδρηνού 66 , Αμπελόκηποι , Αθήνα τκ:11522')
add(11,'n',u'Στοιχεία Ταυτότητας : Α.Τ. Ξ5678')
add(30)
add(12,'t',u'ΟΥΣΙΩΔΕΙΣ ΟΡΟΙ')
add(10)
add(11,'n',u'Α.Είδος Σύμβασης : Αορίστου χρόνου')
add(11,'n',u'  1.Ημερομηνία έναρξης σύμβασης : 15/3/2010')
add(11,'n',u'  2.Ημερομηνία λήξης σύμβασης : ')
add(11,'n',u'Β.Χρόνος απασχόλησης')
add(11,'n',u'  1.Ημέρες εβδομαδιαίως : Μία')
add(11,'n',u'  2.Ώρες εβδομαδιαίως : 6')
add(11,'n',u'  3.Ωράριο ημερήσιας απασχόλησης : 10:30 - 16:30')
add(11,'n',u'Γ.Τόπος παροχής εργασίας: Αγαθημέρου 3 Αθήνα')
add(11,'n',u'Δ.Ειδικότητα εργαζομένου : Υπάλληλος γραφείου')
add(11,'n',u'Ε.Αποδοχές : 60,54 ευρώ')
add(30)
add(12,'t',u'ΟΙ ΣΥΜΒΑΛΛΟΜΕΝΟΙ')
add(10)
#add(11,'r',u'Δοκιμή')

doc.build(story) 