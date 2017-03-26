
import os
import platform
from uuid import uuid4
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QPalette, QColor, QFontDatabase, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR

from utils.logger import log
from utils import info, settings, project_data, updates, language, ui_util


def get_app():
    """ Returns the current QApplication instance of OpenShot """
    return QApplication.instance()


class PyMilesApp(QApplication):
    """ This class is the primary QApplication for OpenShot """

    def __init__(self, *args):
        QApplication.__init__(self, *args)

        # Log some basic system info
        try:
            log.info("openshot-qt version: %s" % info.VERSION)
            log.info("platform: %s" % platform.platform())
            log.info("processor: %s" % platform.processor())
            log.info("machine: %s" % platform.machine())
            log.info("python version: %s" % platform.python_version())
            log.info("qt5 version: %s" % QT_VERSION_STR)
            log.info("pyqt5 version: %s" % PYQT_VERSION_STR)
        except:
            pass

        # Setup appication
        self.setApplicationName('pymiles')
        self.setApplicationVersion(info.SETUP['version'])

        # Init settings
        self.settings = settings.SettingStore()
        try:
            self.settings.load()
        except Exception as ex:
            log.error("Couldn't load user settings. Exiting.\n{}".format(ex))
            exit()

        # Init translation system
        language.init_language()

        # Tests of project data loading/saving
        self.project = project_data.ProjectDataStore()

        # Init Update Manager
        self.updates = updates.UpdateManager()

        # It is important that the project is the first listener
        # if the key gets update
        self.updates.add_listener(self.project)

        # Load ui theme if not set by OS
        ui_util.load_theme()

        # Track which dockable window received a context menu
        self.context_menu_object = None

        # Set unique install id (if blank)
        if not self.settings.get("unique_install_id"):
            self.settings.set("unique_install_id", str(uuid4()))

            # Track 1st launch metric
            # import utils.metrics
            # classes.metrics.track_metric_screen("initial-launch-screen")

        # Set Font for any theme
        if self.settings.get("theme") != "No Theme":
            # Load embedded font
            try:
                fnt = os.path.join(info.IMAGES_PATH, "fonts", "Ubuntu-R.ttf")
                log.info("Setting font to %s" % fnt)
                font_id = QFontDatabase.addApplicationFont(fnt)
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                font = QFont(font_family)
                font.setPointSizeF(10.5)
                QApplication.setFont(font)
            except Exception as ex:
                log.error("Error setting Ubuntu-R.ttf QFont: %s" % str(ex))

        # Set Experimental Dark Theme
        if self.settings.get("theme") == "Humanity: Dark":
            # Only set if dark theme selected
            log.info("Setting custom dark theme")
            self.setStyle(QStyleFactory.create("Fusion"))

            darkPalette = self.palette()
            darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
            darkPalette.setColor(QPalette.WindowText, Qt.white)
            darkPalette.setColor(QPalette.Base, QColor(25, 25, 25))
            darkPalette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
            darkPalette.setColor(QPalette.ToolTipText, Qt.white)
            darkPalette.setColor(QPalette.Text, Qt.white)
            darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
            darkPalette.setColor(QPalette.ButtonText, Qt.white)
            darkPalette.setColor(QPalette.BrightText, Qt.red)
            darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            darkPalette.setColor(QPalette.HighlightedText, Qt.black)
            darkPalette.setColor(QPalette.Disabled,
                                 QPalette.Text,
                                 QColor(104, 104, 104))
            self.setPalette(darkPalette)
            sts = 'QToolTip { color: #ffffff; '
            sts += 'background-color: #2a82da; '
            sts += 'border: 0px solid white; }'
            self.setStyleSheet(sts)

        # Create main window
        from windows.main_window import MainWindow
        self.window = MainWindow()
        self.window.show()

        log.info('Process command-line arguments: %s' % args)
        if len(args[0]) == 2:
            path = args[0][1]
            if ".osp" in path:
                # Auto load project passed as argument
                self.window.open_project(path)
            else:
                # Auto import media file
                self.window.filesTreeView.add_file(path)

        # Reset undo/redo history
        self.updates.reset()
        self.window.updateStatusChanged(False, False)

    def _tr(self, message):
        return self.translate("", message)

    # Start event loop
    def run(self):
        """ Start the primary Qt event loop for the interface """

        res = self.exec_()

        try:
            self.settings.save()
        except Exception as ex:
            log.error("Couldn't save user settings on exit.\n{}".format(ex))

        # return exit result
        return res
