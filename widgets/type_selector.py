'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk

from models.spec_manager import GetAvailableTypes
import models.compositor

class TypeSelector():
    def __init__( self, master ):
        self.master = master
        models.compositor.RegisterView( self )

        self._setup_view()
        self.on_model_updated()

    def _setup_view( self ):
        temp = tk.Label( self.master, text = "Game Type" )
        temp.pack()

        self._setup_types()

    def _setup_types( self ):
        types = GetAvailableTypes()
        types = [data.name for data in types.values()]
        self.variable = tk.StringVar( self.master )
        self.variable.trace( 'w', self._on_type_selection_changed )
        self.variable.set( types[0] )  # default value

        type_menu = tk.OptionMenu( self.master, self.variable, *types )
        type_menu.pack()

    def _on_type_selection_changed( self, name, index, mode ):
        print "Setting type to: %s" % self.variable.get()
        models.compositor.SetSelectedType( self.variable.get() )

    def on_model_updated( self ):
        # TODO: The compositor changed state, so make sure we're up to date, too.
        pass

# TODO: Hook window close and deregister with the compositor
