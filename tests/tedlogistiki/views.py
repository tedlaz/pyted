# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
#from ted.tedFunctions import dec
from tedlogistiki.logistiki.models import Lmo, Tran, Tran_d
import datetime
import locale
def lf(num):
    return locale.format("%.2f", num, 1)
def hello(request,onom):
    onoma = onom
    ora = datetime.datetime.now()
    return render_to_response('current_datetime.html', locals())
    
def lmo_list(request):
    lmoi = Lmo.objects.order_by('code')
    return render_to_response('lmo_list.html',locals())
class elem():
    def __init__(self,imnia,per,xr,pi,ytd,id):
        self.imnia = imnia
        self.per = per
        self.xr = xr
        self.pi = pi
        self.ytd = ytd
        self.id = id
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
                    select imnia, per, xr, pi, logistiki_tran.id
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
        a = elem(gr[0],gr[1],lf(gr[2]),lf(gr[3]), lf(ytd),gr[4])
        grammes.append(a)
    return render_to_response('lmo_det.html',locals())
class tr_det():
    def __init__(self,lmos,per2,xr,pi):
        self.lmos = lmos
        self.per2  = per2
        self.xr   = locale.format("%.2f",xr,1)
        self.pi   = locale.format("%.2f",pi,1)
def arthro(request,no,tr):
    head = Tran.objects.filter(id=tr)
    det = Tran_d.objects.filter(tran=tr)
    total_xr = total_pi = 0
    lin =[]
    for el in det:
        lin.append(tr_det(el.lmos,el.per2,el.xr,el.pi))
        total_xr += el.xr
        total_pi += el.pi
    total_xr = lf(total_xr)
    total_pi = lf(total_pi)
    imnia, per, par = head[0].imnia, head[0].per, head[0].par
    return render_to_response('arthro.html',locals())