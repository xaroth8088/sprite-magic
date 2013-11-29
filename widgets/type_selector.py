'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk

from models.spec_manager import GetAvailableTypes
from models.compositor import COMPOSITOR

class TypeSelector( tk.Frame ):
    def __init__( self, master ):
        tk.Frame.__init__( self, master )
        COMPOSITOR.RegisterView( self )

        self._setup_view()
        self.on_model_updated()

    def _setup_view( self ):
        temp = tk.Label( self, text = "Game Type" )
        temp.grid()

        self._setup_types()

    def _setup_types( self ):
        types = GetAvailableTypes()
        types = [data.name for data in types.values()]
        self.variable = tk.StringVar( self )
        self.variable.trace( 'w', self._on_type_selection_changed )
        self.variable.set( types[0] )  # default value

        type_menu = tk.OptionMenu( self, self.variable, *types )
        type_menu.grid()

    def _on_type_selection_changed( self, name, index, mode ):
        print "Setting type to: %s" % self.variable.get()
        COMPOSITOR.SetSelectedType( self.variable.get() )

    def on_model_updated( self ):
        # TODO: The compositor changed state, so make sure we're up to date, too.
        pass

# TODO: Hook window close and deregister with the compositor
