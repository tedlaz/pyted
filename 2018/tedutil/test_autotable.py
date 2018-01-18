import PyQt5.QtWidgets as Qw
from tedutil.qt import AutoFormTable


if __name__ == '__main__':
    import sys
    dbf = '/home/tedlaz/prj/django/src/db.sqlite3'
    app = Qw.QApplication(sys.argv)
    ui = AutoFormTable(dbf, 'mi_misthodosiatype')
    ui.show()
    # print(ui.id)
    appex = app.exec_()
    sys.exit(appex)