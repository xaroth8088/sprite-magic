""" A toplevel window to say what Sprite Magic is all about!
"""
from Tkinter import *
from ttk import *

from widgets.about import About

class AboutWindow( Toplevel ):
    def __init__( self, master ):
        Toplevel.__init__( self, master )

        self.geometry( "640x480-10-40" )
        self.transient( master )
        self.title( "About Sprite Magic" )

        self.about = About( self )
        self.about.pack( fill = BOTH, expand = True, padx = 5, pady = 5 )
