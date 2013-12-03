__author__ = 'mishy'

import logging

class pdfLogger(object):
    """
    General use logger for Figdocs

    @TODO get this production ready
    """

    _instance = None

    @staticmethod
    def writeInfo(msg):
        """Write an info line to the log"""
        logging.info(msg)

    @staticmethod
    def writeError(self, msg):
        """Write an error to the log"""
        out = "Timestamp " + msg
        logging.error(out)

    @staticmethod
    def everythingWentWrong(self):
        """For major problems where the server can no longer function"""
        self._writeError("Oh nooooooooooo")

    @staticmethod
    def _sendToAS400():
        """Write log to the i"""
        return None

    @staticmethod
    def _endLog(self):
        # not sure we have to do much here
        self.writeInfo("======================")
        self.writeInfo("ENDING LOG" + "timestamp")
        self.writeInfo("======================")

    @staticmethod
    def _createLog():
        # need to add the date to the filename
        logging.basicConfig(filename="test.log", level=logging.DEBUG)

    #def __new__(cls, *args, **kwargs):
    #    if not cls._instance:
    #        cls._instance = super(pdfLogger, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        self._createLog()