import importlib
from xml.etree.ElementTree import parse


class FormRunner():

    def __init__(self, inputfile):
        """Set up a formrunner object by importing the relevant module.

        This first gets the name for the module out of the XML file, then
        imports the module. It doesn't catch any exceptions, so that should
        be watched for in the calling module.
        """

        self._datafile = inputfile
        self._form_name = self._get_form_name(inputfile)
        self._module = importlib.import_module("pdfprod.forms." + self._form_name)

    def produce_pdf(self, outdir):
        """Call the 'run' function in the module that we loaded in __init__.

        This should produce the PDF based on the XML that we pass in and place it
        in the output directory that we tell it to.
        """

        self._module.run(self._datafile, outdir)

    def _get_form_name(self, inputfile):
        """Fetch the form name out of the XML file"""

        pack = parse(inputfile).getroot()
        form = pack.findtext("./Routing[1]/Header4[1]/PpFileName[1]")
        return form.strip().lower()

if __name__ == '__main__':

    r = FormRunner(r"C:\Users\talbotj\Desktop\testftp\inputxml" +
                   r"\CONTBD.09213F0211U.PO.20131205.130119.xml")
    r.produce_pdf(r"C:\Users\talbotj\Desktop\testftp\pdfs")
