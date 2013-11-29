""" The pane that handles selecting a type and layers
"""

import Tkinter as tk

from widgets.type_selector import TypeSelector
from widgets.sheet_selector import SheetSelector
import models.compositor

class Selector( tk.Frame ):
    def __init__( self, master ):
        tk.Frame.__init__( self, master )

        # Register for changes on the compositor
        models.compositor.RegisterView( self )

        self._setup_controls()

        self.on_model_updated()

    def on_model_updated( self ):
        # TODO: The compositor changed state, so make sure we're up to date, too.
        pass

    def _setup_controls( self ):
        self.type_selector = TypeSelector( self )
        self.type_selector.pack()

        # TODO: DEBUG
        layers = models.compositor.GetAvailableLayers()
        self.layer_selector = SheetSelector( self, layers[0] )
        self.layer_selector.pack()
