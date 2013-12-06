__author__ = 'DicksonH'

from File import XML_file
from Logging import logger

def get_file_from_iSeries():
    # start the FTP process and get a file
    log.writeInfo("Getting xml file from iSeries")
    file = XML_file() # need an object relating to the file
    return file

def run_pdf_template(in_file):
    log.writeInfo("Picked up xml file and got to the runner")


log = logger.pdfLogger()
log.writeInfo("Starting process up")

if __name__ == '__main__':
    """This is the main service. It initialises everything.

    This is not bespoke script."""

    file = get_file_from_iSeries()
    run_pdf_template(file)

