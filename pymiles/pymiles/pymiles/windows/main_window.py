import os
from PyQt5.QtWidgets import QMainWindow
from utils import info
from utils import ui_util
# from utils.logger import log


class MainWindow(QMainWindow):
    """ This class contains the logic for the main window widget """

    # Path to ui file
    ui_path = os.path.join(info.PATH, 'windows', 'ui', 'tmain.ui')

    def __init__(self):

        QMainWindow.__init__(self)

        ui_util.load_ui(self, self.ui_path)

    def updateStatusChanged(self, undo_status, redo_status):
        pass
