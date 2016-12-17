import socket
import sys
import os
import logging
import socket
import datetime
import config

# uncomment only one
#
logging.basicConfig(format='%(message)s', level=logging.INFO)
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# get data from socket and process it
#
import uds

# push data to file
#
try:
    settings = config.log

    logging.debug("loading log updater")
    from updater_log import LogUpdater
    updater = LogUpdater(settings)

    uds.add(updater.push)

except AttributeError:
    logging.debug("no configuration for log")

# push data to the sql database
#
try:
    settings = config.mysql

    logging.debug("loading MySQL updater")
    from updater_mysql import MysqlUpdater
    updater = MysqlUpdater(settings)
    updater.use_database()

    uds.add(updater.push)

except AttributeError:
    logging.debug("no configuration for MySQL")

# push data to influx database
#
try:
    settings = config.influxdb

    logging.debug("loading InfluxDB updater")
    from updater_influx import InfluxdbUpdater
    updater = InfluxdbUpdater(settings)
    updater.use_database()

    uds.add(updater.push)

except AttributeError:
    logging.debug("no configuration for InfluxDB")

# perpetual loop to receive data and trigger all updaters
#
uds.process()
