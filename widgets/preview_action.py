""" A widget with all the directions for a given action represented
"""

import Tkinter as tk

from models.compositor import COMPOSITOR
from widgets.preview_animation import PreviewAnimation

class PreviewAction( tk.Frame ):
    def __init__( self, master, action ):
        tk.Frame.__init__( self, master )
        self.action = action
        self._setup_view()

    def _setup_view( self ):
        selected_type = COMPOSITOR.get_selected_type()
        if selected_type is None:
            temp = tk.Label( self, text = "No type selected" )
            temp.grid()
            return

        label = tk.Label( self, text = self.action["name"] )
        label.grid( row = 0, column = 0 )

        column = 0
        for direction in selected_type.directions:
            label = tk.Label( self, text = direction )
            label.grid( row = 1, column = column )

            anim = PreviewAnimation( self, COMPOSITOR.get_sprites( self.action["name"], direction ) )
            anim.grid( row = 2, column = column )

            column = column + 1
