import urllib2
from multipprocessing.dummy import Pool as ThreadPool

urls = [
	"http://www.baidu.com",
	"http://www.baidu.com"
]

pool = ThreadPool(4)

results = pool.map(urllib2.urlopen, urls)

pool.close()
pool.join()