__author__ = 'TalbotJ'

from xml.etree.ElementTree import parse
from reportlab.lib import pagesizes
import reportlab.pdfgen.canvas
import importlib
import pdfprod.parsers.contractparser as contractparser
import os.path


class PdfProducer():

    """Parse an XML 'form', take an XML input file, and turn them into a PDF."""

    def __init__(self, form, out_file_name):

        self.form = self._parse_xml(form)
        self.styles = self._extract_elements(self.form, 'Style')
        self.pages = self._extract_elements(self.form, 'Page')
        self.canvas = None
        self.out_file_name = out_file_name
        self.data = None

    def _extract_elements(self, form, data_type):

        for child in form:
            if child.tag == data_type:
                yield child

    def _parse_xml(self, xml):

        return parse(xml).getroot()

    def _parse_input_file(self, input_file):

        data = {}
        #src = self._parse_xml(input_file)
        #for sub in src:
        #    if sub.tag == 'Print':
        #        data[sub.findtext("./PrintCode")] = self._parse_single_print(sub)

        # Hard coded this as contract notes for now. They probably need to be a special case anyway.
        data['CONTBD'] = contractparser.ContractNote(input_file)

        return data

    def _parse_single_print(self, prt):

        # this looks eerily similar to the function above - abstract out duplicate logic somehow?
        data = {}
        for sub in prt:
            if sub.tag != 'PrintCode':
                data[sub.tag] = self._parse_data_type(sub)

        return data

    def _parse_data_type(self, data_type):

        # Errr... more dynamic module loading stuff to go here...
        pass

    def _get_form_name(self, input_file):
        """Fetch the form name out of the XML file"""

        pack = parse(input_file).getroot()
        form = pack.findtext("./Routing[1]/Header4[1]/PpFileName[1]")
        return form.strip().lower()

    def produce_pdf(self, input_file=None, out_directory=None):

        out = os.path.join(out_directory, self.out_file_name)
        self.data = self._parse_input_file(input_file)
        canvas = reportlab.pdfgen.canvas.Canvas(out, pagesize=pagesizes.A4)
        map(lambda p: self._process_page(canvas, p), self.pages)
        canvas.showPage()
        canvas.save()

    def _process_page(self, canvas, page):

        print_code = self._extract_print_code(page)
        components = self._extract_elements(page, 'Component')
        map(lambda c: self._render_component(c, canvas, print_code), components)

    def _extract_print_code(self, page):

        return page.attrib["print_code"]

    def _render_component(self, component, canvas, print_code):

        canvas.saveState()
        component_type = self._extract_component_type(component)
        processor = importlib.import_module("pdfprod.{0}".format(component_type))
        processor.render_on(canvas, self.data[print_code], self.styles)
        canvas.restoreState()

    def _extract_component_type(self, component):

        return component.attrib["type"]

if __name__ == '__main__':

    pp = PdfProducer(r"C:\Users\User\Desktop\testftp\cnformxml.xml", "jattest.pdf")
    pp.produce_pdf(r"C:\Users\user\Desktop\testftp\inputxml" +
                   r"\CONTBD.09213F021KB.PO.20131216.105400.xml",
                   r"C:\Users\user\Desktop\testftp\pdfs")
    import os
    os.system(r'start "" /max "C:\Users\User\Desktop\testftp\pdfs\jattest.pdf"')