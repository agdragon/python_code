#!/usr/bin/python
#coding=utf-8

import os
import sys

'''
##  作用: 修改指定目录下指定后缀格式为其余格式的操作
##  用法: python dir/ jpg png
### 参数说明:
    ## sys.argv[1] ---> 文件目录
    ## sys.argv[2] ---> 原后缀
    ## sys.argv[3] ---> 新后缀
'''

def swap_extensions(dir, old_suffix, new_suffix):
    for path, subdir, files in os.walk(dir):
        for oldfile in files:
            oldfileList = os.path.splitext(oldfile)
            if oldfileList[1] == old_suffix:
                oldfileName = os.path.join(path, oldfile)
                newfileName = os.path.join(path, oldfileList[0] + "." + new_suffix)

                os.rename(oldfile, newfile)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage:swap_extension.py rootdir before after'
        sys.exit(1)

    swap_extensions(sys.argv[1], sys.argv[2], sys.argv[3])