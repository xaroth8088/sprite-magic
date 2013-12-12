""" Acts as an in-memory cache for PIL Image objects, to reduce how much we have to go to disk.
"""

from PIL import Image
import numpy as np
from collections import defaultdict
from math import sin, cos, radians

class _ImageManager():
    def __init__( self ):
        self._images = defaultdict( lambda: {} )

    def get_colorized_image( self, image_name, hsv ):
        # Do we already have this sitting in memory?
        if image_name not in self._images or hsv not in self._images[image_name]:
            raw_image = Image.open( image_name )
            self._images[image_name][hsv] = self._colorize( raw_image, hsv )

        # return the cached version
        return self._images[image_name][hsv]

    def _shift_hsv( self, arr, delta_hue, saturation, value ):
        # Adapted from algorithm at http://beesbuzz.biz/code/hsv_color_transforms.php
        delta_hue = float( delta_hue )
        print "hsv: %s %s %s" % ( delta_hue, saturation, value )
        v = value
        s = saturation
        u = cos( radians( delta_hue ) )
        w = sin( radians( delta_hue ) )

        rgba_to_yiq = np.matrix( 
          [[ 0.299   , 0.587   , 0.114, 0.0   ],
            [ 0.595716, -0.274453, -0.321263, 0.0],
            [ 0.211456, -0.522591, 0.311135, 0.0],
            [ 0.0, 0.0, 0.0, 1.0]
            ] )

        yiq_to_rgba = rgba_to_yiq.I

        hsv_adjust = np.matrix( 
            [
             [v, 0.0, 0.0, 0.0],
             [0.0, v * s * u, -v * s * w, 0.0],
             [0.0, v * s * w, v * s * u, 0.0],
             [0.0, 0.0, 0.0, 1.0]
             ], dtype = "double"
        )

        transform_matrix = np.asarray( yiq_to_rgba.dot( hsv_adjust ).dot( rgba_to_yiq ) )

        shape = np.shape( arr )  # x, y, 4
        temp = arr.reshape( ( shape[0] * shape[1], 4 ) )
        out = temp.dot( transform_matrix.T )
        out = out.clip( 0.0, 255.0 )
        out_s = out.reshape( shape )

        return out_s

    def _colorize( self, sheet, hsv ):
        arr = np.asarray( sheet ).astype( 'float' )
        colorized_sheet = Image.fromarray( self._shift_hsv( arr, hsv[0], hsv[1], hsv[2] ).astype( 'uint8' ), 'RGBA' )
        return colorized_sheet


IMAGE_MANAGER = _ImageManager()
