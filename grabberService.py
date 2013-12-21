__author__ = 'DicksonH'

from functions.core.grabber import Grabber
from logger.figdocLogger import FigdocLogger


class GrabberService():
    """Wrapper service for the grabber module

    Can be called directly or from the MainService"""
    def __init__(self):
        log = FigdocLogger()
        print "FigDoc grabber (FTP) service starting. Use Ctrl-C to end"
        log.write_info("Grabber (FTP) service starting up. Use Ctrl-C to end.")
        # get the config

    @staticmethod
    def go():
        in_location = "nowhere"
        get_it = Grabber()
        while True:
            print "FTP running"
            get_it.go(in_location)

if __name__ == '__main__':
    grab = GrabberService()
    grab.go()