#coding=utf-8
import urllib2,urllib,sys, os, time, datetime, re, logging, getopt, thread,re
from urlparse import urlparse
from time import strftime
import urllib2
import gzip
import StringIO
import codecs

if __name__ == "__main__":
        f1 = codecs.open('result1.txt', 'wb', 'utf-8') 
        f = open('result.txt', 'r')
        line = f.readline()
        while line:
                ip = line.strip().split(',')[0].strip()
                url = "http://www.ip138.com/ips138.asp?ip="+ip+"&action=2"
                request = urllib2.Request(url)
                myResponse = urllib2.urlopen(request)
                html = myResponse.read()
                myResponse.close()
                html = html.decode("gbk")
                #myMatch = re.search(r'<td align="center"><ul class="ul1"><li>(.*?)</li></ul></td>', html, re.S)
                myMatch = re.search(r'<td align="center"><ul class="ul1"><li>(.*?)</li>', html, re.S)
                tmp_str = myMatch.group(1)
                tmp_str = tmp_str.replace(u'本站主数据：','')
                
                tmp_str = line.strip('\r\n') + " , " + tmp_str
                print tmp_str
                f1.write(tmp_str + os.linesep)
                line = f.readline()
        f.close()
        f1.close()
