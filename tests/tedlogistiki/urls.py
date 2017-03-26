# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from tedlogistiki import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
#edo kodikas gia Databrowse
from django.contrib import databrowse
from tedlogistiki.logistiki.models import Lmo
databrowse.site.register(Lmo)

urlpatterns = patterns('',
    # Example:
    #(r'^$',views.lmo_list),
    #('/(\d{1,2})/$',views.lmo_det),
    (r'^hello/(\d+)/$',views.hello),
    (r'^lmoi/$',views.lmo_list),
    (r'^lmoi/(\d+)/$',views.lmo_det),
    (r'^lmoi/(\d+)/(\d+)/$',views.arthro),
    # (r'^ted/', include('ted.foo.urls')),
    (r'^db/(.*)',databrowse.site.root),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
