'''
Created on Nov 28, 2013

@author: Xaroth
'''

from Tkinter import *
from ttk import *


from models.compositor import COMPOSITOR

class add_layer( Frame ):
    def __init__( self, master ):
        Frame.__init__( self, master )
        self._setup_button()

    def _setup_button( self ):
        button = Button( self, text = "+", command = self._on_add_pressed )
        button.pack()

    def _on_add_pressed( self ):
        COMPOSITOR.add_layer()
