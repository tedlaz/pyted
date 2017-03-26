# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
import fld__parameters as par
SQLITE_DATE_FORMAT = 'yyyy-MM-dd'
GREEK_DATE_FORMAT = 'dd/MM/yyyy'


class Date(QtGui.QDateEdit):

    '''
    Date values for most cases
    '''

    def __init__(self, pin, parent=None):
        super(Date, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.parent = parent

        self.setCalendarPopup(True)
        self.set(pin.get('val', None))
        self.setDisplayFormat("d/M/yyyy")
        self.setMinimumHeight(par.MIN_HEIGHT)
        # self.setMaximumWidth(par.DATE_MAX_WIDTH)
        self.setMinimumWidth(par.DATE_MAX_WIDTH)
        self.setMaximumHeight(par.MAX_HEIGHT)

    def set(self, sqliteDate):
        if sqliteDate:
            if len(sqliteDate) > 10:
                sqliteDate = sqliteDate[:10]
            yr, mn, dt = sqliteDate.split('-')
            qd = QtCore.QDate()
            qd.setDate(int(yr), int(mn), int(dt))
            self.setDate(qd)
        else:
            self.setDate(QtCore.QDate.currentDate())

    def get(self):
        return '%s' % self.date().toString(SQLITE_DATE_FORMAT)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dlg = Date({'val': None})
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
