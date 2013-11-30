""" Shows an animated preview of a sprite with a given action and direction.
"""

from Tkinter import *
from ttk import *
from PIL import Image, ImageTk

from models.compositor import COMPOSITOR

class PreviewAnimation( Frame ):
    def __init__( self, master, sprites ):
        Frame.__init__( self, master )

        self.frame_counter = 0
        self.sprites = []
        for frame in sprites:
            self.sprites.append( ImageTk.PhotoImage( frame ) )

        # TODO: pull the frame dimensions from the selected type
        self._setup_view()
        self._advance_frame()

    def _draw_frame( self ):
        # set our sprite into the label container
        # TODO: debug static frame
        frame_image = self.sprites[self.frame_counter % len( self.sprites )]
        self.label.configure( image = frame_image )
        self.label.image = frame_image  # keep a reference!

    def _advance_frame( self ):
        self.frame_counter = self.frame_counter + 1
        self._draw_frame()

        self.frame_label.configure( text = "Frame: %s" % ( self.frame_counter % len( self.sprites ) ) )

        self.after( COMPOSITOR.get_animation_speed(), self._advance_frame )  # Animate!

    def _setup_view( self ):
        self.label = Label( self )
        self.label.grid()

        self.frame_label = Label( self, text = "Frame:" )
        self.frame_label.grid()

        self._draw_frame()
