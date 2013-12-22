__author__ = 'DicksonH'

#
# Wrapper service for the grabber class
#
# This service FTPs files from the iSeries over to the server
#

# configuration
# _interval - polling interval (in seconds)
# _from_location - where on the iSeries to pick up files from
# _to_location - where to put the files on the Figdoc server

# @TODO: find a way to pick things up from more than one location - change config structure?
# @TODO: have the config ... now use it ...

from Functions.Core.grabber import Grabber
from logger.figdocLogger import FigdocLogger
from figconfig import figconfig as figConfig


class GrabberService():
    """Wrapper service for the grabber module

    Can be called directly or from the MainService"""

    _interval = 4
    _from_location = ''
    _to_location = ''

    def __init__(self):
        log = FigdocLogger()

        # print message to the screen as well as here
        print "FigDoc grabber (FTP) service starting. Use Ctrl-C to end"
        log.write_info("Grabber (FTP) service starting up. Use Ctrl-C to end.")

        # get the config
        try:
            self._config = figConfig.get_config("grabber")
            GrabberService._interval = self._config["interval"]
            GrabberService._from_location = self._config["fromDir"]
            GrabberService._to_location = self._config["toDir"]
        except IOError as e:
            print "There was an error getting the Grabber Service configuration. Please contact you system administrator"
            # you can't do much from here - exit

    @staticmethod
    def go():
        get_it = Grabber()
        try:
            while True:
                print "FTP running"
                get_it.go(GrabberService._from_location)
        except KeyboardInterrupt:
            print "Shutting down"

# You can run this directly if you want to
if __name__ == '__main__':
    grab = GrabberService()
    grab.go()