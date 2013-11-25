'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk

from models.type_manager import GetAvailableTypes
import models.compositor

class Selector():
    def __init__( self, master ):
        self.master = master
        models.compositor.RegisterView( self )
        self.setupView()
        self.onModelUpdated()

    def setupView( self ):
        temp = tk.Label( self.master, text = "selection pane goes here" )
        temp.pack()
        
        self.setupTypes()
    
    def setupTypes(self):
        types = [data.name for data in GetAvailableTypes()]
        variable = tk.StringVar(self.master)
        variable.set(types[0]) # default value
        
        w = apply(tk.OptionMenu, (self.master, variable) + tuple(types))
        w.pack()

    def onModelUpdated( self ):
        # TODO: The compositor changed state, so make sure we're up to date, too.
        pass

# TODO: Hook window close and deregister with the compositor
