""" The compositor is responsible for keeping track of which sprite layers the user wants to combine, and how.
"""

from collections import defaultdict
from PIL import Image

import spec_manager
from models.image_manager import IMAGE_MANAGER

class _Compositor():
    def __init__( self ):
        self._selected_type = None  # Which sprite type has the user selected?
        self._selected_layers = []  # The layers that the user is actively looking at, in order
        self._animation_speed = 60  # Number of milliseconds between frames
        self._registered_views = []  # Which views want to know when we update?
        self._sprites = defaultdict( lambda: defaultdict( lambda: [] ) )  # PIL Image objects for each action and direction
        self._selected_sheets = {}  # The sprite_sheet objects that are presently active
        self._loaded = False

        # Ensure the spec manager actually has specs for us
        spec_manager.LoadSpecs()

    def RegisterView( self, view ):
        self._registered_views.append( view )

    def DeregisterView( self, view ):
        self._registered_views.remove( view )

    def _notify_views( self ):
        for view in self._registered_views:
            view.on_model_updated()

    def SetSelectedType( self, sprite_type_name ):
        self._selected_sheets = {}
        self._selected_layers = []
        self._selected_type = spec_manager.GetTypeByName( sprite_type_name )
        self._update_sprites()
        self._notify_views()

    def GetSheetsByLayer( self, layer_name ):
        layers = spec_manager.GetGroupSheetsByLayer( self._selected_type.group_name, layer_name )
        return layers

    def GetAvailableLayers( self ):
        return spec_manager.GetGroupLayers( self._selected_type.group_name )

    def GetSelectedLayers( self ):
        return self._selected_layers

    def AddLayer( self ):
        # Add the next available layer from the spec_manager that we don't already have
        all_layers = spec_manager.GetGroupLayers( self._selected_type.group_name )
        for layer in all_layers:
            if layer not in self._selected_layers:
                # Add the selected layer and pick a default selected sheet for that layer
                self._selected_layers.append( layer )
                sheets = self.GetSheetsByLayer( layer ).keys()
                self._selected_sheets[layer] = spec_manager.GetSheet( self._selected_type.group_name, layer, sheets[0] )

                self._update_sprites()
                self._notify_views()
                return

    def RemoveLayer( self, layer_name ):
        self._selected_layers.pop( self._selected_layers.index( layer_name ) )
        self._selected_sheets.pop( layer_name )
        self._update_sprites()
        self._notify_views()

    def MoveLayerUp( self, layer_name ):
        self._move_layer( layer_name, -1 )

    def MoveLayerDown( self, layer_name ):
        self._move_layer( layer_name, 1 )

    def _move_layer( self, layer_name, direction ):
        # Get our two indices to swap
        i = self._selected_layers.index( layer_name )
        j = i + direction

        # Don't move past the beginning or end of the list
        if j < 0:
            return

        if j >= len( self._selected_layers ):
            return

        self._selected_layers[i], self._selected_layers[j] = self._selected_layers[j], self._selected_layers[i]

        self._update_sprites()
        self._notify_views()

    def SelectSheet( self, layer_name, sheet_name ):
        self._selected_sheets[layer_name] = spec_manager.GetSheet( self._selected_type.group_name, layer_name, sheet_name )
        self._update_sprites()
        self._notify_views()

    def _update_sprites( self ):
        self._sprites = defaultdict( lambda: defaultdict( lambda: [] ) )

        # For each action in the selected type,
        for action in self._selected_type.actions:
            # For each direction in the action,
            for direction in self._selected_type.directions:
                # For each frame:
                for frame in range( 0, action["frames"] ):
                    # Make a new Image to store the sprite frame
                    sprite = Image.new( "RGBA", ( self._selected_type.tile_width, self._selected_type.tile_height ) )

                    # For each selected layer:
                    for layer in self._selected_layers:
                        selected_sheet = self._selected_sheets[layer]
                        if selected_sheet is None:
                            continue
                        # Load the raw spritesheet image
                        image_name = selected_sheet.file_path
                        path = "assets/%s/%s" % ( self._selected_type.group_name, image_name )
                        raw_sheet = IMAGE_MANAGER.get_image( path )

                        # Composite the layer sprite onto the frame image

                        # Pull out the Xth x Yth frame to display
                        left = selected_sheet.actions[action["name"]].directions[direction].frames[frame][0] * self._selected_type.tile_width
                        top = selected_sheet.actions[action["name"]].directions[direction].frames[frame][1] * self._selected_type.tile_height
                        right = left + self._selected_type.tile_width - 1
                        bottom = top + self._selected_type.tile_height - 1
                        cropped_image = raw_sheet.crop( ( left, top, right, bottom ) )
                        sprite.paste( cropped_image, ( 0, 0, self._selected_type.tile_width - 1, self._selected_type.tile_height - 1 ), cropped_image )

                    # Add it to the collection of sprites
                    self._sprites[action["name"]][direction].append( sprite )

    def GetSprites( self, action, direction ):
        return self._sprites[action][direction]

    def GetAnimationSpeed( self ):
        return self._animation_speed

    def GetSelectedType( self ):
        return self._selected_type

    def GetSelectedSheets( self ):
        return self._selected_sheets

# Instantiate the external-facing instance
COMPOSITOR = _Compositor()
