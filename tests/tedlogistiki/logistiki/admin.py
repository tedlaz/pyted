# -*- coding: utf-8 -*-
from tedlogistiki.logistiki.models import *
from django.contrib import admin

class Tran_dInLine(admin.TabularInline):
    model = Tran_d
    extra = 4

class TranAdmin(admin.ModelAdmin):
    list_display = ('id','imnia','per')
    #list_per_page = 5000
    date_hierarchy = 'imnia'
    inlines = [Tran_dInLine]

class LmoAdmin(admin.ModelAdmin):
    list_display = ('id','code','per','ypol')
    #inlines = [Tran_dInLine]

class TrandAdmin(admin.ModelAdmin):
    list_display = ('id','tran','lmos','xr','pi')
    #list_per_page = 5000
    list_filter  = ('lmos',)

admin.site.register(Tran,TranAdmin)
admin.site.register(Tran_d,TrandAdmin)
admin.site.register(Lmo,LmoAdmin)

