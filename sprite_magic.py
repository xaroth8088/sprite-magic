""" Sprite Magic startup controller
"""

import os
import sys
from windows.main_window import MainWindow

def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe """
    if hasattr( sys, "frozen" ):
        return os.path.dirname( unicode( sys.executable, sys.getfilesystemencoding() ) )

    return os.path.dirname( unicode( __file__, sys.getfilesystemencoding() ) )

os.chdir( module_path() )

def main():
    app = MainWindow()
    app.mainloop()

if __name__ == '__main__':
    main()
