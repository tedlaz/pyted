import sys
import os
import subprocess
from PyQt5 import QtCore as Qc
from PyQt5 import QtGui as Qg
from PyQt5 import QtWidgets as Qw
from PyQt5 import QtWebKitWidgets as Qwkit


class Fwget(Qw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        vlayout = Qw.QVBoxLayout(self)
        url_layout = Qw.QHBoxLayout()

        self.url = Qw.QLineEdit(self)
        self.burl = Qw.QToolButton(self)
        self.burl.setArrowType(Qc.Qt.DownArrow)
        url_layout.addWidget(self.url)
        url_layout.addWidget(self.burl)
        vlayout.addLayout(url_layout)
        # Webkit
        self.web = Qwkit.QWebView(self)
        self.web.setUrl(Qc.QUrl("http://users.otenet.gr/~o6gnvw"))
        vlayout.addWidget(self.web)
        sp1 = Qw.QSpacerItem(20, 10, Qw.QSizePolicy.Minimum,
                             Qw.QSizePolicy.Minimum)
        vlayout.addItem(sp1)
        # Path layout
        path_layout = Qw.QHBoxLayout()
        vlayout.addLayout(path_layout)
        path_layout.addWidget(Qw.QLabel('Save Path :'))
        self.save_path = Qw.QLineEdit(self)
        self.save_path.setText('/home/tedlaz/Downloads/dpython')

        path_layout.addWidget(self.save_path)
        self.bpath = Qw.QToolButton(self)
        self.bpath.setText('...')
        path_layout.addWidget(self.bpath)

        ext_layout = Qw.QHBoxLayout()
        vlayout.addLayout(ext_layout)
        ext_layout.addWidget(Qw.QLabel('extensions :'))
        self.extensions = Qw.QLineEdit(self)
        self.extensions.setText('mp4,pdf')
        ext_layout.addWidget(self.extensions)

        button_layout = Qw.QHBoxLayout()
        vlayout.addLayout(button_layout)
        sp2 = Qw.QSpacerItem(40, 20, Qw.QSizePolicy.Expanding,
                             Qw.QSizePolicy.Minimum)
        button_layout.addItem(sp2)
        self.bexec = Qw.QPushButton('Save files', self)
        button_layout.addWidget(self.bexec)
        # Connections
        self.burl.clicked.connect(self.update_web)
        self.bpath.clicked.connect(self.update_path)
        self.bexec.clicked.connect(self.execute)
        self.web.urlChanged.connect(self.update_url)

    def update_path(self):
        old = self.save_path.text()
        opt = Qw.QFileDialog.DontResolveSymlinks | Qw.QFileDialog.ShowDirsOnly
        path = Qw.QFileDialog.getExistingDirectory(self, 'path', old, opt)
        if path:
            self.save_path.setText(path)

    def execute(self):
        url = self.url.text()
        save_path = self.save_path.text()
        ext = self.extensions.text()
        os.chdir(save_path)
        # print(subprocess.run(["ls", "-l"], stdout=subprocess.PIPE))
        # wget -A <filetype> -m -p -E -k -K -np <path to files>
        par = ['wget', '-A', ext, '-m', '-p', '-E', '-k', '-K', '-np', url]
        # print(' '.join(par))
        print(subprocess.run(par, stdout=subprocess.PIPE))

    def update_web(self):
        self.web.setUrl(Qc.QUrl(self.url.text()))

    def update_url(self):
        self.url.setText(self.web.url().toString())


if __name__ == '__main__':

    app = Qw.QApplication(sys.argv)
    ui = Fwget()
    ui.show()
    appex = app.exec_()
    sys.exit(appex)




