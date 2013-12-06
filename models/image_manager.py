""" Acts as an in-memory cache for PIL Image objects, to reduce how much we have to go to disk.
"""

from PIL import Image
import numpy as np
from collections import defaultdict

class _ImageManager():
    def __init__( self ):
        self._images = defaultdict( lambda: {} )

    def get_colorized_image( self, image_name, hue ):
        # Do we already have this sitting in memory?
        if image_name not in self._images or hue not in self._images[image_name]:
            raw_image = Image.open( image_name )
            # If we're not adjusting the hue, there's no sense running colorize on it.
            if hue == 0:
                self._images[image_name][hue] = raw_image
            else:
                self._images[image_name][hue] = self._colorize( raw_image, hue )

        # return the cached version
        return self._images[image_name][hue]

    # Colorize, shift_hue, rgb_to_hsv and hsv_to_rgb adapted from code found at http://stackoverflow.com/questions/7274221/changing-image-hue-with-python-pil
    def _rgb_to_hsv( self, rgb ):
        # Translated from source of colorsys.rgb_to_hsv
        hsv = np.empty_like( rgb )
        hsv[..., 3:] = rgb[..., 3:]
        r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
        maxc = np.max( rgb[..., :3], axis = -1 )
        minc = np.min( rgb[..., :3], axis = -1 )
        hsv[..., 2] = maxc
        hsv[..., 1] = ( maxc - minc ) / maxc
        rc = ( maxc - r ) / ( maxc - minc )
        gc = ( maxc - g ) / ( maxc - minc )
        bc = ( maxc - b ) / ( maxc - minc )
        hsv[..., 0] = np.select( [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default = 4.0 + gc - rc )
        hsv[..., 0] = ( hsv[..., 0] / 6.0 ) % 1.0
        idx = ( minc == maxc )
        hsv[..., 0][idx] = 0.0
        hsv[..., 1][idx] = 0.0
        return hsv

    def _hsv_to_rgb( self, hsv, delta_hue ):
        # Translated from source of colorsys.hsv_to_rgb
        rgb = np.empty_like( hsv )
        rgb[..., 3:] = hsv[..., 3:]
        h, s, v = hsv[..., 0] + delta_hue, hsv[..., 1], hsv[..., 2]
        i = ( h * 6.0 ).astype( 'uint8' )
        f = ( h * 6.0 ) - i
        p = v * ( 1.0 - s )
        q = v * ( 1.0 - s * f )
        t = v * ( 1.0 - s * ( 1.0 - f ) )
        i = i % 6
        conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
        rgb[..., 0] = np.select( conditions, [v, q, p, p, t, v], default = v )
        rgb[..., 1] = np.select( conditions, [v, v, v, q, p, p], default = t )
        rgb[..., 2] = np.select( conditions, [v, p, t, v, v, q], default = p )
        return rgb

    def _shift_hue( self, arr, delta_hue ):
        hsv = self._rgb_to_hsv( arr )
        rgb = self._hsv_to_rgb( hsv, delta_hue )
        return rgb

    def _colorize( self, sheet, hue ):
        arr = np.array( np.asarray( sheet ).astype( 'float' ) )
        colorized_sheet = Image.fromarray( self._shift_hue( arr, float( hue ) / 360.0 ).astype( 'uint8' ), 'RGBA' )
        return colorized_sheet


IMAGE_MANAGER = _ImageManager()
