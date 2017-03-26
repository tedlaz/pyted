from distutils.core import setup
import py2exe
import os.path
'''
packages=[
    'reportlab',
    'reportlab.graphics.charts',
    'reportlab.graphics.samples',
    'reportlab.graphics.widgets',
    'reportlab.graphics.barcode',
    'reportlab.graphics',
    'reportlab.lib',
    'reportlab.pdfbase',
    'reportlab.pdfgen',
    'reportlab.platypus',
]

mydata = [('',['mispar.sql3','newDb.sql']),('osyk',['osyk/osyk.zip','ika.txt','doy.txt'])]

'''
mydata = [('',['newDb.sql',]),('osyk',['osyk/osyk.zip','osyk/ika.txt','osyk/doy.txt'])]
setup(
    windows=[{"script":"m13.pyw",'icon_resources':[(1,'m13.ico')]}],
    data_files = mydata,
    options={
        "py2exe" : {
            "includes" : ["sip",],
            #"packages" : packages,
            'dist_dir' : 'C:/m13_releases',
        },
        "build" : { 'build_base': 'C:/m13_releases/build' }
    }
)
'''
zipfil = 'C:/m13_releases/library.zip'
import zipfile
zf = zipfile.ZipFile(zipfil,'a')

zf.write('reportl/Alkaios.ttf')
zf.write('reportl/Alkaios-Bold.ttf')
zf.write('reportl/Alkaios-BoldItalic.ttf')
zf.write('reportl/Alkaios-Italic.ttf')
zf.close()
'''