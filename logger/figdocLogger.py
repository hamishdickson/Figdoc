__author__ = 'DicksonH'

# So, basically ... don't ever use logging directly, instead use this class. This will work out if you should be
# logging locally or to the iSeries ... and if something has gone wrong (like the connection to the i gets lost),
# this will deal with it for you (and write locally)

# There is a good explanation of what logging should be used when here
# http://docs.python.org/2/howto/logging.html

# FigdocLogger.write_info should be used when recording normal operation
# FigdocLogger.write_warning should be used when recording something may cause incorrect data coming out
# FigdocLogger.write_error should be used when something bad happens and the form doesn't run
# FigdocLogger.write_to_log is just a general wrapper

# So it turns out that that core python logging class is a bit odd, in that it's designed so you don't subclass it,
# the idea is that instead you can call it from lots of different places and it uses the same log

# Yes, I too have read that you shouldn't really use static methods in python and it's something only java programmers
# try to use .. but I've done this so I can use __init__ to set up everything .. I may change my mind about all this
# later ... but right now it makes sense

# @TODO: check to see if using the write log, if not .. create a new one
# @TODO: basically do all the iseries work!

import logging
import time
import datetime
import os
import figconfig as figConfig


class FigdocLogger():

    # static variables ... creates a log even if nothing is configured .. don't unstatic (that's totally a word)
    _log_to_i = False
    _daily_log = False
    _local_file_location = "logs"
    _local_file_name = "localLog.log"
    _is_instance = False

    _log_name = ""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

    # This gets set on when a write to the i failed ... switched off whenever a successful write happens
    _failed_i_write_warning = False

    @staticmethod
    def _get_datetime():
        ts = time.time()
        st = "" + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + ": "
        return st

    @staticmethod
    def _failed_i_write(msg):
        # only come in here if the write to the i failed
        FigdocLogger._sort_out_file_name()
        if not FigdocLogger._failed_i_write_warning:
            FigdocLogger._failed_i_write_warning = True
            logging.error(FigdocLogger._get_datetime() + "Failed write to iSeries")

        logging.info(FigdocLogger._get_datetime() + msg)

    @staticmethod
    def _todays_log_name():
        # Returns the name of today's log
        today = time.strftime("%Y%m%d")
        return today + "_" + FigdocLogger._local_file_name

    @staticmethod
    def _create_new_log_file():
        file = FigdocLogger._local_file_location + "\\" + FigdocLogger._todays_log_name()
        try:
            if not os.path.exists(FigdocLogger._local_file_location):
                os.makedirs(FigdocLogger._local_file_location)

            logging.basicConfig(filename=file, level=logging.DEBUG)
            FigdocLogger._log_name = file
        except:
            # note: if this dies, any log messages will go to the command line
            print "Create new log failed. Please stop this process and contact your administrator"

    @staticmethod
    def _sort_out_file_name():
        if FigdocLogger._log_name == FigdocLogger._todays_log_name():
            # then we're good, go home ...
            pass
        else:
            FigdocLogger._create_new_log_file()

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
            if FigdocLogger._log_to_i:
                try:
                    print "write here and say process is starting up"
                except:
                    print "BAD BAD ERROR - COULDN'T LOG TO I ... log locally instead"

                    FigdocLogger._sort_out_file_name()
                    logging.info("=========================================================================")
                    logging.info(FigdocLogger._get_datetime() + "STARTING LOG")
                    logging.exception(FigdocLogger._get_datetime() + "Failed attempt to write to i")
                    logging.info("=========================================================================")
            else:
                FigdocLogger._sort_out_file_name()
                logging.info("=========================================================================")
                logging.info(FigdocLogger._get_datetime() + "STARTING LOG")
                logging.info("=========================================================================")

    @staticmethod
    def write_to_log(msg, level=None):
        if level is None or level == FigdocLogger.INFO:
            FigdocLogger.write_info(msg)
        elif level == FigdocLogger.WARNING:
            FigdocLogger.write_warning(msg)
        elif level == FigdocLogger.ERROR:
            FigdocLogger.write_error(msg)
        else:
            FigdocLogger.write_error("Bad logging message")

    @staticmethod
    def write_info(msg):
        if FigdocLogger._log_to_i:
            try:
                # connect to the iseries
                print "logging to i"
            except:
                FigdocLogger._failed_i_write(msg)
        else:
            # log locally
            FigdocLogger._sort_out_file_name()
            logging.info(FigdocLogger._get_datetime() + msg)

    @staticmethod
    def write_warning(msg):
        if FigdocLogger._log_to_i:
            try:
                # connect to the iseries
                print "logging to i"
            except:
                FigdocLogger._failed_i_write(msg)
        else:
            # log locally
            FigdocLogger._sort_out_file_name()
            logging.warning(FigdocLogger._get_datetime() + msg)

    @staticmethod
    def write_error(msg):
        if FigdocLogger._log_to_i:
            try:
                # connect to the iseries
                print "logging to i"
            except:
                FigdocLogger._failed_i_write(msg)
        else:
            # log locally
            FigdocLogger._sort_out_file_name()
            logging.error(FigdocLogger._get_datetime() + msg)


# quick test stub ...
if __name__ == '__main__':
    a = FigdocLogger()
    a.write_info("write to i")

    b = FigdocLogger()
    b.write_info("second instance")

    a.write_warning("this is a warning")
    b.write_error("arrgh! stuff broke!!")