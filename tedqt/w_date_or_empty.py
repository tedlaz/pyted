# -*- coding: utf-8 -*-

import PyQt5.QtCore as Qc
import PyQt5.QtWidgets as Qw
from tedqt import parameters as par

MSG_RESET_DATE = u'right mouse click sets Date to empty string'


class Date_or_empty(Qw.QToolButton):

    '''
    Date or empty string values
    '''

    def __init__(self, val=None, parent=None):
        super().__init__(parent)
        self.setPopupMode(Qw.QToolButton.MenuButtonPopup)
        self.setMenu(Qw.QMenu(self))
        self.cal = Qw.QCalendarWidget()
        self.action = Qw.QWidgetAction(self)
        self.action.setDefaultWidget(self.cal)
        self.menu().addAction(self.action)
        self.cal.clicked.connect(self.menuCalendar)
        self.setSizePolicy(Qw.QSizePolicy.Expanding, Qw.QSizePolicy.Fixed)
        self.setToolTip(MSG_RESET_DATE)
        self.setMinimumHeight(par.MIN_HEIGHT)
        self.set(val)

    def mousePressEvent(self, event):
        if event.button() == Qc.Qt.RightButton:
            self.setText('')
            self.cal.setSelectedDate(Qc.QDate.currentDate())
        else:
            Qw.QToolButton.mousePressEvent(self, event)

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
        qd = Qc.QDate()
        qd.setDate(int(y), int(m), int(d))
        self.cal.setSelectedDate(qd)

    def get(self):
        if len(self.text()) == 0:
            return ''
        d, m, y = self.text().split('/')
        qd = Qc.QDate()
        qd.setDate(int(y), int(m), int(d))
        return '%s' % qd.toString(par.SQLITE_DATE_FORMAT)
