__author__ = 'TalbotJ'

import reportlab.pdfgen.canvas
from reportlab.lib import units


def render_on(canvas, data, styles):

    canvas.setFont('Helvetica-Bold', 12)
    txt = 'Contract Note'
    txtobj = canvas.beginText(3*units.cm, 15*units.cm)
    txtobj.textLine(txt)
    print data.contract_ref
    canvas.drawText(txtobj)
