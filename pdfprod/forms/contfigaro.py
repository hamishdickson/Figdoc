import pdfprod.parsers.contractparser as contractparser
import reportlab.pdfgen.canvas
from reportlab.lib import pagesizes
from reportlab.lib import units
import os.path


def run(datafile, outdir):
    data = contractparser.ContractNote(datafile)
    filepath = os.path.join(outdir, _get_filename(datafile))
    pdfobj = ContractNotePdf(filepath)
    pdfobj.create_pdf(data)


def _get_filename(wholepath):
    directory, filename = os.path.split(wholepath)
    namebit, ext = os.path.splitext(filename)
    return namebit + '.pdf'


class ContractNotePdf():

    def __init__(self, filename):

        self.c = reportlab.pdfgen.canvas.Canvas(filename, pagesize=pagesizes.A4)
        self.set_dft_font()
        self.width, self.height = pagesizes.A4

    def create_pdf(self, data):
        lmargin = 1*units.cm
        self.c.translate(lmargin, self.height-3*units.cm)
        for line in data.address:
            self.c.drawString(0, 0, line)
            self.c.translate(0, -1*units.cm)
        self.c.drawString(0, 0, "Client Account: "+data.account)
        self.c.translate(0, -1*units.cm)
        self.c.drawString(0, 0, "Security: "+data.r1+" "+data.r2)

        self.c.showPage()
        self.c.save()

    def set_dft_font(self):
        self.c.setFont("Helvetica", 9)

if __name__ == '__main__':
    dta = contractparser.ContractNote(r"C:\Users\talbotj\desktop\testftp\CONTBD.09213F0211U.PO.20131205.130119.xml")
    pdf = ContractNotePdf(r"C:\Users\talbotj\Desktop\testftp\testcn.pdf")
    pdf.create_pdf(dta)
