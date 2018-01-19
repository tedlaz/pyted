import PyQt5.QtWidgets as Qw
from tedutil.qt import AutoForm


if __name__ == '__main__':
    import sys
    dbf = '/home/tedlaz/prj/pyted/2018/tedutil/aa.sql3'
    app = Qw.QApplication(sys.argv)
    ui = AutoForm(dbf, 'ergazomenos', 2)
    ui.show()
    appex = app.exec_()
    sys.exit(appex)