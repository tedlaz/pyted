# -*- coding: utf-8 -*-

import classReport as cr

if __name__ == '__main__':
    pin = {}
    pin['title'] = u'Δοκιμαστική εκτύπωση'
    pin['title2'] = u'Δεύτερη εταιρική χρήση'
    pin['foot'] = u'Ακτή Φάραγγα Πάρου ΕΠΕ ΑΦΜ:001122331' 
    pin['titles'] = [u'Δοκιμή', u'Παρ/κό', u'Ημ/νία', u'Ποσό']  
    #v.append([pr.tcb(u'Τέλος'), pr.tcb(u'Τέλος'),pr.dcb('1963-02-10'),pr.nb('1210.23')])
    pin['data'] = [[u'Δοκιμαστικό', u'ΤΠΥ334', '2015-01-01', 1245.24]] * 10
    pin['sizes'] = [120, 120, 60, 60]
    pin['filename'] = 'tst2.pdf'
    cr.create_portrait(pin)
