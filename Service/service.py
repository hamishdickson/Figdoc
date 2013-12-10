__author__ = 'DicksonH'

from Logging import logger
from Functions.Core.grabber import Grabber
import figconfig
from xml.etree.ElementTree import parse
import os
import time


def get_files_from_i(in_location):
    # start the FTP process and get a file
    log.write_info("Getting all waiting xml files from iSeries")
    grab = Grabber()
    grab.go(in_location)  # this should pull everything to the directory in the config file

    
def get_next_file_and_process(location):
    log.write_info("Get a file listing and process each file")
    file_listing = os.listdir(location)
    if len(file_listing) > 0:
        for x in file_listing:
            log.write_info("Process file " + x)
            process_xml_file(x)
    else:
        log.write_info("There ain't out to process ere...")


def process_xml_file(in_file):
    tree = parse(in_file)
    root = tree.getroot()
    log.write_info("Root of file " + in_file + " is " + root)

log = logger.PdfLogger()
log.write_info("Starting process up")

if __name__ == '__main__':
    """This is the main service. It initialises everything.

    This is not bespoke script."""

    _config = figconfig.get_config("service")
    location = _config["todir"]
    wait_time = _config["interval"]

    while True:
        get_files_from_i(location)
        get_next_file_and_process(location)
        time.sleep(wait_time)