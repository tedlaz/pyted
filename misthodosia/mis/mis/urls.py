# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'm12.views.main_form'),
    url(r'^searchf/$', 'm12.views.search_form'),
    url(r'^search/$', 'm12.views.search'),
    url(r'^erg/$', 'm12.views.spro'),
    url(r'^paroysies/(\d{4})/(\d{2})/$', 'm12.views.paroysies'),
    url(r'^pdf/$', 'm12.views.some_view'),
    # url(r'^mis/', include('mis.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
)
