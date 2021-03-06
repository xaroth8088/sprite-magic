""" A SpriteType is used to specify which SpriteLayers can be grouped.
"""
class SpriteType():
    def __init__( self, data, group_name ):
        self.group_name = group_name
        self.name = data.get( "name", "Default Type" )
        self.tile_width = data.get( "tile_width", 32 )
        self.tile_height = data.get( "tile_height", 32 )
        self._init_directions( data.get( "directions", [] ) )
        self._init_actions( data.get( "actions", [] ) )

    def _init_directions( self, data ):
        self.directions = []
        for direction in data:
            self.directions.append( direction )

    def _init_actions( self, data ):
        self.actions = []
        # TODO: error checking
        for raw_action in data:
            action = {}
            action["name"] = raw_action.get( "name", "Unnamed Action" )
            action["frames"] = raw_action.get( "frames", 1 )
            self.actions.append( action )

    def get_longest_action_length( self ):
        """ Gets the length of the longest action, as measured in number of frames.
        """
        max_len = 0
        for action in self.actions:
            if action["frames"] > max_len:
                max_len = action["frames"]

        return max_len

    def get_number_of_actions( self ):
        return len( self.actions )

    def get_number_of_directions( self ):
        return len( self.directions )
