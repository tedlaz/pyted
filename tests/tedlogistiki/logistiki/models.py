# -*- coding: utf-8 -*-
from django.db import models
from tedlogistiki.tedFunctions import dec
# Create your models here.
import locale
locale.setlocale(locale.LC_ALL, '')
class Lmo(models.Model):
    code  = models.CharField(verbose_name=u'Κωδικός',help_text=u'Κωδικός λογαριασμού',max_length=15)
    per   = models.CharField(verbose_name=u'Περιγραφή',max_length=50)
    #txr , tpi = self.total_lmo()
    def total_lmo(self,cod):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('''
            select sum(xr), sum(pi)
            from logistiki_lmo
            inner join logistiki_tran_d on logistiki_lmo.id=logistiki_tran_d.lmos_id
            where code='%s'
            group by lmos_id;''' % cod)
        l  = cursor.fetchone()
        if l <> None:
            return l
        return 0,0
        
    def ypol(self):
        txr, tpi = self.total_lmo(self.code)
        ypol = dec(txr - tpi)
        return locale.format("%.2f",ypol,1)
    ypol.short_description = u'Υπόλοιπο'
    def __unicode__(self):
        return u"%s , %s " % (self.code, self.per)
        #return u"%s" % (self.code)
    class Meta:
        ordering = ['code']
        verbose_name = u'Λογαριασμό'
        verbose_name_plural = u'Λογαριασμοί'
class Tran(models.Model):
    imnia = models.DateField(verbose_name=u'Ημερομηνία')
    par   = models.CharField(verbose_name=u'Παραστατικό',max_length=20)
    per   = models.CharField(verbose_name=u'Περιγραφή',max_length=50)
    def __unicode__(self):
        return u"%s , %s, %s, %s" % (self.imnia,self.per,self.par,self.id)
        #return u"%s , %s" % (self.imnia,self.id)
    class Meta:
        ordering = ['-imnia']
        verbose_name = u'Άρθρο'
        verbose_name_plural = u'Άρθρα'
class Tran_d(models.Model):
    tran = models.ForeignKey(Tran,verbose_name=u'Άρθρο')
    lmos = models.ForeignKey(Lmo,verbose_name=u'Λογαριασμός')
    per2 = models.CharField(verbose_name=u'Περ.2',max_length=50)
    xr   = models.DecimalField(verbose_name=u'Χρέωση',max_digits=19, decimal_places=2,default=0)
    pi   = models.DecimalField(verbose_name=u'Πίστωση',max_digits=19, decimal_places=2,default=0)
    def __unicode__(self):
        return u"%s, %s, %s, %s" % (self.tran,self.lmos,self.xr,self.pi)
    class Meta:
        verbose_name = u'Αναλυτική γραμμή'
        verbose_name_plural = u'Αναλυτικές γραμμές'