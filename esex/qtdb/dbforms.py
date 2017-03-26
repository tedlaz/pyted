# -*- coding: utf-8 -*-
'''
Created on Nov 8, 2013

@author: tedlaz
'''

from suds.client import Client

from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtProperty

from collections import OrderedDict
import sqlite3
import os.path
import decimal
import res_rc

debuging = False
zdb = 'zdb.sql3'


class grMsgBox(QtGui.QMessageBox):
    def __init__(self, **kwds):
        super(grMsgBox, self).__init__(**kwds)
        self.button(grMsgBox.Yes).setText(u"Ναί")
        self.button(grMsgBox.No).setText(u"Όχι")


def dprint(val):
    if debuging:
        print(val)


def readFromRes(resname):
    f = QtCore.QFile(resname)
    if f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
        stream = QtCore.QTextStream(f)
        stream.setCodec('utf-8')
        vstr = u''
        while not stream.atEnd():
            vstr += u'%s\n' % stream.readLine().__str__()
    f.close()
    return vstr


def executeScript(script, db):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.executescript(script)
        con.commit()

    except sqlite3.Error, e:
        if con:
            con.rollback()
        dprint("dbforms Line 45 Error : %s" % e.args[0])
    finally:
        cur.close()
        con.close()

if not os.path.exists(zdb):
    zql = readFromRes(':sql/zdb.sql')
    executeScript(zql, zdb)
tblStyle = "alternate-background-color: rgba(208,246,230);"


def checkVat(afm, countryCode='EL'):
    '''
    using SOAP client
    returns dictionary with:
    countryCode,vatNumber,requestDate,valid,name,address
    '''
    url = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    result = {'valid': False}
    try:
        client = Client(url, timeout=10)
        result = client.service.checkVat(countryCode, afm)
    except:
        result['conError'] = True
    return result


def addLogToDb(logText, dbfile=None):
    datetime = strDateTime()
    if dbfile:
        commitToDb("INSERT INTO lg(ldt,logp) VALUES (?,?)",
                   [datetime, logText],
                   dbfile)


def allowInsertDate(strDate, db):
    '''
    Checks if closeDate exists
    if Yes
        If closeDate >= strDate returns False
        else returns True
    if No
        returns True
    '''
    sql = "SELECT lkd FROM lk WHERE id=?"
    closeDate = getDbSingleVal(sql, (1,), db)
    # print('dbforms line 92 %s , %s' % (strDate, closeDate))
    if closeDate:
        if strDate <= closeDate:
            return False
        else:
            return True
    else:
        return True


def strDateTime():
    '''
    returns datetime string (2010-01-31 20:30:15)
    '''
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# GENERIC UTILITIES
def isNum(value):  # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters :
            1.value : the value to check against.
        output: True or False
        """
    if value is None:
        return False
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def dec(poso, dekadika=2):
    """
    use : Given a number, it returns a decimal with a specific number of
          decimal digits
    input Parameters:
          1.poso     : The number for conversion in any format
                       (e.g. string or int ..)
          2.dekadika : The number of decimals (default 2)
    output: A decimal number
    """
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


def sha1OfFile(filepath):
    import hashlib
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()
# ENDGENERIC UTILITIES
# DATABASE UTILITIES


def getDbSingleVal(sql, sqlp, db):
    if not os.path.exists(db):
        return None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(sql, sqlp)  # sql with ? instead of %s
        val = cur.fetchone()[0]
        cur.close()
        con.close()
    except sqlite3.Error, e:
        dprint("dbforms line 124 Error 39: %s" % e.args[0])
        dprint("dbforms line 125 sql:%s sqlp: %s db: %s" % (sql, sqlp, db))
        val = None
    except:
        val = None
    return val


def getDbOneRow(sql, db):
    if not os.path.exists(db):
        return None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(sql)
        row = cur.fetchone()
    except sqlite3.Error, e:
        dprint("dbforms line 140 Error: %s" % e.args[0])
        row = []
    finally:
        cur.close()
        con.close()
    return row


def getDbRows(sql, db):
    if not os.path.exists(db):
        return [], []
    columnNames = []

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(sql)
        columnNames = [t[0] for t in cur.description]
        rws = cur.fetchall()
        cur.close()
        con.close()
    except sqlite3.Error, e:
        dprint("dbforms line 161 Error : %s" % e.args[0])
        rws = []
    return rws, columnNames


def commitToDb(sql, sqlp, db):  # For insert or Update records
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(sql, sqlp)  # sql with ? instead of %s
        last_id = cur.lastrowid
        con.commit()
    except sqlite3.Error, e:
        if con:
            con.rollback()
        dprint("dbforms line 175 Error 93: %s" % e.args[0])
        dprint("dbforms line 176 sql: %s sqlp: %s" % (sql, sqlp))
        last_id = None
    finally:
        cur.close()
        con.close()
    return last_id


def getLabels(fldArr):
    '''
    Requires master DB with zfield table
    '''
    labels = []
    for el in fldArr:
        labels.append(getLabel(el))
    return labels


def getLabel(fld):
    sql = "SELECT flp FROM zfld WHERE fln='%s'"
    v = getDbOneRow(sql % fld, zdb)
    if v:
        return v[0]
    else:
        return fld


def parseDDL(table, db):
    fields, headers = getDbRows('pragma table_info(%s)' % table, db)
    finalArray = []
    for fld in fields:
        cname = fld[1]
        tempTyp = fld[2].lower()
        if tempTyp == 'integer':
            ctype = 'int'
        elif tempTyp[:7] == 'varchar':
            ctype = 'txt'
        elif tempTyp[:4] == 'text':
            ctype = 'txt'
        elif tempTyp[:4] == 'date':
            ctype = 'dat'
        elif tempTyp[:7] == 'decimal':
            ctype = 'dec'
        elif tempTyp[:4] == 'bool':
            ctype = 'boo'
        else:
            ctype = 'txt'
        if fld[3] == '1':
            requi = True
        else:
            requi = False

        lbl = valFromTableOrDefault(cname,
                                    "SELECT flp FROM zfld WHERE fln=?",
                                    zdb)
        if '_id' in cname:
            ctype = 'key'
            fromzdb = getDbSingleVal("SELECT sq1 FROM fkey WHERE fln=?",
                                     (cname,),
                                     zdb)
            if fromzdb:
                sqlInsert = fromzdb
            else:
                sqlInsert = "SELECT * FROM %s" % cname[:-3]
            finalArray.append({'cname': cname,
                               'ctype': ctype,
                               'requi': requi,
                               'lbl': lbl,
                               'sqin': sqlInsert})
        else:
            finalArray.append({'cname': cname,
                               'ctype': ctype,
                               'requi': requi,
                               'lbl': lbl})
    return finalArray


def valFromTableOrDefault(defVal, sql, db):
    val = getDbSingleVal(sql, (defVal,), db)
    if val:
        return val
    else:
        return defVal

# END DATABASE UTILITIES

# WIDGETS AND UTILITIES


def makeTitle(wtitle):
    title = QtGui.QLabel(wtitle)
    font = QtGui.QFont()
    font.setPointSize(11)
    font.setBold(True)
    font.setWeight(75)
    title.setFont(font)
    title.setStyleSheet("color: rgb(0, 0, 127);")
    return title


def populateTableWidget(tableWidget, lines, headers):
    '''
    Function that rus sql on database db and fills the tablewidget with returning values
    '''
    def strItem(strv):
        st = '%s' % strv
        if st == 'None':
            st = ''
        item = QtGui.QTableWidgetItem(st)
        return item

    def numItem(no):
        if isNum(no):
            no = '%s' % no
            no = no.replace(',', '.')
            item = QtGui.QTableWidgetItem(QtCore.QString("%L1").arg(float(no),
                                          0, "f", 2))
        else:
            item = strItem(no)
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        return item

    def setType(val, typos=0):
        if typos == 0:  # text
            return strItem(val)
        elif typos == 1:  # Number
            return numItem(val)
        else:
            return val

    def setLine(line, typ=0):
        rc = tableWidget.rowCount()
        tableWidget.setRowCount(rc+1)
        colNo = 0
        for col in line:
            '''
            if colTypes == []:
                tableWidget.setItem(rc,colNo,setType(col,typ))
            else:
                tableWidget.setItem(rc,colNo,setType(col,colTypes[colNo]))

            '''
            if isNum(col):
                b = QtGui.QTableWidgetItem()
                b.setData(QtCore.Qt.EditRole, QtCore.QVariant(col))
                b.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                tableWidget.setItem(rc, colNo,b)
            else:
                tableWidget.setItem(rc,colNo,strItem(col))
            colNo += 1
    # Εδώ ορίζουμε το πλάτος της γραμμής του grid
    tableWidget.verticalHeader().setDefaultSectionSize(20)
    tableWidget.verticalHeader().setStretchLastSection(False)
    tableWidget.verticalHeader().setVisible(False)
    tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    tableWidget.setRowCount(0)
    tableWidget.setColumnCount(len(headers))
    tableWidget.setHorizontalHeaderLabels(headers)
    # tableWidget.setColumnHidden(0,True) #κρύβει την πρώτη στήλη
    for line in lines:
        setLine(line)

    tableWidget.resizeColumnsToContents()

    return len(lines)


class mytbl(QtGui.QTableWidget):
    def __init__(self, parent=None):
        super(mytbl, self).__init__(parent)
        if parent:
            self.tbl = parent.tbl
            self.db = parent.db
        else:
            self.tbl = None
            self.db = None

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)

        Action = menu.addAction(u"Επεξεργασία Εγγραφής")
        Action.triggered.connect(self.openForEdit)
        menu.exec_(event.globalPos())

    def openForEdit(self):
        frm = autoDialog(self.tbl,
                         self.db,
                         self.item(self.currentRow(), 0).text(),
                         parent=self)
        if frm.exec_() == QtGui.QDialog.Accepted:
            pass


class fFind(QtGui.QDialog):
    '''
    Form returning search values
    sql: search sql
    db : Current DB
    insTbl : 0 for no insert button, 1 for insert button
    parent:
    '''
    def __init__(self, sql, db, tabl, canInsertNewRecord=1, parent=None):
        QtGui.QDialog.__init__(self)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.lines, self.headers = getDbRows(sql, db)

        self.sql = sql
        self.db = db
        self.tbl = tabl
        self.canInsertNewRecord = canInsertNewRecord
        self.parent = parent
        self.colwidths = []

        self.table = mytbl(self)  # QtGui.QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(tblStyle)
        self.table.setSortingEnabled(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        if canInsertNewRecord:
            self.newEggr = QtGui.QPushButton(u'Νέα εγγραφή')
            layout.addWidget(self.newEggr)
            self.newEggr.clicked.connect(self.newRecord)
        self.setLayout(layout)
        self.setWindowTitle(u"Αναζήτηση ")
        self.setMinimumSize(400, 500)

        self.populateTable()
        self.connect(self.table,
                     QtCore.SIGNAL("cellDoubleClicked(int, int)"),
                     self.sendVals)
        self.array = []

    def newRecord(self):
        frmnr = autoDialog(self.tbl, self.db, parent=self)
        if frmnr.exec_() == QtGui.QDialog.Accepted:
            self.populateTable()
            print 'line 276 populate'

    def keyPressEvent(self, ev):
        '''
        use enter or return for fast selection nad form close ...
        '''
        if (ev.key() == QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            self.sendVals(self.table.currentRow(), self.table.currentColumn())
        QtGui.QDialog.keyPressEvent(self, ev)

    def val(self):
        return self.array

    def sendVals(self, x, y):
        for colu in range(self.table.columnCount()):
            self.array.append(self.table.item(x, colu).text())
        self.accept()

    def populateTable(self):
        lines, colHeaders = getDbRows(self.sql, self.db)
        populateTableWidget(self.table, lines, getLabels(colHeaders))


def findSelector2(sql, db, tabl=None):
    # 1.Συγκέντρωση δεδομένων απο DB
    # 2.Εάν έχω:
    # 2.1  καμμία εγγραφή
    # 2.2  Μία εγγραφή
    # 2.3  Πολλές εγγραφές
    lines, colHeaders = getDbRows(sql, db)
    '''
    numberOfRecords =len(lines)

    if numberOfRecords == 0:
        return 0,'No Data'
    elif numberOfRecords == 1:
        return lines[0][0],lines[0][1]
    else:
        form = fFind(lines,getLabels(colHeaders),db)
        return form
    '''
    form = fFind(lines, getLabels(colHeaders), None, 1, db, tabl)
    return form


class DbLineEdit(QtGui.QLineEdit):
    def __init__(self, txtVal=None, isRequired=False, parent=None):
        super(DbLineEdit, self).__init__(parent)
        self.isReq = isRequired
        self.setValue(txtVal)

    def setValue(self, txtVal):
        if txtVal:
            ttxtVal = '%s' % txtVal
            self.setText(ttxtVal.strip())
        else:
            self.setText('')

    def getValue(self):
        tmpval = '%s' % self.text()
        return tmpval.strip()

    def str_(self):
        return self.getValue()

    @pyqtProperty(str)
    def timi(self):
        return self.getValue()

    @timi.setter
    def timi(self, timi):
        self.setValue(timi)


class DbDoubleSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, intVal=0, mini=-999999999, maxi=999999999,
                 parent=None, row=-1, col=-1):
        super(DbDoubleSpinBox, self).__init__(parent)
        self.setMinimum(mini)
        self.setMaximum(maxi)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        # For use in QTableWidget
        self.row = row
        self.col = col
        if intVal:
            self.setValue(intVal)
        else:
            self.setValue(0)

    def getValue(self):
        return self.value()

    def str_(self):
        return '%s' % self.value()

    @pyqtProperty(float)
    def timi(self):
        return self.getValue()

    @timi.setter
    def timi(self, timi):
        self.setValue(timi)


class DbSpinBox(QtGui.QSpinBox):
    def __init__(self, intVal=0, mini=0, maxi=999999999, parent=None):
        super(DbSpinBox, self).__init__(parent)
        self.setMinimum(mini)
        self.setMaximum(maxi)
        if intVal:
            self.setValue(intVal)
        else:
            self.setValue(0)

    def getValue(self):
        return self.value()

    def str_(self):
        return '%s' % self.value()

    @pyqtProperty(int)
    def timi(self):
        return self.getValue()


class DbDateEdit(QtGui.QDateEdit):
    def __init__(self, sqliteDate=None, parent=None):
        super(DbDateEdit, self).__init__(parent)

        self.setCalendarPopup(True)
        self.setValue(sqliteDate)

    def setValue(self, sqliteDate):
        if sqliteDate:
            if len(sqliteDate) > 10:
                sqliteDate = sqliteDate[:10]
            yr, mn, dt = sqliteDate.split('-')
            qd = QtCore.QDate()
            qd.setDate(int(yr), int(mn), int(dt))
            self.setDate(qd)
        else:
            self.setDate(QtCore.QDate.currentDate())

    def getValue(self):
        return self.date().toString('yyyy-MM-dd')

    def str_(self):
        return self.getValue()

    @pyqtProperty(str)
    def timi(self):
        return self.getValue()


class DbComboBox(QtGui.QComboBox):
    def __init__(self, cdata = [[]], parent=None):
        super(DbComboBox, self).__init__(parent)
        self.id = []
        self.setData(cdata)

    def setData(self, cdata=[[]]):
        for el in cdata:
            self.id.append(el[0])
            self.addItem(el[1])

    def setValue(self, val):
        for i in range(len(self.id)):
            if self.id[i] == val:
                self.setCurrentIndex(i)

    def getValue(self):
        return self.id[self.currentIndex()]

    def str_(self):
        return '%s' % self.getValue()

    @pyqtProperty(int)
    def timi(self):
        return self.getValue()


class DbButtonLineEdit(QtGui.QLineEdit):
    '''
    QlineEdit with button and sql based values
    Παράμετροι
    sql     = Το sql που μας δίνει τα δεδομένα του παράθυρου επιλογής
    titles  = Επικεφαλίδες για το table του παράθυρου επιλογής
              (string με διαχωριστικό το |)
    db      = Η διαδρομή του αρχείου μισθοδοσίας
    sizes   = Τα πλάτη των στηλών του παράθυρου επιλογής
    idVal   = Το πρωτεύον κλειδί που άμα πάρει αρχική τιμή μας εμφανίζει
              συγκεκριμένη εγγραφή
    '''
    def __init__(self, sql=None, titles=None, db=None, idVal=None, sql1=None,
                 sizes=[30, 300], tbl=None, parent=None, row=-1, col=-1):
        super(DbButtonLineEdit, self).__init__(parent)

        self.tbl = tbl.split('_')[0]
        self.sql = sql
        self.sql1 = sql1  # SQL ειδικά για το setValue ...
        self.titles = titles
        self.db = db
        self.sizes = sizes
        self.setValue(idVal)
        self.row = row
        self.col = col
        self.setReadOnly(True)
        self.button = QtGui.QToolButton(self)
        iconFind = QtGui.QIcon()
        iconFind.addPixmap(QtGui.QPixmap(":images/icon_find.png"),
                           QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
        self.button.setIcon(QtGui.QIcon(iconFind))
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.clicked)
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()
        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth*2 + 2),max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth*2 + 2))

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),(self.rect().bottom() - buttonSize.height() + 1)/2)
        super(DbButtonLineEdit, self).resizeEvent(event)
    '''
    def keyPressEvent(self,ev):
        if (ev.key()==QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            self.clicked()
    '''

    def clicked(self):
        a = fFind(self.sql, self.db, self.tbl)
        if a.exec_() == QtGui.QDialog.Accepted:
            self.idValue = a.array[0]
            ttxt = ''
            for i in range(1, len(a.array)):
                ttxt += '%s ' % a.array[i]
            self.setText(ttxt)
        QtGui.QLineEdit.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))

    def getValue(self):
        return self.idValue

    def setValue(self, idVal):
        if idVal is None:
            self.idValue = None
            return
        # Με την προυπόθεση ότι πάντα το πρώτο πεδίο είναι το [table_name].id
        idName = self.sql.split()[1][:-1]
        if ',' in idName:
            idName = idName.split(',')[0]
        if idName == '':
            idName = 'id'
        if self.sql1:
            sql = self.sql1 % idVal  # Μάλλον ακυρώνεται ...
        else:
            if 'WHERE' in self.sql:
                sqlWhere = " AND %s='%s'" % (idName, idVal)
            else:
                # sqlWhere = " WHERE %s=%s" % (idName,idVal)
                sqlWhere = " WHERE %s='%s'" % (idName, idVal)

            sql = self.sql + sqlWhere

        v = getDbOneRow(sql, self.db)

        if v:
            txtv = ''
            for i in range(1, len(v)):
                txtv += '%s ' % v[i]
            self.setText(txtv)
            self.idValue = idVal
        else:
            self.setText('')
            self.idValue = None

    def str_(self):

        return '%s %s' % (self.idValue, self.text())

    @pyqtProperty(int)
    def timi(self):
        return self.getValue()

BLANK, GREEN = range(2)


class WeekDays(QtGui.QWidget):
    def __init__(self, vals=[1, 1, 1, 1, 1, 0, 0], parent=None,
                 dayNames=u'ΔΕ ΤΡ ΤΕ ΠΕ ΠΑ ΣΑ ΚΥ'):
        super(WeekDays, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                             QtGui.QSizePolicy.Expanding))
        self.setValue(vals)  # Δημιουργεί το self.grid
        self.selected = [0, 0]
        self.dayNames = dayNames.split()
        self.setMinimumSize(QtCore.QSize(170, 20))
        self.setMaximumSize(QtCore.QSize(170, 20))
        self.setToolTip(u'Επιλέξτε τις Εργάσιμες ημέρες\nΜε δεξί κλικ μηδενίστε')

    def sizeHint(self):
        return QtCore.QSize(170, 20)

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            xOffset = self.width() / 7
            yOffset = xOffset  # self.height()
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
            if event.y() < xOffset:
                y = 0
            # print event.x(), event.y()
            cell = self.grid[x]
            if cell == BLANK:
                cell = GREEN
            else:
                cell = BLANK
            self.grid[x] = cell
            self.selected = [x, 0]
            self.update()

        elif event.button() == Qt.Qt.RightButton:
            self.reset()

    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        xOffset = self.width() / 7
        yOffset = self.height()  # / 7
        for x in range(7):
            cell = self.grid[x]
            rect = QtCore.QRectF(x * xOffset,
                                 0,
                                 xOffset,
                                 yOffset).adjusted(0.5, 0.5, -0.5, -0.5)
            color = None
            painter.drawRect(rect.adjusted(2, 2, -2, -2))
            if cell == GREEN:
                color = Qt.Qt.green
            if color is not None:
                painter.save()
                painter.setPen(Qt.Qt.black)
                painter.setBrush(color)
                # painter.drawEllipse(rect.adjusted(2, 2, -2, -2))
                painter.drawRect(rect.adjusted(2, 2, -2, -2))
                color = Qt.Qt.black
                painter.restore()
            painter.setPen(Qt.Qt.black)
            painter.drawText(rect.adjusted(6, 3, -3, -3), self.dayNames[x])
            painter.drawRect(rect)
        # print self.getValues()

    def getValue(self, strVal=False):
        # strval : Εάν η επιστρεφόμενη τιμή είναι string ή array
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

    def str_(self):
        return self.getValue(True)

    def setValue(self, darr=[0, 0, 0, 0, 0, 0, 0]):
        'Set values to days vector. But first checks for '
        'proper array length and type'
        darr = '%s' % darr
        tmparr = eval(darr)
        if len(tmparr) == 7:
            self.grid = tmparr
        else:
            self.grid = [0, 0, 0, 0, 0, 0, 0]
        self.update()

    def reset(self):
        'Set everything to Null'
        self.setValue([0, 0, 0, 0, 0, 0, 0])

    def set5days(self):
        'Set Standard five days week'
        self.setValue([1, 1, 1, 1, 1, 0, 0])

    @pyqtProperty(str)
    def timi(self):
        return self.getValue(True)


def fieldFactory(typ, params=[], isRequired=False):
    paramLen = len(params)
    if typ == 'txt':
        if paramLen == 0:
            return DbLineEdit()
        else:
            return DbLineEdit(params[0], isRequired)
    elif typ == 'int':
        if paramLen == 0:
            return DbSpinBox()
        else:
            return DbSpinBox(params[0])
    elif typ == 'dec':
        if paramLen == 0:
            return DbDoubleSpinBox()
        else:
            return DbDoubleSpinBox(params[0])
    elif typ == 'dat':
        if paramLen == 0:
            return DbDateEdit()
        else:
            return DbDateEdit(params[0])
    elif typ == 'key':
        if paramLen == 4:
            return DbButtonLineEdit(params[0], params[1], params[2],
                                    tbl=params[3])
        else:
            return DbButtonLineEdit(params[0], params[1], params[2])
    elif typ == 'box':
        return DbComboBox(params[0])
    elif typ == 'boo':
        return DbLineEdit()
    elif typ == 'wdy':
        if params:
            return WeekDays(params[0])
        else:
            return WeekDays()
    else:
        return None, None


class autoDialog(QtGui.QDialog):
    def __init__(self, tname='m12_mis', db=None, idv=None, parent=None):
        super(autoDialog, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        if not db:
            self.accept()
        self.close = True  # εάν το κουμπί αποθήκευση κλείνει και τη φόρμα
        self.showSaveUpdateMessages = False
        self.table = tname
        wtitle = valFromTableOrDefault(tname,
                                       "SELECT tbp FROM ztbl WHERE tbn=?",
                                       zdb)
        self.setWindowTitle(wtitle)
        self.db = db
        self.id = idv
        self.lb = []
        self.od = OrderedDict()
        self.layout = QtGui.QGridLayout()
        bsave = QtGui.QPushButton(u'Αποθήκευση')
        self.bquit = QtGui.QPushButton(u'Επιστροφή χωρίς αποθήκευση')
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.bquit)
        buttonLayout.addItem(QtGui.QSpacerItem(20,
                                               60,
                                               QtGui.QSizePolicy.Minimum,
                                               QtGui.QSizePolicy.Expanding))
        buttonLayout.addWidget(bsave)
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(self.layout)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
        bsave.clicked.connect(self.updateOrInsert)
        self.bquit.clicked.connect(self.reject)
        self.__makeControls()
        self.__populate()
        # self.sqls()

    def __makeControls(self):
        fields = parseDDL(self.table, self.db)
        fields.pop(0)  # αφαίρεση της στήλης του id
        for line in fields:
            typ = line['ctype']
            name = line['cname']
            req = line['requi']
            self.lb.append(line['lbl'])
            if typ == 'key':
                self.od[name] = fieldFactory(typ, [line['sqin'],
                                                   'parOff',
                                                   self.db,
                                                   name])
            else:
                self.od[name] = fieldFactory(typ, isRequired=req)
        i = 0
        for key in self.od:
            try:
                self.layout.addWidget(QtGui.QLabel(self.lb[i]), i, 0)
            except:
                pass
            self.layout.addWidget(self.od[key], i, 1)
            i += 1

    def __populate(self):
        if not self.id:  # Εάν δεν έχει τιμή το id επιστρέφουμε ...
            return None
        # Πρώτα απ'όλα βρίσκουμε την εγγραφή
        rowVal = getDbOneRow(self.selectSQL(), self.db)
        i = 0
        if rowVal:
            for key in self.od:
                self.od[key].setValue(rowVal[i])
                i += 1

    def __areDataValid(self):
        errorLog = ''
        i = 0
        for key in self.od:
            if self.od[key].getValue() is None:
                errorLog += u'Το πεδίο %s δεν έχει σωστή τιμή\n' % self.lb[i]
            i += 1
        if errorLog:
            QtGui.QMessageBox.warning(self, u'Προσοχή υπάρχουν λάθη', errorLog)
            return False
        return True

    def updateOrInsert(self):
        if not self.__areDataValid():
            return  # Τα μυνήματα θα μας τα δώσει η συνάρτηση self.validation

        if self.id:
            sql, sqlp = self.updateSQL()
            # make update Here
        else:
            sql, sqlp = self.insertSQL()
            # Make insert Here
        insNo = commitToDb(sql, sqlp, self.db)
        if insNo:
            addLogToDb(u'Αποθήκευση στον πίνακα %s νέαςεγγραφής No: %s' % (self.table,insNo),self.db)
        else:
            addLogToDb(u'Ενημέρωση στον πίνακα %s εγγραφής No: %s' % (self.table,self.id),self.db)
        if self.showSaveUpdateMessages:
            if insNo:
                QtGui.QMessageBox.warning(self,
                                          u'Όλα Καλά',
                                          u'Η εγγραφή αποθηκευτηκε με αριθμό : %s' % insNo)
            else:
                QtGui.QMessageBox.warning(self,
                                          u'Όλα Καλά',
                                          u'Η εγγραφή με αριθμό : %s Ενημερώθηκε' % self.id)
        if self.close:
            self.accept()

    def insertSQL(self):
        str1 = "INSERT INTO %s (" % self.table
        str2 = "("
        sqlp = []
        for key in self.od:
            str1 += "%s," % key
            # str2 += "'%s'," % self.od[key].getValue()
            str2 += "?,"  # % self.od[key].getValue()
            sqlp.append('%s' % self.od[key].getValue())
        str1 = str1[:-1] + ") VALUES "
        str2 = str2[:-1] + ')'
        sqlInsert = str1 + str2
        return sqlInsert, sqlp

    def updateSQL(self):
        sqlUpdate = "UPDATE %s SET " % self.table
        sqlp = []
        for key in self.od:
            sqlUpdate += "%s=?," % key
            sqlp.append('%s' % self.od[key].getValue())
        sqlUpdate = sqlUpdate[:-1] + ' '
        sqlUpdate += "WHERE id=%s" % self.id
        return sqlUpdate, sqlp

    def selectSQL(self):
        sqlSelect = "SELECT "
        for key in self.od:
            sqlSelect += "%s," % key
        sqlSelect = sqlSelect[:-1] + ' '
        sqlSelect += "FROM %s " % self.table
        sqlSelect += "WHERE id=%s" % self.id
        return sqlSelect

    def sqls(self):
        print self.selectSQL()
        print self.insertSQL()
        print self.updateSQL()

    def canAdd(self):
        self.close = False
        self.bquit.setVisible(False)
        return False


class ftableData(QtGui.QDialog):
    '''
    Form returning search values
    sql: search sql
    db : Current DB
    insTbl : 0 for no insert button, 1 for insert button
    parent:
    inPanel: If True extra QLabel ,no save button
    '''
    def __init__(self, tbl, db, parent=None, inPanel=False):
        super(ftableData, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.db = db
        self.tbl = tbl
        self.parent = parent
        self.selSQL = getDbSingleVal("SELECT tsql FROM ztbl WHERE tbn=?",
                                     (self.tbl,),
                                     zdb)
        if not self.selSQL:
            self.selSQL = 'SELECT * FROM %s' % self.tbl
        self.colwidths = []  # colwidths
        self.table = QtGui.QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(tblStyle)
        self.table.setSortingEnabled(True)
        layout = QtGui.QVBoxLayout()
        wtitle = valFromTableOrDefault(self.tbl,
                                       "SELECT tbpm FROM ztbl WHERE tbn=?",
                                       zdb)
        if inPanel:
            title = QtGui.QLabel(wtitle)
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            title.setFont(font)
            title.setStyleSheet("color: rgb(0, 0, 127);")
            layout.addWidget(makeTitle(wtitle))
        layout.addWidget(self.table)
        if not inPanel:
            self.newEggr = QtGui.QPushButton(u'Νέα εγγραφή')
            layout.addWidget(self.newEggr)
            self.newEggr.clicked.connect(self.newRecord)
        self.setLayout(layout)
        self.setWindowTitle(wtitle)
        self.setMinimumSize(400, 200)
        self.populateTable()
        self.connect(self.table,
                     QtCore.SIGNAL("cellDoubleClicked(int, int)"),
                     self.openForEdit)
        self.array = []

    def newRecord(self):
        frm = autoDialog(self.tbl, self.db, parent=self)
        if frm.exec_() == QtGui.QDialog.Accepted:
            self.populateTable()

    def keyPressEvent(self, ev):
        '''
        use enter or return for fast selection nad form close ...
        '''
        if (ev.key() == QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            self.sendVals(self.table.currentRow(), self.table.currentColumn())
        QtGui.QDialog.keyPressEvent(self, ev)

    def val(self):
        return self.array

    def openForEdit(self, x, y):
        frm = autoDialog(self.tbl,
                         self.db,
                         self.table.item(x,0).text(),
                         parent=self)
        if frm.exec_() == QtGui.QDialog.Accepted:
            self.populateTable()

    def populateTable(self):
        lines, colHeaders = getDbRows(self.selSQL, self.db)
        populateTableWidget(self.table, lines, getLabels(colHeaders))

    def canAdd(self):
        return True


class fsqlData(QtGui.QDialog):
    '''
    Form returning search values
    sql: search sql
    db : Current DB
    insTbl : 0 for no insert button, 1 for insert button
    parent:
    inPanel: If True extra QLabel ,no save button
    '''
    def __init__(self, sql, db, parent=None, inPanel=False, wtitle='Δοκιμή'):
        super(fsqlData, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.db = db
        self.sql = sql
        self.parent = parent
        self.colwidths = []  # colwidths
        self.table = QtGui.QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(tblStyle)
        self.table.setSortingEnabled(True)
        layout = QtGui.QVBoxLayout()
        if inPanel:
            layout.addWidget(makeTitle(wtitle))
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle(wtitle)
        self.setMinimumSize(400, 200)
        self.populateTable()
        self.array = []

    def newRecord(self):
        frm = autoDialog(self.tbl, self.db, parent=self)
        if frm.exec_() == QtGui.QDialog.Accepted:
            self.populateTable()

    def keyPressEvent(self, ev):
        '''
        use enter or return for fast selection nad form close ...
        '''
        if (ev.key() == QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            self.sendVals(self.table.currentRow(), self.table.currentColumn())
        QtGui.QDialog.keyPressEvent(self, ev)

    def val(self):
        return self.array

    def openForEdit(self, x, y):
        frm = autoDialog(self.tbl,
                         self.db,
                         self.table.item(x, 0).text(),
                         parent=self)
        if frm.exec_() == QtGui.QDialog.Accepted:
            self.populateTable()

    def populateTable(self):
        lines, colHeaders = getDbRows(self.sql,
                                      self.db)
        populateTableWidget(self.table, lines, getLabels(colHeaders))

    def canAdd(self):
        return False


class fmasterDetail(QtGui.QDialog):
    '''
    '''
    def __init__(self, tblm, tbld, db, parent=None):
        QtGui.QDialog.__init__(self)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.tblm = tblm
        self.tbld = tbld
        self.db = db
        sqlm = getDbSingleVal("SELECT tsql FROM ztbl WHERE tbn=?",
                              (self.tblm,), zdb)
        if sqlm:
            self.sqlm = sqlm
        else:
            self.sqlm = "SELECT * FROM %s" % self.tblm

        self.qtblm = QtGui.QTableWidget()
        self.qtblm.setAlternatingRowColors(True)
        self.qtblm.setStyleSheet(tblStyle)
        self.qtbld = QtGui.QTableWidget()
        self.qtbld.setAlternatingRowColors(True)
        self.qtbld.setStyleSheet(tblStyle)
        layout = QtGui.QVBoxLayout()
        splitter = QtGui.QSplitter()
        splitter.setOrientation(QtCore.Qt.Vertical)
        splitter.addWidget(self.qtblm)
        splitter.addWidget(self.qtbld)
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.popTables(self.qtblm, self.sqlm)
        self.connect(self.qtblm,
                     QtCore.SIGNAL("currentCellChanged(int, int,int,int)"),
                     self.updateQtbld)

    def popTables(self, qtable, sql):
        lines, colHeaders = getDbRows(sql, self.db)
        populateTableWidget(qtable, lines, getLabels(colHeaders))

    def updateQtbld(self, x, y, a, b):
        qtblmKeyValue = self.qtblm.item(x, 0).text()
        sqlv = getDbSingleVal("SELECT tsql FROM ztbl WHERE tbn=?",
                              (self.tbld,), zdb)
        fkey = '%s_id' % self.tblm
        if sqlv:
            sqld = sqlv + ' ' + ("WHERE %s='%s'" % (fkey, qtblmKeyValue))
        else:
            sqld = "SELECT * FROM %s WHERE %s='%s'" % (self.tbld,
                                                       fkey, qtblmKeyValue)
        self.popTables(self.qtbld, sqld)

    def canAdd(self):
        return False


class fmain(QtGui.QDialog):
    def __init__(self, db, parent=None):
        super(fmain, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.db = db
        self.setWindowTitle('Db : %s' % self.db)
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        self.qtbl = QtGui.QTableWidget()
        self.qtbl.verticalHeader().setVisible(False)
        self.qtbl.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.qtbl.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.qtbl.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.qtbl)
        self.setLayout(layout)
        lines, heads = getDbRows(sql, self.db)
        lines.sort()
        populateTableWidget(self.qtbl, lines, getLabels(heads))

        self.connect(self.qtbl,
                     QtCore.SIGNAL("cellDoubleClicked(int, int)"),
                     self.openForEdit)

    def openForEdit(self, x, y):
        tabl = str(self.qtbl.item(x, 0).text())
        frm = ftableData(tabl, self.db, self)
        frm.show()


class fwizzard(QtGui.QDialog):
    def __init__(self, parent=None):
        super(fwizzard, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.f = {}
        vlay = QtGui.QVBoxLayout()  # vertical layout - main
        blay = QtGui.QHBoxLayout()  # Button Horizontal layout
        self.stackw = QtGui.QStackedWidget()
        vlay.addWidget(self.stackw)
        self.bprin = QtGui.QPushButton(u'Προηγούμενο')
        self.bmeta = QtGui.QPushButton(u'Επόμενο')
        self.bfin = QtGui.QPushButton(u'Ολοκλήρωση')
        self.bprin.clicked.connect(self.prin)
        self.bmeta.clicked.connect(self.meta)
        self.bfin.clicked.connect(self.fin)
        blay.addWidget(self.bprin)
        blay.addWidget(self.bmeta)
        blay.addWidget(self.bfin)
        vlay.addLayout(blay)
        self.setLayout(vlay)
        # self.stackw.addWidget(QtGui.QWidget())
        self.exStatus()

    def exStatus(self):
        if self.stackw.currentIndex() > 0:
            self.bprin.setEnabled(True)
        else:
            self.bprin.setEnabled(False)
        if self.stackw.currentIndex() == self.stackw.count()-1:
            self.bmeta.setEnabled(False)
        else:
            self.bmeta.setEnabled(True)
        if self.stackw.currentIndex() == self.stackw.count()-1:
            self.bfin.setEnabled(True)
        else:
            self.bfin.setEnabled(False)

    def addOnStack(self, dlg=None):
        self.stackw.addWidget(dlg)
        self.exStatus()

    def prin(self):
        '''
        Function to go back to previus stack
        '''
        self.stackw.setCurrentIndex(self.stackw.currentIndex()-1)
        print self.stackw.count(), self.stackw.currentIndex()
        self.exStatus()

    def meta(self):
        '''
        Function to go back to previus stack
        '''
        self.stackw.setCurrentIndex(self.stackw.currentIndex()+1)
        print self.stackw.count(), self.stackw.currentIndex()
        self.exStatus()

    def fin(self):
        self.accept()


def testfMain(db):
    import sys
    sql = 'SELECT es.id,es.dat from es'
    app = QtGui.QApplication([])
    dlg = fwizzard()
    df = QtGui.QWidget()
    df2 = QtGui.QWidget()
    dlg.addOnStack(df)
    dlg.addOnStack(df2)
    dlg.show()
    sys.exit(app.exec_())


def testmasterDetail(db):
    import sys
    app = QtGui.QApplication([])
    dlg = fmasterDetail('es', 'esd', db)
    dlg.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    testfMain('tst.sql3')
    # executeScript(sql, 'skata.sql3')
    # testmasterDetail('tst.sql3')
    # print sha1OfFile('tsts.sql3')
    # print checkVat('105909732')
