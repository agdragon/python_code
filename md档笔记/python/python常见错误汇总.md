#python常见错误汇总

###概述:
python常见错误汇总


##**内容**

* 目录：
    * [UnicodeEncodeError: 'ascii' codec can't encode characters](#user-content-UnicodeEncodeError: 'ascii' codec can't encode characters)
    * [python 读取中文文件名/中文路径](#user-content-python 读取中文文件名/中文路径)



<br>


* ####UnicodeEncodeError: 'ascii' codec can't encode characters:
    在执行Python脚本时报如下错误：
        
        UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-78: ordinal not in range(128)

    解决方法：
    
    在python脚本中开头处加上以下两句代码即可：
    
        reload(sys)   
        sys.setdefaultencoding('utf8') 


* ####python 读取中文文件名/中文路径:
    Python直接读取中文路径的文件时失败，可做如下处理：

        inpath = 'D:/work/yuanxx/在线导航/驾车导航/walk_log/20130619_172355.txt'
        uipath = unicode(ipath , "utf8")

    然后用"uipath"经过编码后的路径去open()即可:

        fin = open(uipath)