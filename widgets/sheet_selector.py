""" A widget to select a sheet to use for a given layer.
"""

import Tkinter as tk

import models.compositor

class SheetSelector( tk.Frame ):
    def __init__( self, master, layer_name ):
        tk.Frame.__init__( self, master )
        self.layer_name = layer_name
        self._setup_order_buttons()
        self._setup_optionmenu()

    def _setup_order_buttons( self ):
        button = tk.Button( self, command = self._on_up_pressed, text = "Up" )
        button.pack()

        button = tk.Button( self, command = self._on_down_pressed, text = "Down" )
        button.pack()

    def _setup_optionmenu( self ):
        layers = models.compositor.GetSheetsByLayer( self.layer_name ).keys()

        self.variable = tk.StringVar( self )
        self.variable.trace( 'w', self._on_layer_selection_changed )
        self.variable.set( layers[0] )

        layer_menu = tk.OptionMenu( self, self.variable, *layers )
        layer_menu.pack()

    def _on_layer_selection_changed( self, name, index, mode ):
        print "Layer selection: %s" % self.variable.get()

    def _on_up_pressed( self ):
        print "Up"

    def _on_down_pressed( self ):
        print "Down"
