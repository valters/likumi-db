#!/usr/bin/python3

import lxml.html
import json
import sys

docfile = 'satversme' if len(sys.argv) == 1 else sys.argv[1]
print(docfile)

root = lxml.html.parse(docfile+'.html')
versions_el = root.xpath("//div[@id='ver_date']")
versions_text = versions_el[0].text_content()
print(versions_text)

out = open(docfile+'.ver', 'w')
versions = json.loads(versions_text)
for ver in versions['data']:
	print(ver['value'], file=out)

out.close()
