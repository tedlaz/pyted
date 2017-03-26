import os

VERSION = "0.0.1"
DATE = "20160331000000"
NAME = "pymiles"
PRODUCT_NAME = "pymiles Database Application Generator"
GPL_VERSION = "3"
DESCRIPTION = "Generate Database Applications like msAccess"
COMPANY_NAME = "Ted Lazaros"
COPYRIGHT = "Copyright (c) 2005-2016 %s" % COMPANY_NAME
SUPPORTED_LANGUAGES = ["English", "Greek"]
CWD = os.getcwd()
PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # Primary openshot folder
HOME_PATH = os.path.join(os.path.expanduser("~"))
USER_PATH = os.path.join(HOME_PATH, ".pymiles")
BACKUP_PATH = os.path.join(USER_PATH, "backup")
THUMBNAIL_PATH = os.path.join(USER_PATH, "thumbnail")
CACHE_PATH = os.path.join(USER_PATH, "cache")
TITLE_PATH = os.path.join(USER_PATH, "title")
PROFILES_PATH = os.path.join(PATH, "profiles")
IMAGES_PATH = os.path.join(PATH, "images")
EXPORT_TESTS = os.path.join(USER_PATH, "tests")

# Create PATHS if they do not exist (this is where temp files are stored... such as cached thumbnails)
for folder in [USER_PATH, THUMBNAIL_PATH, CACHE_PATH, TITLE_PATH, PROFILES_PATH, IMAGES_PATH,
               EXPORT_TESTS, BACKUP_PATH]:
    if not os.path.exists(folder.encode("UTF-8")):
        os.makedirs(folder, exist_ok=True)

# names of all contributers, using "u" for unicode encoding
TL = {"name": u"Ted Lazaros", "email": "tedlaz@gmail.com", "website":"http://users.otenet.gr/~o6gnvw"}

# credits
CREDITS = {
    "code": [TL],
    "artwork": [TL],
    "documentation": [TL],
    "translation": [TL],
}

SETUP = {
    "name": NAME,
    "version": VERSION,
    "author": TL["name"] + " and others",
    "author_email": TL["email"],
    "maintainer": TL["name"],
    "maintainer_email": TL["email"],
    "url": "http://users.otenet.gr/~o6gnvw",
    "license": "GNU GPL v." + GPL_VERSION,
    "description": DESCRIPTION,
    "long_description": "Generate database applications\n"
                        " An easy to use database application generator.\n"
                        " Features include:\n"
                        "  * Auto form creation\n"
                        "  * Auto reporting\n"
                        "  * Time data analysis\n",

    # see http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "classifiers": [
                       "Development Status :: 3 - Alpha",
                       "Environment :: X11 Applications",
                       "Environment :: X11 Applications :: GTK",
                       "Intended Audience :: End Users/Desktop",
                       "License :: OSI Approved :: GNU General Public License (GPL)",
                       "Operating System :: OS Independent",
                       "Operating System :: POSIX :: Linux",
                       "Programming Language :: Python",
                       "Topic :: Artistic Software",
                       "Topic :: Multimedia :: Video :: Non-Linear Editor", ] +
                   ["Natural Language :: " + language for language in SUPPORTED_LANGUAGES],

    # Automatic launch script creation
    "entry_points": {
        "gui_scripts": [
            "pymiles = pymiles.launch:main"
        ]
    }
}
