__author__ = 'TalbotJ'


class BaseFigdocComponent():
    """The base class for all components used to display data in a Figdoc PDF.

    This basically just contains logic to do with setting up styles at the moment, since that's
    about all I've noticed that every component needs to do so far.
    """

    def __init__(self, canvas, component, styles):

        self.component = component
        style_name = component.findtext("./Style")
        if style_name:
            self.style = styles[style_name]
        self.canvas = canvas
        self.dynamic = False

    def render(self, data=None):
        """Draw this component on the canvas, using the provided data.

        This is likely to be the only method (other than the constructor) called from the
        outside world and obviously needs to be overridden by a concrete implementation.
        """
        pass
