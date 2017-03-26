# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from ui_fmeta_tables import Ui_Fmeta_tables


class Dialog(QtGui.QDialog, Ui_Fmeta_tables):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Dialog()
    print(window.__dict__)
    window.show()
    sys.exit(app.exec_())
