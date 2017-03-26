import sys
import os
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
from PyQt5.QtWidgets import QAction as Qa
from tedutil import db
import res
import qisozygio
import qedit
import qlmo
import logging


logger = logging.getLogger()
EXT = 'aba'  # SQlite file extension
APP_ID = 20170313  # Aplication specific id


def readFromRes(resname):
    f = Qc.QFile(resname)
    if f.open(Qc.QFile.ReadOnly | Qc.QFile.Text):
        stream = Qc.QTextStream(f)
        stream.setCodec('utf-8')
        vstr = u''
        while not stream.atEnd():
            vstr += u'%s\n' % stream.readLine().__str__()
    f.close()
    return vstr


class Main(Qw.QMainWindow):
    signal_updated = Qc.pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.settings.setValue("dbf", 'This is a test')
        # self.settings.setValue("epo", 'Kala κρασιά')
        # print(self.settings.value("epo", defaultValue=Qc.QVariant('')))
        self._ui()
        self._get_settings()
        self._actions_menus_toolbars()

    def _get_settings(self, dbval=None):
        """
        Here we load application settings and database
        """
        self.settings = Qc.QSettings()
        if dbval:  # if open or new file
            self.settings.setValue("dbf", dbval)  # first we save to conf
        tempdbf = self.settings.value("dbf", defaultValue=Qc.QVariant(''))
        if db.app_id(tempdbf) == APP_ID:  # Check if database has proper appid
            self.dbf = tempdbf
            # self.stack.addWidget(qisozygio.Fisozygio(self.dbf, self))
        else:
            self.dbf = ''
            self.settings.setValue("dbf", '')
            self.stack_reset()
        self.onoma = u'Αβάκιο 2016 (%s)' % self.dbf
        self.setWindowTitle(self.onoma)

    def _todo(self):
        """
        A default todo message box useful during active development
        """
        title = u"Υπό κατασκευή"
        txt = (u"Η εφαρμογή <b>%s</b> είναι υπό κατασκευή<br>"
               u"Η ενέργεια που επιλέξατε δεν έχει υλοποιηθεί ακόμη.")
        Qw.QMessageBox.about(self, title, txt % self.onoma)

    def ma(self, name, per, tip):
        """
        Make Action
        name : The name of the action. Here we make the assumption that
               the action name is the same with the icon name
        per : Description of the action
        tip : Status tip of the action
        """
        icn = Qg.QIcon(':/images/%s.png' % name)
        self.actions[name] = Qa(icn, per, self, statusTip=tip)

    def _ui(self):
        """
        Create user interface here
        """
        frame = Qw.QFrame(self)
        self.setCentralWidget(frame)
        mlay = Qw.QHBoxLayout(frame)
        # Here we define the stack widget !!!
        self.stack = Qw.QStackedWidget()
        mlay.addWidget(self.stack)
        # Set Status Bar
        self.statusbar = Qw.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        # Set Minimum Size
        self.setMinimumSize(600, 150)

    def _actions_menus_toolbars(self):
        self.actions = {}
        self.ma('open', u"Άνοιγμα αρχείου", u"Άνοιγμα υπάρχοντος αρχείου")
        self.ma('new', u"Νέo αρχείο", u"Δημιουργία νέου αρχείου")
        self.ma('exit', u'Έξοδος', u'Τερματισμός λειτουργίας')
        self.ma('isoz', u"Ισοζύγιο", u"Ισοζύγιο λογαριασμών")
        self.ma('add', u"Νέα εγγραφή", u"Νέα εγγραφή")
        self.ma('nacc', u"Νέoς Λογαριασμός", u"Νέος Λογαριασμός λογιστικής")
        # Create Menus
        self.fileMenu = self.menuBar().addMenu(u"&Αρχείο")
        self.fileMenu.addAction(self.actions['open'])
        self.fileMenu.addAction(self.actions['new'])
        self.fileMenu.addAction(self.actions['exit'])
        # Create Toolbars
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.actions['open'])
        self.fileToolBar.addAction(self.actions['new'])
        self.dbtoolbar = self.addToolBar('Database')
        self.dbtoolbar.addAction(self.actions['isoz'])
        self.dbtoolbar.addAction(self.actions['add'])
        self.dbtoolbar.addAction(self.actions['nacc'])
        # Action triggers
        self.actions['open'].triggered.connect(self._open)
        self.actions['new'].triggered.connect(self._new)
        self.actions['exit'].triggered.connect(self.close)
        self.actions['isoz'].triggered.connect(self.isozygio)
        self.actions['add'].triggered.connect(self.add)
        self.actions['nacc'].triggered.connect(self.new_acc)

    def stack_status(self):
        if self.stack.count() > 1:
            pass
        else:
            pass

    def stack_reset(self):
        no = self.stack.count()
        for i in range(no):
            forRemoval = self.stack.currentWidget()
            self.stack.removeWidget(forRemoval)
            forRemoval.setParent(None)
        self.stack_status()

    def add(self):
        pass

    def back(self):
        '''
        Function to go back to previus stack
        '''
        if self.stack.count() > 1:
            forRemoval = self.stack.currentWidget()
            self.stack.removeWidget(forRemoval)
            forRemoval.setParent(None)
            # forRemoval.Delete()
            self.stack_status()
            # self.setwinTitle()

    def isozygio(self):
        qis = qisozygio.Fisozygio(self.dbf, self)
        self.signal_updated.connect(qis.slot_updated)
        qis.show()

    def add(self):
        fedit = qedit.Fedit(self.dbf, parent=self)
        fedit.signal_updated.connect(self.slot_updated)
        fedit.show()

    def new_acc(self):
        fedit = qlmo.Fedit(self.dbf, parent=self)
        fedit.show()

    def _open(self):
        fname = Qw.QFileDialog.getOpenFileName(self,
                                               u'Επιλογή Αρχείου',
                                               self.dbf,
                                               u"%s (*.%s)" % (EXT, EXT))
        if len(fname[0]) > 3:
            self._get_settings(fname[0])

    def _new(self):
        titl = u'Νέο αρχείο'
        path = os.path.dirname(self.dbf)
        ext = u"%s (*.%s)" % (EXT, EXT)
        fname = Qw.QFileDialog.getSaveFileName(self, titl, path, ext)
        sql = readFromRes(':create.sql')
        if len(fname[0]) > 3:
            strfname = fname[0]
            ext = '.%s' % EXT
            if not strfname.endswith(ext):
                strfname += ext
            db.execute_script(strfname, sql)
            self._get_settings(strfname)

    @Qc.pyqtSlot()
    def slot_updated(self):
        self.signal_updated.emit()

if __name__ == "__main__":
    # initialize logger here
    # logging levels are : DEBUG, INFO, WARNING, ERROR, CRITICAL
    logging.basicConfig(level=logging.ERROR)
    logger.debug('Here starts application')
    app = Qw.QApplication(sys.argv)
    app.setOrganizationName('NT')
    app.setOrganizationDomain('NT_Domain')
    app.setApplicationName('abakion')
    myApp = Main()
    myApp.show()
    sys.exit(app.exec_())
