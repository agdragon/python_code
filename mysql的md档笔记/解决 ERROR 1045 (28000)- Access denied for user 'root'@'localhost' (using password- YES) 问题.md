# 解决 ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES) 问题  

tags： MYSQL

---

最近新装好的mysql在进入mysql工具时，总是有错误提示:
```
mysql -u root -p
Enter password:
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)
或者
# mysql -u root -p password 'newpassword'
Enter password:
mysqladmin: connect to server at 'localhost' failed
error: 'Access denied for user 'root'@'localhost' (using password: YES)' 
```

现在终于找到解决方法了。本来准备重装的，现在不必了。
方法操作很简单，如下：
```
/etc/init.d/mysql stop
mysqld_safe --user=mysql --skip-grant-tables --skip-networking &
mysql -u root mysql
mysql> UPDATE user SET Password=PASSWORD('newpassword') where USER='root' and host='root' or host='localhost';//把空的用户密码都修改成非空的密码就行了。
mysql> FLUSH PRIVILEGES;
mysql> quit
/etc/init.d/mysqld restart
mysql -uroot -p
Enter password: <输入新设的密码newpassword> 
```



