'''
Created on Nov 24, 2013

@author: Xaroth
'''

import Tkinter as tk

class Selector():
    def __init__( self, master ):
        self.master = master
        temp = tk.Label( self.master, text = "selection pane goes here" )
        temp.pack()
