import json
import urllib
import urllib2

data = {
	'userName':'aaa',
	'password':'aaa'
}

req = urllib2.Request('http://10.0.0.149:8888/login')
#req = urllib2.Request('http://10.0.0.149:8888/regist')

req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))

html = response.read()

print html