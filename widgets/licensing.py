'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk

from models.compositor import COMPOSITOR

class Licensing( tk.Frame ):
    def __init__( self, master ):
        tk.Frame.__init__( self, master )
        COMPOSITOR.register_view( self )
        self._setup_view()
        self.on_model_updated()

    def _setup_view( self ):
        label = tk.Label( self, text = "Licensing and Attribution Information" )
        label.grid()
        self.license_box = tk.Text( self, state = tk.DISABLED )
        self.license_box.grid()

    def on_model_updated( self ):
        # The compositor changed state, so make sure we're up to date, too.
        self.license_box.configure( state = tk.NORMAL )
        self.license_box.delete( 1.0, tk.END )
        license_texts = {}
        sheets = COMPOSITOR.get_selected_sheets()
        for sheet in sheets.values():
            license_texts["'%s' by %s ( %s ).  Used under license (%s)." % ( sheet.name, sheet.credit_name, sheet.credit_url, sheet.license )] = True
        self.license_box.insert( tk.END, "\n".join( license_texts.keys() ) )
        self.license_box.configure( state = tk.DISABLED )

# TODO: Hook window close and deregister with the compositor
