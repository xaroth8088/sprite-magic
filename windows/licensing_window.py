""" A toplevel window to display licensing-related widgets
"""
from Tkinter import *
from ttk import *

from widgets.licensing import Licensing

class LicensingWindow( Toplevel ):
    def __init__( self, master ):
        Toplevel.__init__( self, master )

        self.geometry( "640x200-10-40" )
        self.transient( master )
        self.title( "Licensing and Attribution Information" )

        self.licensing_window = Licensing( self )
        self.licensing_window.pack( fill = BOTH, expand = True, padx = 5, pady = 5 )
