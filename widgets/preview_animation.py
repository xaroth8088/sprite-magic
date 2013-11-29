""" Shows an animated preview of a sprite with a given action and direction.
"""

import Tkinter as tk
from PIL import Image, ImageTk

from models.compositor import COMPOSITOR

class PreviewAnimation( tk.Frame ):
    def __init__( self, master, sprites ):
        tk.Frame.__init__( self, master )
        self.sprites = []
        for frame in sprites:
            self.sprites.append( ImageTk.PhotoImage( frame ) )

        # TODO: pull the frame dimensions from the selected type
        self.speed = COMPOSITOR.GetAnimationSpeed()
        self._setup_view()

    def _draw_frame( self ):
        # set our sprite into the label container
        # TODO: debug static frame
        frame_image = self.sprites[0]
        self.label.configure( image = frame_image )
        self.label.image = frame_image  # keep a reference!

    def _setup_view( self ):
        self.label = tk.Label( self )
        self.label.grid()
        self._draw_frame()
