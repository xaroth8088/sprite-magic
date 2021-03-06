""" Gives a selectable list of available layers.
"""

from Tkinter import *
from ttk import *
from models.compositor import COMPOSITOR

class AvailableLayers( Frame ):
    def __init__( self, master ):
        Frame.__init__( self, master )
        self._setup_view()
        COMPOSITOR.register_view( self )

    def _setup_view( self ):
        button = Button( self, command = self._on_button_pressed, text = "Add Layer" )
        button.pack( side = BOTTOM, pady = 5 )
        scrollbar = Scrollbar( self, orient = VERTICAL )
        self.listbox = Listbox( self, yscrollcommand = scrollbar.set )
        scrollbar.config( command = self.listbox.yview )
        scrollbar.pack( side = RIGHT, fill = Y )
        self.listbox.pack( side = LEFT, fill = BOTH, expand = 1 )
        self.listbox.bind( "<Double-Button-1>", self._on_listbox_double_clicked )

        selected_layers = COMPOSITOR.get_selected_layers()
        for layer in COMPOSITOR.get_available_layers():
            if layer not in selected_layers:
                self.listbox.insert( END, layer )

    def _on_button_pressed( self ):
        COMPOSITOR.add_layer( self.listbox.selection_get() )

    def on_model_updated( self, reason ):
        if reason not in [COMPOSITOR.SELECTED_TYPE_CHANGED, COMPOSITOR.LAYER_ADDED, COMPOSITOR.LAYER_REMOVED]:
            return

        # The compositor changed state, so make sure we're up to date, too.
        for child in self.winfo_children():
            child.destroy()
        self._setup_view()

    def _on_listbox_double_clicked( self, event ):
        COMPOSITOR.add_layer( self.listbox.selection_get() )

    def destroy( self ):
        COMPOSITOR.deregister_view( self )
        Frame.destroy( self )
