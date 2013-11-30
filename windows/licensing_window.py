""" A toplevel window to display licensing-related widgets
"""
from Tkinter import *
from ttk import *

from widgets.licensing import Licensing

class LicensingWindow( Toplevel ):
    def __init__( self, master ):
        Toplevel.__init__( self, master )

        self.geometry( "640x400+40-40" )
        self.transient( master )
        self.title( "License Information" )

        self.licensing_window = Licensing( self )
        self.licensing_window.pack( fill = BOTH, expand = True )
