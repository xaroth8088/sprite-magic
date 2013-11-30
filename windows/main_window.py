""" The controlling window for the application.
Serves as the hub for all other widgets.
"""
from Tkinter import *
from ttk import *

from widgets.selector import Selector

from windows.preview_window import PreviewWindow
from windows.licensing_window import LicensingWindow

class MainWindow( Tk ):
    def __init__( self ):
        Tk.__init__( self )

        # Set up the menu window
        self.title( "Sprite Magic" )
        self.geometry( '400x400+40+40' )

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

        filemenu.add_command( label = "Quit", accelerator = 'Ctrl+Q', command = self.quit, underline = 0 )
        self.bind_all( "<Control-q>", self.exit )

        menubar.add_cascade( label = "File", menu = filemenu )

        # View
        viewmenu = Menu( menubar, tearoff = 0 )
        viewmenu.add_command( label = "Preview", command = self.showPreview )
        viewmenu.add_command( label = "Licensing", command = self.showLicensing )

        menubar.add_cascade( label = "View", menu = viewmenu )

        # Make it active
        self.config( menu = menubar )

    def setupMainWindow( self ):
        self.selector = Selector( self )
        self.selector.grid()

    def showPreview( self ):
        self.preview_window = PreviewWindow( self )

    def showLicensing( self ):
        self.licensing_window = LicensingWindow( self )

    def exit( self, event ):
        self.quit()
