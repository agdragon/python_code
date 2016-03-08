import urllib2, urllib

data = {'name' : 'www'}
f = urllib2.urlopen(
	url = 'http://192.168.0.105:8080/login',
	data    = urllib.urlencode(data)
	)
print f.read()