'''
Created on Nov 24, 2013

@author: Xaroth
'''

from Tkinter import *
from ttk import *
from ScrolledText import ScrolledText

from models.compositor import COMPOSITOR

class Licensing( Frame ):
    def __init__( self, master ):
        Frame.__init__( self, master )
        COMPOSITOR.register_view( self )
        self._setup_view()
        self.on_model_updated( COMPOSITOR.OTHER_UPDATED )

    def _setup_view( self ):
        label = Label( self, text = "Licensing and Attribution Information" )
        label.grid()

        self.license_box = ScrolledText( self )
        self.license_box.grid()

    def on_model_updated( self, reason ):
        if reason not in [COMPOSITOR.OTHER_UPDATED, COMPOSITOR.SELECTED_TYPE_CHANGED, COMPOSITOR.LAYER_ADDED, COMPOSITOR.LAYER_REMOVED, COMPOSITOR.SHEET_SELECTED]:
            return

        # The compositor changed state, so make sure we're up to date, too.
        self.license_box.delete( 1.0, END )
        license_texts = {}
        sheets = COMPOSITOR.get_selected_sheets()
        for sheet in sheets.values():
            license_texts["'%s' by %s ( %s ).  Used under license (%s)." % ( sheet.name, sheet.credit_name, sheet.credit_url, sheet.license )] = True
        self.license_box.insert( END, "\n".join( license_texts.keys() ) )

# TODO: Hook window close and deregister with the compositor
