# -*- coding: utf-8 -*-
'''
Created on ${date}

@author: ${user}
'''
from PyQt4 import QtGui,QtCore,Qt
import sys, os

class WigglyWidget(QtGui.QWidget):
    def __init__(self, txt,parent=None):
        super(WigglyWidget, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.setBackgroundRole(QtGui.QPalette.Midlight)
        self.setAutoFillBackground(True)

        newFont = self.font()
        newFont.setPointSize(newFont.pointSize() + 20)
        self.setFont(newFont)

        self.timer = QtCore.QBasicTimer()
        self.text = ''

        self.step = 0;
        self.timer.start(60, self)   
        self.setText(txt)
        self.setMinimumSize(200, 100)
        
    def paintEvent(self, event):
        sineTable = (0, 38, 71, 92, 100, 92, 71, 38, 0, -38, -71, -92, -100, -92, -71, -38)

        metrics = QtGui.QFontMetrics(self.font())
        x = (self.width() - metrics.width(self.text)) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        color = QtGui.QColor()

        painter = QtGui.QPainter(self)

        for i, ch in enumerate(self.text):
            index = (self.step + i) % 16
            color.setHsv((15 - index) * 16, 255, 191)
            painter.setPen(color)
            painter.drawText(x, y - ((sineTable[index] * metrics.height()) / 400), ch)
            x += metrics.width(ch)

    def setText(self, newText):
        self.text = newText

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.step += 1
            self.update()
        else:
            super(WigglyWidget, self).timerEvent(event)
          
class dlg(QtGui.QDialog):
    def __init__(self, txt, about, parent=None):
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.txt = txt
        self.about = about
        self.setupGui()
        self.makeConnections()
        self.setWindowTitle(u"Περί ...")
        
    def setupGui(self):
        self.movie = WigglyWidget(self.txt)
        #self.setGeometry(100, 100, size.width(), size.height())
        self.txt = QtGui.QTextBrowser()
        self.txt.setHtml(self.about)
        self.txt.setOpenExternalLinks(True)
        self.txt.setFrameShape(QtGui.QFrame.NoFrame)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.movie)
        layout.addWidget(self.txt)
        bok = QtGui.QPushButton(u'Εντάξει')
        bok.clicked.connect(self.accept)
        layout.addWidget(bok)
        self.setLayout(layout)
        self.setMinimumSize(400, 300)
        
    def makeConnections(self):
        pass
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()