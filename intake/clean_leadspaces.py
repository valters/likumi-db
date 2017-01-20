#!/usr/bin/python3

""" remove leading whitespace in generated .txt files """

import sys
import os
import io

def clean_visibility( folder, filename ):
    print(filename)
    temp_file = folder + filename + '.tmp';

    os.rename(folder + filename, temp_file )

    with open( temp_file, encoding='utf-8' ) as fin:
        with open( folder + filename, 'w', encoding='utf-8' ) as fout:
            for line in fin:
                fout.write( cleaned(line) )

def cleaned(line):
    """ simply delete first 3 spaces - if present """
    if line[0:3] == '   ':
        return line[3:]
    else:
        return line

def process_all_files( folder, extension = '.txt'):
    files = [ f for f in os.listdir(folder) if f.endswith(extension) ]
    for f in files:
        clean_visibility(folder, f)

if len(sys.argv) == 2:
    process_all_files(sys.argv[1])

else:
    test1 = 'abc'
    if test1 == cleaned(test1):
        print('.')

    test2 = '   abc'
    if test1 == cleaned(test2):
        print('.')
