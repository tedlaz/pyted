# -*- coding: utf-8 -*-
'''
Created on May 4, 2015

@author: tedlaz
'''
from fld_button_text import ButtonText
from fld_button_text2 import ButtonText2
from fld_checkbox import CheckBox
from fld_date import Date
from fld_date_or_empty import DateOrEmpty
from fld_integer import Integer
from fld_numeric import Numeric
from fld_text import Text
from fld_textline import TextLine
from fld_textline import TextLineMasked
from fld_weekdays import WeekDays

CTYPES = {'ButtonText': ButtonText,
          'ButtonText2': ButtonText2,
          'CheckBox': CheckBox,
          'Date': Date,
          'DateOrEmpty': DateOrEmpty,
          'Integer': Integer,
          'Numeric': Numeric,
          'Text': Text,
          'TextLine': TextLine,
          'TextLineMasked': TextLineMasked,
          'WeekDays': WeekDays}
