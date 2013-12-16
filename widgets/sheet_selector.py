""" A widget to select a sheet to use for a given layer.
"""

from Tkinter import *
from ttk import *
from PIL import Image, ImageTk

from widgets.color_adjuster import ColorAdjuster

from models.compositor import COMPOSITOR

class SheetSelector( Frame ):
    def __init__( self, master, layer_name ):
        Frame.__init__( self, master )
        self.layer_name = layer_name

        self.configure( borderwidth = 2, padding = 5, relief = GROOVE )
        self.columnconfigure( 1, weight = 1 )

        self._setup_title()
        self._setup_optionmenu()
        self._setup_destroy_button()
        self._setup_export_button()
        self._setup_order_buttons()
        self._setup_color_adjusters()

    def _setup_title( self ):
        title = Label( self, text = self.layer_name )
        title.grid( row = 0, column = 0 )

    def _setup_optionmenu( self ):
        layers = COMPOSITOR.get_sheets_by_layer( self.layer_name ).keys()
        layers.insert( 0, "" )  # Need a blank entry at the head, otherwise ttk.OptionMenu will cause the first entry to disappear

        self.variable = StringVar( self )
        self.variable.set( layers[1] )

        layer_menu = OptionMenu( self, self.variable, *layers )
        layer_menu.grid( row = 0, column = 1 )
        self.variable.trace( 'w', self._on_layer_selection_changed )

    def _setup_destroy_button( self ):
        raw_image = Image.open( "ui_images/destroy.png" )
        raw_image.thumbnail( ( 32, 32 ), Image.ANTIALIAS )
        self.destroy_image = ImageTk.PhotoImage( raw_image )
        button = Button( self, image = self.destroy_image, command = self._on_destroy_button_pressed )
        button.grid( row = 0, column = 2, sticky = E )

    def _setup_export_button( self ):
        button = Button( self, text = "Export layer", command = self._on_export_pressed )
        button.grid( row = 2, column = 2, sticky = E )

    def _setup_order_buttons( self ):
        raw_image = Image.open( "ui_images/up.png" )
        raw_image.thumbnail( ( 32, 32 ), Image.ANTIALIAS )
        self.up_image = ImageTk.PhotoImage( raw_image )
        button = Button( self, command = self._on_up_pressed, image = self.up_image )
        button.grid( row = 1, column = 0, sticky = W )

        raw_image = Image.open( "ui_images/down.png" )
        raw_image.thumbnail( ( 32, 32 ), Image.ANTIALIAS )
        self.down_image = ImageTk.PhotoImage( raw_image )
        button = Button( self, command = self._on_down_pressed, image = self.down_image )
        button.grid( row = 2, column = 0, sticky = W )

    def _setup_color_adjusters( self ):
        adjuster = ColorAdjuster( self, self.layer_name )
        adjuster.grid( row = 1, column = 1, rowspan = 2 )

    def _on_layer_selection_changed( self, name, index, mode ):
        COMPOSITOR.select_sheet( self.layer_name, self.variable.get() )

    def _on_up_pressed( self ):
        COMPOSITOR.move_layer_up( self.layer_name )

    def _on_down_pressed( self ):
        COMPOSITOR.move_layer_down( self.layer_name )

    def _on_destroy_button_pressed( self ):
        COMPOSITOR.remove_layer( self.layer_name )

    def _on_export_pressed( self ):
        COMPOSITOR.export_layer_sheet( self.layer_name )
