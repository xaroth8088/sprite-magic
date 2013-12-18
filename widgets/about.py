""" A widget to say what Sprite Magic is all about!
"""

from Tkinter import *
from ttk import *

from widgets.vertical_scrolled_frame import VerticalScrolledFrame
from models.licensing import LICENSING
from models.compositor import COMPOSITOR
from models.spec_manager import GetAllSheets

class About( Frame ):
    def __init__( self, master ):
        Frame.__init__( self, master )
        self._setup_view()

    def _setup_view( self ):
        self.right_frame = VerticalScrolledFrame( self )
        self.right_frame.pack( side = LEFT, fill = BOTH, expand = True )

        self.about_frame = Frame( self.right_frame.interior )
        self.about_frame.pack( fill = X, expand = True )
        self.about_frame.columnconfigure( 0, weight = 1 )

        label = Label( self.about_frame, text = "About Sprite Magic" )
        label.pack( pady = 30 )

        label = Label( self.about_frame, text = "Code Contributors" )
        label.pack( pady = 10 )

        label = Label( self.about_frame, text = "Geoffrey Benson" )
        label.pack()

        label = Label( self.about_frame, text = "Artwork used in the Sprite Magic UI itself" )
        label.pack( pady = 20 )

        label = Label( self.about_frame, text = "Arrow and X icons are under the public domain." )
        label.pack()

        label = Label( self.about_frame, text = "Artwork in the library" )
        label.pack( pady = 40 )

        # TODO: Format this nicer
        text = Text( self.about_frame )
        text.insert( END, self._get_licensing_info() )
        text.configure( state = DISABLED )
        text.pack( fill = BOTH, expand = True )

    def _get_licensing_info( self ):
        sheets = GetAllSheets()
        license_text = LICENSING.get_formatted_licensing( sheets )
        return license_text
