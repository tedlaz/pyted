from distutils.core import setup

# python setup.py sdist --formats=gztar,zip

setup(name='pyMiles',
      version='1.0',
      license='GPL3',
      description='Database application generator',
      author='Ted Lazaros',
      author_email='tedlaz@gmail.com',
      packages=['pymiles',
                'pymiles.gui',
                'pymiles.gui.fields',
                'pymiles.gui.forms',
                'pymiles.sqlite',
                'pymiles.utils',
                'pymiles.tests'],
      data_files=[('', ['pymiles/tests/tst.sql3',
                        'pymiles/tests/app.meta'])],
      )
