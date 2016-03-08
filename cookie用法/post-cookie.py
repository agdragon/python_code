#coding:utf-8
import urllib,urllib2,cookielib 

cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_path = 'http://10.0.0.149:8080/login'

data = {"name":"xds","passwd":"xxxxxxxx"}
post_data = urllib.urlencode(data)
request = urllib2.Request(login_path,post_data)
html = opener.open(request).read()
if cj:
	print cj
cj.save('cookiefile.txt')