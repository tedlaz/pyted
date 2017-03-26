#!/usr/bin/python
# *- coding: utf-8 -*
'''
Created on 3 Mar 2013

@author: ted lazaros
'''

from PyQt4 import QtGui, Qt
import qt_table_report as tr


class testprn1(QtGui.QDialog):
    def __init__(self, parent=None):
        super(testprn1, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        f ={'orientation': 0,
            'pdfName': 'test.pdf',
            'fontFamily': 'Helvetica', #'Alkaios',
            'ReportHeader1': u'Report Header 1',
            'ReportHeader2': u'Report Header 2',
            'ReportHeader3': u'Report Header 3',
            'headerLabels': [u'head1', u'sf', u'head2', u'head3', u'head4 is bigger'],
            'footerLine': False,
            'footerText': u'This is page footer',
            'footerPageNumberText': u'Page',
            'data': [[u'Test Data', 10.34, u'INV334', '2015-01-01', 1245.2],
                     [u'Line2 Data with lots of data inside for testing purposes', 2.4, u'INV431', '2015-04-18', 22340.25]] * 1000
            }

        self.rep = tr.qtTableReport(f)
        tstButton = QtGui.QPushButton('test')
        tstButton.clicked.connect(self.onClick)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(tstButton)
        self.setLayout(layout)

    def onClick(self):
        self.rep.printPreview()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = testprn1()
    window.show()
    app.exec_()
