"""
 @file
 @brief This file contains the current version number of MyApp, along with
        other global settings.
 @author Ted Lazaros <tedlaz@gmail.com>

 @section LICENSE
 """

import os

VERSION = "1.0.0"
DATE = "20150601100000"
NAME = 'myapp'
GPL_VERSION = '3'
SUPPORTED_LANGUAGES = ['Greek', 'English']
CWD = os.getcwd()
# Primary openshot folder
PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
print(PATH)
USER_PATH = os.path.join(os.path.expanduser("~"), ".myapp")
THUMBNAIL_PATH = os.path.join(USER_PATH, "thumbnail")

# Create PATHS if they do not exist
# (this is where temp files are stored... such as cached thumbnails)
for folder in [USER_PATH, THUMBNAIL_PATH]:
    if not os.path.exists(folder.encode('UTF-8')):
        os.makedirs(folder)

# names of all contributers, using 'u' for unicode encoding
TL = {'name': u'Ted Lazaros', 'email': 'tedlaz@gmail.com'}


# credits
CREDITS = {
    'code': [TL],
    'artwork': [TL],
    'documentation': [TL],
    'translation': [TL],
}

SETUP = {
    'name': NAME,
    'version': VERSION,
    'author': TL['name'] + ' and others',
    'author_email': TL['email'],
    'maintainer': TL['name'],
    'maintainer_email': TL['email'],
    'url': 'http://users.otenet.gr/~o6gnvw',
    'license': 'GNU GPL v.' + GPL_VERSION,
    'description': 'Not implemented yet',
    'long_description': "Not implemented yet",

    # see http://pypi.python.org/pypi?%3Aaction=list_classifiers
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Financial Software',
        'Topic :: Acounting :: Finacial :: pythonic', ] +
    ['Natural Language :: ' + language for language in SUPPORTED_LANGUAGES],
}
