# -*- coding: utf-8 -*-

from fld_button_text import Button_text
from fld_checkbox import CheckBox
from fld_date import Date
from fld_date_or_empty import Date_or_empty
from fld_integer import Integer
from fld_numeric import Numeric
from fld_text import Text
from fld_textline import TextLine
from fld_textline import TextLineMasked
from fld_weekdays import Weekdays

CTYPES = {'texb': Button_text,
          'chck': CheckBox,
          'date': Date,
          'datee': Date_or_empty,
          'int': Integer,
          'num': Numeric,
          'txt': Text,
          'txtl': TextLine,
          'txtlm': TextLineMasked,
          'wdays': Weekdays}


def makefld(typ, name, parent):
    '''
    Factory for fld classes.
    '''
    if name[-3:] == '_id':
        return Button_text(None, name, parent)
    if typ == 'num':
        return Numeric({'val': ''}, parent)
    elif typ == 'txtlinem':
        return TextLineMasked({'val': ''}, parent)
    elif typ == 'txt':
        return Text({'val': ''}, parent)
    elif typ == 'date':
        return Date({'val': ''}, parent)
    else:
        return TextLine({'val': ''}, parent)
