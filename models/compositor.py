""" The compositor is responsible for keeping track of which sprite layers the user wants to combine, and how.
"""

import spec_manager

_SELECTED_TYPE = None  # Which sprite type has the user selected?
_SELECTED_LAYERS = []  # The layers that the user is actively looking at, in order
_ANIMATION_SPEED = 0.25  # Number of seconds between frames
_REGISTERED_VIEWS = []  # Which views want to know when we update?

_LOADED = False

def RegisterView( view ):
    _REGISTERED_VIEWS.append( view )

def DeregisterView( view ):
    _REGISTERED_VIEWS.remove( view )

def _NotifyViews():
    for view in _REGISTERED_VIEWS:
        view.on_model_updated()

def SetSelectedType( sprite_type_name ):
    global _SELECTED_TYPE
    _SELECTED_TYPE = spec_manager.GetTypeByName( sprite_type_name )

def GetSheetsByLayer( layer_name ):
    global _SELECTED_TYPE
    layers = spec_manager.GetGroupSheetsByLayer( _SELECTED_TYPE.group_name, layer_name )
    return layers

def GetAvailableLayers():
    global _SELECTED_TYPE
    return spec_manager.GetGroupLayers( _SELECTED_TYPE.group_name )

def GetSelectedLayers():
    global _SELECTED_LAYERS
    return _SELECTED_LAYERS

spec_manager.LoadSpecs()
