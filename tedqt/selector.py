# -*- coding: utf-8 -*-

from tedqt.w_checkbox import Checkbox
from tedqt.w_date import Date
from tedqt.w_date_or_empty import Date_or_empty
from tedqt.w_integer import Integer
from tedqt.w_integer_spin import Integer_spin
from tedqt.w_numeric import Numeric
from tedqt.w_numeric_spin import Numeric_spin
from tedqt.w_text import Text
from tedqt.w_text_button import Text_button
from tedqt.w_text_combo import Combo
from tedqt.w_textline import Text_line
from tedqt.w_textline_numbers_only import Textline_numbers_only
from tedqt.w_weekdays import Weekdays
from tedqt.w_yesno_combo import Yes_no_combo


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
