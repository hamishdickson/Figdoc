__author__ = 'mishy'

# TODO: Basically, this needs rewriting

import logging
import time
import datetime


class FigdocLogger(logging.Logger):
    def set_up(self):
        logging.basicConfig(level=self.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='myapp.log',
                    filemode='w')
        console = self.StreamHandler()
        console.setLevel(self.INFO)

        formatter = self.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

        console.setFormatter(formatter)
        self.getLogger('').addHandler(console)

        self.info("==========================================")
        self.info("Starting new log instance")
        self.info("==========================================")


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
        logging.info()
        """Write an info line to the log"""
        logging.info(" " + self._get_datetime + msg)

    def write_error(self, msg):
        """Write an error to the log"""
        logging.error(" " + self._get_datetime + msg)

    @staticmethod
    def everything_went_wrong(self):
        """For major problems where the server can no longer function"""
        self._writeError(" " + self._get_datetime + "Oh nooooooooooo")

    @staticmethod
    def _send_to_i():
        """Write log to the i"""
        return None

    def end_log(self):
        # not sure we have to do much here
        logging.info("========================================")
        logging.info(" " + self._get_datetime + " ENDING LOG")
        logging.info("========================================")

    def __new__(self, *args, **kwargs):
        # find out what to call it
        logging.basicConfig(filename='test.log', level=logging.DEBUG)
        logging.info("==========================================")
        logging.info(" " + self._get_datetime() + " STARTING LOG")
        logging.info("==========================================")

    def __init__(self):
        self.write_info("New logging instance")

if __name__ == '__main__':
    c = Logger('mylog')
    c.set_up()
    c.info("something")