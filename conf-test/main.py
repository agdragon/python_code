#!/usr/bin/python
# -*- coding:utf-8 -*-
#author: lingyue.wkl
#desc: use to db ops
#---------------------
#2012-02-18 created
#---------------------

import sys,os
import ConfigParser

# print os.path.join(os.getcwd(), "token_conf.conf")

if __name__ == "__main__":
    config_file_path = "db_config.ini"
    
    while  1:
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        db_host = cf.get("test","host")
    
        print cf.get("test","port")