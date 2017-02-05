# -*- coding: utf-8 -*-
"""
This modules amis at testing an 'updater'
"""
import logging
import random
import time
import config

# uncomment only one
#
logging.basicConfig(format='%(message)s', level=logging.INFO)
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# load camera configuration
#
try:
    settings = config.camera

except:
    settings = {}

# transmit updates via Unix Domain Socket
#
import uds

# send some fake measurements
#
counter = 0
while counter < 50:
    counter += 1

    # build a random update: <camera_id> <standing> <moves> <faces>
    #
    message = '%s %d %d %d' % (settings.get('id', 'camera42'),
                               random.randint(0, 10),
                               random.randint(0, 3),
                               random.randint(0, 3))
    uds.push(message)

    # wait a bit
    #
    logging.debug('sleeping')
    time.sleep(2)
