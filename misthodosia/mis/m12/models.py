# -*- coding: utf-8 -*-
from django.db import models
#from mis.tedutils import dec as d
import locale
locale.setlocale(locale.LC_ALL, '')

class DbFld(models.Model):
    fldnam = models.CharField(verbose_name=u'Όνομα πεδίου σε DB',help_text=u'Όνομα πεδίου στους πίνακες της DB',max_length=30,unique=True)
    fldlbl  = models.CharField(verbose_name=u'Τίτλος πεδίου',help_text=u'Τίτλος πεδίου ',max_length=30)

    def __unicode__(self):
        return u"%s %s" % (self.fldName, self.fldLbl)
        
    class Meta:
        ordering = ['fldName']
        verbose_name = u'Ονομα και τίτλος πεδίου'
        verbose_name_plural = u'Ονόματα και τίτλοι πεδίων'
            
class CoTyp(models.Model):
    cotyp  = models.CharField(verbose_name=u'Κωδικός',help_text=u'Κωδικός τύπου',max_length=1,unique=True)
    cotypp = models.CharField(verbose_name=u'Τύπος επιχείρησης',help_text=u'Τύπος επιχείρησης',max_length=1,unique=True)
    
    def __unicode__(self):
        return u"%s %s" % (self.cotyp, self.cotypp)
        
    class Meta:
        ordering = ['cotyp']
        verbose_name = u'Τύπος επιχείρησης'
        verbose_name_plural = u'Τύποι επιχείρησης' 
           
class Co(models.Model):
    cop = models.CharField(verbose_name=u'Επωνυμία',help_text=u'Επωνυμία εταιρείας ή Επώνυμο',max_length=60,unique=True)
    o1no = models.CharField(verbose_name=u'Όνομα',help_text=u'όνομα φυσικού προσώπου',max_length=20,blank=True)
    pat = models.CharField(verbose_name=u'Πατρώνυμο',help_text=u'Πατρώνυμο φυσικού προσώπου',max_length=20,blank=True)
    cotyp = models.ForeignKey(CoTyp,verbose_name=u'Τύπος επιχείρησης')
    ame = models.CharField(verbose_name=u'A.M.E.',help_text=u'Αριθμός Μητρώου ΙΚΑ Επιχείρησης',max_length=10,unique=True)
    afm = models.CharField(verbose_name=u'Α.Φ.Μ.',help_text=u'Αριθμός Φορολογικού Μητρώου',max_length=9,unique=True)
    doy = models.CharField(verbose_name=u'Εφορία',help_text=u'Εφορία που ανήκει',max_length=60)
    dra = models.CharField(verbose_name=u'Δραστηριότητα',help_text=u'Αντικείμενο δραστηριότητας εταιρείας',max_length=60)
    pol = models.CharField(verbose_name=u'Πόλη',help_text=u'Διεύθυνση Πόλη',max_length=30)
    odo = models.CharField(verbose_name=u'Οδός',help_text=u'Διεύθυνση Οδός',max_length=30)
    num = models.CharField(verbose_name=u'Αριθμός',help_text=u'Διεύθυνση Αριθμός',max_length=5)
    tk  = models.CharField(verbose_name=u'ΤΚ',help_text=u'Ταχυδρομικός κωδικός',max_length=5)
    ikac= models.CharField(verbose_name=u'Κωδικός Υποκαταστήματος ΙΚΑ',help_text=u'ΙΚΑ υποβολής',max_length=3)
    ikap= models.CharField(verbose_name=u'Υποκατάστημα ΙΚΑ',help_text=u'Ονομασία υποκαταστήματος ΙΚΑ',max_length=50)
    
    def __unicode__(self):
        return u"%s %s" % (self.cop, self.afm)
        
    class Meta:
        ordering = ['cop']
        verbose_name = u'Εταιρεία'
        verbose_name_plural = u'Εταιρείες'
        
class Coy(models.Model):
    co  = models.ForeignKey(Co,verbose_name=u'Εταιρεία',help_text=u'Εταιρεία')
    coyp= models.CharField(verbose_name=u'Υποκατάστημα',help_text=u'Ονομασία υποκαταστήματος',max_length=60,unique=True)
    kad = models.CharField(verbose_name=u'ΚΑΔ',help_text=u'Κωδικός αριθμός δραστηριότητας',max_length=4)
    
    def __unicode__(self):
        return u"%s %s" % (self.co, self.coyp)
        
    class Meta:
        ordering = ['co','coyp']
        verbose_name = u'Υποκατάστημα'
        verbose_name_plural = u'Υποκαταστήματα'
                      
class Xrisi(models.Model):
    xrisi  = models.CharField(verbose_name=u'Χρήση',help_text=u'Χρήση',max_length=4,unique=True)
    xrisip = models.CharField(verbose_name=u'Περιγραφή',help_text=u'Περιγραφή χρήσης',max_length=50,unique=True)
    
    def __unicode__(self):
        return u"%s" % self.xrisi
        
    class Meta:
        ordering = ['xrisi']
        verbose_name = u'Χρήση'
        verbose_name_plural = u'Χρήσεις'
        
class Dimino(models.Model):
    dimp = models.CharField(verbose_name=u'Δίμηνο',help_text=u'Δίμηνο',max_length=60,unique=True)
    
    def __unicode__(self):
        return u"%s" % self.dimp
        
    class Meta:
        ordering = ['id']
        verbose_name = u'Δίμηνο'
        verbose_name_plural = u'Δίμηνα'    

class Trimino(models.Model):
    trimp = models.CharField(verbose_name=u'Τρίμηνο',help_text=u'Τρίμηνο',max_length=60,unique=True)
    perapo= models.CharField(verbose_name=u'Περίοδος Από',help_text=u'Κωδικός περιόδου',max_length=2,unique=True)
    pereos= models.CharField(verbose_name=u'Περίοδος Έως',help_text=u'Κωδικός περιόδου',max_length=2,unique=True)
    
    def __unicode__(self):
        return u"%s" % self.trimp
        
    class Meta:
        ordering = ['id']
        verbose_name = u'Τρίμηνο'
        verbose_name_plural = u'Τρίμηνα'
        
class Apdp(models.Model):
    trimp = models.CharField(verbose_name=u'Περίοδος ΑΠΔ',help_text=u'Περίοδος ΑΠΔ',max_length=60,unique=True)
    perapo= models.CharField(verbose_name=u'Περίοδος Από',help_text=u'Κωδικός περιόδου',max_length=2,unique=True)
    pereos= models.CharField(verbose_name=u'Περίοδος Έως',help_text=u'Κωδικός περιόδου',max_length=2,unique=True)
    
    def __unicode__(self):
        return u"%s" % self.trimp
        
    class Meta:
        ordering = ['id']
        verbose_name = u'Περίοδος ΑΠΔ'
        verbose_name_plural = u'Περίοδοι ΑΠΔ'  
                  
class Period(models.Model):
    period  = models.CharField(verbose_name=u'Περίοδος',help_text=u'Κωδικός περιόδου',max_length=2,unique=True)
    periodp = models.CharField(verbose_name=u'Περιγραφή',help_text=u'Περιγραφή περιόδου',max_length=20,unique=True)
    dimino  = models.ForeignKey(Dimino,verbose_name=u'Δίμηνο')
    trimino = models.ForeignKey(Trimino,verbose_name=u'Τρίμηνο')
    
    def __unicode__(self):
        return u"%s , %s " % (self.period, self.periodp)
        
    class Meta:
        ordering = ['period']
        verbose_name = u'Περίοδος'
        verbose_name_plural = u'Περίοδοι'

                        
class Eid(models.Model):
    eidp = models.CharField(verbose_name=u'Ειδικότητα',help_text=u'Περιγραφή ειδικότητας',max_length=60,unique=True)
    keid = models.CharField(verbose_name=u'Κωδικός ΙΚΑ',help_text=u'Κωδικός ΙΚΑ ειδικότητας',max_length=60,unique=True)
    
    def __unicode__(self):
        return u"%s" % self.eidp
        
    class Meta:
        ordering = ['eidp']
        verbose_name = u'Ειδικότητα'
        verbose_name_plural = u'Ειδικότητες'
        
class Sex(models.Model):
    sexp = models.CharField(verbose_name=u'Φύλο',max_length=10,unique=True)

    def __unicode__(self):
        return u"%s" % self.sexp
        
    class Meta:
        ordering = ['sexp']
        verbose_name = u'Φύλο'
        verbose_name_plural = u'Φύλα'
            
class Fpr(models.Model): #Φυσικό πρόσωπο
    epon = models.CharField(verbose_name=u'Επώνυμο',help_text=u'Επώνυμο',max_length=20)
    onom = models.CharField(verbose_name=u'Όνομα',help_text=u'Όνομα',max_length=20)
    patr = models.CharField(verbose_name=u'Πατρώνυμο',help_text=u'Όνομα πατέρα',max_length=20)
    mitr = models.CharField(verbose_name=u'Μητρώνυμο',help_text=u'Όνομα μητέρας',max_length=20)
    sex  = models.ForeignKey(Sex,verbose_name=u'Φύλο')
    igen = models.DateField(verbose_name=u'Ημνία γέννησης',help_text=u'Ημερομηνία γέννησης')
    afm  = models.CharField(verbose_name=u'ΑΦΜ',help_text=u'Αριθμός φορολογικού μητρώου',max_length=9)
    amka = models.CharField(verbose_name=u'ΑΜΚΑ',help_text=u'Αριθμός μητρώου κοινωνικής ασφάλισης',max_length=11)
    aika = models.CharField(verbose_name=u'ΑμΙΚΑ',help_text=u'Αριθμός μητρώου ΙΚΑ',max_length=7,blank=True)
    pol = models.CharField(verbose_name=u'Πόλη',help_text=u'Διεύθυνση Πόλη',max_length=30)
    odo = models.CharField(verbose_name=u'Οδός',help_text=u'Διεύθυνση Οδός',max_length=30)
    num = models.CharField(verbose_name=u'Αριθμός',help_text=u'Διεύθυνση Αριθμός',max_length=5)
    tk  = models.CharField(verbose_name=u'ΤΚ',help_text=u'Ταχυδρομικός κωδικός',max_length=5)
    doy = models.CharField(verbose_name=u'ΔΟΥ',help_text=u'Δημόσια Οικονομική Εφορία',max_length=50,blank=True)
    tno = models.CharField(verbose_name=u'Αρ.Ταυτότητας',help_text=u'Αρ.Ταυτότητας',max_length=10,blank=True)
    ano = models.CharField(verbose_name=u'Αρ.Άδειας Αλλοδαπού',help_text=u'Αρ.Άδειας Αλλοδαπού',max_length=15,blank=True)
        
    def getAge(self):
        import datetime
        return int(((datetime.date.today() - self.igen).days/ 365.25))
    
    def __unicode__(self):
        return u"%s %s" % (self.epon,self.onom)
        
    class Meta:
        ordering = ['epon','onom','patr']
        verbose_name = u'Εργαζόμενος βασικά στοιχεία'
        verbose_name_plural = u'Εργαζόμενοι βασικά στοιχεία' 
        unique_together = ('epon','onom','patr','mitr')
           
class Fprd(models.Model): #Μεταβαλλόμενα δεδομένα φυσικού προσώπου
    fpr  = models.ForeignKey(Fpr,verbose_name=u'Φυσικό πρόσωπο',help_text=u'Φυσικό πρόσωπο')
    dat  = models.DateField(verbose_name=u'Ημνία ισχύος',help_text=u'Ημερομηνία ισχύος')
    mars_choices = (('0','Άγαμος'),('1','Έγγαμος'),('2','Χήρος'))
    mars = models.CharField(verbose_name=u'Οικογ.Κατ',help_text=u'Οικογενειακή κατάσταση',max_length=1,choices=mars_choices)
    pedi = models.IntegerField(verbose_name=u'Παιδιά',help_text=u'Αριθμός παιδιών',default=0)
    
    def __unicode__(self):
        return u"%s %s %s %s" % (self.fpr,self.dat,self.mars,self.pedi)
        
    class Meta:
        ordering = ['fpr','dat','mars']
        verbose_name = u'Εργαζόμενος συμπληρωματικά στοιχεία'
        verbose_name_plural = u'Εργαζόμενοι συμπληρωματικά στοιχεία'
        unique_together = ('fpr','dat') 

class Aptyp(models.Model): #Τύπος αποδοχών (Μισθός, ημερομίσθιο, ωρομίσθιο)
    aptypp = models.CharField(verbose_name=u'Τύπος αποδοχών',help_text=u'Περιγραφή τύπου αποδοχών',max_length=20,unique=True)
     
    def __unicode__(self):
        return u"%s" % self.aptypp
        
    class Meta:
        ordering = ['aptypp']
        verbose_name = u'Τύπος αποδοχών'
        verbose_name_plural = u'Τύποι αποδοχών'

class SymTyp(models.Model): #Τύπος Σύμβασης εργασίας
    symtyp = models.CharField(verbose_name=u'Τύπος Σύμβασης',help_text=u'Τύπος σύμβασης εργασίας',max_length=20,unique=True)
    olerg  = models.BooleanField(verbose_name=u'Όλες εργάσιμες',help_text=u'Όλες οι μέρες εργάσιμες',default=False)
    
    def olesErgasimes(self):
        if self.olerg:
            return u'Όλες εργάσιμες'
        else:
            return u'Δεν είναι όλες εργάσιμες'
        
    def __unicode__(self):
        return u"%s" % (self.symtyp)
        
    class Meta:
        ordering = ['symtyp']
        verbose_name = u'Τύπος Σύμβασης'
        verbose_name_plural = u'Τύποι Σύμβασης'
            
class Orar(models.Model): # Πρόγραμμα εργασίας ,Μέρες και Ωράριο 
    orar = models.CharField(verbose_name=u'Ωράριο εργασίας',help_text=u'Τύπος σύμβασης εργασίας',max_length=100,unique=True) 
    mbdo = models.DecimalField(verbose_name=u'Μέρ.εργ./Βδομ.',help_text=u'Ημέρες εργασίας / Βδομάδα',max_digits=2, decimal_places=0,default=5)
    obdo = models.DecimalField(verbose_name=u'Ώρ.εργ./Βδομ.',help_text=u'Ώρες εργασίας / Βδομάδα',max_digits=2, decimal_places=0,default=40)
    
    def __unicode__(self):
        return u"%s" % self.orar
        
    class Meta:
        ordering = ['orar']
        verbose_name = u'Πρόγραμμα εργασίας'
        verbose_name_plural = u'Προγράμματα εργασίας'
                           
class Pro(models.Model): #Πρόσληψη εργαζομένου
    prod = models.DateField(verbose_name=u'Ημνία πρόσληψης',help_text=u'Ημερομηνία πρόσληψης')
    fpr  = models.ForeignKey(Fpr,verbose_name=u'Φυσικό πρόσωπο',help_text=u'Φυσικό πρόσωπο')
    coy  = models.ForeignKey(Coy,verbose_name=u'Υποκατάστημα',help_text=u'Υποκατάστημα που ανήκει')
    eid  = models.ForeignKey(Eid,verbose_name=u'Ειδικότητα',help_text=u'Ειδικότητα εργασίας')
    proy = models.IntegerField(verbose_name=u'Προυπηρεσία',help_text=u'Προυπηρεσία (Έτη)',default=0)
    aptyp= models.ForeignKey(Aptyp,verbose_name=u'Τύπος αποδοχών',help_text=u'Περιγραφή τύπου αποδοχών')
    apod = models.DecimalField(verbose_name=u'Αποδοχές',help_text=u'Μισθός,ημερομίσθιο ή ωρομίσθιο',max_digits=7, decimal_places=2,default=0)
    
    def getKPK(self):
        import osyk
        #print '111'
        sa = osyk.kpk_find(osyk.kadeidkpk_find(self.coy.kad,self.eid.kad),'201210')
        return sa[0]
    
    def getOromisthio(self):
        if self.aptyp.id == 1:
            return (self.apod / 25) * 6 /40
        elif self.aptyp.id == 2:
            return self.apod * 6 / 40
        elif self.aptyp.id == 3:
            return self.apod
        
    def getImeromisthio(self):
        if self.aptyp.id == 1:
            return self.apod / 25
        elif self.aptyp.id == 2:
            return self.apod
        elif self.aptyp.id == 3:
            return self.apod * 40 / 6
                
    def __unicode__(self):
        return u"%s %s %s" % (self.prod,self.fpr,self.eid)
        
    class Meta:
        ordering = ['prod','id','fpr','eid']
        verbose_name = u'Εργαζόμενος πρόσληψη'
        verbose_name_plural = u'Εργαζόμενοι προσλήψεις'
        unique_together = ('prod','fpr')
           
class Symb(models.Model): #Σύμβαση εργασίας
    symd   = models.DateField(verbose_name=u'Ημνία Σύμβασης',help_text=u'Ημερομηνία κατάρτισης σύμβασης εργασίας')
    pro    = models.ForeignKey(Pro,verbose_name=u'Εργαζόμενος',help_text=u'Εργαζόμενος') 
    xrisi  = models.ForeignKey(Xrisi,verbose_name=u'Χρήση',help_text=u'Χρήση')
    period = models.ForeignKey(Period,verbose_name=u'Περίοδος',help_text=u'Περίοδος')
    symtyp = models.ForeignKey(SymTyp,verbose_name=u'Τύπος σύμβασης',help_text=u'Τύπος σύμβασης εργασίας',default=2) 
    orar   = models.ForeignKey(Orar,verbose_name=u'Πρόγραμμα εργασίας',help_text=u'Πρόγραμμα και ημέρες εργασίας')
    dial = models.CharField(verbose_name=u'Ωρες διαλλείματος',help_text=u'Ωρες διαλλείματος-Διακοπής',max_length=20)
    
    def __unicode__(self):
        return u"%s %s %s %s" % (self.symd,self.pro,self.symtyp,self.orar)
        
    class Meta:
        ordering = ['symd','pro','xrisi','period']
        verbose_name = u'Εργαζόμενος πρόσληψη Σύμβαση Εργασίας'
        verbose_name_plural = u'Εργαζόμενοι προσλήψεις Συμβάσεις Εργασίας'
        unique_together = ('pro','xrisi','period')      
    
class ProMis(models.Model): #Αλλαγές μισθού
    pro    = models.ForeignKey(Pro,verbose_name=u'Εργαζόμενος',help_text=u'Εργαζόμενος') 
    xrisi  = models.ForeignKey(Xrisi,verbose_name=u'Χρήση',help_text=u'Χρήση')
    period = models.ForeignKey(Period,verbose_name=u'Περίοδος',help_text=u'Περίοδος')
    poso   = models.DecimalField(verbose_name=u'Τιμή',max_digits=12, decimal_places=2,default=0)  
    
    def __unicode__(self):
        return u"%s %s %s %s" % (self.pro,self.xrisi,self.period,self.poso)
        
    class Meta:
        ordering = ['pro','xrisi','period','poso']
        verbose_name = u'Αποδοχές εργαζομένου'
        verbose_name_plural = u'Αποδοχές εργαζομένων'
        unique_together = ('pro','xrisi','period') 
        
class ApoTyp(models.Model): # Τύπος αποχώρησης
    apotypp = models.CharField(verbose_name=u'Τύπος', help_text=u'Τύπος αποχώρησης', max_length=30, unique=True)
    
    def __unicode__(self):        
        return u"%s" % (self.apotypp)    
    class Meta:
        ordering = ['apotypp',]
        verbose_name = u'Τύπος αποχώρησης'
        verbose_name_plural = u'Τύποι αποχώρησης εργαζομένων'
            
class Apo(models.Model): #Αποχώρηση / Απόλυση εργαζομένου
    apod = models.DateField(verbose_name=u'Ημνία',help_text=u'Ημερομηνία αποχώρησης')
    pro  = models.OneToOneField(Pro,verbose_name=u'Πρόσληψη',help_text=u'Πρόσληψη')
    apot_choices = (('0',u'Απόλυση'),('1',u'Οικιοθελής αποχώρηση'))
    apot = models.CharField(verbose_name=u'Τύπος',help_text=u'Τύπος αποχώρησης',max_length=1,choices=apot_choices)
    
    def apotp(self):
        for el in self.apot_choices:
            if self.apot == el[0]:
                return el[1]
                break
            else:
                return ''
            
    def __unicode__(self):        
        return u"%s %s %s" % (self.apod,self.pro,self.apotp())
        
    class Meta:
        ordering = ['apod','pro','apot']
        verbose_name = u'Αποχώρηση εργαζομένου'
        verbose_name_plural = u'Εργαζόμενοι αποχωρήσεις'
        
class Mxr(models.Model): # Μονάδες χρόνου
    mxrp  =  models.CharField(verbose_name=u'Μονάδα χρόνου',help_text=u'Μονάδα χρόνου',max_length=20,unique=True)
    
    def __unicode__(self):    
        return u"%s" % self.mxrp
        
    class Meta:
        ordering = ['mxrp']
        verbose_name = u'Μονάδα χρόνου'
        verbose_name_plural = u'Μονάδες χρόνου'
        
class Ptyp(models.Model):
    ptypp  = models.CharField(verbose_name=u'Τύπος',help_text=u'Τύπος Παρουσίας',max_length=20,unique=True)
    mxr    = models.ForeignKey(Mxr,verbose_name=u'Μονάδα Χρόνου',help_text=u'Μονάδα χρόνου')
    def __unicode__(self):    
        return u"%s(%s)" % (self.ptypp,self.mxr)
        
    class Meta:
        ordering = ['ptypp']
        verbose_name = u'Τύπος παρουσίας'
        verbose_name_plural = u'Τύποι παρουσίας'
        
class Par(models.Model):
    xrisi  = models.ForeignKey(Xrisi,verbose_name=u'Χρήση',help_text=u'Χρήση')
    period = models.ForeignKey(Period,verbose_name=u'Περίοδος',help_text=u'Περίοδος')
    #pro    = models.ForeignKey(Pro,verbose_name=u'Εργαζόμενος',help_text=u'Εργαζόμενος')
    #ptyp   = models.ForeignKey(Ptyp,verbose_name=u'Τύπος',help_text=u'Τύπος παρουσίας')
    #pos    = models.DecimalField(verbose_name=u'Ποσότητα',max_digits=5, decimal_places=1,default=0)
    
    def getKPK(self):
        import osyk
        #print 'GetKPK'
        sa = osyk.kpk_find(osyk.kadeidkpk_find(self.pro.coy.kad,self.pro.eid.kad),self.xrisi.xrisi + self.period.period)
        print sa
        return sa[0]
        
    def apod(self):   
        if self.ptyp.id == 1:
            #print 'apod'
            return self.pro.apod * self.pos
        else:
            return 0
        
    def ikaenos(self):
        return d(d(self.getKPK()[2]) * d(self.apod()) / d(100))
    
    def ika(self):
        return float(self.getKPK()[4]) * float(self.apod()) / 100 
       
    def __unicode__(self):    
        return u"%s %s" % (self.xrisi,self.period)
        
    class Meta:
        ordering = ['xrisi','period']
        verbose_name = u'Παρουσία'
        verbose_name_plural = u'Παρουσίες'
        unique_together = ('xrisi','period')      

class Pard(models.Model):
    par    = models.ForeignKey(Par,verbose_name=u'Περίοδος Παρουσίας',help_text=u'Χρήση και μήνας παρουσίας')
    pro    = models.ForeignKey(Pro,verbose_name=u'Εργαζόμενος',help_text=u'Εργαζόμενος')
    ptyp   = models.ForeignKey(Ptyp,verbose_name=u'Τύπος',help_text=u'Τύπος παρουσίας')
    pos    = models.DecimalField(verbose_name=u'Ποσότητα',max_digits=5, decimal_places=1,default=0) 
        
    def __unicode__(self):    
        return u"%s %s %s %s %s" % (self.par,self.pro,self.ptyp,self.pos)
    
    class Meta:
        ordering = ['par','pro','ptyp']
        verbose_name = u'Παρουσία αναλυτικά'
        verbose_name_plural = u'Παρουσίες αναλυτικά'
        unique_together = ('par','pro','ptyp') 
                                      
class Parf(models.Model):
    xrisi  = models.ForeignKey(Xrisi,verbose_name=u'Χρήση',help_text=u'Χρήση')
    period = models.ForeignKey(Period,verbose_name=u'Περίοδος',help_text=u'Περίοδος')
    pro    = models.ForeignKey(Pro,verbose_name=u'Εργαζόμενος',help_text=u'Εργαζόμενος')
    kerg   = models.DecimalField(verbose_name=u'Κανονικές εργάσιμες',max_digits=5, decimal_places=1,default=0)
    kad    = models.DecimalField(verbose_name=u'Σε κανονική άδεια',max_digits=5, decimal_places=1,default=0)
    asl3   = models.DecimalField(verbose_name=u'Ασθένεια έως 3 ημέρες',max_digits=5, decimal_places=1,default=0)
    asm3   = models.DecimalField(verbose_name=u'Ασθένεια πάνω από 3 ημέρες',max_digits=5, decimal_places=1,default=0)
    
    def getKPK(self):
        import osyk
        #print 'GetKPK'
        sa = osyk.kpk_find(osyk.kadeidkpk_find(self.pro.coy.kad,self.pro.eid.kad),self.xrisi.xrisi + self.period.period)
        return sa[0]
    
    def calc(self):
        ika = self.getKPK()
        a = {}
        #Υπολογισμός τακτικών αποδοχών 01
        a['mis']     = d(self.pro.apod) * d(self.kerg + self.kad)
        a['ikaenos'] = d(a['mis'] * d(ika[2]) / d(100))
        a['ika']     = d(d(a['mis']) * d(ika[4]) / d(100))
        a['ikaetis'] = a['ika'] - a['ikaenos']
        a['foros']   = 0  
        a['eea']     = 0
        a['tkenos']  = a['ikaenos'] + a['foros'] + a['eea']
        a['plir']    = a['mis'] - a['tkenos']
        return a
    
    def __unicode__(self):    
        return u"%s %s %s %s" % (self.xrisi,self.period,self.pro,self.kerg)
        
    class Meta:
        ordering = ['xrisi','period','pro']
        verbose_name = u'Παρουσία F'
        verbose_name_plural = u'Παρουσίες F'
        unique_together = ('xrisi','period','pro')             
class Mist(models.Model):
    mistp  =  models.CharField(verbose_name=u'Τύπος μισθοδοσίας',help_text=u'Κανονική, συμπληρωματική,Δ.Πάσχα,Δ.Χριστ.,Επ.αδείας',max_length=20,unique=True)
    
    def __unicode__(self):    
        return u"%s.%s" % (self.id,self.mistp)
        
    class Meta:
        ordering = ['id','mistp']
        verbose_name = u'Τύπος μισθοδοσίας'
        verbose_name_plural = u'Τύποι μισθοδοσίας'
                   
class Mis(models.Model):
    xrisi   = models.ForeignKey(Xrisi,verbose_name=u'Χρήση',help_text=u'Χρήση')
    period = models.ForeignKey(Period,verbose_name=u'Περίοδος Μισθοδοσίας',help_text=u'Περίοδος')
    mist    = models.ForeignKey(Mist,verbose_name=u'Τύπος',help_text=u'Τύπος μισθοδοσίας')
    imnia   = models.DateField(verbose_name=u'Ημνία',help_text=u'Ημερομηνία έκδοσης μισθοδοσίας')
    
    def __unicode__(self):
        return u"%s %s %s %s" % (self.xrisi,self.period,self.mist,self.imnia)
        
    class Meta:
        ordering = ['xrisi','period','mist','imnia']
        verbose_name = u'Μισθοδοσία'
        verbose_name_plural = u'Μισθοδοσίες'
        unique_together = ('xrisi','period','mist')
        
class Mtyp(models.Model):
    mtypp  =  models.CharField(verbose_name=u'Τύπος',help_text=u'Τύπος Μισθολογικού δεδομένου',max_length=20,unique=True)
    
    def __unicode__(self):    
        return u"%s" % self.mtypp
        
    class Meta:
        ordering = ['id','mtypp']
        verbose_name = u'Τύπος μισθολογικού δεδομένου'
        verbose_name_plural = u'Τύποι μισθολογικών δεδομένων' 
              
class Misd(models.Model):
    mis  = models.ForeignKey(Mis,verbose_name=u'Μισθοδοσία',help_text=u'Μισθοδοσία')
    pro  = models.ForeignKey(Pro,verbose_name=u'Εργαζόμενος',help_text=u'Εργαζόμενος')
    mtyp = models.ForeignKey(Mtyp,verbose_name=u'Τύπος',help_text=u'Τύπος')
    val  = models.DecimalField(verbose_name=u'Τιμή',max_digits=12, decimal_places=2,default=0)
    
    def __unicode__(self):    
        return u"%s %s %s %s" % (self.mis,self.pro,self.mtyp,self.val)
        
    class Meta:
        ordering = ['mis','pro','mtyp']
        verbose_name = u'Λεπτομέρεια μισθοδοσίας'
        verbose_name_plural = u'Λεπτομέρειες μισθοδοσίας'
        unique_together = ('mis','pro','mtyp')
           