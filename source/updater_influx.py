import datetime
import logging
from influxdb import InfluxDBClient


class InfluxdbUpdater(object):
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
        Opens a database to save data
        """

        logging.info("using InfluxDB database")

        self.db = InfluxDBClient(
            self.settings.get('host', 'localhost'),
            self.settings.get('port', 8086),
            self.settings.get('user', 'root'),
            self.settings.get('password', 'root'),
            self.settings.get('database', 'smart-video-counter'),
            )
        self.db.create_database(self.settings.get('database', 'smart-counter'))
        return self.db

    def reset_database(self):
        """
        Opens a database for points
        """

        logging.info("resetting InfluxDB database")

        self.db = InfluxDBClient(
            self.settings.get('host', 'localhost'),
            self.settings.get('port', 8086),
            self.settings.get('user', 'root'),
            self.settings.get('password', 'root'),
            self.settings.get('database', 'smart-video-counter'),
            )
        self.db.drop_database(self.settings.get('database', 'smart-counter'))
        self.db.create_database(self.settings.get('database', 'smart-counter'))
        return self.db

    def push(self, data):
        """
        Pushes one update to the database

        :param data: new record, e.g., "camera42 5 2 2"
        :type data: ``str``

        """

        logging.debug("updating InfluxDB database")

        items = data.split(' ')
        while len(items) < 4:
            items.append('0')

        measurement = {
                "measurement": 'smart-counter',
                "tags": {
                    "sender": items[0],
                },
                "time": datetime.datetime.utcnow(),
                "fields": {
                    "standing": int(items[1]),
                    "moves": int(items[2]),
                    "faces": int(items[3]),
                }
            }

        logging.debug(measurement)

        self.db.write_points([measurement])
