import pdfprod.parsers.contractparser as contractparser
import reportlab.pdfgen.canvas
import reportlab.lib.styles
from reportlab.lib import pagesizes
from reportlab.lib import units
import reportlab.platypus
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
        self.lmargin = 2*units.cm
        self.rmargin = self.width - self.lmargin
        self.value_col_location = 16*units.cm
        self.currency_col_location = 17*units.cm

    def create_pdf(self, data):
        self.data = data
        self.do_address(self.lmargin, 24*units.cm)
        self.do_title(self.lmargin, 20*units.cm)
        self.do_account_details(self.lmargin, 18*units.cm)
        self.do_top_right(self.lmargin+10*units.cm, 19*units.cm)
        self.do_horizontal_line(16*units.cm)
        self.do_trade_details(15*units.cm)
        self.do_horizontal_line(11*units.cm)
        self.do_charges(10*units.cm)
        self.do_horizontal_line(8*units.cm)
        self.do_total_line(7*units.cm)
        self.c.showPage()
        self.c.save()

    def do_total_line(self, top):
        self.c.setFont('Helvetica-Bold', 12)
        txt = 'Total %s due on settlement date %s' % (self.data.credit_or_debit, self.data.settlement_date)
        txtobj = self.c.beginText(self.lmargin, top)
        txtobj.textLine(txt)
        self.c.drawRightString(self.value_col_location, top, self.data.total_payment)
        self.c.drawString(self.currency_col_location, top, self.data.price_currency)
        self.c.drawText(txtobj)

    def do_charges(self, top):
        def print_line(height, label, value, currency):
            labtxt = self.c.beginText(1.5*self.lmargin, height)
            labtxt.textLine(label)
            self.c.drawRightString(self.value_col_location, height, value)
            self.c.drawString(self.currency_col_location, height, currency)
            self.c.drawText(labtxt)

        self.do_subheading(top, 'Commission and Charges')
        self.set_dft_font()
        h = top - 1*units.cm
        for charge in self.data.charges:
            print_line(h, charge['label'], charge['value'], charge['currency'])
            h -= 1*units.cm

    def do_trade_details(self, top):
        def para_style():
            s = reportlab.lib.styles.ParagraphStyle('test', parent=None, fontName='Helvetica')
            return s
        self.do_subheading(top, 'Trade Details')
        self.set_dft_font()
        dets_txt = 'On your behalf as agent we have bought for you ' + self.data.quantity + ' ' +\
            self.data.r1 + ' ' + self.data.r2 + ' at a price of ' + self.data.price + ' ' +\
            self.data.price_currency
        dets = reportlab.platypus.Paragraph(dets_txt, para_style())
        dets.wrapOn(self.c, 10*units.cm, 5*units.cm)
        dets.drawOn(self.c, 1.5*self.lmargin, top-2*units.cm)
        self.c.drawRightString(self.value_col_location, top-2*units.cm-dets.height, self.data.consideration)
        self.c.drawString(self.currency_col_location, top-2*units.cm-dets.height, self.data.price_currency)
        self.c.drawString(self.lmargin, top-2*units.cm-dets.height, 'Consideration')

    def do_subheading(self, top, txt):
        heading = self.c.beginText(self.lmargin, top)
        self.c.setFont('Helvetica-Bold', 12)
        heading.textLine(txt)
        self.c.drawText(heading)

    def do_horizontal_line(self, height):
        self.c.setLineWidth(1)
        p = self.c.beginPath()
        p.moveTo(self.lmargin, height)
        p.lineTo(self.rmargin, height)
        p.close()
        self.c.drawPath(p)

    def do_top_right(self, left, top):
        def do_left(left, top):
            dets = self.c.beginText(left, top)
            dets.textLines("""Contract Reference:
            Contract Date:
            Contract Time:
            Order Type:
            Stock Code:
            Venue:
            Counterparty:
            """)
            self.c.drawText(dets)

        def do_right(left, top):
            dets = self.c.beginText(left, top)
            dets.textLine(self.data.contract_ref)
            dets.textLine(self.data.contract_date)
            dets.textLine(self.data.contract_time)
            dets.textLine(self.data.order_type)
            dets.textLine(self.data.sedol)
            dets.textLine(self.data.venue)
            dets.textLine(self.data.counterparty)
            self.c.drawText(dets)

        do_left(left, top)
        do_right(left+4*units.cm, top)

    def do_account_details(self, left, top):
        dets = self.c.beginText(left, top)
        self.set_dft_font()
        x, y = dets.getCursor()
        dets.textLines("""Account Name:


        Account Reference:""")
        dets.setTextOrigin(x+3.1*units.cm, y)
        dets.textLine(self.data.account_name)
        dets.textLine()
        dets.textLine()
        dets.textLine(self.data.account+'/'+self.data.business_getter)

        self.c.drawText(dets)

    def do_title(self, left, top):
        title = self.c.beginText(left, top)
        self.c.setFont('Helvetica-Bold', 14)
        title.textLine('Contract Note')
        self.c.drawText(title)

    def do_address(self, left, top):
        addr = self.c.beginText(left, top)
        addr.textLine(self.data.account_name)
        for line in self.data.address:
            addr.textLine(line)
        self.c.drawText(addr)

    def set_dft_font(self):
        self.c.setFont("Helvetica", 9)

if __name__ == '__main__':
    dta = contractparser.ContractNote(r"C:\Users\talbotj\desktop\testftp\CONTBD.09213F0211U.PO.20131205.130119.xml")
    pdf = ContractNotePdf(r"C:\Users\talbotj\Desktop\testftp\testcn.pdf")
    pdf.create_pdf(dta)
