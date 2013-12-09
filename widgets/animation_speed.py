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
        label.grid( row = 0, column = 0, sticky = W )

        self.fps_label = Label( self, text = "" )
        self.fps_label.grid( row = 0, column = 1, sticky = W + E )

        self.slider = Scale( self, from_ = COMPOSITOR.MIN_FPS, to = COMPOSITOR.MAX_FPS, orient = HORIZONTAL, command = self.on_slider_changed,
                             length = 200 )
        self.slider.set( int( floor( 1000.0 / float( COMPOSITOR.get_animation_speed() ) ) ) )
        self.slider.grid( row = 1, column = 0, columnspan = 2, sticky = W + E )

    def on_slider_changed( self, value ):
        fps = int( float( value ) )
        COMPOSITOR.set_animation_speed( fps )
        self.fps_label.configure( text = str( fps ) + " FPS" )
