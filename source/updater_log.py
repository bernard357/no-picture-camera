import datetime
import logging
import os


class LogUpdater(object):
    """
    Updates a logging facility
    """

    def __init__(self, settings={}):
        """
        Sets updater settings

        :param settings: the parameters for this updater
        :type settings: ``dict``

        """

        self.settings = settings
        self.file = settings.get('file', './smart-video-counter.log')

    def use_database(self):
        """
        Opens a database to save data
        """

        pass

    def reset_database(self):
        """
        Opens a database for points
        """

        try:
            if os.path.exists(self.file):
                mode = 'a'
            else:
                mode = 'w'

            with open(self.file, mode) as handle:
                handle.truncate()

        except:
            logging.debug("could not truncate log file")

    def push(self, data):
        """
        Pushes one update to the database

        :param data: new record, e.g., "camera42 5 2 2"
        :type data: ``str``

        """

        try:
            logging.debug("logging into {}".format(self.file))

            if os.path.exists(self.file):
                mode = 'a'
            else:
                mode = 'w'

            with open(self.file, mode) as handle:
                handle.write(data+'\n')

        except:
            logging.debug("could not update log file")
