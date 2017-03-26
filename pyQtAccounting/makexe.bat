rd /s /q dist
python c:\Python27\pyinst151\Makespec.py -w qmain.pyw
python c:\Python27\pyinst151\Build.py qmain.spec
rd /s /q build
copy Alkaios*.* .\dist\qmain\