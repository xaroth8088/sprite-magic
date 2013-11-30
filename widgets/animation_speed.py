""" A widget for adjusting the speed of the animation preview
"""

from Tkinter import *
from ttk import *

from math import floor

from models.compositor import COMPOSITOR

class AnimationSpeed( Frame ):
    def __init__( self, master ):
        Frame.__init__( self, master )
        self._setup_view()

    def _setup_view( self ):
        label = Label( self, text = "Preview Speed" )
        label.grid()

        self.slider = Scale( self, from_ = COMPOSITOR.MIN_SPEED, to = COMPOSITOR.MAX_SPEED, orient = HORIZONTAL, command = self.on_slider_changed,
                                length = ( int )( floor( ( COMPOSITOR.MAX_SPEED - COMPOSITOR.MIN_SPEED ) / 2 ) ) )
        self.slider.set( COMPOSITOR.get_animation_speed() )
        self.slider.grid()

    def on_slider_changed( self, value ):
        COMPOSITOR.set_animation_speed( int( float( value ) ) )
