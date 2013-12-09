""" A control to permit adjusting the hue of a given sprite
"""

""" A widget for adjusting the speed of the animation preview
"""

from Tkinter import *
from ttk import *
from Tkinter import Radiobutton  # use Tkinter version

from models.compositor import COMPOSITOR

class HueAdjuster( Frame ):
    def __init__( self, master, layer ):
        Frame.__init__( self, master )
        self.layer = layer
        self._setup_view()

    def _setup_view( self ):
        label = Label( self, text = "Hue" )
        label.grid( row = 0, column = 0 )

        self.selected_hue = IntVar()
        self.selected_hue.trace( 'w', self._on_hue_selection_changed )

        for i in range( 0, 6 ):
            text = "Original"
            if i > 0:
                text = "Hue %d" % ( i, )

            Radiobutton( self, text = text, variable = self.selected_hue, value = ( i * 60 ), indicatoron = 0, padx = 10 ).grid( row = 1, column = i )

    def _on_hue_selection_changed( self, name, index, mode ):
        root = self.master
        while root.master is not None:
            root = root.master

        root.config( cursor = "watch" )
        root.update()
        COMPOSITOR.colorize_layer( self.layer, self.selected_hue.get() )
        root.config( cursor = "" )
        root.update()
