""" A SpriteLayer is the overall collection of individual frames (which may be spread across files) that define one layer of the final sprite.
"""

class SpriteLayer():
    def __init__( self ):
        self.name = ""
        self.layer = "Base"
        self.credit_name = "Artist Name"
        self.credit_url = "https://github.com/xaroth8088/sprite-magic"
        self.license = "Not specified (do not use this artwork without permission from the artist!)"
        self.actions = []
