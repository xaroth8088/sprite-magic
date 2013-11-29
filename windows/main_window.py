""" The controlling window for the application.
Serves as the hub for all other widgets.
"""
import Tkinter as tk

from widgets.licensing import Licensing
from widgets.preview import Preview
from widgets.selector import Selector

class MainWindow( tk.Tk ):
    def __init__( self ):
        tk.Tk.__init__( self )

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
        menubar = tk.Menu( self )

        # File
        filemenu = tk.Menu( menubar, tearoff = 0 )

        filemenu.add_command( label = "Quit", accelerator = 'Ctrl+Q', command = self.quit, underline = 0 )
        self.bind_all( "<Control-q>", self.exit )

        menubar.add_cascade( label = "File", menu = filemenu )

        # View
        viewmenu = tk.Menu( menubar, tearoff = 0 )
        viewmenu.add_command( label = "Preview", command = self.showPreview )
        viewmenu.add_command( label = "Licensing", command = self.showLicensing )

        menubar.add_cascade( label = "View", menu = viewmenu )

        # Make it active
        self.config( menu = menubar )

    def setupMainWindow( self ):
        self.selector = Selector( self )
        self.selector.grid()

    def showPreview( self ):
        window = tk.Toplevel( self )
        window.geometry( '400x400-40+40' )
        window.transient( self )
        window.title( "Preview" )
        self.preview_window = Preview( window )
        self.preview_window.grid()

    def showLicensing( self ):
        window = tk.Toplevel( self )
        window.geometry( "400x200+40-40" )
        window.transient( self )
        window.title( "License Information" )
        self.licensing_window = Licensing( window )
        self.licensing_window.grid()

    def exit( self, event ):
        self.quit()
