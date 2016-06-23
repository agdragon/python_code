启动mysql:
sudo /usr/local/mysql/support-files/mysql.server start

启动PHP:
export PHP_HOME=/usr/local/opt/php56
export PATH=${PHP_HOME}/bin:${PHP_HOME}/sbin:$PATH

pkill php-fpm
php-fpm &


启动nginx:
nginx -s reload 重启(如果之前没有启动nginx，直接nginx即可)


MAC查看端口占用情况:
命令 lsof -i tcp:port  （port替换成端口号，比如6379）可以查看该端口被什么程序占用，并显示PID，方便KILL