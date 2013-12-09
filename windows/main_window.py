""" The controlling window for the application.
Serves as the hub for all other widgets.
"""
from Tkinter import *
from ttk import *
from functools import partial

from widgets.selector import Selector
from windows.preview_window import PreviewWindow
from windows.licensing_window import LicensingWindow
from models.spec_manager import GetAvailableTypes
from models.compositor import COMPOSITOR

class MainWindow( Tk ):
    def __init__( self ):
        Tk.__init__( self )

        # Set up the menu window
        self.title( "Sprite Magic" )
        self.geometry( '710x800+10+10' )

        # Menu bar for the main window
        self.setupMenuBar()

        # Spawn windows for each major function
        self.showPreview()
        self.showLicensing()

        # Setup of main window
        self.setupMainWindow()

    def setupMenuBar( self ):
        menubar = Menu( self )

        # File
        filemenu = Menu( menubar, tearoff = 0 )

        filemenu.add_command( label = "Export combined sheet", accelerator = 'Ctrl+S', command = self._on_export_combined )
        self.bind_all( "<Control-s>", lambda arg: self._on_export_combined() )
        filemenu.add_separator()
        filemenu.add_command( label = "Quit", accelerator = 'Ctrl+Q', command = self.quit, underline = 0 )
        self.bind_all( "<Control-q>", self.exit )

        menubar.add_cascade( label = "File", menu = filemenu )

        # View
        viewmenu = Menu( menubar, tearoff = 0 )
        viewmenu.add_command( label = "Preview", command = self.showPreview )
        viewmenu.add_command( label = "Licensing", command = self.showLicensing )

        menubar.add_cascade( label = "View", menu = viewmenu )

        # Game Types
        typesmenu = Menu( menubar, tearoff = 0 )
        types = GetAvailableTypes()
        types = [data.name for data in types.values()]
        for game_type in types:
            typesmenu.add( "radiobutton", label = game_type, command = partial( self._on_type_selection_changed, game_type ) )

        menubar.add_cascade( label = "Game Types", menu = typesmenu )

        # Make it active
        self.config( menu = menubar )

    def _on_type_selection_changed( self, game_type ):
        COMPOSITOR.set_selected_type( game_type )

    def _on_export_combined( self ):
        COMPOSITOR.export_combined_sheet()

    def setupMainWindow( self ):
        self.selector = Selector( self )
        self.selector.pack( fill = BOTH, expand = True )

    def showPreview( self ):
        self.preview_window = PreviewWindow( self )

    def showLicensing( self ):
        self.licensing_window = LicensingWindow( self )

    def exit( self, event ):
        self.quit()
