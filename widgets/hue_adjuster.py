""" A control to permit adjusting the hue of a given sprite
"""

""" A widget for adjusting the speed of the animation preview
"""

from Tkinter import *
from ttk import *

from models.compositor import COMPOSITOR
from functools import partial

class HueAdjuster( Frame ):
    def __init__( self, master, layer ):
        Frame.__init__( self, master )
        self.layer = layer
        self._setup_view()

    def _setup_view( self ):
        label = Label( self, text = "Hue" )
        label.grid( row = 0, column = 0 )

        for i in range( 0, 6 ):
            button = Button( self, command = partial( self._on_button_pressed, ( i * 60 ) ), text = ( i * 60 ) )
            button.grid( row = 1, column = i )

    def _on_button_pressed( self, value ):
        COMPOSITOR.colorize_layer( self.layer, value )
