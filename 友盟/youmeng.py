#coding=utf-8

import time

import hashlib
import requests
import json
import urllib2

def md5(s):
    m = hashlib.md5(s)
    return m.hexdigest()

def push_unicast(appkey, app_master_secret, device_token):
    timestamp = int(time.time() * 1000 )
    method = 'POST'
    url = 'http://msg.umeng.com/api/send'
    params = {'appkey': appkey,
              'timestamp': timestamp,
              'production_mode' : 'true',
              'device_tokens': device_token,
              'type': 'unicast',
              
              'payload': {'aps': {
                                  'alert': 'test123',          
                                  'badge': 'xx',
                                  'sound': 'xx',        
                                  'content-available': 'xx',
                                  'category': 'xx'
                          },

                          'body': {'ticker': 'Hello World',
                                   'title':'test',
                                   'text':'from server',
                                   'after_open': 'go_app'},
                          'display_type': 'notification'
              }
    }

    post_body = json.dumps(params)
    print post_body
    sign = md5('%s%s%s%s' % (method,url,post_body,app_master_secret))
    print sign
    try:
        r = urllib2.urlopen(url + '?sign='+sign, data=post_body)
        print r.read()
    except urllib2.HTTPError,e:
        print e.read()
    except urllib2.URLError,e:
        print e.reason

if __name__ == '__main__':
    appkey = '556973eb67e58e40ca0069ff'
    app_master_secret = 'dnqmfbemfgwq4m1z9xoolitxpbbpmahg'
    device_token = 'fa42e85af9da1e17713453a4955bf7ee5ed328f3116a991778171849a3bd185b'

    push_unicast(appkey, app_master_secret, device_token)