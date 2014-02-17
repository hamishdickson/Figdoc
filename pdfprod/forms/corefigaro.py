import pdfprod.parsers.valuationparser as valuationparser
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate
from reportlab.platypus.frames import Frame
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.tables import Table, LongTable, TableStyle
from reportlab.lib import pagesizes, units, colors
import os.path
import datetime
import time


def run(datafile, outdir):
    data = valuationparser.ValuationData(datafile)
    filepath = os.path.join(outdir, _get_filename(datafile))
    pdfobj = ValuationPrint(filepath)
    pdfobj.create_pdf(data)


def _get_filename(wholepath):
    directory, filename = os.path.split(wholepath)
    namebit, ext = os.path.splitext(filename)
    return namebit + '.pdf'


class ValuationPrint():

    def __init__(self, filename):

        self.width, self.height = pagesizes.A4
        self.lmargin = 1*units.cm
        self.rmargin = self.width - self.lmargin
        #styles = getSampleStyleSheet()
        #self.styleH = styles['Heading1']
        #self.styleN = styles['Normal']
        self.doc = BaseDocTemplate(filename)
        self.val_template = PageTemplate(id='valuation',
                                         frames=[Frame(self.lmargin, 7.5*units.cm,
                                                       19*units.cm, 13*units.cm, id='table',
                                                       showBoundary=0)],
                                         onPage=self.setup_page)
        self.doc.addPageTemplates(self.val_template)

    def setup_page(self, canvas, doc):
        canvas.saveState()
        self.do_title(canvas)
        self.do_client_name(canvas)
        self.do_date(canvas)
        self.do_person_bg(canvas)
        canvas.restoreState()

    def do_person_bg(self, canvas):
        canvas.saveState()
        ref = self.data.person_code + '/' + self.data.business_getter
        canvas.setFont('Times-Roman', 12)
        canvas.drawRightString(self.rmargin, 22*units.cm, ref)
        canvas.restoreState()

    def do_date(self, canvas):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
        dt = time.strptime(self.data.valuation_date, '%Y%m%d')
        canvas.drawString(self.lmargin, 22*units.cm, datetime.date(*dt[0: 3]).strftime('%dth %B %Y'))
        canvas.restoreState()

    def do_title(self, canvas):
        canvas.saveState()
        canvas.setFont('Times-Bold', 14)
        canvas.drawString(self.lmargin, 25*units.cm, 'Portfolio Valuation')
        canvas.restoreState()

    def do_client_name(self, canvas):
        canvas.saveState()
        canvas.setFont('Times-Bold', 14)
        canvas.drawString(self.lmargin, 23*units.cm, self.data.name_and_address["client_name"])
        canvas.restoreState()

    def create_pdf(self, data):
        self.data = data
        story = []
        dta = [[ValuationTable.heading_line(['Description', 'Book Cost', 'Holding',
                                            'Price', 'Value', 'Est. Income', 'Yield (%)'])]]
        dta.extend(ValuationTable.format_data(self.data.holdings))
        dta.extend(ValuationTable.format_cash_lines(self.data.valuation_cash, self.data.name_and_address))
        story.append(ValuationTable(dta))
        self.doc.build(story)


class ValuationTable(LongTable):

    def __init__(self, data, colWidths=None, rowHeights=None, style=None,
                repeatRows=0, repeatCols=0, splitByRow=1, emptyTableAction=None, ident=None,
                hAlign=None,vAlign=None, normalizedData=0, cellStyles=None):

        row_heights = self.get_row_heights()
        table_style = self.get_table_style()
        LongTable.__init__(self, data, [reduce(lambda x, y: x + y, ValuationTable.column_widths)], row_heights,
                           style=table_style, repeatRows=1, ident='valtable')

    heading_style = TableStyle([('FONT', (0, 0), (-1, -1), 'Times-Bold', 12),
                                #('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                                #('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                #('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                #('BOX', (0, 0), (-1, -1), 0.25, colors.aqua),
                                ('LEFTPADDING', (0, 0), (-1, -1), 0)])

    column_widths = [5*units.cm, 2.3*units.cm, 2.3*units.cm, 2.3*units.cm, 2.3*units.cm, 2.3*units.cm, 2.3*units.cm]
    style_sheet = {
        'Body': ParagraphStyle({
            'fontName': 'Times-Bold',
            'fontSize': 16,
            'leading': 20
        }),
        'Heading': ParagraphStyle({
            'fontName': 'Times-Bold',
            'fontSize': 19
        }),
        'SubHeading': ParagraphStyle({
            'fontName': 'Times-Bold',
            'fontSize': 12,
            'leading': 15
        })
    }

    @staticmethod
    def format_cash_lines(data, na):
        subhed = Paragraph('Cash', style=ValuationTable.style_sheet['SubHeading'])
        ret = [[Table([[subhed]], colWidths=[reduce(lambda x, y: x + y, ValuationTable.column_widths)])]]
        for curr in data:
            ret.append([ValuationTable.format_cash_line(curr, na)])
        return ret

    @staticmethod
    def format_cash_line(cash, na):
        paras = [
            ValuationTable.markup_detail_field(na["client_name"]+" "+na["account_type"]+" "+na["account_number"]+" "+
                                               cash["currency"], 'left'),
            ValuationTable.markup_detail_field(cash['balance'], 'right'),
            ValuationTable.markup_detail_field("", 'left')
        ]
        return Table([paras], colWidths=[10*units.cm, 4.2*units.cm, 4.6*units.cm], style=ValuationTable.heading_style)


    @staticmethod
    def get_table_style():
        return TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Times-Bold', 10),
            #('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            #('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            #('BOX', (0, 0), (-1, -1), 0.25, colors.aqua),
            #('INNERGRID', (0, 0), (-1,-1), 0.25, colors.black)
            #('LEFTPADDING', (0, 0), (-1, -1), 8)
        ])

    def get_row_heights(self):
        return None

    @staticmethod
    def heading_line(strs):
        return Table([map(lambda x: Paragraph(ValuationTable.markup_heading(x), ValuationTable.style_sheet["Body"]), strs)],
                     colWidths=ValuationTable.column_widths,
                     style=ValuationTable.heading_style)

    @staticmethod
    def markup_heading(heading):
        if heading == 'Description':
            aln = 'LEFT'
        else:
            aln = 'RIGHT'
        return '<para align="{0}"><font face="times" size=12><b>{1}</b></font></para>'.format(aln, heading)

    @staticmethod
    def format_data(data):
        tabdata = []
        for line in data:
            if isinstance(line, str):
                tabdata.append([ValuationTable.markup_subheading(line)])
            elif isinstance(line, dict):
                tabdata.append(ValuationTable.detail_line(line))
            else:
                tabdata.extend(ValuationTable.format_data(line))
        return tabdata

    @staticmethod
    def detail_line(line):
        out = [
            ValuationTable.markup_detail_field(line['r1'] + ' ' + line['r2'], 'left'),
            ValuationTable.markup_detail_field(line['book_cost'], 'right'),
            ValuationTable.markup_detail_field(line['holding'], 'right'),
            ValuationTable.markup_detail_field(line['price'], 'right'),
            ValuationTable.markup_detail_field(line['value'], 'right'),
            ValuationTable.markup_detail_field(line['income'], 'right'),
            ValuationTable.markup_detail_field(line['yield'], 'right')]

        return [Table([out], colWidths=ValuationTable.column_widths, style=ValuationTable.heading_style)]

    @staticmethod
    def markup_subheading(line):
        return Table(
            [[Paragraph('<para align="left"><font face="times" size=9><b>' + line + '</b></font></para>',
                        style=ValuationTable.style_sheet["Body"])]],
            colWidths=[reduce(lambda x, y: x + y, ValuationTable.column_widths)],
            rowHeights=None,
            style=ValuationTable.get_table_style())


    @staticmethod
    def markup_detail_field(line, align):
        return Paragraph(
            '<para align="{0}"><font face="times" size=7>{1}</font></para>'.format(align, line),
            style=ValuationTable.style_sheet["Body"])
