#!/usr/bin/env python
# author = Vitali

import urllib
import json
serviceurl = "http://ip-api.com/json/"
f = open('hosts.txt', 'r+')
w = open('where.data', 'w+')
count = 0
for line in f:
    if count > 150 : break
    url = urllib.urlopen(serviceurl+line)
    data = url.read()
    json_data = json.loads(data)
    w.write(json_data['city']+ '\n')
f.close()
w.close()
