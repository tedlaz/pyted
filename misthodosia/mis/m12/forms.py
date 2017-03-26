# -*- coding: utf-8 -*-

from django import forms

class TstForm(forms.Form):
    sub    = forms.CharField()
    email  = forms.EmailField(required=False)