'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk

from widgets.Selector import Selector
from widgets.Licensing import Licensing
from widgets.Preview import Preview

class App( tk.Tk ):
    def __init__( self ):
        tk.Tk.__init__( self )

        # Set up the menu window
        self.title( "Sprite Magic" )
        self.resizable( False, False )

        # Menu bar for the main window
        self.setupMenuBar()

        # Spawn windows for each major function
        self.showSelector()
        self.showPreview()
        self.showLicensing()

    def setupMenuBar( self ):
        menubar = tk.Menu( self )

        # File
        filemenu = tk.Menu( menubar, tearoff = 0 )

        filemenu.add_command( label = "Quit", accelerator = 'Ctrl+Q', command = self.quit, underline = 0 )
        self.bind_all( "<Control-q>", self.exit )

        menubar.add_cascade( label = "File", menu = filemenu )

        # View
        viewmenu = tk.Menu( menubar, tearoff = 1 )
        viewmenu.add_command( label = "Selector", command = self.showSelector )
        viewmenu.add_command( label = "Preview", command = self.showPreview )
        viewmenu.add_command( label = "Licensing", command = self.showLicensing )

        menubar.add_cascade( label = "View", menu = viewmenu )

        # Make it active
        self.config( menu = menubar )

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

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
