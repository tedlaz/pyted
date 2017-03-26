# -*- coding: utf-8 -*-
from django.contrib import admin

import m12.models as m12models


class MisAdmin(admin.ModelAdmin):
    #list_display = ('xrisi','period','mist','imnia')
    list_filter = ['xrisi','period','mist']


class ParAdmin(admin.ModelAdmin):
    list_display = ['xrisi','period','pro','ptyp','pos']
        
class MisdAdmin(admin.ModelAdmin):
    list_display = ('mis','pro')
    list_filter = ['mis','pro']
    
class ProAdmin(admin.ModelAdmin):
    list_display =['prod','fpr','coy','eid','apod']
    date_hierarchy = 'prod'
    
admin.site.register(m12models.Co)   
admin.site.register(m12models.Coy)   
admin.site.register(m12models.Xrisi)
admin.site.register(m12models.Apo)
admin.site.register(m12models.Eid)
admin.site.register(m12models.Fpr)
admin.site.register(m12models.Fprd)
admin.site.register(m12models.Pro,ProAdmin)
admin.site.register(m12models.SymTyp)
admin.site.register(m12models.Orar)
admin.site.register(m12models.Symb)
admin.site.register(m12models.ProMis)
admin.site.register(m12models.Par)#,ParAdmin)
admin.site.register(m12models.Parf)
admin.site.register(m12models.Period)
admin.site.register(m12models.Mxr)
admin.site.register(m12models.Ptyp)
admin.site.register(m12models.Mis,MisAdmin)
admin.site.register(m12models.Mist)
admin.site.register(m12models.Misd,MisdAdmin)
admin.site.register(m12models.Mtyp)