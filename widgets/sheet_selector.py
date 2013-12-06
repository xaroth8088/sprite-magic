""" A widget to select a sheet to use for a given layer.
"""

from Tkinter import *
from ttk import *

from widgets.hue_adjuster import HueAdjuster

from models.compositor import COMPOSITOR

class SheetSelector( Frame ):
    def __init__( self, master, layer_name ):
        Frame.__init__( self, master )
        self.layer_name = layer_name
        self._setup_title()
        self._setup_order_buttons()
        self._setup_optionmenu()
        self._setup_destroy_button()
        self._setup_color_adjusters()

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
        layers.insert( 0, "" )  # Need a blank entry at the head, otherwise ttk.OptionMenu will cause the first entry to disappear

        self.variable = StringVar( self )
        self.variable.set( layers[1] )

        layer_menu = OptionMenu( self, self.variable, *layers )
        layer_menu.grid( row = 1, column = 2 )
        self.variable.trace( 'w', self._on_layer_selection_changed )

    def _setup_destroy_button( self ):
        button = Button( self, text = "X", command = self._on_destroy_button_pressed )
        button.grid( row = 1, column = 3 )

    def _setup_color_adjusters( self ):
        adjuster = HueAdjuster( self, self.layer_name )
        adjuster.grid( row = 2, column = 0, columnspan = 4 )

    def _on_layer_selection_changed( self, name, index, mode ):
        COMPOSITOR.select_sheet( self.layer_name, self.variable.get() )

    def _on_up_pressed( self ):
        COMPOSITOR.move_layer_up( self.layer_name )

    def _on_down_pressed( self ):
        COMPOSITOR.move_layer_down( self.layer_name )

    def _on_destroy_button_pressed( self ):
        COMPOSITOR.remove_layer( self.layer_name )
