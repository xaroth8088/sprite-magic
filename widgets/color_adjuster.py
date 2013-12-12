""" A control to permit adjusting the hue of a given sprite
"""

""" A widget for adjusting the speed of the animation preview
"""

from Tkinter import *
from ttk import *
from math import floor

from models.compositor import COMPOSITOR

class ColorAdjuster( Frame ):
    def __init__( self, master, layer ):
        Frame.__init__( self, master )
        self.layer = layer

        self._old_h = 0.0
        self._old_s = 1.0
        self._old_v = 1.0

        self._setup_view()

    def _setup_view( self ):
        self._setup_hue()
        self._setup_saturation()
        self._setup_value()
        self._setup_commands()  # doing this after, so that all initial values can be set without triggering the command

    def _setup_commands( self ):
        self.hue_scale.configure( command = self._on_slider_changed )
        self.saturation_scale.configure( command = self._on_slider_changed )
        self.value_scale.configure( command = self._on_slider_changed )
        self._on_slider_changed( None )

    def _setup_hue( self ):
        self.hue_label = Label( self )
        self.hue_label.grid( row = 0, column = 0 )

        self.hue_scale = Scale( self, from_ = 0.0, to = 360.0, orient = HORIZONTAL, length = 200 )
        self.hue_scale.set( 0.0 )
        self.hue_scale.grid( row = 1, column = 0 )

    def _setup_saturation( self ):
        self.saturation_label = Label( self )
        self.saturation_label.grid( row = 2, column = 0 )

        self.saturation_scale = Scale( self, from_ = 0.0, to = 2.0, orient = HORIZONTAL, length = 200 )
        self.saturation_scale.set( 1.0 )
        self.saturation_scale.grid( row = 3, column = 0 )

    def _setup_value( self ):
        self.value_label = Label( self )
        self.value_label.grid( row = 4, column = 0 )

        self.value_scale = Scale( self, from_ = 0.0, to = 2.0, orient = HORIZONTAL, length = 200 )
        self.value_scale.set( 1.0 )
        self.value_scale.grid( row = 5, column = 0 )

    def _on_slider_changed( self, value ):
        self._update_colorization()

    def _nearest_n( self, value, resolution ):
        fraction = 1 / resolution;
        return floor( fraction * value ) / fraction

    def _update_colorization( self ):
        h = self._nearest_n( self.hue_scale.get(), 15.0 )
        self.hue_label.configure( text = "hue: %s" % ( h, ) )

        s = self._nearest_n( self.saturation_scale.get(), 0.2 )
        self.saturation_label.configure( text = "saturation: %s" % ( s, ) )

        v = self._nearest_n( self.value_scale.get(), 0.2 )
        self.value_label.configure( text = "brightness: %s" % ( v, ) )

        if self._old_h != h or self._old_s != s or self._old_v != v:
            hsv = ( h, s, v )
            COMPOSITOR.colorize_layer( self.layer, hsv )

        self._old_h = h
        self._old_s = s
        self._old_v = v
