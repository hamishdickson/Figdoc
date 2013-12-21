__author__ = 'DicksonH'

# So, basically ... don't ever use logging directly, instead use this class. This will work out if you should be
# logging locally or to the iSeries ... and if something has gone wrong (like the connection to the i gets lost),
# this will deal with it for you (and write locally)

# There is a good explanation of what logging should be used when here
# http://docs.python.org/2/howto/logging.html

# FigdocLogger.write_info should be used when recording normal operation
# FigdocLogger.write_warning should be used when recording something may cause incorrect data coming out
# FigdocLogger.write_error should be used when something bad happens and the form doesn't run


# So it turns out that that core python logging class is a bit odd, in that it's designed so you don't subclass it,
# the idea is that instead you can call it from lots of different places and it uses the same log

import logging
import time
import datetime
import os
import figconfig as figConfig


class FigdocLogger():

    _log_to_i = False
    _daily_log = False
    _local_file_location = "logs"
    _local_file_name = "localLog.log"
    _is_instance = False

    @staticmethod
    def _get_datetime():
        ts = time.time()
        st = "" + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + ": "
        return st

    def __init__(self):
        if not FigdocLogger._is_instance:
            # get the config
            FigdocLogger._is_instance = True
            try:
                #get the log configuration
                print "trying to get the config"
                self._config = figConfig.get_config("logging")
                FigdocLogger._log_to_i = self._config["logToI"]
                FigdocLogger._local_file_location = self._config["location"]
                FigdocLogger._local_file_name = self._config["fileName"]
                FigdocLogger._daily_log = self._config["dailyLog"]
            except IOError as e:
                print "There was an error getting the logging configuration. Local logging will be used"
                # use the hard coded config

            # create the log/connection
            if self._log_to_i:
                try:
                    print "write here and say process is starting up"
                except:
                    print "BAD BAD ERROR - COULDN'T LOG TO I"
                    self.file = FigdocLogger._local_file_location + "\\" + FigdocLogger._local_file_name
                    if not os.path.exists(FigdocLogger._local_file_location):
                        os.makedirs(FigdocLogger._local_file_location)

                    logging.basicConfig(filename=self.file, level=logging.DEBUG)
                    logging.info("=========================================================================")
                    logging.info(self._get_datetime() + "STARTING LOG")
                    logging.exception(self._get_datetime() + "Failed attempt to write to i")
                    logging.info("=========================================================================")
            else:
                self.file = FigdocLogger._local_file_location + "\\" + FigdocLogger._local_file_name
                if not os.path.exists(FigdocLogger._local_file_location):
                    os.makedirs(FigdocLogger._local_file_location)

                logging.basicConfig(filename=self.file, level=logging.DEBUG)
                logging.info("=========================================================================")
                logging.info(self._get_datetime() + "STARTING LOG")
                logging.info("=========================================================================")

    def write_info(self, msg):
        if self._log_to_i:
            try:
                # connect to the iseries
                print "logging to i"
            except:
                logging.exception("Couldn't write to iSeries")
                logging.info(self._get_datetime() + msg)
        else:
            # log locally
            logging.info(self._get_datetime() + msg)

    def write_warning(self, msg):
        if self._log_to_i:
            try:
                # connect to the iseries
                print "logging to i"
            except:
                logging.exception("Couldn't write to iSeries")
                logging.warning(self._get_datetime() + msg)
        else:
            # log locally
            logging.warning(self._get_datetime() + msg)

    def write_error(self, msg):
        if self._log_to_i:
            try:
                # connect to the iseries
                print "logging to i"
            except:
                logging.exception("Couldn't write to iSeries")
                logging.error(self._get_datetime() + msg)
        else:
            # log locally
            logging.error(self._get_datetime() + msg)

# quick test stub ...
if __name__ == '__main__':
    a = FigdocLogger()
    a.write_info("write to i")

    b = FigdocLogger()
    b.write_info("second instance")

    a.write_warning("this is a warning")
    b.write_catastrophe("arrgh! stuff broke!!")