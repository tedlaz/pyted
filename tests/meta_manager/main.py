# -*- coding: utf-8 -*-
import sys
import os
from PyQt4 import QtGui
from ui_fmeta_main import Ui_MainWindow
from ui_fmeta_tables import Ui_Fmeta_tables


class Dialog(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.dbname = ""

        self.tbls = Ui_Fmeta_tables()
        self.tbls.setupUi(self.tab_tables)
        # self.tbls.tblname.setText('sdsdf')
        self.create_actions()

    def open_db(self):
        pass

    def create_actions(self):
        self.actionNew.activated.connect(self.new_db)
        self.actionOpen.activated.connect(self.file_open)
        self.tbls.new_table.clicked.connect(self.to_do)
        self.tbls.save.clicked.connect(self.to_do)

    def file_open(self):
        fname = QtGui.QFileDialog.getOpenFileName(
            self,
            u'Επιλογή Αρχείου',
            self.dbname,
            u"Αρχείο (*.sql3)")
        if fname:
            self.dbname = str(fname)
            self.setWindowTitle("Meta Manager : %s" % self.dbname)

    def new_db(self):
        from sqlmeta import make_new_db
        fname = QtGui.QFileDialog.getSaveFileName(
            self,
            u"Δημιουργία Νέου αρχείου",
            os.path.dirname('filename'),
            u"Αρχείο (*.sql3)")
        if not fname:
            return
        if '.sql3' not in fname:
            fname = '%s.sql3' % fname
        fname = str(fname)  # Be sure it is always python string
        result = make_new_db(fname)
        if result:
            self.dbname = str(fname)
            self.setWindowTitle("Meta Manager : %s" % self.dbname)

    def to_do(self):
        QtGui.QMessageBox.about(
            self,
            u"Υπό κατασκευή",
            u"Η εφαρμογή <b>M13</b> είναι "
            u"υπό κατασκευή<br>"
            u"Η ενέργεια που επιλέξατε "
            u"δεν έχει υλοποιηθεί ακόμη.")

app = QtGui.QApplication(sys.argv)
window = Dialog()
print(dir(window.tbls))
window.show()
sys.exit(app.exec_())
