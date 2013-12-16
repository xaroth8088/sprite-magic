""" The pane that handles selecting a type and layers
"""

from Tkinter import *
from ttk import *

from widgets.sheet_selector import SheetSelector
from widgets.animation_speed import AnimationSpeed
from widgets.available_layers import AvailableLayers
from widgets.vertical_scrolled_frame import VerticalScrolledFrame
from models.compositor import COMPOSITOR

class Selector( Frame ):
    def __init__( self, master ):
        Frame.__init__( self, master )

        self.sheet_selectors = {}
        self.warning = None

        self._setup_controls()

        # Register for changes on the compositor
        COMPOSITOR.register_view( self )

        self.on_model_updated( COMPOSITOR.OTHER_UPDATED )

    def on_model_updated( self, reason ):
        if reason not in [COMPOSITOR.OTHER_UPDATED, COMPOSITOR.SELECTED_TYPE_CHANGED, COMPOSITOR.LAYER_ADDED, COMPOSITOR.LAYER_REMOVED, COMPOSITOR.LAYER_ORDER_CHANGED]:
            return

        # Add a layer by default
        if reason == COMPOSITOR.SELECTED_TYPE_CHANGED:
            self._add_default_layer()

        # The compositor changed state, so make sure we're up to date, too.
        self._reorder_sheet_selectors()

    # Add a layer by default.  Prefer "base", then "body", else first one we find.
    def _add_default_layer( self ):
        layers = COMPOSITOR.get_available_layers()
        if "base" in layers:
            COMPOSITOR.add_layer( "base" )
        elif "body" in layers:
            COMPOSITOR.add_layer( "body" )
        else:
            COMPOSITOR.add_layer( layers[0] )


    def _reorder_sheet_selectors( self ):
        selected_layers = COMPOSITOR.get_selected_layers()

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

        # Show a message if no type has been selected
        if self.warning is not None:
            self.warning.destroy()
            self.warning = None

        if COMPOSITOR.get_selected_type() == None:
            self.warning = Label( self.sheet_selectors_frame, text = "Select a Game Type to get started!" )
            self.warning.pack()
            return
        elif len( selected_layers ) == 0:
            self.warning = Label( self.sheet_selectors_frame, text = "Add layers to make your sprites" )
            self.warning.pack()
            return

        # For each layer in the compositor,
        row = 1
        for layer in selected_layers:
            # If the sheet_selector exists in our local state, re-attach it to the frame in the right spot
            if layer in self.sheet_selectors:
                self.sheet_selectors.get( layer ).grid( row = row, column = 0, sticky = E + W )
            else:
                # Else, create a new sheet_selector for that layer, attach it to the frame.
                layer_selector = SheetSelector( self.sheet_selectors_frame, layer )
                layer_selector.grid( row = row, column = 0, sticky = E + W )
                self.sheet_selectors[layer] = layer_selector

            row = row + 1

    def _setup_controls( self ):
        # Left frame
        self.left_frame = Frame( self, padding = 5 )
        self.left_frame = Frame( self )
        self.left_frame.pack( side = LEFT, fill = Y )

        speed_control = AnimationSpeed( self.left_frame )
        speed_control.pack( fill = X )

        self.avail_layers = AvailableLayers( self.left_frame )
        self.avail_layers.pack( fill = BOTH, expand = True )

        # Right frame
        self.right_frame = VerticalScrolledFrame( self )
        self.right_frame.pack( side = LEFT, fill = BOTH, expand = True )

        self.sheet_selectors_frame = Frame( self.right_frame.interior )
        self.sheet_selectors_frame.pack( fill = X, expand = True )
        self.sheet_selectors_frame.columnconfigure( 0, weight = 1 )

    def destroy( self ):
        COMPOSITOR.deregister_view( self )
        Frame.destroy( self )
