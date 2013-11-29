""" The pane that handles selecting a type and layers
"""

import Tkinter as tk

from widgets.type_selector import TypeSelector
from widgets.sheet_selector import SheetSelector
from widgets.add_layer import AddLayer
import models.compositor

class Selector( tk.Frame ):
    def __init__( self, master ):
        tk.Frame.__init__( self, master )

        self.sheet_selectors = {}

        self._setup_controls()

        # Register for changes on the compositor
        models.compositor.RegisterView( self )

        self.on_model_updated()

    def on_model_updated( self ):
        # The compositor changed state, so make sure we're up to date, too.
        self._reorder_sheet_selectors()

    def _reorder_sheet_selectors( self ):
        selected_layers = models.compositor.GetSelectedLayers()

        # For each of our layers,
        layers_to_remove = []
        for layer in self.sheet_selectors.keys():
            # Check if it exists in the compositor.  If not, delete that layer.
            if layer not in selected_layers:
                layers_to_remove.append( layer )

        # actually delete the layers
        for layer in layers_to_remove:
            self.sheet_selectors.get( layer ).destroy()
            self.sheet_selectors.pop( layer )

        # For each layer in the compositor,
        row = 1
        for layer in selected_layers:
            # If the sheet_selector exists in our local state, re-attach it to the frame in the right spot
            if layer in self.sheet_selectors:
                self.sheet_selectors.get( layer ).grid( row = row, column = 0 )
            else:
                # Else, create a new sheet_selector for that layer, attach it to the frame.
                layer_selector = SheetSelector( self.sheet_selectors_frame, layer )
                layer_selector.grid( row = row, column = 0 )
                self.sheet_selectors[layer] = layer_selector

            row = row + 1

        # Hide if empty, or show if we have something
        if len( selected_layers ) > 0:
            self.sheet_selectors_frame.grid()
        else:
            self.sheet_selectors_frame.grid_remove()

    def _setup_controls( self ):
        self.type_selector = TypeSelector( self )
        self.type_selector.grid( row = 0, column = 0 )

        self.sheet_selectors_frame = tk.Frame( self )
        self.sheet_selectors_frame.grid( row = 1, column = 0 )

        self._add_layer = AddLayer( self )
        self._add_layer.grid( row = len( self.sheet_selectors ) + 2 )
