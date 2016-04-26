import gevent
from gevent.pool import Pool
from gevent.pool import Group
import time
import requests
from gevent import getcurrent

pool = Pool(2)

print pool
print len(pool)

def down(url):
    tmp_len = len(requests.get(url).content)
    # print tmp_len
    print "#" * 30
    print getcurrent().parent
    print "#" * 30
    
urls = ['http://www.maiziedu.com/', 'http://www.iqiyi.com/'
        , 'http://www.baidu.com/', 'http://www.iteye.com/']

# group = Group()


for i in urls:
    a = pool.spawn(down, i)


print "*" * 30
for geeenlet in list(pool):
	print geeenlet

print "*" * 30

t1 = time.time()

pool.join()



print 'use ', time.time()-t1
