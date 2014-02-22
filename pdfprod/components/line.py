__author__ = 'TalbotJ'

from reportlab.lib import units
import pdfprod.components.base


class Component(pdfprod.components.base.BaseFigdocComponent):

    def render(self, data=None):

        self.canvas.setStrokeColor(self.component.findtext("./Colour"))
        self.canvas.setLineWidth(self.component.findtext("./Weight"))
        self.canvas.line(float(self.component.findtext("./StartLeftPos"))*units.cm,
                         float(self.component.findtext("./StartBottomPos"))*units.cm,
                         float(self.component.findtext("./EndLeftPos"))*units.cm,
                         float(self.component.findtext("./EndBottomPos"))*units.cm)