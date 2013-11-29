""" A SpriteSheet is the overall collection of individual frames (which may be spread across files) that define one layer of the final sprite.
"""

from models.sprite_action import SpriteAction

class SpriteSheet():
    def __init__( self, data, group_name ):
        if "file_path" not in data:
            raise "file_path element missing in layer.  Unable to load .spec file if we don't know which sheet you mean"

        self.file_path = data.get( "file_path" )
        self.group_name = group_name
        self.name = data.get( "name", "Unnamed Layer" )
        self.layer = data.get( "layer", "Unspecified Layer" )
        self.credit_name = data.get( "credit_name", "Unknown Artist" )
        self.credit_url = data.get( "credit_url", "" )
        self.license = data.get( "license", "Not specified (do not use this artwork without explicit written permission from the artist!)" )

        self.actions = {}
        avail_actions = data.get( "actions", [] )
        for action_data in avail_actions:
            new_action = SpriteAction( action_data )
            self.actions[new_action.name] = new_action
