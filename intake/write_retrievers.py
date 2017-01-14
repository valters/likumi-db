#!/usr/bin/python3

""" read toc.json, and corresponding .ver files, and generate retriever scripts """
import json
import os
import stat
import sys

TOC = 'toc.json'

CURL_TEMPL = """curl -o {iso_date}.html \
'http://likumi.lv/body_print.php?id={print_id}&version_date={version_date}&grozijumi=1&pielikumi=0&saturs=1&piezimes=0&large_font=0' \
-H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, sdch' \
-H 'Accept-Language: en-US,en;q=0.8,de;q=0.6,lv;q=0.4,ru;q=0.2' \
-H 'Upgrade-Insecure-Requests: 1' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36' \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' \
-H 'Connection: keep-alive' \
--compressed
"""

def _to_iso( date ):
    day, month, year = date.split( '.' )
    return year+month+day

def _set_exec( fname ):
    st = os.stat( fname )
    os.chmod( fname, st.st_mode | stat.S_IEXEC )

def _write_script( key, key_section ):
    ver_fname = key+'.ver'
    with open( ver_fname, 'rt' ) as ver_file:
        _write_script_int( key, key_section, ver_file )

def _write_script_int( key, key_section, ver_file ):
    """ generate versions retrieval script """
    os.makedirs( key, exist_ok = True )
    script_fname = key+'/retr.'+key+'.sh'
    with open( script_fname, 'wt' ) as script_file:
        for line in ver_file:
            version_date = line.rstrip()
            print( version_date )
            iso_date = _to_iso( version_date )
            print( CURL_TEMPL.format( key = key, iso_date = iso_date, print_id = key_section['print_id'], version_date = version_date ), file = script_file )
    _set_exec( script_fname )

def read_toc():
    with open( TOC, 'r' ) as toc_file:
        toc_json = json.load( toc_file )

    likumi = toc_json['likumi']
    return likumi


def write_all():
    likumi = read_toc()
    for key in likumi.keys():
        print( key )
        _write_script( key, likumi[key] )

def write_single( key ):
    print( 'write single: ' + key )
    likumi = read_toc()
    _write_script( key, likumi[key] )


if len(sys.argv) == 1:
    write_all()
else:
    write_single( sys.argv[1] )
