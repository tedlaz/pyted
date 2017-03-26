import sys
from cx_Freeze import setup, Executable

application_title = "es-ex"
main_python_file = "ee.py"

base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ["atexit", "re"]

setup(name=application_title,
      version="0.1",
      escription="Sample cx_Freeze PyQt4 script",
      options={"build_exe": {"includes": includes}},
      executables=[Executable(main_python_file, base=base)]
      )
