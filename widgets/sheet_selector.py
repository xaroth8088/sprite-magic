""" A widget to select a sheet to use for a given layer.
"""

from Tkinter import *
from ttk import *


from models.compositor import COMPOSITOR

class SheetSelector( Frame ):
    def __init__( self, master, layer_name ):
        Frame.__init__( self, master )
        self.layer_name = layer_name
        self._setup_title()
        self._setup_order_buttons()
        self._setup_optionmenu()
        self._setup_destroy_button()

    def _setup_title( self ):
        title = Label( self, text = self.layer_name )
        title.grid( row = 0, column = 0 )

    def _setup_order_buttons( self ):
        button = Button( self, command = self._on_up_pressed, text = "Up" )
        button.grid( row = 1, column = 0 )

        button = Button( self, command = self._on_down_pressed, text = "Down" )
        button.grid( row = 1, column = 1 )

    def _setup_optionmenu( self ):
        layers = COMPOSITOR.get_sheets_by_layer( self.layer_name ).keys()

        self.variable = StringVar( self )
        self.variable.set( layers[0] )

        layer_menu = OptionMenu( self, self.variable, *layers )
        layer_menu.grid( row = 1, column = 2 )
        self.variable.trace( 'w', self._on_layer_selection_changed )

    def _setup_destroy_button( self ):
        button = Button( self, text = "X", command = self._on_destroy_button_pressed )
        button.grid( row = 1, column = 3 )

    def _on_layer_selection_changed( self, name, index, mode ):
        print "Layer selection: %s" % self.variable.get()
        COMPOSITOR.select_sheet( self.layer_name, self.variable.get() )

    def _on_up_pressed( self ):
        COMPOSITOR.move_layer_up( self.layer_name )

    def _on_down_pressed( self ):
        COMPOSITOR.move_layer_down( self.layer_name )

    def _on_destroy_button_pressed( self ):
        print "Removing layer: %s" % self.layer_name
        COMPOSITOR.remove_layer( self.layer_name )
