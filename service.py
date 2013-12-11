__author__ = 'DicksonH'

from functions.core.grabber import Grabber
from logger.logger import PdfLogger
from figconfig import figconfig
from xml.etree.ElementTree import parse
import os
import time


class Service():
    """This is the main service. It initialises everything.

    This is not bespoke script."""

    def __init__(self):
        self._config = figconfig.get_config("service")
        self.location = self._config["todir"]
        self.wait_time = self._config["interval"]

    @staticmethod
    def get_files_from_i(in_location):
        # start the FTP process and get a file
        log.write_info("Getting all waiting xml files from iSeries")
        grab = Grabber()
        grab.go(in_location)  # this should pull everything to the directory in the config file

    def get_next_file_and_process(self, in_location):
        log.write_info("Get a file listing and process each file")
        file_listing = os.listdir(in_location)
        if len(file_listing) > 0:
            for x in file_listing:
                log.write_info("Process file " + x)
                self.process_xml_file(x)
        else:
            log.write_info("There ain't out to process ere...")

    @staticmethod
    def process_xml_file(in_file):
        tree = parse(in_file)
        root = tree.getroot()
        log.write_info("Root of file " + in_file + " is " + root)


if __name__ == '__main__':
    log = PdfLogger()
    log.write_info("Starting process up")

    run_it = Service()

    try:
        while True:
            run_it.get_files_from_i(run_it.location)
            run_it.get_next_file_and_process(run_it.location)
            assert isinstance(run_it.wait_time, int)
            time.sleep(run_it.wait_time)
    finally:
        log.end_log()