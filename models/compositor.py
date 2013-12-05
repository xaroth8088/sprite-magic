""" The compositor is responsible for keeping track of which sprite layers the user wants to combine, and how.
"""

from collections import defaultdict
from PIL import Image
from math import floor
import tkFileDialog

import spec_manager
from models.image_manager import IMAGE_MANAGER

class _Compositor():
    MIN_SPEED = 10
    MAX_SPEED = 500

    def __init__( self ):
        self._selected_type = None  # Which sprite type has the user selected?
        self._selected_layers = []  # The layers that the user is actively looking at, in order
        self._animation_speed = ( int )( floor( ( self.MAX_SPEED + self.MIN_SPEED ) / 2 ) )  # Number of milliseconds between frames
        self._registered_views = []  # Which views want to know when we update?
        self._sprites = defaultdict( lambda: defaultdict( lambda: [] ) )  # PIL Image objects for each action and direction
        self._selected_sheets = {}  # The sprite_sheet objects that are presently active
        self._loaded = False

        # Ensure the spec manager actually has specs for us
        spec_manager.LoadSpecs()

    def register_view( self, view ):
        self._registered_views.append( view )

    def deregister_view( self, view ):
        self._registered_views.remove( view )

    def _notify_views( self ):
        for view in self._registered_views:
            view.on_model_updated()

    def set_selected_type( self, sprite_type_name ):
        self._selected_sheets = {}
        self._selected_layers = []
        self._selected_type = spec_manager.GetTypeByName( sprite_type_name )
        self._update_sprites()
        self._notify_views()

    def get_sheets_by_layer( self, layer_name ):
        layers = spec_manager.GetGroupSheetsByLayer( self._selected_type.group_name, layer_name )
        return layers

    def get_available_layers( self ):
        if self._selected_type is None:
            return []
        return spec_manager.GetGroupLayers( self._selected_type.group_name )

    def get_selected_layers( self ):
        return self._selected_layers

    def add_layer( self, layer ):
        if layer not in self._selected_layers:
                self._selected_layers.append( layer )
                sheets = self.get_sheets_by_layer( layer ).keys()
                self._selected_sheets[layer] = spec_manager.GetSheet( self._selected_type.group_name, layer, sheets[0] )

                self._update_sprites()
                self._notify_views()

    def remove_layer( self, layer_name ):
        self._selected_layers.pop( self._selected_layers.index( layer_name ) )
        self._selected_sheets.pop( layer_name )
        self._update_sprites()
        self._notify_views()

    def move_layer_up( self, layer_name ):
        self._move_layer( layer_name, -1 )

    def move_layer_down( self, layer_name ):
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

    def select_sheet( self, layer_name, sheet_name ):
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
                        right = left + self._selected_type.tile_width
                        bottom = top + self._selected_type.tile_height
                        cropped_image = raw_sheet.crop( ( left, top, right, bottom ) )
                        sprite.paste( cropped_image, ( 0, 0, self._selected_type.tile_width, self._selected_type.tile_height ), cropped_image )

                    # Add it to the collection of sprites
                    self._sprites[action["name"]][direction].append( sprite )

    def get_sprites( self, action, direction ):
        return self._sprites[action][direction]

    def get_animation_speed( self ):
        return self._animation_speed

    def set_animation_speed( self, speed ):
        self._animation_speed = speed

    def get_selected_type( self ):
        return self._selected_type

    def get_selected_sheets( self ):
        return self._selected_sheets

    def export_combined_sheet( self ):
        # Prompt for save file location
        file_path = self._get_save_location()
        if not file_path:
            return

        # Determine the best size for the sheet
        # Create the Image to hold the sprites
        export_sheet = self._create_export_sheet()

        # Format: Each action+direction will be one row, each frame one column
        row = 0
        column = 0
        sprite_width = self._selected_type.tile_width
        sprite_height = self._selected_type.tile_height

        # For each action,
        for action in self._selected_type.actions:
            # For each direction,
            for direction in self._selected_type.directions:
                # Get the sprites for this action + direction
                sprites = self.get_sprites( action["name"], direction )

                # For each sprite,
                for sprite in sprites:
                    # Add the layer to the Image for that frame
                    export_sheet.paste( sprite, ( column * sprite_width, row * sprite_height, ( column + 1 ) * sprite_width, ( row + 1 ) * sprite_height ) )
                    column = column + 1
                # Next row
                row = row + 1
                column = 0
        # Export the file
        export_sheet.save( file_path, "PNG" )

    def _create_export_sheet( self ):
        # Format: Each action+direction will be one row, each frame one column
        width = self._selected_type.tile_width * self._selected_type.get_longest_action_length()
        height = self._selected_type.tile_height * self._selected_type.get_number_of_actions() * self._selected_type.get_number_of_directions()

        sheet = Image.new( 'RGBA', ( width, height ) )
        return sheet

    def _get_save_location( self ):
        options = {}
        options['defaultextension'] = '.png'
        options['filetypes'] = [( 'PNG files', '.png' )]
        options['initialfile'] = 'exported_spritesheet.png'
        options['title'] = 'This is a title'

        return tkFileDialog.asksaveasfilename( **options )

# Instantiate the external-facing instance
COMPOSITOR = _Compositor()
