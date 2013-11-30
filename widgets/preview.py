'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk


from widgets.preview_action import PreviewAction
from models.compositor import COMPOSITOR

class Preview( tk.Frame ):
    def __init__( self, master ):
        tk.Frame.__init__( self, master )
        COMPOSITOR.register_view( self )
        self._setup_view()
        self.on_model_updated()

    def _setup_view( self ):
        selected_type = COMPOSITOR.get_selected_type()
        if selected_type is None:
            temp = tk.Label( self, text = "No type selected" )
            temp.grid()
            return

        for action in selected_type.actions:
            anim = PreviewAction( self, action )
            anim.grid()

    def on_model_updated( self ):
        # TODO: The compositor changed state, so make sure we're up to date, too.
        for child in self.winfo_children():
            child.destroy()
        self._setup_view()

# TODO: Hook window close and deregister with the compositor
