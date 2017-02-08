# -*- coding: utf-8 -*-
"""Standard log module"""
import logging
import os


class LogUpdater(object):
    """
    Updates a logging facility
    """

    def __init__(self, settings=None):
        """
        Sets updater settings

        :param settings: the parameters for this updater
        :type settings: ``dict``

        """
        if settings is None:
            settings = {}
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
            mode = 'a' if os.path.exists(self.file) else 'w'
            with open(self.file, mode) as handle:
                handle.truncate()

        except IOError:
            logging.debug('could not truncate log file')

    def push(self, data):
        """
        Pushes one update to the database

        :param data: new record, e.g., "camera42 5 2 2"
        :type data: ``str``
        """
        try:
            logging.debug('logging into %s', self.file)
            mode = 'a' if os.path.exists(self.file) else 'w'
            with open(self.file, mode) as handle:
                handle.write(data + '\n')

        except IOError:
            logging.debug('could not update log file')
