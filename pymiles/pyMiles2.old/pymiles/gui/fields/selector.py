# -*- coding: utf-8 -*-

from checkbox import Checkbox
from date import Date
from date_or_empty import Date_or_empty
from integer import Integer
from integer_spin import Integer_spin
from numeric import Numeric
from numeric_spin import Numeric_spin
from text import Text
from text_button import Text_button
from text_combo import Combo
from textline import Text_line
from textline_numbers_only import Textline_numbers_only
from weekdays import Weekdays
from yesno_combo import Yes_no_combo


def qtfield(typ, parent, name):
    '''
    Factory for fld classes.
    '''
    typo = typ.upper()
    if typo == 'BOOLEAN':
        return Checkbox(parent)
    elif typo == 'DATE':
        return Date(parent)
    elif typo == 'DATEN':
        return Date_or_empty(parent)
    elif typo == 'INTEGER':
        return Integer(parent)
    elif typo == 'INTEGERS':
        return Integer_spin(parent)
    elif typo == 'NUMERIC':
        return Numeric(parent)
    elif typo == 'NUMERICS':
        return Numeric_spin(parent)
    elif typo == 'TEXT':
        return Text(parent)
    elif typo == 'IDBUTTON':
        assert(name.endswith('_id'))
        return Text_button(parent, name)
    elif typo == 'IDCOMBO':
        assert(name.endswith('_id'))
        return Combo(parent, name)
    elif typo == 'VARCHAR':
        return Text_line(parent)
    elif typo == 'VARCHARN':
        return Textline_numbers_only(parent)
    elif typo == 'WEEKDAYS':
        return Weekdays(parent)
    elif typo == 'YESNO':
        return Yes_no_combo(parent)
    else:
        return Text_line(parent)
