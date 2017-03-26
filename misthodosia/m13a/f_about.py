# -*- coding: utf-8 -*-
'''
Created on ${date}

@author: ${user}
'''
from PyQt4 import QtGui,QtCore,Qt
import sys, os

class WigglyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WigglyWidget, self).__init__(parent)

        self.setBackgroundRole(QtGui.QPalette.Midlight)
        self.setAutoFillBackground(True)

        newFont = self.font()
        newFont.setPointSize(newFont.pointSize() + 20)
        self.setFont(newFont)

        self.timer = QtCore.QBasicTimer()
        self.text = ''

        self.step = 0;
        self.timer.start(60, self)   
        self.setText(u'Μισθοδοσία M13')
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
htmlVal = u'''
<b>Μ13 Έκδοση : 0.1</b><br/>
<br/> Δημιουργήθηκε από τον Θεόδωρο Λάζαρο</a>.
<br/><br/>Άδεια χρήσης  :  <a href=\"http://www.gnu.org/licenses/gpl.html\"> GPL 3</a>
<br/><br/>Για περισσότερες πληροφορίες :
<br/><a href=\"http://users.otenet.gr/~o6gnvw/\">Ted Lazaros Pages</a>
'''            
class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.setupGui()
        self.makeConnections()
        self.setWindowTitle(u"Πρόγραμμα μισθοδοσίας Μ13 ...")
        
    def setupGui(self):
        
        gfile = '%s/%s' %(sys.path[0],'m13.gif')
        self.movie = WigglyWidget()
        #self.setGeometry(100, 100, size.width(), size.height())
        self.txt = QtGui.QTextBrowser()
        self.txt.setHtml(htmlVal)
        self.txt.setOpenExternalLinks(True)
        self.txt.setFrameShape(QtGui.QFrame.NoFrame)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.movie)
        layout.addWidget(self.txt)
        self.setLayout(layout)
        self.setMinimumSize(400, 300)
        
    def makeConnections(self):
        pass
        
    def show1(self):
        #dlg.dlg(parent=self).show
        pass
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()