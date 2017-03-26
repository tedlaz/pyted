"""
 @file
 @brief This file loads and saves settings
 @author Ted Lazaros <tedlaz@gmail.com>

 @section LICENSE

 """

# SettingStore - class which allows getting/storing of settings,
# loading and saving to json
import os
from PyQt4 import QtCore
from classes.logger import log
from classes import info
from classes.json_data import JsonDataStore


def get_settings():
    """ Get the current QApplication's settings instance """
    return QtCore.QCoreApplication.instance().settings


class SettingStore(JsonDataStore):
    """This class only allows setting pre-existing keys taken from default
       settings file, and merges user settings on load, assumes default OS dir.
    """

    def __init__(self):
        JsonDataStore.__init__(self)
        # Set the data type name for logging clarity
        # (base class functions use this variable)
        self.data_type = "user settings"
        self.settings_filename = "myapp.settings"
        fname = os.path.join(info.PATH, 'settings', '_default.settings')
        self.default_settings_filename = fname

    def get_all_settings(self):
        """ Get the entire list of settings (with all metadata) """
        return self._data

    def set(self, key, value):
        """
        Store setting, but adding isn't allowed. All possible settings
        must be in default settings file.
        """
        key = key.lower()

        # Load user setting's values (for easy merging)
        user_values = {}
        for item in self._data:
            if "setting" in item and "value" in item:
                user_values[item["setting"].lower()] = item

        # Save setting
        if key in user_values:
            user_values[key]["value"] = value
        else:
            log.warn("{} key '{}' not valid. Those are valid: {}".format(
                self.data_type, key, list(self._data.keys())))

    def load(self):
        """
        Load user settings file from disk, merging with allowed settings
        in default settings file. Creates user settings if missing.
        """

        # Default and user settings objects
        default_settings, user_settings = {}, {}

        # try to load default settings,
        # on failure will raise exception to caller
        default_settings = self.read_from_file(self.default_settings_filename)

        # Try to find user settings file
        file_path = QStandardPaths.locate(
            QStandardPaths.ConfigLocation, self.settings_filename)

        # If user settings file doesn't exist yet,
        # try to create a default settings file
        if not file_path:
            writable_path = QStandardPaths.writableLocation(
                QStandardPaths.ConfigLocation)

            # Create folder if not found
            if not os.path.exists(writable_path.encode('UTF-8')):
                try:
                    os.mkdir(writable_path)
                except Exception as ex:
                    msg = ("Couldn't create {} folder for app:\n{}\n{}".format(
                        self.data_type, writable_path, ex))
                    log.error(msg)
                    raise Exception(msg)

            # Set path to user settings file (will be created below)
            file_path = os.path.join(writable_path, self.settings_filename)

        # File was found, try to load settings
        else:
            # Will raise exception to caller on failure to read
            user_settings = self.read_from_file(file_path)

        # Merge default and user settings, excluding settings not in default,
        # Save settings
        self._data = self.merge_settings(default_settings, user_settings)

        # Return success of saving user settings file back after merge
        return self.write_to_file(file_path, self._data)

    def save(self):
        """ Save user settings file to disk """

        # Try to find user settings file
        file_path = QStandardPaths.locate(
            QStandardPaths.ConfigLocation, self.settings_filename)

        # If user settings file doesn't exist yet, try to create a default settings file
        if not file_path:
            msg = ("Couldn't find {} file on save(). Load must create any missing {} file.".format(self.data_type, self.data_type))
            log.error(msg)
            raise Exception(msg)

        # try to save data to file, will raise exception on failure
        self.write_to_file(file_path, self._data)
