""" This represents the location of the frames needed to render a given sprite in a given direction.
For example, the file and physical location needed to render a character walking to the left.
"""

class ActionDirection():
    def __init__( self, data ):
        self.name = data.get( "name", "Unnamed direction" )
        self.frames = []
        avail_frames = data.get( "frames", [] )
        for frame in avail_frames:
            self.frames.append(frame)
