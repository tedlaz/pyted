import sys
import os
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import qisozygio

cpath = os.path.dirname(os.path.abspath(__file__))
icn = os.path.join(cpath, 'tray.png')
DBPATH = '/home/tedlaz/pyted/tedaccounting/tst.db'


class SystemTrayIcon(Qw.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        Qw.QSystemTrayIcon.__init__(self, icon, parent)
        menu = Qw.QMenu(parent)
        a_db = menu.addAction('db:%s' % DBPATH)
        a_isoz = menu.addAction("Ισοζύγιο")
        a_exit = menu.addAction("Έξοδος")
        self.setContextMenu(menu)
        a_isoz.triggered.connect(self.isoz)
        a_exit.triggered.connect(self.exit)
        self.activated.connect(self.click1)

    def click1(self, val):
        if val == self.Trigger:
            zenu = Qw.QMenu()
            b_db = zenu.addAction('Αρχείο:%s' % DBPATH)
            b_isoz = zenu.addAction("Ισοζύγιο")
            zenu.addSeparator()
            b_exit = zenu.addAction("Έξοδος")
            b_isoz.triggered.connect(self.isoz)
            b_exit.triggered.connect(self.exit)
            zenu.exec_(Qg.QCursor.pos())

    def isoz(self):
        ui = qisozygio.Fisozygio(DBPATH)
        ui.exec_()

    def exit(self):
        Qc.QCoreApplication.exit()


def main():
    app = Qw.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    # wid = Qw.QWidget()
    trayicon = SystemTrayIcon(Qg.QIcon(icn))
    trayicon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
