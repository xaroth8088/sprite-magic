""" A control to permit adjusting the hue of a given sprite
"""

""" A widget for adjusting the speed of the animation preview
"""

from Tkinter import *
from ttk import *
from Tkinter import Radiobutton  # use Tkinter version

from models.compositor import COMPOSITOR

class ColorAdjuster( Frame ):
    def __init__( self, master, layer ):
        Frame.__init__( self, master )
        self.layer = layer
        self._setup_view()

    def _setup_view( self ):
        self._setup_hue()
        self._setup_saturation()
        self._setup_value()

    def _setup_hue( self ):
        label = Label( self, text = "Hue" )
        label.grid( row = 0, column = 0 )

        self.selected_hue = IntVar()
        self.selected_hue.trace( 'w', self._on_hue_selection_changed )

        for i in range( 0, 6 ):
            text = "Original"
            if i > 0:
                text = "Hue %d" % ( i, )

            Radiobutton( self, text = text, variable = self.selected_hue, value = ( i * 60 ), indicatoron = 0, padx = 10 ).grid( row = 1, column = i )

    def _setup_saturation( self ):
        label = Label( self, text = "saturation" )
        label.grid( row = 2, column = 0 )

        self.selected_saturation = IntVar()
        self.selected_saturation.trace( 'w', self._on_hue_selection_changed )

        for i in range( 0, 6 ):
            text = "Original"
            if i < 5:
                text = "sat. %d" % ( i, )

            Radiobutton( self, text = text, variable = self.selected_saturation, value = i, indicatoron = 0, padx = 10 ).grid( row = 3, column = i )

    def _setup_value( self ):
        label = Label( self, text = "Value" )
        label.grid( row = 4, column = 0 )

        self.selected_value = IntVar()
        self.selected_value.trace( 'w', self._on_hue_selection_changed )

        for i in range( 0, 6 ):
            text = "Original"
            if i < 5:
                text = "Value %d" % ( i, )

            Radiobutton( self, text = text, variable = self.selected_value, value = i, indicatoron = 0, padx = 10 ).grid( row = 5, column = i )

    def _on_hue_selection_changed( self, name, index, mode ):
        root = self.master
        while root.master is not None:
            root = root.master

        root.config( cursor = "watch" )
        root.update()

        hsv = ( self.selected_hue.get(), float( self.selected_saturation.get() ) * 0.2, self.selected_value.get() * 0.2 )

        COMPOSITOR.colorize_layer( self.layer, hsv )
        root.config( cursor = "" )
        root.update()
