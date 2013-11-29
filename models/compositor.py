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
    global _SELECTED_LAYERS
    _SELECTED_LAYERS = []
    _SELECTED_TYPE = spec_manager.GetTypeByName( sprite_type_name )
    _NotifyViews()

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

def AddLayer():
    # Add the next available layer from the spec_manager that we don't already have
    all_layers = spec_manager.GetGroupLayers( _SELECTED_TYPE.group_name )
    for layer in all_layers:
        if layer not in _SELECTED_LAYERS:
            _SELECTED_LAYERS.append( layer )
            _NotifyViews()
            return

def RemoveLayer( layer_name ):
    _SELECTED_LAYERS.pop( _SELECTED_LAYERS.index( layer_name ) )
    _NotifyViews()

def MoveLayerUp( layer_name ):
    _MoveLayer( layer_name, -1 )

def MoveLayerDown( layer_name ):
    _MoveLayer( layer_name, 1 )

def _MoveLayer( layer_name, direction ):
    # Get our two indices to swap
    i = _SELECTED_LAYERS.index( layer_name )
    j = i + direction

    # Don't move past the beginning or end of the list
    if j < 0:
        return

    if j >= len( _SELECTED_LAYERS ):
        return

    _SELECTED_LAYERS[i], _SELECTED_LAYERS[j] = _SELECTED_LAYERS[j], _SELECTED_LAYERS[i]

    _NotifyViews()

# Ensure the spec manager actually has specs for us
spec_manager.LoadSpecs()
