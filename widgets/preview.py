'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk


from widgets.preview_animation import PreviewAnimation
from models.compositor import COMPOSITOR

class Preview( tk.Frame ):
    def __init__( self, master ):
        tk.Frame.__init__( self, master )
        COMPOSITOR.RegisterView( self )
        self._setup_view()
        self.on_model_updated()

    def _setup_view( self ):
        temp = tk.Label( self, text = "preview pane goes here" )
        temp.grid()

        selected_type = COMPOSITOR.GetSelectedType()
        if selected_type is None:
            temp = tk.Label( self, text = "No type selected" )
            temp.grid()
            return

        for direction in selected_type.directions:
            for action in selected_type.actions:
                anim = PreviewAnimation( self, COMPOSITOR.GetSprites( action["name"], direction ) )
                anim.grid()

    def on_model_updated( self ):
        # TODO: The compositor changed state, so make sure we're up to date, too.
        for child in self.winfo_children():
            child.destroy()
        self._setup_view()

# TODO: Hook window close and deregister with the compositor
