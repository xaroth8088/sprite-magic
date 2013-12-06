'''
Created on Nov 24, 2013

@author: Xaroth
'''

from Tkinter import *
from ttk import *


from models.spec_manager import GetAvailableTypes
from models.compositor import COMPOSITOR

class TypeSelector( Frame ):
    def __init__( self, master ):
        Frame.__init__( self, master )
        COMPOSITOR.register_view( self )

        self._setup_view()
        self.on_model_updated( COMPOSITOR.OTHER_UPDATED )

    def _setup_view( self ):
        temp = Label( self, text = "Game Type" )
        temp.grid()

        self._setup_types()

    def _setup_types( self ):
        types = GetAvailableTypes()
        types = [data.name for data in types.values()]
        self.variable = StringVar( self )

        types.insert( 0, "" )  # Need a blank entry at the head, otherwise ttk.OptionMenu will cause the first entry to disappear

        type_menu = OptionMenu( self, self.variable, *types )
        type_menu.grid()

        self.variable.trace( 'w', self._on_type_selection_changed )
        self.variable.set( types[1] )  # default value

    def _on_type_selection_changed( self, name, index, mode ):
        COMPOSITOR.set_selected_type( self.variable.get() )

    def on_model_updated( self, reason ):
        # TODO: The compositor changed state, so make sure we're up to date, too.

#         if reason not in [COMPOSITOR.SELECTED_TYPE_CHANGED, COMPOSITOR.LAYER_ADDED, COMPOSITOR.LAYER_REMOVED]:
#             return
        pass

# TODO: Hook window close and deregister with the compositor
