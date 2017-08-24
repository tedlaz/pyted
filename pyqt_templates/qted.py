import decimal
import datetime
import textwrap
import sqlite3
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg

GRLOCALE = Qc.QLocale(Qc.QLocale.Greek, Qc.QLocale.Greece)
MSG_RESET_DATE = u'right mouse click sets Date to empty string'
MIN_HEIGHT = 30
MAX_HEIGHT = 40
DATE_MAX_WIDTH = 120
SQLITE_DATE_FORMAT = 'yyyy-MM-dd'
GREEK_DATE_FORMAT = 'd/M/yyyy'
WEEKDAYS = ['Δε', 'Τρ', 'Τε', 'Πέ', 'Πα', 'Σά', 'Κυ']
MSG_SELECT_DAYS = 'Επιλέξτε τις Εργάσιμες ημέρες\nΜε δεξί κλικ μηδενίστε'
BLANK, GREEN = range(2)
lbl = {'id': 'αα', 'afm': 'ΑΦΜ', 'epon': 'Επώνυμο', 'addr': 'Διεύθυνση'}


def get_lbl(fld):
    '''Return label if exists for fld otherwise fld'''
    return lbl.get(fld, fld)


def grup(txtval):
    '''
    Trasforms a string to uppercase special for Greek comparison
    '''
    ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΐΊκλμνξοόΌπρσςτυύϋΰΎφχψωώΏ"
    ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΪΪΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΫΫΥΦΧΨΩΩΩ"
    ftxt = u''
    for letter in txtval:
        if letter in ar1:
            ftxt += ar2[ar1.index(letter)]
        else:
            ftxt += letter.upper()
    return ftxt


def isNum(val):  # is val number or not ?
    """Check if val is number or not
    :param val: value to check
    :return: Boolean
    """
    try:
        float(val)
    except ValueError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """
    Always returns a decimal number. If poso is not a number or None
    returns dec(0)

    :param poso: Mumber in any format (string, float, int, ...)
    :param decimals: Number of decimals (default 2)
    :return: A decimal number rounded to decimals parameter
    """
    if poso is None:
        poso = 0
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(poso)
    else:
        tmp = decimal.Decimal('0')
    # in case of tmp = -0.00 to remove negative sign
    if tmp == decimal.Decimal(0):
        tmp = decimal.Decimal(0)
    return tmp.quantize(PLACES)


def triades(txt, separator='.'):
    '''
    Help function to split digits to thousants ( 123456 becomes 123.456 )
    '''
    return separator.join(textwrap.wrap(txt[::-1], 3))[::-1]


def dec2gr(poso, decimals=2, zero_as_space=False):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    dposo = dec(poso, decimals)
    if dposo == dec(0):
        if zero_as_space:
            return ' '
    sdposo = str(dposo)
    meion = '-'
    separator = '.'
    decimal_ceparator = ','
    prosimo = ''
    if sdposo.startswith(meion):
        prosimo = meion
        sdposo = sdposo.replace(meion, '')
    if '.' in sdposo:
        sint, sdec = sdposo.split('.')
    else:
        sint = sdposo
        decimal_ceparator = ''
        sdec = ''
    return prosimo + triades(sint) + decimal_ceparator + sdec


def is_positive_integer(val):
    '''True if posotive integer False otherwise'''
    intv = 0
    try:
        intv = int(val)
    except ValueError:
        return False
    if intv <= 0:
        return False
    return True


def is_iso_date(strdate):
    """Check if strdate is isodate (yyyy-mm-dd)"""
    ldate = len(strdate)
    if ldate != 10:
        return False
    if strdate[4] != '-':
        return False
    if strdate[7] != '-':
        return False
    yyy, mmm, ddd = strdate.split('-')
    if not is_positive_integer(yyy):
        return False
    if not is_positive_integer(mmm):
        return False
    if not is_positive_integer(ddd):
        return False
    return True


def date2gr(date, removezero=False):
    '''
    :param date: iso date 'yyyy-mm-dd'
    :type date: iso_date
    :param removezero: Month, Day without trailing zeros (If True '2017-01-09'
     => '9/1/2017'. If False '2017-01-09' => '09/01/2017')
    :return: 'dd/mm/yyyy'

    Example::

        >>> import dategr
        >>> dategr.date2gr('2017-01-15)
        '15/01/2017'
        >>> dategr.dat2gr('2017-01-15, True)
        '15/1/2017'
    '''
    def remove_zero(stra):
        """Remove trailing zeros"""
        if len(stra) > 1 and stra[0] == '0':
            return stra[1:]
        else:
            return stra
    if not date:
        return ''
    year, month, day = date.split('-')
    if removezero:
        return '%s/%s/%s' % (remove_zero(day), remove_zero(month), year)
    else:
        return '%s/%s/%s' % (day, month, year)


# SQLITE FUNCTIONS
def fields_of(dbf, table_or_view, with_id=True):
    """A Tuple with table or view fields
    :param table_or_view: Table or View name
    :param with_id: If True includes field named id
    """
    sql = 'SELECT * FROM %s LIMIT 0' % table_or_view
    con = sqlite3.connect(dbf)
    cur = con.cursor()
    cur.execute(sql)
    if with_id:
        column_names = [t[0] for t in cur.description]
    else:
        column_names = [t[0] for t in cur.description if t[0] != 'id']
    cur.close()
    con.close()
    return tuple(column_names)


def select(dbf, sql, return_type=None):
    """select data records
    :param dbf: Database file path
    :param sql: SQL to run
    :param rtype: return type
    :return: list of tuples [(), (), ...]
    """
    if not sql[:6].upper() in ('SELECT', 'PRAGMA'):
        raise DbException('Wrong sql : %s' % sql)
    con = sqlite3.connect(dbf)
    cur = con.cursor()
    con.create_function("grup", 1, grup)
    try:
        cur.execute(sql)
    except sqlite3.OperationalError:
        return None
    column_names = tuple([t[0] for t in cur.description])
    rows = cur.fetchall()
    cur.close()
    con.close()
    rtypes = ('names-tuples', 'dicts')
    if return_type not in rtypes:
        return rows
    if return_type == 'names-tuples':
        return column_names, rows
    if return_type == 'dicts':
        diclist = []
        for row in rows:
            dic = {}
            for i, col in enumerate(row):
                dic[column_names[i]] = col
            diclist.append(dic)
        diclen = len(diclist)
        if diclen > 0:
            return diclist
        return [{}]


def select2(dbf, sql):
    """select data records
    :param dbf: Database file path
    :param sql: SQL to run
    """
    if not sql[:6].upper() in ('SELECT', 'PRAGMA'):
        return None
    con = sqlite3.connect(dbf)
    cur = con.cursor()
    cur.execute(sql)
    column_names = tuple([t[0] for t in cur.description])
    rows = cur.fetchall()
    cur.close()
    con.close()
    if not rows:
        return column_names, {}
    else:
        dic = {}
    for i, col in enumerate(rows[0]):
        if col:
            dic[column_names[i]] = '%s' % col
        else:
            dic[column_names[i]] = ''
    return column_names, dic


def find_by_id(dbf, vid, table, rtype):
    """Find a record by id
    """
    sql1 = "SELECT * FROM %s WHERE id='%s'" % (table, vid)
    return select(dbf, sql1, rtype)


def find(dbf, table_name, search_string, rtype='dicts'):
    """Find records with multiple search strings
    :param table_name: Table or View name
    :param search_string: A string with space separated search values
    :return: List of dicts
    """
    search_list = search_string.split()
    search_sql = []
    flds = fields_of(dbf, table_name, False)
    search_field = " || ' ' || ".join(flds)
    sql = "SELECT * FROM %s \n" % table_name
    where = ''
    for search_str in search_list:
        grup_str = grup(search_str)
        tstr = " grup(%s) LIKE '%%%s%%'\n" % (search_field, grup_str)
        search_sql.append(tstr)
        where = 'WHERE'
    # if not search_string sql is simple select
    final_sql = sql + where + ' AND '.join(search_sql)
    return select(dbf, final_sql, rtype)


def script(dbf, sql):
    '''sql   : A set of sql commands (create, insert or update)'''
    try:
        con = sqlite3.connect(dbf)
        cur = con.cursor()
        cur.executescript(sql)
        con.commit()
    except sqlite3.Error:
        con.rollback()
        cur.close()
        con.close()
        return False
    cur.close()
    con.close()
    return True


# My Qt Widgets
class TCheckbox(Qw.QCheckBox):
    """
    True or False field
    Gets / Sets two values : 0 for unchecked , 2 for checked
    """
    def __init__(self, val=False, parent=None):
        super().__init__(parent)
        self.set(val)
        self.setMinimumHeight(MIN_HEIGHT)

    def set(self, txtVal):
        if txtVal:
            self.setChecked(txtVal)
        else:
            self.setChecked(False)

    def get(self):
        return self.checkState() != 0


class TDate(Qw.QDateEdit):
    '''Date values for most cases'''
    def __init__(self, val=None, parent=None):
        super().__init__(parent)
        self.set(val)
        self.setCalendarPopup(True)
        self.setDisplayFormat(GREEK_DATE_FORMAT)
        # self.setMinimumHeight(par.MIN_HEIGHT)
        self.setMaximumWidth(DATE_MAX_WIDTH)
        # self.setMinimumWidth(par.DATE_MAX_WIDTH)
        self.setMaximumHeight(MAX_HEIGHT)
        self.setLocale(GRLOCALE)

    def set(self, iso_date):
        if iso_date:
            if len(iso_date) > 10:
                iso_date = iso_date[:10]
            yyy, mmm, ddd = iso_date.split('-')
            qdate = Qc.QDate()
            qdate.setDate(int(yyy), int(mmm), int(ddd))
            self.setDate(qdate)
        else:
            self.setDate(Qc.QDate.currentDate())

    def get(self):
        return '%s' % self.date().toString(SQLITE_DATE_FORMAT)


class TDateEmpty(Qw.QToolButton):
    '''Date or empty string values'''
    def __init__(self, val=None, parent=None):
        super().__init__(parent)
        self.setPopupMode(Qw.QToolButton.MenuButtonPopup)
        self.setMenu(Qw.QMenu(self))
        self.cal = Qw.QCalendarWidget()
        self.action = Qw.QWidgetAction(self)
        self.action.setDefaultWidget(self.cal)
        self.menu().addAction(self.action)
        self.cal.clicked.connect(self.menu_calendar)
        self.setSizePolicy(Qw.QSizePolicy.Expanding, Qw.QSizePolicy.Fixed)
        self.setToolTip(MSG_RESET_DATE)
        self.setMinimumHeight(MIN_HEIGHT)
        self.set(val)

    def mousePressEvent(self, event):
        if event.button() == Qc.Qt.RightButton:
            self.setText('')
            self.cal.setSelectedDate(Qc.QDate.currentDate())
        else:
            Qw.QToolButton.mousePressEvent(self, event)

    def menu_calendar(self):
        self.setText(self.cal.selectedDate().toString(GREEK_DATE_FORMAT))
        self.menu().hide()

    def set(self, iso_date):
        if not iso_date:
            return
        if len(iso_date) == 0:
            return
        yyy, mmm, ddd = iso_date.split('-')
        self.setText('%s/%s/%s' % (ddd, mmm, yyy))
        qdt = Qc.QDate()
        qdt.setDate(int(yyy), int(mmm), int(ddd))
        self.cal.setSelectedDate(qdt)

    def get(self):
        if len(self.text()) == 0:
            return ''
        ddd, mmm, yyy = self.text().split('/')
        qdt = Qc.QDate()
        qdt.setDate(int(yyy), int(mmm), int(ddd))
        return '%s' % qdt.toString(SQLITE_DATE_FORMAT)


class TIntegerSpin(Qw.QSpinBox):
    '''Integer values (eg 123)'''
    def __init__(self, val=0, parent=None):
        super().__init__(parent)
        self.set(val)
        self.setMinimum(0)
        self.setMaximum(999999999)
        self.setAlignment(Qc.Qt.AlignRight |
                          Qc.Qt.AlignTrailing |
                          Qc.Qt.AlignVCenter)
        self.setButtonSymbols(Qw.QAbstractSpinBox.NoButtons)

    def get(self):
        return self.value()

    def set(self, val):
        if val:
            self.setValue(int(val))
        else:
            self.setValue(0)


class TNumeric(Qw.QLineEdit):
    '''Text field with numeric chars only.'''
    def __init__(self, val='0', parent=None):
        super().__init__(parent)
        self.set(val)
        rval = Qc.QRegExp('(\d*)([1-9,])(\d*)')
        self.setValidator(Qg.QRegExpValidator(rval))
        self.setAlignment(Qc.Qt.AlignRight)

    def focusOutEvent(self, ev):
        self.set(self.get())
        Qw.QLineEdit.focusOutEvent(self, ev)

    def set(self, txt):
        if txt:
            self.setText(dec2gr(txt))
        else:
            self.setText(dec2gr(0))

    def get(self):
        greek_div = ','
        normal_div = '.'
        tmp = '%s' % self.text()
        tmp = tmp.replace(normal_div, '')
        tmp = tmp.replace(greek_div, normal_div)
        return dec(tmp.strip())


class TNumericSpin(Qw.QDoubleSpinBox):
    '''Numeric (decimal 2 ) values (eg 999,99)'''
    def __init__(self, val=0, parent=None):
        super().__init__(parent)

        self.set(val)

        self.setMinimum(-99999999999)
        self.setMaximum(99999999999)
        self.setAlignment(Qc.Qt.AlignRight |
                          Qc.Qt.AlignTrailing |
                          Qc.Qt.AlignVCenter)
        self.setButtonSymbols(Qw.QAbstractSpinBox.NoButtons)
        # self.setMinimumHeight(par.MIN_HEIGHT)
        self.setSingleStep(0)  # Για να μην αλλάζει η τιμή με τα βελάκια
        self.setGroupSeparatorShown(True)
        self.setLocale(GRLOCALE)

    def get(self):
        return dec(self.value())

    def set(self, val):
        if val:
            self.setValue(val)
        else:
            self.setValue(0)


class TText(Qw.QTextEdit):
    """Text field"""
    def __init__(self, val='', parent=None):
        super().__init__(parent)

        self.set(val)

    def set(self, txt):
        """:param txt: value to set"""
        if txt:
            ttxt = '%s' % txt
            self.setText(ttxt.strip())
        else:
            self.setText('')

    def get(self):
        """:return: Text value of control"""
        tmpval = '%s' % self.toPlainText().replace("'", "''")
        return tmpval.strip()


class TTextLine(Qw.QLineEdit):
    """Text Line Class"""
    def __init__(self, val='', parent=None):
        super().__init__(parent)
        self.set(val)
        self.setMinimumHeight(MIN_HEIGHT)

    def set(self, txt):
        if txt:
            ttxt = '%s' % txt
            self.setText(ttxt.strip())
        else:
            self.setText('')
        self.setCursorPosition(0)

    def get(self):
        tmp = '%s' % self.text()
        return tmp.strip()


class TInteger(TTextLine):
    '''Text field with numeric chars only left aligned.'''
    def __init__(self, val='', parent=None):
        super().__init__(val, parent)
        rval = Qc.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(Qg.QRegExpValidator(rval))
        self.setAlignment(Qc.Qt.AlignRight)


class TTextlineNum(TTextLine):
    '''Text field with numeric chars only left aligned.'''
    def __init__(self, val='', parent=None):
        super().__init__(val, parent)
        rval = Qc.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(Qg.QRegExpValidator(rval))


class TYesNoCombo(Qw.QComboBox):
    '''Yes/No Combo'''
    def __init__(self, val=0, noyes=['No', 'Yes'], parent=None):
        super().__init__(parent)
        self.addItem(noyes[0])
        self.addItem(noyes[1])
        self.set(val)

    def get(self):
        return self.currentIndex() != 0

    def set(self, val):
        idx = 0
        if int(val) != 0:
            idx = 1
        self.setCurrentIndex(idx)


class TWeekdays(Qw.QWidget):
    '''
    Weekdays selection ( [1,1,1,1,1,0,0] 7 values 0 or 1, one per weekday)
    '''
    def __init__(self, val=[1, 1, 1, 1, 1, 0, 0], parent=None):
        '''pin: {'name': xx, 'vals': [1,1,1,1,1,1,1], 'dayNames': []}'''
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.parent = parent
        self.setSizePolicy(
            Qw.QSizePolicy(
                Qw.QSizePolicy.Expanding, Qw.QSizePolicy.Expanding))
        self.set(val)
        self.selected = [0, 0]
        self.dayNames = WEEKDAYS
        self.setMinimumSize(Qc.QSize(170, 20))
        self.setMaximumSize(Qc.QSize(170, 20))
        self.setToolTip(MSG_SELECT_DAYS)
        self.setMinimumHeight(MIN_HEIGHT)

    def sizeHint(self):
        return Qc.QSize(170, 20)

    def mousePressEvent(self, event):
        if event.button() == Qc.Qt.LeftButton:
            xOffset = self.width() / 7
            # yOffset = xOffset #self.height()
            if event.x() < xOffset:
                x = 0
            elif event.x() < 2 * xOffset:
                x = 1
            elif event.x() < 3 * xOffset:
                x = 2
            elif event.x() < 4 * xOffset:
                x = 3
            elif event.x() < 5 * xOffset:
                x = 4
            elif event.x() < 6 * xOffset:
                x = 5
            else:
                x = 6
            cell = self.grid[x]
            if cell == BLANK:
                cell = GREEN
            else:
                cell = BLANK
            self.grid[x] = cell
            self.selected = [x, 0]
            self.update()

        elif event.button() == Qc.Qt.RightButton:
            self.reset()

    def paintEvent(self, event=None):
        painter = Qg.QPainter(self)
        painter.setRenderHint(Qg.QPainter.Antialiasing, True)
        xOffset = self.width() / 7
        yOffset = self.height()
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        for x in range(7):
            cell = self.grid[x]
            rect = Qc.QRectF(x * xOffset, 0, xOffset,
                             yOffset).adjusted(0.1, 0.1, -0.1, -0.1)
            color = None
            painter.drawRect(rect.adjusted(2, 2, -2, -2))
            if cell == GREEN:
                color = Qc.Qt.green
            if color is not None:
                painter.save()
                painter.setPen(Qc.Qt.black)
                painter.setBrush(color)
                painter.drawRect(rect.adjusted(2, 2, -2, -2))
                color = Qc.Qt.black
                painter.restore()
            painter.setPen(Qc.Qt.black)
            painter.drawText(rect.adjusted(4, 3, -3, -3), self.dayNames[x])
            painter.drawRect(rect)

    def get(self, strVal=True):
        if strVal:
            st = '['
            for i in range(7):
                if i == 6:
                    st += '%s]' % self.grid[i]
                else:
                    st += '%s,' % self.grid[i]
            return st
        else:
            return self.grid

    def set(self, darr=[0, 0, 0, 0, 0, 0, 0]):
        # Set values to days vector. But first checks for
        # proper array length and type
        darr = '%s' % darr
        tmparr = eval(darr)
        if len(tmparr) == 7:
            self.grid = tmparr
        else:
            self.grid = [0, 0, 0, 0, 0, 0, 0]
        self.update()

    def reset(self):
        'Set everything to Null'
        self.set([0, 0, 0, 0, 0, 0, 0])

    def set5days(self):
        'Set Standard five days week'
        self.set([1, 1, 1, 1, 1, 0, 0])


class TCombo(Qw.QComboBox):
    '''Combo'''
    def __init__(self, val=0, vlist=[], parent=None):
        super().__init__(parent)
        self.populate(vlist)
        self.set(val)  # val must be a valid id

    def get(self):
        return self.index2id[self.currentIndex()]

    def set(self, id_):
        if id_:
            self.setCurrentIndex(self.id2index[id_])

    def __init__(self, val=0, vlist=[], parent=None):
        super().__init__(parent)
        self.populate(vlist)
        self.set(val)  # val must be a valid id

    def get(self):
        return self.index2id[self.currentIndex()]

    def set(self, id_):
        if id_:
            self.setCurrentIndex(self.id2index[id_])

    def populate(self, vlist):
        """
        1.get values from Database
        2.fill Combo
        3.set current index to initial value
        """
        self.index2id = {}
        self.id2index = {}
        for i, elm in enumerate(vlist):
            self.addItem('%s' % elm[1])
            self.index2id[i] = elm[0]
            self.id2index[elm[0]] = i


class SortWidgetItem(Qw.QTableWidgetItem):
    """Sorting"""
    def __init__(self, text, sortKey):
        super().__init__(text, Qw.QTableWidgetItem.UserType)
        self.sortKey = sortKey

    def __lt__(self, other):
        return self.sortKey < other.sortKey


def item_int(num):
    '''Returns integer item'''
    item = Qw.QTableWidgetItem()
    # item.setData(QtCore.Qt.DisplayRole, QtCore.QVariant(num))
    item.setData(Qc.Qt.DisplayRole, num)
    item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
    return item


def item_num(num):
    '''Returns Numeric item'''
    item = sortWidgetItem(dec2gr(num), num)
    item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
    return item


def item_str(strv):
    '''Returns String item'''
    st = '%s' % strv
    if st == 'None':
        st = ''
    item = Qw.QTableWidgetItem(st)
    return item


def item_date(strv):
    '''Returns Date item'''
    strv = '%s' % strv
    if len(strv) < 10:
        item = sortWidgetItem(strv, strv)
    else:
        y, m, d = strv.split('-')
        item = sortWidgetItem('%s/%s/%s' % (d, m, y), strv)
    return item


class Form_find_2(Qw.QDialog):
    signal_selected_id = Qc.pyqtSignal(str)
    signal_make_new = Qc.pyqtSignal(str)

    def __init__(self, dbf, sql, lbl, parent=None, frm=None,
                 sclose=True, title=None):
        """
        dbf : Database file path
        sql : final sql to run
        lbl : column labels
        frm : Name of the form to edit or add records
        sclose : True if immediately closing form after record selection
                 False otherwise
        title : Form Title
        """
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle(title)
        # Save initialization data
        self.dbf = dbf
        self.sql = sql
        self.lbl = lbl
        self.parent = parent
        self.frm = frm
        self.sclose = sclose
        layout = Qw.QVBoxLayout()
        self.setLayout(layout)
        self.tbl = Qw.QTableWidget()
        self.tbl.cellDoubleClicked.connect(self.get_values)
        self.tbl.verticalHeader().setStretchLastSection(False)
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setSelectionMode(Qw.QAbstractItemView.SingleSelection)
        self.tbl.setSelectionBehavior(Qw.QAbstractItemView.SelectRows)
        self.tbl.setEditTriggers(Qw.QAbstractItemView.NoEditTriggers)
        self.tbl. setAlternatingRowColors(True)
        # self.setStyleSheet("alternate-background-color: rgba(208,246,230);")
        self.tbl.setSortingEnabled(True)
        self.tbl.wordWrap()
        layout.addWidget(self.tbl)
        self.resize(300, 200)
        self.populate()

    def contextMenuEvent(self, event):
        menu = Qw.QMenu(self)
        Action = menu.addAction(u"Δημιουργία νέας παρόμοιας εγγραφής")
        Action.triggered.connect(self.make_new)
        menu.exec_(event.globalPos())

    def make_new(self):
        i = self.tbl.currentRow()
        self.signal_make_new.emit('%s' % self.tbl.item(i, 0).text())

    def populate(self):
        rows = db.rowst(self.dbf, self.sql)
        self.tbl.setRowCount(len(rows))
        self.tbl.setColumnCount(len(self.lbl))
        self.tbl.setHorizontalHeaderLabels(self.lbl)
        total = dec.dec(0)
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                if dec.isNum(col):
                    if self.lbl[j][-2:] == 'id':
                        self.tbl.setItem(i, j, item_int(col))
                    elif type(col) is tdec:
                        self.tbl.setItem(i, j, item_num(col))
                    else:
                        # self.setItem(i, j, self._numItem(col))
                        self.tbl.setItem(i, j, item_num(col))
                elif (len(col) == 10) and (col[4] == '-'):
                    self.tbl.setItem(i, j, item_date(col))
                else:
                    self.tbl.setItem(i, j, item_str(col))
            total += dec.dec(row[-2]) - dec.dec(row[-1])
            self.tbl.setItem(i, len(self.lbl) - 1, item_num(total))
        self.tbl.resizeColumnsToContents()

    def get_values(self):
        i = self.tbl.currentRow()
        self.signal_selected_id.emit('%s' % self.tbl.item(i, 0).text())
        if self.sclose:
            self.accept()

    def keyPressEvent(self, ev):
        '''use enter or return for fast selection nad form close ...'''
        if (ev.key() == Qc.Qt.Key_Enter or
                ev.key() == Qc.Qt.Key_Return):
            self.get_values()
        Qw.QDialog.keyPressEvent(self, ev)

    @Qc.pyqtSlot()
    def slot_updated(self):
        self.populate()


class Table_widget(Qw.QTableWidget):
    """:param data: Tuple with two elements (labels, rows)"""
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.labels, self.rows = data
        self.parent = parent
        # Εδώ ορίζουμε το πλάτος της γραμμής του grid
        # self.verticalHeader().setDefaultSectionSize(20)
        self.verticalHeader().setStretchLastSection(False)
        self.verticalHeader().setVisible(False)
        self.setSelectionMode(Qw.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(Qw.QAbstractItemView.SelectRows)
        self.setEditTriggers(Qw.QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        # self.setStyleSheet("alternate-background-color: rgba(208,246,230);")
        self.setSortingEnabled(True)
        self.populate()
        self.wordWrap()

    def _intItem(self, num):
        item = Qw.QTableWidgetItem()
        item.setData(Qc.Qt.DisplayRole, num)
        item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
        return item

    def _numItem(self, num):
        item = SortWidgetItem(dec2gr(num), num)
        item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
        return item

    def _strItem(self, strv):
        st = str(strv)
        if st == 'None':
            st = ''
        item = Qw.QTableWidgetItem(st)
        return item

    def populate(self):
        self.setRowCount(len(self.rows))
        self.setColumnCount(len(self.labels))
        self.setHorizontalHeaderLabels(self.labels)
        for i, row in enumerate(self.rows):
            for j, col in enumerate(row):
                if isNum(col):
                    # if col == 'id' or col ends with id (e.g. erg_id)
                    if self.labels[j].endswith('id'):
                        self.setItem(i, j, self._intItem(col))
                    elif type(col) is decimal.Decimal:
                        self.setItem(i, j, self._numItem(col))
                    else:
                        self.setItem(i, j, self._numItem(col))
                elif is_iso_date(col):
                    self.setItem(i, j, SortWidgetItem(date2gr(col), col))
                else:
                    self.setItem(i, j, self._strItem(col))
        self.resizeColumnsToContents()


class Form_find(Qw.QDialog):
    valselected = Qc.pyqtSignal(str)

    def __init__(self, data, title, parent=None, selectAndClose=True):
        super().__init__(parent)
        self.selectAndClose = selectAndClose
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        layout = Qw.QVBoxLayout()
        self.tbl = Table_widget(data, parent)
        self.tbl.cellDoubleClicked.connect(self._setvals)
        layout.addWidget(self.tbl)
        self.setLayout(layout)
        self.setWindowTitle(title)
        self.resize(550, 400)

    def _setvals(self):
        self.vals = []
        i = self.tbl.currentRow()
        for j in range(self.tbl.columnCount()):
            self.vals.append(self.tbl.item(i, j).text())
        self.valselected.emit('%s' % self.vals[0])
        if self.selectAndClose:
            self.accept()

    def keyPressEvent(self, ev):
        '''use enter or return for fast selection'''
        if (ev.key() == Qc.Qt.Key_Enter or ev.key() == Qc.Qt.Key_Return):
            self._setvals()
        Qw.QDialog.keyPressEvent(self, ev)


class TTextButton(Qw.QWidget):
    """Advanced control for foreign key fields
    :param val: the id value of foreign relation
    :param table: Table or View
    :param parent: The parent object
    .. warning:: Parent object must have db member
    """
    # SIGNALS HERE
    valNotFound = Qc.pyqtSignal(str)

    def __init__(self, val, table, parent):
        """Init"""
        super().__init__(parent)
        self.table = table  # the table or view name
        self.dbf = parent.dbf  # parent must have .dbf
        # create gui
        self.text = Qw.QLineEdit(self)
        self.button = Qw.QToolButton(self)
        self.button.setText('?')
        self.button.setFocusPolicy(Qc.Qt.NoFocus)
        layout = Qw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.setLayout(layout)
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        # connections
        self.text.textChanged.connect(self.text_changed)
        self.button.clicked.connect(self.button_clicked)
        # init gui as red and try to fill it with existing value from db
        self.red()
        self.set(val)

    def set(self, idv):
        self.val = find_by_id(self.dbf, idv, self.table, 'names-tuples')
        self.vap = self.txt_val()
        self.text.setText(self.vap)
        self.setToolTip(self.rpr_val())
        self.text.setCursorPosition(0)
        lval = len(self.val[1])
        if lval > 0:
            self.green()
        else:
            self.red()

    def txt_val(self):
        """[('id', 'fld1', ..), [(id0, f0, ...), ...]"""
        atxt = []
        if self.val[1] == []:
            return ''
        for i, field in enumerate(self.val[0]):
            if field != 'id':
                atxt.append('%s' % self.val[1][0][i])
        return ' '.join(atxt)

    def rpr_val(self):
        """all fields: values of table mainly for tooltip use"""
        atxt = ''
        if self.val[1] == []:
            return ''
        for i, field_name in enumerate(self.val[0]):
            atxt += '%s : %s\n' % (field_name, self.val[1][0][i])
        return atxt

    def get(self):
        field_names, vals = self.val
        if 'id' not in field_names:
            return ''
        id_index = field_names.index('id')
        if self.isGreen:
            return '%s' % vals[0][id_index]
        else:
            return ''

    def text_changed(self):
        if self.vap != self.text.text():
            self.red()
        else:
            self.green()

    def button_clicked(self):
        self.button.setFocus()
        self.find('')

    def green(self):
        self.button.setStyleSheet('background-color: rgba(0, 180, 0);')
        self.isGreen = True

    def red(self):
        self.button.setStyleSheet('background-color: rgba(239, 41, 41);')
        self.isGreen = False

    def keyPressEvent(self, ev):
        if ev.key() == Qc.Qt.Key_Enter or ev.key() == Qc.Qt.Key_Return:
            if self.vap != self.text.text():
                self.find(self.text.text())
        return Qw.QWidget.keyPressEvent(self, ev)

    def find(self, text):
        """
        :param text: text separated by space multi-search values 'va1 val2 ..'
        """
        oldvalue = self.get()
        vals = find(self.dbf, self.table, text, 'names-tuples')
        # print(vals)
        if len(vals[1]) == 1:
            # We assume that the first element of first tuple is id
            self.set(vals[1][0][0])
        elif len(vals[1]) > 1:
            ffind = Form_find(vals, u'Αναζήτηση', self)
            if ffind.exec_() == Qw.QDialog.Accepted:
                self.set(ffind.vals[0])
            else:
                if oldvalue == self.get():
                    pass
                else:
                    self.red()
        else:
            self.valNotFound.emit(self.text.text())


class FTable(Qw.QDialog):
    '''Form to display and edit row table data'''
    def __init__(self, dbf, table, did=None, parent=None):
        '''
        :param dbf: Database file path
        :param table: Database table
        :param did: The id of the record. None for new record.
        '''
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Form template')
        # basic data here
        self._db = dbf
        self._table = table
        self._id = did
        self.fields = []
        self.labels = []
        self.data = {}
        # Set main layout
        self.mainlayout = Qw.QVBoxLayout()
        self.setLayout(self.mainlayout)
        # Create widgets here and add them to formlayout
        self._create_and_fill_fields()
        self._create_buttons()

    def _create_and_fill_fields(self):
        self.dbf = self._db
        if  self._id:
            sql = "SELECT * FROM %s WHERE id='%s'" % (self._table, self._id)
        else:
            sql = "SELECT * FROM %s limit 0" % self._table
        self.fields, self.data = select2(self._db, sql)
        for fld in self.fields:
            self.labels.append(get_lbl(fld))
        flayout = Qw.QFormLayout()
        self.mainlayout.addLayout(flayout)
        self.widgets = {}
        # Add fields to form
        for i, fld in enumerate(self.fields):
            if fld.endswith('_id'):
                self.widgets[fld] = TTextButton(None, fld[:-3], self)
            elif fld == 'id':
                self.widgets[fld] = TInteger()
                self.widgets[fld].setEnabled(False)
            else:
                self.widgets[fld] = TTextLine()
            flayout.insertRow(i, Qw.QLabel(self.labels[i]),
                              self.widgets[fld])
            if fld in self.data:  # if not None or empty string
                if self.data[fld]:
                    self.widgets[fld].set('%s' % self.data[fld])
                else:
                    self.data[fld] = ''
            # replace possible None with empty string for correct comparisson
            else:
                self.data[fld] = ''
        print(self.is_empty(), self._id)

    def is_empty(self):
        for fld in self.widgets:
            if self.widgets[fld].text() != '':
                return False
        self._id = None
        return True

    def _create_buttons(self):
        '''Create buttons for the form'''
        # Create layout first
        buttonlayout = Qw.QHBoxLayout()
        self.mainlayout.addLayout(buttonlayout)
        # Create buttons here
        self.bcancel = Qw.QPushButton(u'Ακύρωση', self)
        self.bsave = Qw.QPushButton(u'Αποθήκευση', self)
        # Make them loose focus
        self.bcancel.setFocusPolicy(Qc.Qt.NoFocus)
        self.bsave.setFocusPolicy(Qc.Qt.NoFocus)
        # Add them to buttonlayout
        buttonlayout.addWidget(self.bcancel)
        buttonlayout.addWidget(self.bsave)
        # Make connections here
        self.bcancel.clicked.connect(self.close)
        self.bsave.clicked.connect(self.save)

    def validate(self):
        return False

    def save(self):
        sqli = 'INSERT INTO %s VALUES (null, %s);'
        sqlu = "UPDATE %s SET %s WHERE id='%s';"
        vals = []
        if not self._id:
            for wid in self.widgets:
                if wid == 'id':
                    continue
                vals.append("'%s'" % self.widgets[wid].get())
            fsql = sqli % (self._table, ','.join(vals))
        else:
            data_for_update = self.get_data_from_form(True)
            if len(data_for_update) == 1:
                return None
            for fld in self.get_data_from_form(True):
                if fld == 'id':
                    continue
                vals.append("%s='%s'" % (fld, self.widgets[fld].get()))
            fsql = sqlu % (self._table, ','.join(vals), self._id)
        script(self._db, fsql)
        print(fsql)
        self.accept()

    def get_data_from_form(self, only_changed=False):
        '''Get data from the form. Assume id already exists.'''
        if 'id' in self.data:
            dtmp = {'id': self.data['id']}
        else:
            dtmp = {'id': ''}
        for field in self.widgets:
            if only_changed:
                if self.data[field] != self.widgets[field].get():
                    dtmp[field] = self.widgets[field].get()
            else:
                dtmp[field] = self.widgets[field].get()
        return dtmp


# Δοκιμαστικά
def qfl(label, widget):
    return [Qw.QLabel(label), widget]


class Test(Qw.QDialog):
    """Testing my controls"""
    def __init__(self, dbf, parent=None):
        super().__init__()
        self.dbf = dbf
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle(u'Δοκιμή qted')
        self.flds = [qfl('TCheckBox', TCheckbox(2, self)),
                     qfl('TDate', TDate('', self)),
                     qfl('TDateEmpty', TDateEmpty('', self)),
                     qfl('TInteger', TInteger(145, self)),
                     qfl('TIntegerSpin', TIntegerSpin(12, self)),
                     qfl('TNumericSpin', TNumericSpin(123.45, self)),
                     qfl('TNumeric', TNumeric(11.23, self)),
                     qfl('TText', TText('This is just text', self)),
                     qfl('TTextButton', TTextButton('1', 'par', self)),
                     qfl('TCombo', TCombo(3,
                                          [[1, u'Ενα'],
                                           [2, u'Δύο'],
                                           [3, u'Τρία'],
                                           [4, u'Τέσσερα']
                                           ],
                                          self)),
                     qfl('TextLine', TTextLine('Ted Lazaros', self)),
                     qfl('TextLineNum', TTextlineNum(123123123, self)),
                     qfl('WeekDays', TWeekdays([1, 1, 1, 0, 0, 0, 1], self)),
                     qfl('YesNoCombo',
                         TYesNoCombo(False, [u'Όχι', u'Ναί'], self))
                     ]
        layout = Qw.QFormLayout()
        for el in self.flds:
            layout.addRow(el[0], el[1])
        btn = Qw.QPushButton(u'Επιστροφή Τιμών')
        layout.addRow(Qw.QLabel(''), btn)
        self.setLayout(layout)
        btn.clicked.connect(self.getVals)
        btn.setFocusPolicy(Qc.Qt.NoFocus)
        self.flds[8][1].valNotFound.connect(self.test_slot)

    @Qc.pyqtSlot(str)
    def test_slot(self, val):
        Qw.QMessageBox.critical(self, u"Λάθος", u'Η τιμή %s δεν υπάρχει' % val)

    def getVals(self):
        ast = ''
        for el in self.flds:
            ast += '%s : %s\n' % (el[0].text(), el[1].get())
        Qw.QMessageBox.information(self, u"Τιμές πεδίων", ast)


if __name__ == '__main__':
    import sys
    dbf0 = '/home/tedlaz/pyted/pyqt_templates/tst_qtwidgets.db'
    app = Qw.QApplication(sys.argv)
    ui = Test(dbf0)
    ui.show()
    # sys.exit(app.exec_())
    dbf1 = "/home/tedlaz/test"
    # app = Qw.QApplication([])
    # dialog = FTable(dbf1, 'pel', 3)
    # dialog.show()
    appex = app.exec_()
    sys.exit(appex)
