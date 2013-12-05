'''
Created on Nov 24, 2013

@author: Xaroth
'''

from Tkinter import *
from ttk import *

from widgets.preview_action import PreviewAction
from models.compositor import COMPOSITOR

class Preview( Frame ):
    def __init__( self, master ):
        Frame.__init__( self, master )
        COMPOSITOR.register_view( self )
        self._setup_view()
        self.on_model_updated()

    def _setup_view( self ):
        selected_type = COMPOSITOR.get_selected_type()
        if selected_type is None:
            temp = Label( self, text = "No type selected" )
            temp.grid()
            return

        for action in selected_type.actions:
            anim = PreviewAction( self, action )
            anim.grid()

    def on_model_updated( self ):
        # The compositor changed state, so make sure we're up to date, too.
        for child in self.winfo_children():
            child.destroy()
        self._setup_view()

# TODO: Hook window close and deregister with the compositor
