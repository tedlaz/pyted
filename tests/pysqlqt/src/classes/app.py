"""
 @file
 @brief This file creates the QApplication, and displays the main window
 @author Ted Lazaros <tedlaz@gmail.com>

 @section LICENSE
 """
from PyQt4 import QtGui
from classes.logger import log
from classes import info
from classes import settings
from classes import language
from gui.main_window import Main_window


def get_app():
    """ Returns the current QApplication instance of MyApp """
    return QtGui.QApplication.instance()


class Qmain(QtGui.QApplication):
    """ This class is the primary QApplication for MyApp """

    def __init__(self, *args):
        QtGui.QApplication.__init__(self, *args)

        # Setup appication
        self.setApplicationName('myapp')
        self.setApplicationVersion('1.0.0')
        self.setWindowIcon(QtGui.QIcon(":/images/app.png"))

        # Init settings
        '''
        self.settings = settings.SettingStore()
        try:
            self.settings.load()
        except Exception as ex:
            log.error("Couldn't load user settings. Exiting.\n{}".format(ex))
            exit()

        # Init translation system
        language.init_language()
        '''
        # Tests of project data loading/saving
        # self.project = project_data.ProjectDataStore()

        # Init Update Manager
        # self.updates = updates.UpdateManager()

        # It is important that the project is the first listener
        # if the key gets update
        # self.updates.add_listener(self.project)

        # Load ui theme if not set by OS
        # ui_util.load_theme()

        # Track which dockable window received a context menu
        self.context_menu_object = None

        # Create main window

        self.window = Main_window()
        self.window.show()

    def _tr(self, message):
        return self.translate("", message)

    # Start event loop
    def run(self):
        """ Start the primary Qt event loop for the interface """

        res = self.exec_()
        '''
        try:
            self.settings.save()
        except Exception as ex:
            log.error("Couldn't save user settings on exit.\n{}".format(ex))
        '''
        # return exit result
        return res
