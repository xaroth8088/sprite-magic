'''
Created on Nov 24, 2013

@author: Xaroth
'''

from Tkinter import *
from ttk import *
from ScrolledText import ScrolledText

from models.compositor import COMPOSITOR
from models.licensing import LICENSING

class Licensing( Frame ):
    BUTTON_TEXT = "Copy to clipboard"

    def __init__( self, master ):
        Frame.__init__( self, master )
        COMPOSITOR.register_view( self )
        self._setup_view()
        self.on_model_updated( COMPOSITOR.OTHER_UPDATED )

    def _setup_view( self ):
        self.rowconfigure( 0, weight = 1 )
        self.columnconfigure( 0, weight = 1 )

        self.license_box = ScrolledText( self, state = DISABLED )
        self.license_box.grid( row = 0, column = 0, sticky = W + E + N + S, padx = 5, pady = 5 )

        self.clipboard_button = Button( self, text = self.BUTTON_TEXT, command = self._on_copy_pressed )
        self.clipboard_button.grid( row = 1, column = 0, sticky = N + E )

    def _on_copy_pressed( self ):
        self.license_box.clipboard_clear()
        self.license_box.clipboard_append( self.license_box.get( '0.0', END ) )
        self.clipboard_button.configure( text = "Copied!", state = DISABLED )
        self.after( 2500, lambda: self.clipboard_button.configure( text = self.BUTTON_TEXT, state = NORMAL ) )

    def on_model_updated( self, reason ):
        if reason not in [COMPOSITOR.OTHER_UPDATED, COMPOSITOR.SELECTED_TYPE_CHANGED, COMPOSITOR.LAYER_ADDED, COMPOSITOR.LAYER_REMOVED, COMPOSITOR.SHEET_SELECTED]:
            return

        # The compositor changed state, so make sure we're up to date, too.
        self.license_box.configure( state = NORMAL )

        # clear the existing text
        self.license_box.delete( 1.0, END )

        sheets = COMPOSITOR.get_selected_sheets().values()
        license_text = LICENSING.get_formatted_licensing( sheets )

        self.license_box.insert( END, license_text )
        self.license_box.configure( state = DISABLED )

    def destroy( self ):
        COMPOSITOR.deregister_view( self )
        Frame.destroy( self )
