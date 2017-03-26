# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class Text(QtGui.QTextEdit):

    """
    Text field
    """

    def __init__(self, pin, parent=None):
        super(Text, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.parent = parent

        self.isreq = pin.get('isRequired', False)
        self.set(pin.get('val', None))

    def set(self, txt):
        if txt:
            ttxt = '%s' % txt
            self.setText(ttxt.strip())
        else:
            self.setText('')

    def get(self):
        tmpval = '%s' % self.toPlainText().replace("'", "''")
        return tmpval.strip()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dlg = Text({'val': 'This is a text box multiline with some special properties. '
               'It just works out of the box'})
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
