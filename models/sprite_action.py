""" A SpriteAction represents the collection of frames for a given sprite action.
For example, it may contain the locations of the frames needed to render a walking animation, in 4 directions.
"""

class SpriteAction():
    def __init__( self ):
        self.name = "Default Action"
        self.directions = []
