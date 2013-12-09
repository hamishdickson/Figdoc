__author__ = 'DicksonH'

from File import File
from Logging import logger
from Functions.Core.grabber import Grabber
import figconfig
from xml.etree.ElementTree as ET
import os

def get_files_from_iSeries(self, location):
    # start the FTP process and get a file
    log.writeInfo("Getting all waiting xml files from iSeries")
    grab = Grabber()
    grab.go(location) # this should pull everything to the directory in the config file

    
def get_next_file_and_process(self, location):
    log.writeInfo("Get a file listing and process each file")
    file_listing = os.listdir(location)
    if len(file_listing) > 0:
        for x in file_listing:
            log.writeInfo("Process file " + x)
            process_xml_file(x)
    else:
        log.writeInfo("There ain't out to process ere...")

def process_xml_file(self, in_file):
    tree = ET.parse(in_file)
    root = tree.getroot()
    log.writeInfo("Root of file " + in_file + " is " + root)

log = logger.pdfLogger()
log.writeInfo("Starting process up")

if __name__ == '__main__':
    """This is the main service. It initialises everything.

    This is not bespoke script."""

    self._config = figconfig.get_config("service")
    self.location = self._config["todir"]
    self.wait_time = self._config["interval"]

    while True:
    	get_files_from_iSeries(self.location)
    	get_next_file_and_process(self.location)
    	time.sleep(self.wait_time)