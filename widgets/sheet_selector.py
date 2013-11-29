""" A widget to select a sheet to use for a given layer.
"""

import Tkinter as tk

import models.compositor

class SheetSelector( tk.Frame ):
    def __init__( self, master, layer_name ):
        tk.Frame.__init__( self, master )
        self.layer_name = layer_name
        self._setup_title()
        self._setup_order_buttons()
        self._setup_optionmenu()
        self._setup_destroy_button()

    def _setup_title( self ):
        title = tk.Label( self, text = self.layer_name )
        title.grid( row = 0, column = 0 )

    def _setup_order_buttons( self ):
        button = tk.Button( self, command = self._on_up_pressed, text = "Up" )
        button.grid( row = 1, column = 0 )

        button = tk.Button( self, command = self._on_down_pressed, text = "Down" )
        button.grid( row = 1, column = 1 )

    def _setup_optionmenu( self ):
        layers = models.compositor.GetSheetsByLayer( self.layer_name ).keys()

        self.variable = tk.StringVar( self )
        self.variable.trace( 'w', self._on_layer_selection_changed )
        self.variable.set( layers[0] )

        layer_menu = tk.OptionMenu( self, self.variable, *layers )
        layer_menu.grid( row = 1, column = 2 )

    def _setup_destroy_button( self ):
        button = tk.Button( self, text = "X", command = self._on_destroy_button_pressed )
        button.grid( row = 1, column = 3 )

    def _on_layer_selection_changed( self, name, index, mode ):
        print "Layer selection: %s" % self.variable.get()

    def _on_up_pressed( self ):
        models.compositor.MoveLayerUp( self.layer_name )

    def _on_down_pressed( self ):
        models.compositor.MoveLayerDown( self.layer_name )

    def _on_destroy_button_pressed( self ):
        print "Removing layer: %s" % self.layer_name
        models.compositor.RemoveLayer( self.layer_name )
