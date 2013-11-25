""" The controlling window for the application.
Serves as the hub for all other widgets.
"""
import Tkinter as tk

from widgets.selector import Selector
from widgets.licensing import Licensing
from widgets.preview import Preview
import models.compositor

class MainWindow( tk.Tk ):
    def __init__( self ):
        tk.Tk.__init__( self )

        # Set up the menu window
        self.title( "Sprite Magic" )
        self.resizable( False, False )

        # Menu bar for the main window
        self.setupMenuBar()

        # Register for changes on the compositor
        models.compositor.RegisterView( self )

        # Spawn windows for each major function
        self.showSelector()
        self.showPreview()
        self.showLicensing()

        # Setup of main window
        self.setupMainWindow()
        self.onModelUpdated()

    def onModelUpdated( self ):
        # TODO: The compositor changed state, so make sure we're up to date, too.
        pass

    def setupMenuBar( self ):
        menubar = tk.Menu( self )

        # File
        filemenu = tk.Menu( menubar, tearoff = 0 )

        filemenu.add_command( label = "Quit", accelerator = 'Ctrl+Q', command = self.quit, underline = 0 )
        self.bind_all( "<Control-q>", self.exit )

        menubar.add_cascade( label = "File", menu = filemenu )

        # View
        viewmenu = tk.Menu( menubar, tearoff = 0 )
        viewmenu.add_command( label = "Selector", command = self.showSelector )
        viewmenu.add_command( label = "Preview", command = self.showPreview )
        viewmenu.add_command( label = "Licensing", command = self.showLicensing )

        menubar.add_cascade( label = "View", menu = viewmenu )

        # Make it active
        self.config( menu = menubar )

    def setupMainWindow( self ):
        pass

    def showSelector( self ):
        window = tk.Toplevel( self )
        window.transient( self )
        self.selector_window = Selector( window )

    def showPreview( self ):
        window = tk.Toplevel( self )
        window.transient( self )
        self.preview_window = Preview( window )

    def showLicensing( self ):
        window = tk.Toplevel( self )
        window.transient( self )
        self.licensing_window = Licensing( window )

    def exit( self, event ):
        self.quit()
