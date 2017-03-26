# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''
from PyQt4 import QtGui, QtCore, Qt
import u_db


def item(text, align='l'):
    '''
    Δημιουργία αντικειμένου tableWidgetItem
    text: το κείμενο που εμφανίζεται
    align: Στοίχιση του κειμένου (l = left, c = center, r = right)
    '''
    el = QtGui.QTableWidgetItem()
    el.setText('%s' % text)
    if align == 'r':
        el.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    elif align == 'c':
        el.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    else:
        el.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    return el


def itemb(text, align='l'):
    el = item(text, align)
    font = QtGui.QFont()
    font.setBold(True)
    font.setWeight(75)
    el.setFont(font)
    return el


def iteml(text, align='r', bold=True):
    if bold:
        el = itemb(text, align)
    else:
        el = item(text, align)

    el.setFlags(QtCore.Qt.ItemIsSelectable |
                QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsUserCheckable)
    return el


class Form_koinoxrista(QtGui.QDialog):

    '''
    Δημιουργία ενός φύλλου εργασίας για την εισαγωγή και διόρθωση
    των ποσοστών ανά διαμέρισμα - δαπάνη.
    '''

    def __init__(self, db, row_tbl, col_tbl, val_tbl, parent=None):
        super(Form_koinoxrista, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.setWindowTitle(u'Κατανομή Δαπανών σε χιλιοστά')
        self.setMinimumSize(800, 400)

        # Database metadata
        self.db = db
        self.row_tbl = row_tbl
        self.col_tbl = col_tbl
        self.val_tbl = val_tbl

        # Δημιουργία του grid
        self.tbl = QtGui.QTableWidget(self)

        # Δημιουργία γραμμής κουμπιών
        spacerItem = QtGui.QSpacerItem(40,
                                       20,
                                       QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Minimum)
        self.btadddi = QtGui.QPushButton(u'Νέο Διαμέρισμα', self)
        self.btaddej = QtGui.QPushButton(u'Νέο Έξοδο', self)
        self.btnsave = QtGui.QPushButton(u'Αποθήκευση', self)

        # layout κουμπιών
        buttonlayout = QtGui.QHBoxLayout()
        buttonlayout.addWidget(self.btadddi)
        buttonlayout.addWidget(self.btaddej)
        buttonlayout.addItem(spacerItem)
        buttonlayout.addWidget(self.btnsave)

        # Κεντρικό layout
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(self.tbl)
        mainlayout.addLayout(buttonlayout)
        self.setLayout(mainlayout)

        self.tbl.cellChanged.connect(self.cell_changed)
        self.btnsave.clicked.connect(self.on_btnsave)
        self.fill_tbl()

    def fill_tbl(self):
        # Δεδομένα από db
        self._diam = u_db.select_table(self.db, self.row_tbl)
        self._ej = u_db.select_table(self.db, self.col_tbl)
        self._vals = u_db.select_table(self.db, self.val_tbl)

        self.tbl.cellChanged.disconnect()
        n_ej = len(self._ej)  # Πλήθος κατηγοριών εξόδων
        n_diam = len(self._diam)  # Πλήθος διαμερισμάτων
        self.tbl.setColumnCount(n_ej)
        self.tbl.setRowCount(n_diam + 2)

        # Τίτλοι στηλών
        for i, ej in enumerate(self._ej):
            self.tbl.setHorizontalHeaderItem(i, item(self._ej[i]['ej'], 'c'))

        # Τίτλοι γραμμών
        for i, diam in enumerate(self._diam):
            self.tbl.setVerticalHeaderItem(i, item(self._diam[i]['dia'], 'l'))
        self.tbl.setVerticalHeaderItem(n_diam, itemb(u'Σύνολο', 'c'))
        self.tbl.setVerticalHeaderItem(n_diam + 1, itemb(u'Υπόλοιπο', 'c'))

        # Αρχικοποίηση δεδομένων πίνακα με μηδενικές τιμές
        for i in range(n_diam):
            for j in range(n_ej):
                self.tbl.setItem(i, j, item('0', 'r'))
        for i in range(n_diam, n_diam + 2):
            for j in range(n_ej):
                self.tbl.setItem(i, j, iteml('0'))

        # Σύνδεση του event μετά από την αρχικοποίηση εδώ
        # έτσι ώστε οι τιμές που εισάγονται παρακάτω να αθροίζονται αυτόματα
        self.tbl.cellChanged.connect(self.cell_changed)

        for val in self._vals:
            row = self.find_row(val['dia_id'])
            col = self.find_col(val['ej_id'])
            if int(val['val']) == 0:
                continue
            if (row is not None) and (col is not None):
                self.tbl.setItem(row, col, item('%s' % val['val'], 'r'))

    def on_btnsave(self):
        fvals = []  # List of dictionaries
        n_ej = len(self._ej)  # Πλήθος κατηγοριών εξόδων
        n_diam = len(self._diam)  # Πλήθος διαμερισμάτων
        for i in range(n_diam):
            for j in range(n_ej):
                val = int(self.tbl.item(i, j).text())
                # if val == 0:
                #     continue
                id = 0
                did = self._diam[i]['id']
                eid = self._ej[j]['id']
                # Έλεγχος εάν υπήρχε από πρίν αυτό το κελί και εάν ναι
                # του δίνουμε το παλίο id έτσι ώστε το σύστημα να κάνει
                # update σε κελιά με id > 0 και insert σε κελιά με id = 0
                flag_idia_timi = False
                for el in self._vals:
                    if did == el['dia_id']:
                        if eid == el['ej_id']:
                            if val == el['val']:
                                flag_idia_timi = True
                            id = el['id']
                            break
                # Για να μην αποθηκεύω συνεχώς κελιά που δεν έχει αλλάξει
                # η τιμή τους χρησιμοποιώ αυτό εδώ το flag
                if flag_idia_timi:
                    flag_idia_timi = False
                else:
                    dic = {'id': id, 'dia_id': did, 'ej_id': eid, 'val': val}
                    fvals.append(dic)
        save_result = u_db.save_many(self.db, self.val_tbl, fvals)

        if len(fvals) == 0:
            QtGui.QMessageBox.about(self, u'Οκ', u'Είναι ήδη αποθηκευμένα ...')
        elif save_result:
            self.fill_tbl()
            QtGui.QMessageBox.about(self, u'Εντάξει', u'Έγινε αποθήκευση ...')

    def cell_changed(self, row, col):
        if row < len(self._diam) and col < len(self._ej):
            self.sum_column(col)

    def sum_column(self, column_number):
        len_diam = len(self._diam)
        total = 0
        if column_number > self.tbl.columnCount() - 1:
            return
        for i in range(len_diam):
            total += int(self.tbl.item(i, column_number).text())
        self.tbl.setItem(len_diam, column_number, iteml('%s' % total))
        self.tbl.setItem(len_diam + 1, column_number, iteml('%s' % (1000 - total)))

    def find_row(self, id):
        for i, diam in enumerate(self._diam):
            if id == diam['id']:
                return i
        return None

    def find_col(self, id):
        for i, ej in enumerate(self._ej):
            if id == ej['id']:
                return i
        return None


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dialog = Form_koinoxrista('tst.sql3', 'dia', 'ej', 'dapx')
    dialog.show()
    appex = app.exec_()
    sys.exit(appex)
