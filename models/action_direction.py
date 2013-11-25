""" This represents the location of the frames needed to render a given sprite in a given direction.
For example, the file and physical location needed to render a character walking to the left.
"""

class ActionDirection():
    def __init__( self ):
        self.direction = "right"
        self.path = ""
        self.frames = []
