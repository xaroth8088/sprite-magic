'''
Created on Nov 28, 2013

@author: Xaroth
'''

import Tkinter as tk

from models.compositor import COMPOSITOR

class add_layer( tk.Frame ):
    def __init__( self, master ):
        tk.Frame.__init__( self, master )
        self._setup_button()

    def _setup_button( self ):
        button = tk.Button( self, text = "+", command = self._on_add_pressed )
        button.pack()

    def _on_add_pressed( self ):
        COMPOSITOR.add_layer()
