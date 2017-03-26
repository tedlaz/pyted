# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
import parameters as par


class Date(QtGui.QDateEdit):

    '''
    Date values for most cases
    '''

    def __init__(self, parent, val=None):
        super(Date, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.set(val)

        self.setCalendarPopup(True)
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
        # get function
        return '%s' % self.date().toString(par.SQLITE_DATE_FORMAT)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dlg = Date(None, '1963-02-10')
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
