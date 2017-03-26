# -*- coding: utf-8 -*-
'''
Created on Oct 13, 2014
@author: tedlaz
'''


from PyQt4 import QtGui, QtCore, Qt
import fld__parameters as par
SQLITE_DATE_FORMAT = 'yyyy-MM-dd'
GREEK_DATE_FORMAT = 'dd/MM/yyyy'
MSG_RESET_DATE = u'right mouse click sets Date to empty string'


class DateOrEmpty(QtGui.QToolButton):
    '''
    Date or empty string values
    '''
    def __init__(self, pin, parent=None):

        super(DateOrEmpty, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.parent = parent

        self.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.setMenu(QtGui.QMenu(self))
        # Control is Dark .Something to do to correct it
        self.cal = QtGui.QCalendarWidget()
        self.action = QtGui.QWidgetAction(self)
        self.action.setDefaultWidget(self.cal)
        self.menu().addAction(self.action)
        self.cal.clicked.connect(self.menuCalendar)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.setToolTip(MSG_RESET_DATE)
        self.set(pin.get('val', None))
        self.setMinimumHeight(par.MIN_HEIGHT)

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.RightButton:
            self.setText('')
        else:
            QtGui.QToolButton.mousePressEvent(self, event)

    def menuCalendar(self):
        self.setText(self.cal.selectedDate().toString(GREEK_DATE_FORMAT))
        self.menu().hide()

    def set(self, sqliteDate):
        if not sqliteDate:
            return
        if len(sqliteDate) == 0:
            return
        y, m, d = sqliteDate.split('-')
        self.setText('%s/%s/%s' % (d, m, y))

    def get(self):
        if len(self.text()) == 0:
            return ''
        d, m, y = self.text().split('/')
        return '%s-%s-%s' % (y, m, d)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dlg = DateOrEmpty({'val': '2014-10-13'})
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
