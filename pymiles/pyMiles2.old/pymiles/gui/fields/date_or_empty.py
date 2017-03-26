# -*- coding: utf-8 -*-


from PyQt4 import QtGui, Qt
import parameters as par

MSG_RESET_DATE = u'right mouse click sets Date to empty string'


class Date_or_empty(QtGui.QToolButton):

    '''
    Date or empty string values
    '''

    def __init__(self, parent, val=None):

        super(Date_or_empty, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.set(val)

        self.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.setMenu(QtGui.QMenu(self))
        # Control is Dark .Something to do to correct it
        self.cal = QtGui.QCalendarWidget()
        self.action = QtGui.QWidgetAction(self)
        self.action.setDefaultWidget(self.cal)
        self.menu().addAction(self.action)
        self.cal.clicked.connect(self.menuCalendar)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Fixed)
        self.setToolTip(MSG_RESET_DATE)
        self.setMinimumHeight(par.MIN_HEIGHT)

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.RightButton:
            self.setText('')
        else:
            QtGui.QToolButton.mousePressEvent(self, event)

    def menuCalendar(self):
        self.setText(self.cal.selectedDate().toString(par.GREEK_DATE_FORMAT))
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
    dlg = Date_or_empty(None, '2014-10-13')
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
