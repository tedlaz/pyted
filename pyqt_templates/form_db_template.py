'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''
from PyQt5 import QtGui as Qg
from PyQt5 import QtCore as Qc
from PyQt5 import QtWidgets as Qw
import sqlite3


def select(dbf, sql):
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


def script(db, sql):
    '''
    sql   : A set of sql commands (create, insert or update)
    '''
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.executescript(sql)
        con.commit()
    except sqlite3.Error as sqe:
        con.rollback()
        cur.close()
        con.close()
        return False
    cur.close()
    con.close()
    return True


class FormTemplate(Qw.QDialog):
    '''Απλή φόρμα για δοκιμή
    '''
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
        if  self._id:
            sql = "SELECT * FROM %s WHERE id='%s'" % (self._table, self._id)
        else:
            sql = "SELECT * FROM %s limit 0" % self._table
        self.fields, self.data = select(self._db, sql)
        self.labels = self.fields
        flayout = Qw.QFormLayout()
        self.mainlayout.addLayout(flayout)
        self.widgets = {}
        # Add fields to form
        for i, fld in enumerate(self.fields):
            self.widgets[fld] = Qw.QLineEdit()
            flayout.insertRow(i, Qw.QLabel(self.labels[i]),
                              self.widgets[fld])
            if fld in self.data:  # if not None or empty string
                if self.data[fld]:
                    self.widgets[fld].setText('%s' % self.data[fld])
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
                vals.append("'%s'" % self.widgets[wid].text())
            fsql = sqli % (self._table, ','.join(vals))
        else:
            data_for_update = self.get_data_from_form(True)
            if len(data_for_update) == 1:
                return None
            for fld in self.get_data_from_form(True):
                if fld == 'id':
                    continue
                vals.append("%s='%s'" % (fld, self.widgets[fld].text()))
            fsql = sqlu % (self._table, ','.join(vals), self._id)
        script(self._db, fsql)
        print(fsql)
        self.accept()

    def get_data_from_form(self, only_changed=False):
        '''Get data from the form. Assume id already exists.
        '''
        if 'id' in self.data:
            dtmp = {'id': self.data['id']}
        else:
            dtmp = {'id': ''}
        for field in self.widgets:
            if only_changed:
                if self.data[field] != self.widgets[field].text():
                    dtmp[field] = self.widgets[field].text()
            else:
                dtmp[field] = self.widgets[field].text()
        return dtmp

    def is_dirty(self):
        '''Check if any value changed by user'''
        startv = {}
        for field in self.data:
            startv[field] = self.data[field]
        if startv == self.get_data_from_form():
            return False
        else:
            return True


if __name__ == '__main__':
    import sys
    dbf1 = "/home/tedlaz/test"
    app = Qw.QApplication([])
    dialog = FormTemplate(dbf1, 'pel', 2)
    dialog.show()
    appex = app.exec_()
    sys.exit(appex)
