""" Handles loading .spec files from disk and translating into the appropriate type or layer objects.
"""

import glob
import json
import os
from collections import defaultdict

from models.sprite_sheet import SpriteSheet
from sprite_type import SpriteType

_SHEETS = None
_TYPES = None

def LoadSpecs():
    global _SHEETS
    global _TYPES

    _SHEETS = defaultdict( lambda: defaultdict( lambda: {} ) )
    _TYPES = {}

    # In assets/types, load each .spec file
    for filename in glob.glob( 'assets/*/*.spec' ):
        _LoadSpec( filename )

def _LoadSpec( filename ):
    # Read in the file
    json_data = open( filename )

    # Parse as JSON
    try:
        data = json.load( json_data )
    except Exception as err:
        print "Unable to load .spec file (%s): %s" % ( err, filename )
        json_data.close()
        return

    # Close file
    json_data.close()

    # Determine which key we'll put this under
    group_name = filename.split( os.sep )[1]

    # If sheets are present, create SpriteSheet objects and organize them into layers
    if "sheets" in data:
        for sheet_data in data["sheets"]:
            sprite_sheet = SpriteSheet( sheet_data, group_name )
            _SHEETS[group_name][sprite_sheet.layer][sprite_sheet.name] = sprite_sheet

    # If a type is enclosed, create a new SpriteType object with that data
    if "type" in data:
        sprite_type = SpriteType( data["type"], group_name )
        _TYPES[sprite_type.name] = sprite_type

def GetGroupSheetsByLayer( group_name, layer_name ):
    return _SHEETS[group_name][layer_name]

def GetGroupLayers( group_name ):
    return _SHEETS[group_name].keys()

def GetTypeByName( type_name ):
    return _TYPES[type_name]

def GetAvailableTypes():
    global _TYPES
    return _TYPES

def GetSheet( group_name, layer_name, sheet_name ):
    global _SHEETS
    return _SHEETS[group_name][layer_name][sheet_name]
