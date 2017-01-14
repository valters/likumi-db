#!/usr/bin/python3

""" extract version info from likumi dump, write .ver file """

import lxml.html
import json
import sys

DEBUG=0

def parse_versions(docfile):
    root = lxml.html.parse(docfile+'.html')
    versions_el = root.xpath("//div[@id='ver_date']")
    versions_text = versions_el[0].text_content()
    print(versions_text) if DEBUG else None
    return versions_text

def write_versions_file(docname,versions_text):
    out = open(docname+'.ver', 'w')
    try:
        versions = json.loads(versions_text)

        for ver in versions['data']:
            print(ver['value'], file=out)
    except json.decoder.JSONDecodeError as e:
        raise RuntimeError("failed to write file: " + repr(e))
    finally:
        out.close()

if __name__ == '__main__':
    """ if testing: provide name of file (without extension) to process single likumi file """
    DEBUG=1
    docfile = 'satversme' if len(sys.argv) == 1 else sys.argv[1]
    print(docfile)
    write_versions_file(docfile, parse_versions(docfile))
