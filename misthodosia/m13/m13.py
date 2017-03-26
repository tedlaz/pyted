#!/usr/bin/env python
#-*- coding:utf-8 -*-
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
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("orgName")
    app.setOrganizationDomain("orgDomain")
    app.setApplicationName("appName")
    myApp = fMain()
    if len(sys.argv) > 1:
        dbase=sys.argv[1]
        myApp.fileFromCommandLine(dbase)
    myApp.show()
    sys.exit(app.exec_())