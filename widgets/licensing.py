'''
Created on Nov 24, 2013

@author: Xaroth
'''

from Tkinter import *
from ttk import *
from ScrolledText import ScrolledText
from collections import defaultdict

from models.compositor import COMPOSITOR

class Licensing( Frame ):
    def __init__( self, master ):
        Frame.__init__( self, master )
        COMPOSITOR.register_view( self )
        self._setup_view()
        self.on_model_updated( COMPOSITOR.OTHER_UPDATED )

    def _setup_view( self ):
        self.rowconfigure( 0, weight = 1 )
        self.columnconfigure( 0, weight = 1 )

        self.license_box = ScrolledText( self )
        self.license_box.grid( row = 0, column = 0, sticky = W + E + N + S, padx = 5, pady = 5 )

        button = Button( self, text = "Copy to clipboard", command = self._on_copy_pressed )
        button.grid( row = 1, column = 0, sticky = N + E )

    def _on_copy_pressed( self ):
        self.license_box.clipboard_clear()
        self.license_box.clipboard_append( self.license_box.get( '0.0', END ) )

    def on_model_updated( self, reason ):
        if reason not in [COMPOSITOR.OTHER_UPDATED, COMPOSITOR.SELECTED_TYPE_CHANGED, COMPOSITOR.LAYER_ADDED, COMPOSITOR.LAYER_REMOVED, COMPOSITOR.SHEET_SELECTED]:
            return

        # The compositor changed state, so make sure we're up to date, too.

        # clear the existing text
        self.license_box.delete( 1.0, END )

        # Organize the license information for display
        licenses = defaultdict( lambda:
            defaultdict( lambda: [] )
        )

        sheets = COMPOSITOR.get_selected_sheets()
        for sheet in sheets.values():
            key = ( sheet.credit_name, sheet.credit_url )
            licenses[sheet.license][key].append( sheet.name )

        # Construct and display the combined license text
        license_text = ""
        for art_license in licenses:
            license_text += "The following artwork is used by permission in accordance with %s:\n" % ( art_license, )
            for key in licenses[art_license]:
                credit, url = key
                license_text += "    Artwork by %s ( %s ):\n        " % ( credit, url )
                license_text += ', '.join( licenses[art_license][( credit, url )] )
                license_text += "\n"
            license_text += "\n"

        self.license_box.insert( END, license_text )

    def destroy( self ):
        COMPOSITOR.deregister_view( self )
        Frame.destroy( self )
