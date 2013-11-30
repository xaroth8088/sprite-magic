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

        self._setup_view()

    def _setup_view( self ):
        self.canvas = Canvas( self, borderwidth = 0 )
        self.frame = Frame( self.canvas )
        self.vsb = Scrollbar( self, orient = "vertical", command = self.canvas.yview )
        self.canvas.configure( yscrollcommand = self.vsb.set )

        self.vsb.pack( side = "right", fill = "y" )
        self.canvas.pack( side = "left", fill = BOTH, expand = True )
        self.canvas.create_window( ( 0, 0 ), window = self.frame, anchor = "nw",
                                  tags = "self.frame" )

        self.frame.bind( "<Configure>", self._on_window_resize )

        self.preview_window = Preview( self.frame )
        self.preview_window.pack( fill = BOTH, expand = True )

    def _on_window_resize( self, event ):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure( scrollregion = self.canvas.bbox( "all" ) )
