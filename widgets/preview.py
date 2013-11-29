'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk

import models.compositor

class Preview( tk.Frame ):
    def __init__( self, master ):
        tk.Frame.__init__( self, master )
        models.compositor.RegisterView( self )
        self._setup_view()
        self.on_model_updated()

    def _setup_view( self ):
        temp = tk.Label( self, text = "preview pane goes here" )
        temp.pack()

    def on_model_updated( self ):
        # TODO: The compositor changed state, so make sure we're up to date, too.
        pass

# TODO: Hook window close and deregister with the compositor
