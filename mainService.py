__author__ = 'DicksonH'

#
# Main Service for Figdocs
#

# I suspect I'm going to have to rewrite this a few times ...

# This will start everything up. By default it will create a thread to go and FTP everything from the iSeries
# and a thread for each new file it finds
#
# This is core functionality, do not change

# @TODO: find a way to make the routing logic bespoke
# @TODO: a lot can go wrong here, catch exceptions and do something useful

from logger import figconfig
from logger.figdocLogger import FigdocLogger
from xml.etree.ElementTree import parse
from threading import Thread
from grabberService import GrabberService
import os
import time


class Service():
    """This is the main service. It initialises everything.

    This is not bespoke script. Do not change"""

    def __init__(self):
        self._config = figconfig.get_config("service")
        self.location = self._config["todir"]
        self.wait_time = self._config["interval"]

    def get_next_file_and_process(self, in_location):
        log.write_info("Get a file listing and process each file")
        file_listing = os.listdir(in_location)
        if len(file_listing) > 0:
            for x in file_listing:
                log.write_info("Process file " + x)
                self.process_xml_file(x)
        else:
            log.write_info("There ain't out to process ere...")

    def email_attachment(self):
        pass

    def email_message(self):
        pass

    def line_print(self):
        pass

    @staticmethod
    def get_routing_flags(self, in_tree):
        # test stub
        out_flag = 'LP'
        return out_flag

    def _archive_input_file(self):
        pass

    def create_pdf(self):
        pass

    def connect_to_dms(self):
        pass

    def email_admin(self, message):
        pass

    def handle_error(self):
        pass

    @staticmethod
    def process_xml_file(self, in_file):
        tree = parse(in_file)
        root = tree.getroot()
        log.write_info("Root of file " + in_file + " is " + root)

        ### Main line ###

        # First thing's first - archive a copy

        # get the routing flags and the file
        routing_flag = self.get_routing_flags(tree)

        # NOTE: there are no switch/case statements in python (apparently)
        if routing_flag == 'LP':
            # create PDF
            # connect to configured printer
            # print the sucka
            pass

        elif routing_flag == 'EA':
            # create PDF
            # email it
            pass

        elif routing_flag == 'EM':
            # oh, well then we want to email a message
            pass

        elif routing_flag == 'PO':
            # create PDF
            # connect to DMS
            pass

        else:
            # we have an error
            # email the configured account details and log everything
            pass

#
# This is the recommended entry point for Figdocs
#
if __name__ == '__main__':
    log = FigdocLogger()
    log.write_info("Starting mainService.")
    print "Starting main Figdoc service."

    # create a new thread for the FTP process
    log.write_info("Creating a new thread for the grabbers")
    grab = GrabberService()
    thread = Thread(target=grab.go())
    thread.start()
    thread.join()

    run_it = Service()

    try:
        while True:
            run_it.get_next_file_and_process(run_it.location)
            assert isinstance(run_it.wait_time, int)
            time.sleep(run_it.wait_time)
    finally:
        log.controlled_shut_down("Shutting down from mainService")