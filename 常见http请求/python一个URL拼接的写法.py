from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath

def myjoin(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

if __name__ == '__main__':
	print myjoin("www.baidu.com/","xxx")