""" Responsible for maintaining the list of available types.
Looks in assets/types and loads/parses all .spec files there.
"""
import glob
import json

from sprite_type import SpriteType

_TYPES = []

def LoadTypes():
    global _TYPES
    _TYPES = []
    # In assets/types, load each .spec file
    for filename in glob.glob( 'assets/types/*.spec' ):
        _LoadSpec( filename )

def _LoadSpec( filename ):
    global _TYPES
    # Read in the file
    json_data=open(filename)

    # Parse as JSON
    try:
        data = json.load(json_data)
    except Exception as err:
        print "Unable to load .spec file (%s): %s" % ( err, filename )
        json_data.close()
        return

    # Close file
    json_data.close()

    # Create a new SpriteType object with that data
    sprite_type = SpriteType( data )
    _TYPES.append(sprite_type)

def GetAvailableTypes():
    global _TYPES
    return _TYPES
