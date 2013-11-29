""" Sprite Magic startup controller
"""

import os
from windows.main_window import MainWindow

os.chdir( os.path.dirname( __file__ ) )

def main():
    app = MainWindow()
    app.mainloop()

if __name__ == '__main__':
    main()
