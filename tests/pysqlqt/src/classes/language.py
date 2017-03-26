"""
 @file
 @brief This file loads the current language based on the computer's
        locale settings
 @author Ted Lazaros <tedlaz@gmail.com>

 @section LICENSE

 """

import os
from PyQt4 import QtCore
from classes.logger import log
from classes import info


def init_language():
    """ Find the current locale, and install the correct translators """

    # Get app instance
    app = QtCore.QCoreApplication.instance()

    # Setup of our list of translators and paths
    translator_types = (
        {"type": 'QT',
         "pattern": 'qt_%s',
         "path": QtCore.QLibraryInfo.location(
             QtCore.QLibraryInfo.TranslationsPath)},
        {"type": 'MyApp',
         "pattern": os.path.join('%s', 'LC_MESSAGES', 'MyApp'),
         "path": os.path.join(info.PATH, 'locale')},
    )

    # Determine the environment locale, or default to system locale name
    locale_names = [os.environ.get('LANG', QtCore.QLocale().system().name()),
                    os.environ.get('LOCALE', QtCore.QLocale().system().name())]

    # Output all system languages detected
    log.info("Qt Detected Languages: {}".format(
        QtCore.QLocale().system().uiLanguages()))
    log.info("LANG Environment Variable: {}".format(
        os.environ.get('LANG', QtCore.QLocale().system().name())))
    log.info("LOCALE Environment Variable: {}".format(
        os.environ.get('LOCALE', QtCore.QLocale().system().name())))

    # Loop through environment variables
    found_language = False
    for locale_name in locale_names:
        # Don't try on default locale,
        # since it fails to load what is the default language
        if 'en_US' in locale_name:
            log.info("Skipping English language : {}".format(locale_name))
            continue

        # Go through each translator and try to add for current locale
        for type in translator_types:
            trans = QtCore.QTranslator(app)
            if find_language_match(type["pattern"],
                                   type["path"],
                                   trans,
                                   locale_name):
                # Install translation
                app.installTranslator(trans)
                found_language = True

        # Exit if found language
        if found_language:
            log.info("Exiting translation system (since we successfully loaded: {})".format(locale_name))
            break


# Try the full locale and base locale trying to find a valid path
#  returns True when a match was found.
#  pattern - a string expected to have one pipe to be filled by locale strings
#  path - base path for file (pattern may contain more path)
#
def find_language_match(pattern, path, translator, locale_name):
    """ Match all combinations of locale, language, and country """

    success = False
    locale_parts = locale_name.split('_')

    i = len(locale_parts)
    while not success and i > 0:
        formatted_name = pattern % "_".join(locale_parts[:i])
        log.info('Attempting to load {} in \'{}\''.format(formatted_name, path))
        success = translator.load(formatted_name, path)
        if success:
            log.info('Successfully loaded {} in \'{}\''.format(formatted_name, path))
        i -= 1

    return success
