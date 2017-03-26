from fpdf.ted_helper2 import Tfpdf


def report(data=[{'poso': 100, 'foros': 10}, {'poso': 30, 'foros': 3}]):
    aa = Tfpdf()
    for el in data:
        aa.new_page()
        le = 46
        aa.hp.txtc(le, 15, 'ΕΛΛΗΝΙΚΗ ΔΗΜΟΚΡΑΤΙΑ')
        aa.hp.txtcb(le, 20, 'ΔΗΜΟΣ ΑΘΗΝΑΙΩΝ', 14)
        aa.hp.txtc(le, 25, 'Δ/ΝΣΗ ΔΗΜΟΤ. ΠΡΟΣΟΔΩΝ')
        aa.hp.txtc(le, 30, 'ΤΜΗΜΑ ΤΕΛΩΝ ΠΑΡΕΠΙΔΗΜΟΥΝΤΩΝ')
        aa.hp.txtc(le, 35, '& ΕΣΟΔΩΝ ΚΕΝΤΡΩΝ ΔΙΑΣΚΕΔΑΣΕΩΣ')
        aa.hp.txtcb(100, 48, 'ΔΗΛΩΣΗ ΤΕΛΟΥΣ 0,5%', 14)
        aa.hp.boxetit(15, 110, 'Α.Φ.Μ.:', '999249820')
        aa.hp.boxetit(15, 120, 'ΑΜΚΑ ΚΑΙ ΚΑΛΑ ΚΡΑΣΙΑ:', '12345678912')
        aa.hp.txtl(15, 65, 'Ποσό: %s' % el['poso'])
        aa.hp.txtl(15, 75, 'Φόρος: %s' % el['foros'])
    aa.save()

report()