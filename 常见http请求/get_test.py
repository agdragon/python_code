#!/usr/bin/env python
# coding=utf-8

import urllib2
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

response = urllib2.urlopen('http://yqwgame8.com/weixinGetData')
result = response.read()

result = json.loads(result)

result = result["result"]

tmp_result = []
for item in result:
	tmp_result.append(item.decode("utf8") + "\n")

inpath = "微信转发ID.txt"
uipath = unicode(inpath , "utf8")

f=file(uipath, "w+")
f.writelines(tmp_result)
f.close()
