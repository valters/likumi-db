#!/usr/bin/python3

""" list all .html files in folder, and generate .ver files for them """

import os

import write_versions

files = [ f for f in os.listdir( '.' ) if os.path.isfile( f ) ]
for f in files:
    print( f, end='' )

    fname, ext = os.path.splitext( os.path.basename(f) )
    if ext == '.html':
        print( ': ', end='' )
        try:
            write_versions.write_versions_file( fname, write_versions.parse_versions( fname ) )
            print('ok')
        except RuntimeError as e:
            print( "error: " + str(e))
    else:
        print(' (ignored)')
