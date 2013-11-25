'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk

class Preview():
    def __init__( self, master ):
        self.master = master
        temp = tk.Label( self.master, text = "preview pane goes here" )
        temp.pack()
