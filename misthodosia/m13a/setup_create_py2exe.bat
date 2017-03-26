del /q c:\m13a_releases\.
md c:\m13_releases\build
python setup.py py2exe
rd /s /q c:\m13a_releases\build
setup.iss
