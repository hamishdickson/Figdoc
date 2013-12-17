__author__ = 'mishy'

import logging
import time
import datetime

class PdfLogger(object):
    """
    General use logger for Figdocs

    @TODO get this production ready
    """
    @staticmethod
    def _get_datetime():
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return st

    def write_info(self, msg):
        """Write an info line to the log"""
        logging.info(self._get_datetime + msg)

    def write_error(self, msg):
        """Write an error to the log"""
        logging.error(self._get_datetime + msg)

    @staticmethod
    def everything_went_wrong(self):
        """For major problems where the server can no longer function"""
        self._writeError(self._get_datetime + "Oh nooooooooooo")

    @staticmethod
    def _send_to_i():
        """Write log to the i"""
        return None

    def end_log(self):
        # not sure we have to do much here
        logging.info("========================================")
        logging.info(self._get_datetime + " ENDING LOG")
        logging.info("========================================")

    @staticmethod
    def _create_log(self):
        # find out what to call it
        logging.basicConfig(filename='test.log', level=logging.DEBUG)
        logging.info("==========================================")
        logging.info(self._get_datetime + " STARTING LOG")
        logging.info("==========================================")

    def __init__(self):
        self._create_log()