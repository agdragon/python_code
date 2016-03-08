#!/usr/bin/python
#coding=utf-8

import redis

if __name__ == "__main__":
	r=redis.Redis(host='127.0.0.1',port=6379,db=1)
	r1=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
	info=r.info()
 
	pipe = r1.pipeline()
	pipe.set('bing', 'baz')
	pipe.set('foo', 'bar')
	pipe.execute()

	for key in info:
		print "%s:%s"%(key,info[key])
     
	print "-------------"*3
 
	print "dbsize%s"%r.dbsize()
	print "ping%s"%r.ping()
 
	print "-------------"*3
	print r.get('name')
 
 
	#----------------------------------String操作------------------------
	#设置元素
	print "-------------"*3
	r.set('name','aa')
	print r.get('name')
 
	#为c1设置值
	print "-------------"*3
	r['c1']='bar'
	print r.getset('c1','jj')
 
	#得到所有包含name的key的值
	print "-------------"*3
	print 'keys:',r.keys('name*')
 
 
	#随机取一个Key值
	print "-------------"*3
	print 'randomkey:',r.randomkey()
 
 
	#查看数据是否存在 有则返回True ，没有则返回Flase
	print r.exists('name')

	print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	print r1.exists('a4904d6c0e9a6013242c121085ccfbb03e877bd0f3829a6fba0f636a9e6ffa6d')
 	print "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

	#删除数据  删除成功返回1
	print 'delete:',r.delete('name')
	print r.delete('c1')
 
	#更改key的值：
	print r.set('name','gina')
	r.rename('name','new_name')
	print r.get('new_name')
 
	#设置数据过期时间
	r.expire('c1',5)
	#查看过期时间  永不过期返回-1
	r.set('name','haha')
	print r.ttl('name')
 
	r.save()
	#取最后一次save时间
	print  r.lastsave()
	r.set('intv','9')
	print r.incr('intv')
	print r.incrby('intv','5')
 
	r['c1']='aa'
	r['c2']='bb'
 
	#批量获取数据
	print r.mget('c1','c2')
 
	#获取开头为c的key的值
	print r.keys('*c*')
 
 
 
	#---------------------对list集合进行操作---------------------
	print r.lpush('students','gina')
	print 'list len:',r.llen('students')
	print r.lrange('students',start=0,end=3)
	#取出一位
	print 'list index 0:',r.lindex('gina',0)
	#截取列表
	print r.ltrim('students',start=0,end=3)
 
