# -*- coding: utf-8 -*-
"""Updater module"""
import logging
import requests
import time

import config

# uncomment only one
#
logging.basicConfig(format='%(message)s', level=logging.INFO)
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def use_database(updater):
    """Wait for server to be ready"""
    attempts = 0
    while True:
        try:
            updater.use_database()
            break
        except:
            attempts += 1
            if attempts > 5:
                raise
            time.sleep(10)

# get data from socket and process it
#
import uds

# push data to file
#
try:
    settings = config.log

    logging.debug('loading log updater')
    from updater_log import LogUpdater
    updater = LogUpdater(settings)

    uds.add(updater.push)

except AttributeError:
    logging.debug('no configuration for log')

# push data to the sql database
#
try:
    settings = config.mysql

    logging.debug('loading MySQL updater')
    from updater_mysql import MysqlUpdater
    updater = MysqlUpdater(settings)

    use_database(updater)

    uds.add(updater.push)

except AttributeError:
    logging.debug('no configuration for MySQL')

# except ConnectionError:
#    logging.error("could not connect to MySQL server")

# push data to influx database
#
try:
    settings = config.influxdb

    logging.debug('loading InfluxDB updater')
    from updater_influx import InfluxdbUpdater
    updater = InfluxdbUpdater(settings)

    use_database(updater)

    uds.add(updater.push)

except AttributeError:
    logging.debug('no configuration for InfluxDB')

except requests.exceptions.ConnectionError:
    logging.error('could not connect to InfluxDB server')

# perpetual loop to receive data and trigger all updaters
#
uds.process()
