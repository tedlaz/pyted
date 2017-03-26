# -*- coding: utf-8 -*-

import classReport as cr
def rs(v,no):
    trs = 0
    for el in v:
        trs += el[no]
        el.append(trs)
    return true
 
pr  = cr.paragraph()
titles = ['Δοκιμή','Παρ/κό']
title  = u'Δοκιμαστική εκτύπωση'
title2 = u'Kala krasia'
foot   = u'Ακτή Φάραγγα Πάρου ΕΠΕ ΑΦΜ:001122331' 

v = []
for i in range(10):
    v.append([pr.d('1963-02-10'),pr.n(10.23)])
v.append([pr.dcb('1963-02-10'),pr.nb('10.23')])

rep = cr.pdfReport()
rep.makepdf(title,titles,v,[60,60],'a.pdf',title2,foot)