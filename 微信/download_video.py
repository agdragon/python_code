#!/usr/bin/python
#coding=utf-8

import json
import urllib
import urllib2

def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print '%.2f%%' % per

def get_meadid():
	data = {
		'type':'video',
		'offset':0,
		'count':20
	}

	req = urllib2.Request('https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=MhyKy6aC0cLTOKimGMGxm1RxS3wQPacx9zlN4Hj56UPzRmzr6Wb1rK4jEGEkwV6emn_Wg2Is2wo6k7XN0vA5uhd78zLVC-FmiRnwRcdN-5fIXoIRzMU5UySmI3SbTqnjTAWdACAIPL')

	req.add_header('Content-Type', 'application/json')

	response = urllib2.urlopen(req, json.dumps(data))

	html = response.read()

	print html

def down_file_get(url, name):
	urllib.urlretrieve(url, name,Schedule)

def down_file_post(access_token, media_id, name):
	# url = "https://api.weixin.qq.com/cgi-bin/media/get"
	url = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=" + access_token


	data = {
		'media_id':media_id
	}

	req = urllib2.Request(url)

	req.add_header('Content-Type', 'application/json')

	response = urllib2.urlopen(req, json.dumps(data))

	html = response.read()

	print html


if __name__ == "__main__":
	access_token = "MhyKy6aC0cLTOKimGMGxm1RxS3wQPacx9zlN4Hj56UPzRmzr6Wb1rK4jEGEkwV6emn_Wg2Is2wo6k7XN0vA5uhd78zLVC-FmiRnwRcdN-5fIXoIRzMU5UySmI3SbTqnjTAWdACAIPL"
	media_id = "HQeo7z_sUf5m4iJeu06eXu2bC3gDnKTq47oMfi4Uuy8"
	name = "oa Sr"
	
	# get_meadid()
	
	down_file_post(access_token, media_id, name)


	# down_file_get("https://v.qq.com/iframe/player.html?vid=r1302oclbtj&width=740&height=555&auto=0&encryptVer=6.0&platform=&cKey=xHMo-O9OU0-y9KYtGQPhKPGRDmWcCbzJqVgshSa5I2q98s5nT3XBM8Et8i_oifFO", "Boa Sr")