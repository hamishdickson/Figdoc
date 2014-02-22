__author__ = 'TalbotJ'

from reportlab.lib import units
import pdfprod.components.base
import reportlab.platypus
import reportlab.lib.styles


class Component(pdfprod.components.base.BaseFigdocComponent):

    def __init__(self, canvas, component, styles):

        pdfprod.components.base.BaseFigdocComponent.__init__(self, canvas, component, styles)
        self.dynamic = True

    def render(self, data=None):

        para_style = self._get_paragraph_style()
        txt = self._format_text(data)
        paragraph = reportlab.platypus.Paragraph(txt, para_style)
        paragraph.wrapOn(self.canvas,
                         float(self.component.findtext("./Width"))*units.cm,
                         float(self.component.findtext("./Height"))*units.cm)
        paragraph.drawOn(self.canvas,
                         float(self.component.findtext("./LeftPos"))*units.cm,
                         float(self.component.findtext("./BottomPos"))*units.cm)

    def _format_text(self, data):
        """Take the text from the template and produce the final text taking any embedded
        codes into account."""

        variable_elements = (var for var in self.component.findall("./Content/Variables/Variable"))
        variables_code = ("data.{0}".format(elem.text) for elem in variable_elements)
        # wow, this must be vulnerable to all kinds of stuff...
        var_txt = [eval(var) for var in variables_code]
        return self.component.findtext("./Content/Text").format(*var_txt)

    def _get_paragraph_style(self):

        return reportlab.lib.styles.ParagraphStyle('test', parent=None,
                                                   fontName=self.style.findtext("./Font"),
                                                   fontSize=float(self.style.findtext("./Size")))