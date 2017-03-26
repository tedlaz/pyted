del /q c:\m13_releases\.
md c:\m13_releases\build
python setup.py py2exe
rd /s /q c:\m13_releases\build
setup.iss