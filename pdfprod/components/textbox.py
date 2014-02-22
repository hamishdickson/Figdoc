__author__ = 'TalbotJ'

from reportlab.lib import units
import pdfprod.components.base


class Component(pdfprod.components.base.BaseFigdocComponent):

    def render(self, data=None):

        self.canvas.setFont(self.style.findtext("./Font"), float(self.style.findtext("./Size")))
        txt = self.component.findtext("./Content")
        txtobj = self.canvas.beginText(float(self.component.findtext("./LeftPos"))*units.cm,
                                       float(self.component.findtext("./BottomPos"))*units.cm)
        txtobj.textLine(txt)
        self.canvas.drawText(txtobj)
