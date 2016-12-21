# credit: https://pymotw.com/2/socket/uds.html

import socket
import sys
import time
import logging
import os

# use a socket file
#
handle = '/tmp/smart-video-counter-socket'
logging.debug('using %s' % handle)

# send data to outbound processing
#
def push(message=None):

    # sanity check
    #
    if message is None:
        message = 'test 0 0 0'

    logging.info("--> %s" % message)

    # use socket file
    #
    logging.debug('opening %s' % handle)
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(handle)
    except socket.error, feedback:
        logging.error(feedback)
        return

    # write data
    #
    try:

        logging.debug('sending "%s"' % message)
        sock.sendall(message)

    finally:
        logging.debug('closing socket')
        sock.close()

# list of updaters
#
updaters = []

def add(updater):
    updaters.append(updater)

# receive and process data
#
def process():

    # purge socket file
    #
    try:
        os.unlink(handle)
    except OSError:
        if os.path.exists(handle):
            raise

    # initialise socket file
    #
    logging.info('hit Ctl-C to break when in interactive mode')
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(handle)
    os.chmod(handle, 0o777)
    sock.listen(1)

    # process every client request
    #
    while True:

        logging.debug('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            logging.debug('processing new connection')

            # receive data sent by the client
            #
            message = ''
            try:
                message = connection.recv(1024)
                logging.debug('received "%s"' % message)
            except socket.error:
                logging.error('socket error')

            # push data to updaters
            #
            logging.info('--> %s' % message)

            for updater in updaters:
                try:
                    updater(message)
                except Exception as feedback:
                    logging.error("Error: update has generated an exception")
                    logging.info(str(feedback))

        # terminate this connection
        #
        finally:
            logging.debug("closing connection")
            connection.close()
