import PyQt5.QtWidgets as Qw
from tedutil.qt import AutoForm


if __name__ == '__main__':
    import sys
    dbf = '/home/tedlaz/prj/django/src/db.sqlite3'
    app = Qw.QApplication(sys.argv)
    ui = AutoForm(dbf, 'mi_sex')
    ui.show()
    appex = app.exec_()
    sys.exit(appex)