""" Acts as an in-memory cache for PIL Image objects, to reduce how much we have to go to disk.
"""

from PIL import Image

class _ImageManager():
    def __init__( self ):
        self._images = {}

    def get_image( self, image_name ):
        if image_name not in self._images:
            self._images[image_name] = Image.open( image_name )

        return self._images[image_name]


IMAGE_MANAGER = _ImageManager()
