""" A SpriteAction represents the collection of frames for a given sprite action.
For example, it may contain the locations of the frames needed to render a walking animation, in 4 directions.
"""

from models.action_direction import ActionDirection

class SpriteAction():
    def __init__( self, data ):
        self.name = data.get( "name", "Default Action" )
        self.directions = {}
        avail_directions = data.get( "directions", [] )
        for direction_data in avail_directions:
            new_direction = ActionDirection( direction_data )
            self.directions[new_direction.name] = new_direction
