from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='ted17',
      version='0.2',
      description='Useful widgets and functions for pyqt development',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      platforms='any',
      keywords='PyQt Gui',
      url='http://tsated.mooo.com/ted17',
      author='Ted Lazaros',
      author_email='tedlaz@gmail.com',
      license='MIT',
      packages=['ted17'],
      install_requires=[
          'PyQt5',
      ],
      include_package_data=True,
      zip_safe=False)
