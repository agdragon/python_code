# coding=utf-8
#!/usr/bin/python
#脚本的用法 python nn_report.py

import sys, os, logging, time, datetime, ConfigParser, string, subprocess
import getopt
from time import strftime

SERVER_VERSION = '1.0.0'
TIME_FORMAT = '%Y%m%dT%H%M%SZ'
TIME_FORMAT_1 = '%Y%m%d%H%M%S'
CUR_PATH = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
LOG_PATH = CUR_PATH
START_TIME = int(time.time())

#定时器重入时间，单位(秒)
INTERVAL_TIME = 50

#默认不重启的天数
NEVER_REBOOT_DAY = 0
#默认不重启的时间段
NEVER_REBOOT_TIME = "00:00-00:00"

task_info = {}

def get_current_local_time():
	local = datetime.datetime.now()
	return local.strftime(TIME_FORMAT_1)

def get_current_utc_time():
	utc = datetime.datetime.utcnow()
	return utc.strftime(TIME_FORMAT)
	newList = []
	for x in old_list:
		if x not in newList :
			newList.append(x)
	return newList

def dir_path_check(dir_path):
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

def daemon_lock_check(id):
	"""检测程序是否可以执行。返回0可以执行，返回非0则不能执行"""
	id_time = ["0"]
	get_lock_id(id,id_time)

	last_time = float(id_time[0])
	if is_time_in_range_1(last_time, INTERVAL_TIME) == False :
		id[0] = id[0] + 1
		daemon_lock_modify(id[0])
		return 0
	else:
		#logging
		logging.error("the current:%s last:%s interval:%s" %(str(time.time()),str(last_time), str(INTERVAL_TIME)))
		return -1

def daemon_lock_modify(id):
	tmp_daemon = "%s/daemon.lock"%(LOG_PATH)
	f = open(tmp_daemon, 'w')
	str = "time="
	str_3 = '\r\n'
	time_str = time.time()
	str_1 = "%s%f%s"%(str, time_str, str_3)
	f.write(str_1)
	
	f.write('id=%d' % id)
	f.close()

def get_lock_id(id, id_time):
	id[0] = 0
	tmp_daemon = "%s/daemon.lock"%(LOG_PATH)
	if os.path.exists(tmp_daemon):
		f = open(tmp_daemon, "r")
		line = f.readline()
		
		while line:
			line.strip()
			if line.startswith("time"):
				line = line.strip('\r\n') 
				array = line.split('=')
				id_time[0] = str(array[1])
				
			if line.startswith('id'):
				line = line.strip('\r\n') 
				array = line.split('=')
				id[0] = int(array[1])
			line = f.readline()
		f.close()

#解析以“-”隔开的时间段字符串
def parser_time_1(str_tmp):
	time_list = []
	time_list.append( str_tmp.strip().split('-')[0].strip())
	time_list.append( str_tmp.strip().split('-')[-1].strip())
	return time_list

#解析以“:”隔开的时间段字符串
def parser_time_2(str_tmp):
	time_list = []
	time_list.append( str_tmp.strip().split(':')[0].strip())
	time_list.append( str_tmp.strip().split(':')[-1].strip())
	return time_list

def check_section_name(section):
	tmp_list = section.split('_')
	if len(tmp_list) == 2:
		if tmp_list[0] == 'process' and tmp_list[1].isdigit() == True:
			return True
	return False

def get_all_task_from_conf():
	logging.info("get all task")
	sections = cf.sections()
	for section in sections:
		if check_section_name(section) == False:
			logging.error("section:%s is wrong. It should be named after process_ and a figure"%(section))
			continue
		task_info[section] = []
		try:
			path = cf.get(section, "path")
			if path == "":
				del task_info[section]
				logging.error("%s's path is null, check your set."%(section))
				continue
			else:
				task_info[section].append(path)
		except Exception,e:
			del task_info[section]
			logging.error("%s"%e)
			logging.info("delete the section:%s"%section)
			continue
		 
		try:
			reboot_day = cf.get(section, "reboot_day")
			if reboot_day == "":
				task_info[section].append(str(NEVER_REBOOT_TIME))
				logging.error("%s's reboot_day is null, set default reboot_day: %s"%(section, str(NEVER_REBOOT_TIME)))
			else:
				reboot_day = reboot_day.strip().split()[0]
				if str(reboot_day).isdigit() == False:
					task_info[section].append(str(NEVER_REBOOT_TIME))
					logging.error("%s's reboot_day should be an integer, set default reboot_day: %s"%(section, str(NEVER_REBOOT_TIME)))
				else:
					task_info[section].append(reboot_day)
		except Exception,e:
			task_info[section].append(str(NEVER_REBOOT_TIME))
			logging.error("%s"%e)
			logging.info("set default reboot day(%s) to %s"%(str(NEVER_REBOOT_TIME), section))
		
		try:
			if reboot_day == str(NEVER_REBOOT_DAY):
				reboot_time = str(NEVER_REBOOT_TIME)
				task_info[section].append(parser_time_1(str(NEVER_REBOOT_TIME)))
				logging.warning("%s's reboot_day is 0, it will never reboot."%(section))
				continue
			reboot_time = cf.get(section, "reboot_time")
			if reboot_time == "":
				task_info[section][1] = NEVER_REBOOT_DAY
				task_info[section].append(parser_time_1(str(NEVER_REBOOT_TIME)))
				logging.warning("%s's reboot_time is null, it will never reboot."%(section))
			else: 
				reboot_time_1 = parser_time_1(str(reboot_time))
				if reboot_time_1[0] == "" or reboot_time_1[1] == "":
					task_info[section][1] = NEVER_REBOOT_DAY
					task_info[section].append(parser_time_1(str(NEVER_REBOOT_TIME)))
					logging.warning("%s's reboot_time %s is illegal, it will never reboot."%(section, reboot_time))
				else:
					reboot_time_2 = parser_time_2(reboot_time_1[0])
					reboot_time_3 = parser_time_2(reboot_time_1[1])
					if reboot_time_2[0] == "" or reboot_time_2[1] == "" or reboot_time_3[0] == "" or reboot_time_3[1] == "":
						task_info[section][1] = NEVER_REBOOT_DAY
						task_info[section].append(parser_time_1(str(NEVER_REBOOT_TIME)))
						logging.warning("%s's reboot_time %s is illegal, it will never reboot."%(section, reboot_time))
					elif int(reboot_time_2[0]) < 0 or int(reboot_time_2[0]) > 23 or int(reboot_time_2[1]) < 0 or int(reboot_time_2[1]) > 59 \
						or int(reboot_time_3[0]) < 0 or int(reboot_time_3[0]) > 23 or int(reboot_time_3[1]) < 0 or int(reboot_time_3[1]) > 59:
						task_info[section][1] = NEVER_REBOOT_DAY
						task_info[section].append(parser_time_1(str(NEVER_REBOOT_TIME)))
						logging.warning("%s's reboot_time %s is illegal, it will never reboot."%(section, reboot_time))
					else:
						task_info[section].append(reboot_time_1)
		except Exception,e:
			task_info[section][1] = NEVER_REBOOT_DAY
			task_info[section].append(parser_time_1(str(NEVER_REBOOT_TIME)))
			logging.error("%s, it will never reboot."%e)

def get_exec_cmd_result(cmd):
	try:
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		a = p.stdout.read().decode('utf8')
		return a.strip()
	except Exception, e:
		logging.error("%s is failed"%cmd)
		return

def get_pid_start_time(pid):
	start_time = 0
	if int(pid) <= 1:
		return 0
	cmd = "ps -eO pid,lstart | grep -w " + str(pid) +" | grep -v grep"
	result = get_exec_cmd_result(cmd)
	results = result.split("\n")
	for tmp_result in results:
		tmp_result = tmp_result.strip()
		tmp_result_list = tmp_result.split()
		if str(pid) == tmp_result_list[1]:
			time_str = str(tmp_result_list[3]) + " " + str(tmp_result_list[4]) + " " + str(tmp_result_list[5]) + " " + str(tmp_result_list[6])
			cmd = "date -d '%s'"%(time_str)
			cmd += " +%s"
			start_time = get_exec_cmd_result(cmd)
	return str(start_time)

def get_the_oldest_pid(pid_list):
	tmp_list = []
	if len(pid_list) <= 0:
		tmp_list.append(0)
		tmp_list.append(-1)
		return tmp_list
	start_time = get_pid_start_time(pid_list[0])
	pid_1 = pid_list[0]
	for pid in pid_list:
		result_time = get_pid_start_time(pid)
		if result_time < start_time:
			start_time = result_time
			pid_1 = pid
			
	tmp_list.append(start_time)
	tmp_list.append(pid_1)
	return tmp_list

def get_pid_by_name(path):
	logging.info("get the task:%s's pid"%path)
	pid_list = []
	cmd = 'ps aux|grep -w ' + os.path.basename(path) + " |grep -v grep"
	info = get_exec_cmd_result(cmd)
	
	info = str(info)
	info = info.strip()
	
	infos = info.split('\n')
	
	if len(infos) == 0:
		pid_list.append(-1)
	
	for tmp_info in infos:
		if len(tmp_info) == 0:
			continue
		tmp_info_list = tmp_info.split()
		pid_list.append(tmp_info_list[1])
	
	if len(pid_list) == 0:
		pid_list.append(-1)
	else:
		pid_list = check_ps(path, pid_list)
	logging.info("pid: %s"%str(pid_list))

	return pid_list

#把XX:XX格式的时间转换成距00:00的分钟数
def trans_time_to_min(h_m_time):
	total_min = 0
	h_m_times = h_m_time.split(":")
	total_min =  int(h_m_times[0])*60 + int(h_m_times[1])
	return total_min

#根据到1970-01-01 00:00:00的秒数来判断当前时间是否在上次执行时间到间隔时间的范围内
def is_time_in_range_1(last_time, interval_time):
	now_time = int(time.time())
	if now_time < int(last_time):
		return False
	if now_time - int(last_time) > int(interval_time):
		return False
	else:
		return True

#根据到00:00的分钟数来判断当前时间是否在开始分钟数和结束分钟数的范围内
def is_time_in_range_2(time_list, now_time):
	begin_time = trans_time_to_min(time_list[0])
	now_time = trans_time_to_min(now_time)
	end_time = trans_time_to_min(time_list[1])
	
	if now_time > begin_time and now_time < end_time:
		return True
	return False

def is_end_time_bigger_than_begin_time(time_list):
	begin_time = trans_time_to_min(time_list[0])
	end_time = trans_time_to_min(time_list[1])
	
	if begin_time >= end_time:
		return False
	else: 
		return True

def check_ps(path,pid_list):
	pid_list_1 = []
	for pid in pid_list:
		proc_path = "/proc/%s"%(str(pid))
		if not os.path.exists(proc_path):
			continue
			
		exe_path = "%s/exe"%(proc_path)
		if not os.path.exists(exe_path):
			continue
			
		cmd_path = "%s/cmdline"%(proc_path)
		if not os.path.exists(cmd_path):
			continue
			
		cmd = "ls -al %s"%(exe_path)
		result = get_exec_cmd_result(cmd)
		if result.split()[-1] == path:
			pid_list_1.append(pid)
			continue
			
		cmd = "cat %s"%(cmd_path)
		result = get_exec_cmd_result(cmd)
		result_1 = repr(result)
		path_1 = str(os.path.basename(path))
		
		result_1.strip()
		path_1.strip()
		if path_1 in result_1:
			pid_list_1.append(pid)
	return pid_list_1

def kill_ps(path,pid_list):
	logging.info("kill the ps:%s"%(path))
	for pid in pid_list:
		cmd  = "kill -9 " + str(pid)
		logging.info("ps kill cmd:%s"%cmd)
		try:
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		except Exception,e:
			logging.error("%s"%e)

def start_ps(path):
	logging.info("start the ps:%s"%(path))
	if not os.path.exists(path):
		logging.error("%s does not exist"%path)
		return
	cmd  = "nohup " + path + " 1>/dev/null 2>/dev/null &"
	logging.info("ps start cmd:%s"%cmd)
	try:
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	except Exception,e:
		logging.error("%s"%e)

if __name__ == "__main__":
	#初始化配置文件模块
	cf = ConfigParser.ConfigParser()
	nn_daemon_v2_conf = "%s/nn_daemon_v2.conf"%(LOG_PATH)
	cf.read(nn_daemon_v2_conf)
	
	log_dir = ("%s/log"%(LOG_PATH))
	dir_path_check( log_dir)
	
	#初始化日志系统
	logging.basicConfig(filename='%s/%s.log.txt' % (log_dir, strftime("%Y%m%d%H")),
						format='%(asctime)s - %(levelname)s - %(message)s',
						datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "d",["debug"])
		if len(opts) == 1:
			#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
			console = logging.StreamHandler()
			console.setLevel(logging.INFO)
			formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
			console.setFormatter(formatter)
			logging.getLogger('').addHandler(console)
	except:
		logging.error("run getopt.getopt failed")
	
	logging.info("VERSION:%s begin running"%SERVER_VERSION)
	
	#程序防重入
	timer_id = [0]
	if daemon_lock_check(timer_id) != 0:
		logging.error("The time is too short")
		exit(0)
	
	#获得守护进程任务
	get_all_task_from_conf()
	logging.info("all task:%s"%str(task_info))
	
	for key in task_info:
		task_info[key].append( get_pid_by_name(task_info[key][0]) )
	
	for key in task_info:
		logging.info("get the oldest ps time:%s"%task_info[key][0])
		task_info[key].append( get_the_oldest_pid(task_info[key][3]))
		logging.info("%s's old time:%s pid:%s"%(task_info[key][0],task_info[key][4][0],task_info[key][4][1]))
	
	logging.info("task info:%s"%(str(task_info)))
	
	logging.info("gets the current time")
	now_time_hour_min = datetime.datetime.now().strftime("%H:%M")
	now_time_second = int(time.time())
	logging.info("hour_min:%s second:%s"%(str(now_time_hour_min), str(now_time_second)))
	
	#获得需要重启的进程，并杀掉
	for key in task_info:
		if int(task_info[key][1]) == NEVER_REBOOT_DAY:
			continue
		if is_end_time_bigger_than_begin_time(task_info[key][2]) == True:
			if is_time_in_range_2(task_info[key][2], now_time_hour_min) == True:
				if int(task_info[key][4][0]) > 0 and (now_time_second - int(task_info[key][4][0])) > (int(task_info[key][1])*24*60*60):
					kill_ps(task_info[key][0],task_info[key][3])
					task_info[key][4] = [0,-1]
		else:
			logging.warning("check the reboot_time %s:the end time must be bigger than the begin time."%(str(task_info[key][2])))
	
	#启动进程
	for key in task_info:
		if task_info[key][4][1] == -1:
			start_ps(task_info[key][0])
	
	
	tmp = timer_id[0]
	tmp_id_time = ["0"]
	get_lock_id(timer_id,tmp_id_time)
	if tmp == timer_id[0]:
		tmp_report = "%s/daemon.lock"%(LOG_PATH)
		os.remove(tmp_report)
		logging.info("delete the lock file")
	else:
		logging.error("delete the lock file failed")
	logging.info("--------------------------The end----------------------------------")