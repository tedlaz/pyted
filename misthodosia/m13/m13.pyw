import sip
sip.setapi(u'QDate', 2)
sip.setapi(u'QDateTime', 2)
sip.setapi(u'QString', 2)
sip.setapi(u'QTextStream', 2)
sip.setapi(u'QTime', 2)
sip.setapi(u'QUrl', 2)
sip.setapi(u'QVariant', 2)
if __name__ == "__main__":
    from PyQt4 import QtGui
    from f_main import fMain
    import sys
    import os

    if '__file__' in globals():
        path = os.path.dirname(os.path.abspath(__file__))
    elif hasattr(sys, 'frozen'):
        path = os.path.dirname(os.path.abspath(sys.executable))  # for py2exe
    else:  # should never happen
        path = os.getcwd()

    os.chdir(path)
    sys.path = [path] + [p for p in sys.path if not p == path]

    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("orgName")
    app.setOrganizationDomain("orgDomain")
    app.setApplicationName("appName")
    myApp = fMain()
    if len(sys.argv) > 1:
        dbase = sys.argv[1]
        myApp.fileFromCommandLine(dbase)
    myApp.show()
    sys.exit(app.exec_())
