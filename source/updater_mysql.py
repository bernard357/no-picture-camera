import datetime
import logging
import MySQLdb as msql

class MysqlUpdater(object):
    """
    Updates a database
    """

    def __init__(self, settings={}):
        """
        Sets updater settings

        :param settings: the parameters for this updater
        :type settings: ``dict``

        """

        self.settings = settings

    def use_database(self):
        """
        Opens a database
        """

        pass

    def reset_database(self):
        """
        Recreates a database
        """

        pass

    def push(self, data):
        """
        Pushes one update to the database

        :param data: new record, e.g., "camera42 5 2 2"
        :type data: ``str``

        """

        try:
            logging.debug("connecting to SQL store")

            db = msql.connect(host=self.settings.get('host', 'localhost'),
                              user=self.settings.get('user', 'root'),
                              passwd=self.settings.get('password', 'root'),
                              db=self.settings.get('database', 'smart-video-counter'),
                              connect_timeout=2)
            cursor = db.cursor()

            sql_insert = ( 'INSERT INTO `{}`'
                           ' (`id`,'
                           '  `sender`,'
                           '  `time_stamp`,'
                           '  `standing`,'
                           '  `moves`,'
                           '  `faces`)'
                           ' VALUES'
                           ' (NULL,'
                           '  %s,'
                           '  %s,'
                           '  %s,'
                           '  %s,'
                           '  %s)' )

            items = data.split(' ')
            while len(items) < 4:
                items.append('0')

            cursor.execute(sql_insert,
                           (items[0],
                            datetime.datetime.utcnow(),
                            int(items[1]),
                            int(items[2]),
                            int(items[3]) ) )

            db.commit()
            cursor.close()

            logging.debug("SQL store has been updated")

        except Exception as feedback:
            logging.warning("Warning: SQL store could not be updated")
            logging.error(str(feedback))
