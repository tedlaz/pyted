from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='ted17',
      version='0.1',
      description='Useful widgets and functions for pyqt development',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Licence :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: PyQt :: Gui',
      ],
      keywords='PyQt Gui',
      url='http://users.otenet.gr/~o6gnvw',
      author='Ted Lazaros',
      author_email='tedlaz@gmail.com',
      license='MIT',
      packages=['ted17'],
      install_requires=[
          'PyQt5',

      ],
      include_package_data=True,
      zip_safe=False)
