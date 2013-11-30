""" A toplevel window to display animation-preview-related widgets
"""

from Tkinter import *
from ttk import *

from widgets.preview import Preview

class PreviewWindow( Toplevel ):
    def __init__( self, master ):
        Toplevel.__init__( self, master )

        self.geometry( '400x400-40+40' )
        self.transient( master )
        self.title( "Preview" )

        self.preview_window = Preview( self )
        self.preview_window.grid()
