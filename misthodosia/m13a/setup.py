from distutils.core import setup
import py2exe
import os.path
applicationName = "m13"
packages = ['f_newEmployeeWizard','utils','utils_qt','report_table']
mydata = [('',['dnewDb.sql','ddoy.txt','dika.txt','osyk.zip']),
          ('plugins',['plugins/pro.py','plugins/co.py','plugins/fpr.py'])]
setup(
    windows=[{"script":'%s.pyw' % applicationName ,'icon_resources':[(1,'%s.ico' % applicationName)]}],
    data_files = mydata,
    options={
        "py2exe" : {
            "includes" : ["sip",],
            "packages" : packages,
            'dist_dir' : 'C:/m13a_releases',
        },
        "build" : { 'build_base': 'C:/m13a_releases/build' }
    }
)
