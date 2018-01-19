"""Main Form Here"""
import sys
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg


class MainWindow(Qw.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    mainform = MainWindow()
    mainform.show()
    sys.exit(app.exec_())
