""" Handles loading .spec files from disk and translating into the appropriate type or layer objects.
"""

import glob
import json

from models.sprite_layer import SpriteLayer
from sprite_type import SpriteType

_LAYERS = {}
_TYPES = []

def LoadSpecs():
    global _LAYERS
    global _TYPES
    
    _LAYERS = {}
    _TYPES = []

    # In assets/types, load each .spec file
    for filename in glob.glob('assets/*/*.spec'):
        _LoadSpec(filename)

def _LoadSpec(filename):
    # Read in the file
    json_data = open(filename)

    # Parse as JSON
    try:
        data = json.load(json_data)
    except Exception as err:
        print "Unable to load .spec file (%s): %s" % (err, filename)
        json_data.close()
        return

    # Close file
    json_data.close()

    # If layers are present, create a new SpriteType object with that data for each layer
    if "layers" in data:
        for layer_data in data["layers"]:
            print "Loading layer spec: ", filename
            sprite_layer = SpriteLayer(layer_data)
            _LAYERS[sprite_layer.name] = sprite_layer

    # If a type is enclosed, create a new SpriteType object with that data
    if "type" in data:
        print "Loading type spec: ", filename
        sprite_type = SpriteType( data["type"] )
        _TYPES.append(sprite_type)


def GetAvailableLayers():
    global _LAYERS
    return _LAYERS

def GetAvailableTypes():
    global _TYPES
    return _TYPES
