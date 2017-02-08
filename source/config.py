# -*- coding: utf-8 -*-
"""
This module contains the configuration of the smart video counter.
"""
#
# each camera should have a different name -- do not put space characters
#

camera = {
    'id': 'camera01',
}

#
# log updater -- put all measurements in a local file
#
# this should be used only for tests, and commented out for production
#

log = {
    'file': './smart-video-counter.log',
}

#
# sql updater -- uncomment and edit if you have a MySQL database
#

# mysql = {
#    'host': 'localhost',
#    'user': 'root',
#    'password': 'root',
#    'database': 'smart-video-counter',
#    }

#
# influxdb updater -- uncomment and edit if you have an influxdb server
#

# influxdb = {
#    'host': 'localhost',
#    'port': 8086,
#    'user': 'root',
#    'password': 'root',
#    'database': 'smart-video-counter',
#    }
