'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk

import models.compositor

class Preview():
    def __init__( self, master ):
        self.master = master
        models.compositor.RegisterView( self )
        self.setupView()
        self.onModelUpdated()

    def setupView( self ):
        temp = tk.Label( self.master, text = "preview pane goes here" )
        temp.pack()

    def onModelUpdated( self ):
        # TODO: The compositor changed state, so make sure we're up to date, too.
        pass

# TODO: Hook window close and deregister with the compositor
