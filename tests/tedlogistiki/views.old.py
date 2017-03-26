# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
#from ted.tedFunctions import dec
from ted.logistiki.models import Lmo
import datetime
import locale

def hello(request,onom):
    onoma = onom
    ora = datetime.datetime.now()
    return render_to_response('current_datetime.html', locals())
    
def lmo_list(request):
    lmoi = Lmo.objects.order_by('code')
    return render_to_response('lmo_list.html',locals())
class elem():
    def __init__(self,imnia,per,xr,pi,ytd):
        self.imnia = imnia
        self.per = per
        self.xr = xr
        self.pi = pi
        self.ytd = ytd
class lmos():
    def __init__(self,code,per):
        self.code = code
        self.per = per
def lmo_det(request,lmo):
    from django.db import connection
    cursor = connection.cursor()
    c0 = connection.cursor()
    c0.execute("select code,per from logistiki_lmo where id = '%s'"% lmo)
    l = c0.fetchone()
    lm = lmos(l[0],l[1])
    cursor.execute('''
                    select imnia, per, xr, pi
                    from logistiki_tran
                    inner join logistiki_tran_d
                    on logistiki_tran.id = logistiki_tran_d.tran_id
                    where lmos_id ='%s'
                    order by imnia;'''%lmo)
    gram  = cursor.fetchall()
    grammes = []
    ytd = 0
    for gr in gram:
        ytd += gr[2]-gr[3]
        a = elem(gr[0],gr[1],locale.format("%.2f",gr[2],1),locale.format("%.2f",gr[3],1),locale.format("%.2f",ytd,1))
        grammes.append(a)
    return render_to_response('lmo_det.html',locals())