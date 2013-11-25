""" A SpriteType is used to specify which SpriteLayers can be grouped.
"""
class SpriteType():
    def __init__( self ):
        self.name = "Default Type"
        self.tile_width = 32
        self.tile_height = 32
        self.directions = 4
        self.actions = []

