__author__ = 'TalbotJ'

import importlib
from xml.etree.ElementTree import parse


class FormRunner():

    def __init__(self, input_file):
        """Set up a formrunner object by importing the relevant module.

        This first gets the name for the module out of the XML file, then
        imports the module. It doesn't catch any exceptions, so that should
        be watched for in the calling module.
        """
        self._datafile = input_file
        self._form_name = self._get_form_name(input_file)
        self._module = importlib.import_module("pdfprod.forms." + self._form_name)

    def produce_pdf(self, out_dir):
        """Call the 'run' function in the module that we loaded in __init__.

        This should produce the PDF based on the XML that we pass in and place it
        in the output directory that we tell it to.
        """

        self._module.run(self._datafile, out_dir)

    @staticmethod
    def _get_form_name(input_file):
        """Fetch the form name out of the XML file"""

        pack = parse(input_file).getroot()
        form = pack.findtext("./Routing[1]/Header4[1]/PpFileName[1]")
        return form.strip().lower()

if __name__ == '__main__':

    import os
    r = FormRunner(r"C:\Users\user\Desktop\testftp\inputxml" +
                   r"\CONTBD.09213F021KB.PO.20131216.105400.xml")
    r.produce_pdf(r"C:\Users\user\Desktop\testftp\pdfs")
    os.system(r'start "" /max "C:\Users\User\Desktop\testftp\pdfs\CONTBD.09213F021KB.PO.20131216.105400.pdf"')
