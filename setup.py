from distutils.core import setup
import py2exe
import os
import shutil
import zipfile

OUTPUT_ARCHIVE = "sprite-magic-win32.zip"

# Clean the existing build and dist directories
shutil.rmtree( 'dist', ignore_errors = True )
shutil.rmtree( 'build', ignore_errors = True )
shutil.rmtree( 'sprite-magic', ignore_errors = True )
try:
    os.unlink( OUTPUT_ARCHIVE )
except:
    pass

# Utility function to recursively add folders to dits/
def tree( src ):
    return [( root, map( lambda f: os.path.join( root, f ), files ) ) for ( root, dirs, files ) in os.walk( os.path.normpath( src ) )]

# Build the list of static files to copy into the dist/ directory
data_files = tree( "assets" )
ui_images = tree( "ui_images" )
data_files = data_files + ui_images

# Actually build the thing
setup( windows = ['sprite_magic.py'],
       name = 'Sprite Magic',
       description = 'A tool for creating game-ready assets',
       author = 'Geoffrey Benson',
       author_email = 'xaroth@gmail.com',
       url = 'https://github.com/xaroth8088/sprite-magic',
       data_files = data_files
        )

os.rename( "dist", "sprite-magic" )

# Create the .zip file
def zipdir( path, zip_file ):
    for root, dirs, files in os.walk( path ):
        for file_ in files:
            zip_file.write( os.path.join( root, file_ ) )

zip_file = zipfile.ZipFile( OUTPUT_ARCHIVE, 'w' )
zipdir( 'sprite-magic/', zip_file )
zip_file.close()

# Clean up
shutil.rmtree( 'build', ignore_errors = True )
shutil.rmtree( 'dist', ignore_errors = True )
shutil.rmtree( 'sprite-magic', ignore_errors = True )
