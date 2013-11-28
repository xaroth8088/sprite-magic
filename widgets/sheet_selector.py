""" A widget to select a sheet to use for a given layer.
"""

import Tkinter as tk

import models.compositor

class SheetSelector():
    def __init__( self, master, layer_name ):
        self.master = master
        self.layer_name = layer_name
        self._setup_optionmenu()

    def _setup_optionmenu( self ):
        layers = models.compositor.GetSheetsByLayer( self.layer_name ).keys()

        self.variable = tk.StringVar( self.master )
        self.variable.trace( 'w', self._on_layer_selection_changed )
        self.variable.set( layers[0] )

        layer_menu = tk.OptionMenu( self.master, self.variable, *layers )
        layer_menu.pack()

    def _on_layer_selection_changed( self, name, index, mode ):
        print "Layer selection: %s" % self.variable.get()
