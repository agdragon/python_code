# coding=utf-8
#!/usr/bin/python
#脚本的用法 python nn_report.py
import json, urllib, urllib2, subprocess, sys, os, logging, time, socket, time, calendar, datetime, ConfigParser, socket, fcntl, struct
import getopt
from xml.etree import ElementTree
from time import strftime


SERVER_VERSION = '1.5.0'
TIME_FORMAT = '%Y%m%dT%H%M%SZ'
TIME_FORMAT_1 = '%Y%m%d%H%M%S'
CUR_PATH = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
LOG_PATH = CUR_PATH

START_TIME = int(time.time())


def create_s2_18_info(i):
	logging.info("create_s2_18_info is calling")
	
	report_info = {total_info[i][3]:{}}
	
	logging.info("get report info create utc time")
	report_info['hardware']['ct'] = get_current_utc_time()
	
	logging.info("get the cpu rate")
	report_info["hardware"]["cr"] = get_cpu_usage()
	
	server_id = get_conf_by_name("server.id")
	report_info["hardware"]["id"] = server_id
	
	#获取系统打开的socket
	used_socket = get_sockets()
	report_info["hardware"]["tlc"] = str(used_socket)
	
	#获得内存大小及使用率
	logging.info("get the mem info")
	mem_total = get_mem_total()
	report_info["hardware"]["m"] = str(mem_total)
	mem_rate = get_mem_usage()
	report_info["hardware"]["mr"] = str(mem_rate)
	
	#取得要获取磁盘大小的路径
	dir_mount = get_dir_mount()
	#得到挂在目录的列表
	value_list = dir_mount.values()
	value_list = unique_list(value_list)
	dir_list = dir_mount.keys()
	
	total_disk = 0
	free_disk = 0
	max_dr = 0.00
	max_ir = 0.00
	
	tmp_list = []
	tmp_dirct = {}
	tmp_dirct["d"] = tmp_list
	report_info["hardware"]["dl"] = tmp_dirct
	tmp_info = {}
	for d_path in dir_list:
		d_path_info = get_fs_path_disk_info(d_path)
		
		if dir_mount[d_path] in value_list:
			total_disk += int(d_path_info[0])
			free_disk += (int(d_path_info[0]) - int(d_path_info[1]))
			value_list.remove(dir_mount[d_path])
		
		tmp_info["n"] = d_path
		tmp_info["s"] = d_path_info[0]
		
		disk_usage = int(d_path_info[1]) / float(d_path_info[0])
		disk_rate = '%.2f' % (disk_usage * 100) 
		tmp_info["r"] = disk_rate
		if float(disk_rate) > float(max_dr):
			max_dr = disk_rate
		 
		tmp_info["itc"] = d_path_info[2] 
		if float(d_path_info[2]) != 0:
			inode_usage = (int(d_path_info[2]) - int(d_path_info[3])) / float(d_path_info[2])
		else:
			inode_usage = 0
		inode_rate = '%.2f' % (inode_usage * 100) 
		tmp_info["ifr"] = inode_rate
		if float(inode_rate) > float(max_ir):
			max_ir = inode_rate
		
		report_info["hardware"]["dl"]["d"].append("%s" % tmp_info)
	
	report_info["hardware"]["ts"] = str(total_disk)
	report_info["hardware"]["fs"] = str(free_disk)
	report_info["hardware"]["mdr"] = max_dr
	report_info["hardware"]["mir"] = max_ir
	
	net_card_list = get_net_card_list()
	net_info_dict = {}
	tmp_list = []
	tmp_dirct = {}
	tmp_dirct["i"] = tmp_list
	report_info["hardware"]["il"] = tmp_dirct
	tmp_info = {}
	net_info_dict = get_network_io_by_net_list(net_card_list)
	for key in net_info_dict:
		tmp_info = {}
		tmp_info["n"] = key
		tmp_info["sb"] = net_info_dict[key][0]
		tmp_info["rb"] = net_info_dict[key][0]
		report_info["hardware"]["il"]["i"].append("%s" % tmp_info)
		
	return report_info

def create_s2_19_info(i):
	logging.info("get cpu info")
	
	report_info = {total_info[i][3]:{}}
	
	cpu_num = get_cpu_phy_num()
	
	#获取cpu信息
	report_info["hardware_ext"]["cl"] = {}
	report_info["hardware_ext"]["cl"]["m"] = get_cpu_type()
	report_info["hardware_ext"]["cl"]["cc"] = get_cpu_core_num()
	
	#获取网卡列表
	tmp_list = []
	tmp_dirct = {}
	tmp_list.append(tmp_dirct)
	report_info["hardware_ext"]["i"] = tmp_list
	net_card_list = get_net_card_list()
	for net_card in net_card_list:
		tmp_dirct[net_card] = get_ip_address(net_card)
		
	report_info["hardware_ext"]["sys"] = {}
	report_info["hardware_ext"]["sys"]["ofc"] = get_open_fd_max_num()
	report_info["hardware_ext"]["sys"]["sv"] = get_system_version()
	
	report_info["hardware_ext"]["ml"] = {}
	report_info["hardware_ext"]["ml"]["c"] = get_mem_phy_num()
	report_info["hardware_ext"]["ml"]["ca"] = get_mem_phy_total()
	
	return report_info

#			  "接口名"	"间隔时间:秒"	"保留时间:秒" 	"参数"	 		"接口函数"	
s2_18_list = ["s2_18",	2*60,  			45*60, 		  	"hardware",		create_s2_18_info]
s2_19_list = ["s2_19",	59*60,			60,				"hardware_ext",	create_s2_19_info]

total_info = []
total_info.append(s2_18_list)
total_info.append(s2_19_list)

def get_current_local_time():
	local = datetime.datetime.now()
	return local.strftime(TIME_FORMAT_1)

def get_current_utc_time():
	utc = datetime.datetime.utcnow()
	return utc.strftime(TIME_FORMAT)

#list去重
def unique_list(old_list):
	newList = []
	for x in old_list:
		if x not in newList :
			newList.append(x)
	return newList

#配置名为name的配置信息是以分号隔开的，返回配置信息列表
def get_conf_list(name):
	tmp_list = []
	filename = "%s/nn_report_v2.conf"%(CUR_PATH)
	f = open(filename, "r")
	line = f.readline()
	
	while line:
		if line.startswith(name):
			line = line.strip('\r\n') 
			array = line.split('=')
			value = array[1].split(";")
			for path in value:
				tmp_list.append(path)
			break
		line = f.readline()
	f.close()
	return tmp_list

#返回配置名为name的配置信息的值
def get_conf_by_name(name):
	conf = ''
	filename = "%s/nn_report_v2.conf"%(CUR_PATH)
	f = open(filename, "r")
	line = f.readline()
	
	while line:
		if line.startswith(name):
			line = line.strip('\r\n') 
			array = line.split('=', 1)
			conf = array[1]
			break
		line = f.readline()
	f.close()
	return conf

#检查路径dir_path是否存在，不存在则创建
def dir_path_check(dir_path):
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

#执行一个命令,将结果返回
def get_exec_cmd_result(cmd):
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	a=p.stdout.read().decode('utf8')
	return a.strip()

def get_cpu_usage():
	f = open('/proc/stat', 'r')
	line = f.readline().split()
	logging.info("line is %s"%line)
	user = line[1]
	nice = line[2]
	system = line[3]
	idle = line[4]
	iowait = line[5]
	irq = line[6]
	softirq = line[7]
	f.close()
	used = int(user) + int(nice) + int(system)
	total = int(user) + int(nice) + int(system) + int(idle) + int(iowait) + int(irq) + int(softirq)
	
	time.sleep(3)
	
	f = open('/proc/stat', 'r')
	line = f.readline().split()
	logging.info("line is %s"%line)
	user2 = line[1]
	nice2 = line[2]
	system2 = line[3]
	idle2 = line[4]
	iowait2 = line[5]
	irq2 = line[6]
	softirq2 = line[7]
	f.close()
	used2 = int(user2) + int(nice2) + int(system2)
	total2 = int(user2) + int(nice2) + int(system2) + int(idle2) + int(iowait2) + int(irq2) + int(softirq2)
	
	cpu_usage = (int(used2) - int(used)) / (float(total2) - float(total))
	cpu_rate = '%.2f' % (cpu_usage * 100)
	return cpu_rate

def get_sockets():
	used_socket = get_exec_cmd_result("netstat -na | grep ESTAB | wc -l")
	return used_socket

#得到内存信息,单位M
def get_mem_total():
	memtotal = 0
	f = open('/proc/meminfo', 'r')
	for line in f.readlines():
		if line.startswith('MemTotal:'):
			memtotal = (int(line.split(' ')[-2]))/1024
			break
	f.close()
	return memtotal
 
def get_mem_usage():
	f = open('/proc/meminfo', 'r')
	for line in f.readlines():
		if line.startswith('MemTotal:'):
			memtotal = line.split(' ')[-2]
		elif line.startswith('MemFree:'):
			memfree = line.split(' ')[-2]
		elif line.startswith('Buffers:'):
			buffers = line.split(' ')[-2]
		elif line.startswith('Cached:'):
			cached = line.split(' ')[-2]
		elif line.startswith('SwapTotal:'):
			swaptotal = line.split(' ')[-2]
		elif line.startswith('SwapFree:'):
			swapfree = line.split(' ')[-2]
	f.close()

	mem_usage = (int(memtotal) - int(memfree) - int(buffers) - int(cached)) / float(memtotal) * 100
	mem_rate = '%.2f' % mem_usage
	return mem_rate

#得到路径和挂载点对应关系的字典
def get_dir_mount():
	dir_mount = dict()
	f = open('/proc/mounts', 'r')
	for line in f.readlines():
		if line.startswith(r'/dev') and 'chroot' not in line:
			line = line.split()
			dir_mount[line[1]] = line[0]
	f.close()
	return dir_mount 
 
	dir_mount = dict()
	f = open('/proc/mounts', 'r')
	for line in f.readlines():
		if line.startswith(r'/dev') and 'chroot' not in line:
			line = line.split()
			dir_mount[line[1]] = line[0]
	f.close()
	return dir_mount

#得到指定路径磁盘大小
def get_fs_path_disk_info(pathname):
	disk_list = []
	total = 0
	used = 0
	disk = os.statvfs(pathname)
	total = total + (int(disk.f_frsize * disk.f_blocks)/(1024 * 1024))
	used = used + (int(disk.f_frsize * (disk.f_blocks - disk.f_bfree)/(1024 * 1024)))
	
	disk_list.append('%d' % total)
	disk_list.append('%d' % used)
	disk_list.append('%d' % disk.f_files)
	disk_list.append('%d' % disk.f_ffree)
	return disk_list
 
#得到网卡列表
def get_net_card_list():
	f = open('/proc/net/dev', 'r')
	lines = f.readlines()
	f.close()
	
	net_card_list = []
	
	for line in lines[2:]:
		if 'Inter' in line or 'face' in line or 'lo:' in line:
			continue
		else:
			name = line.strip().split(':')[0]
			net_card_list.append(name)
			
	return net_card_list

#得到指定网卡的信息
def get_network_io_by_net_list(net_list):
	net_speed = {}
	receive_byte_1 = []
	transmit_byte_1 = []
	
	receive_byte_2 = []
	transmit_byte_2 = []
	
	total_list_1 = {}
	total_list_2 = {}
	
	
	f = open('/proc/net/dev', 'r')
	lines = f.readlines()
	f.close()
	
	for net_card_name in net_list:
		tmp_list = []
		total_list_1[net_card_name] = tmp_list
		for line in lines[2:]:
			if net_card_name in line:
				line = line.split(':')[-1].strip().split()
				tmp_list.append(int(line[0]))
				tmp_list.append(int(line[8]))
				break
  
	time.sleep(1)
		
	f = open('/proc/net/dev', 'r')
	lines = f.readlines()
	f.close()
	
	for net_card_name in net_list:
		tmp_list = []
		total_list_2[net_card_name] = tmp_list
		for line in lines[2:]:
			if net_card_name in line:
				line = line.split(':')[-1].strip().split()
				tmp_list.append(int(line[0]))
				tmp_list.append(int(line[8]))
				break
	
	receive_bytes_rate =  0
	transmit_bytes_rate = 0
	receive_bytes_rate_1 = 0
	transmit_bytes_rate_1 = 0
	for net_card_name in net_list:
		tmp_list = []
		net_speed[net_card_name] = tmp_list
	
		receive_bytes_rate = (int(total_list_2[net_card_name][0]) - int(total_list_1[net_card_name][0])) * 1.0 / (1024*1024)
		transmit_bytes_rate = (int(total_list_2[net_card_name][1]) - int(total_list_1[net_card_name][1])) * 1.0 / (1024*1024)
		receive_bytes_rate_1 = '%.2f'%receive_bytes_rate
		transmit_bytes_rate_1 = '%.2f'%transmit_bytes_rate
		tmp_list.append(receive_bytes_rate_1)
		tmp_list.append(transmit_bytes_rate_1)
	
	return net_speed  
 
def get_cpu_phy_num():
	mem_num = get_exec_cmd_result("cat /proc/cpuinfo | grep 'physical id' | sort | uniq | wc -l")
	return mem_num

def get_cpu_core_num():
	try:
		mem_num = get_exec_cmd_result("cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c").strip().split[0]
	except Exception,e:
		mem_num = "unknown"
	return mem_num

def get_cpu_type():
	cpu_type = None
	f = open('/proc/cpuinfo', 'r')
	for line in f.readlines():
		if line.startswith('model name'):
			cpu_type = (line.strip().split(':')[-1]).strip()
			break
	f.close()
	return cpu_type
	
def get_mem_phy_num():
	try:
		cpu_num = get_exec_cmd_result("dmidecode -t 17 | grep 'Size.*MB' | wc -l")
	except Exception,e:
		logging.error("%s"%e)
		cpu_num = "unknown"
	return cpu_num

def get_mem_phy_total():
	cpu_total = None
	try:
		result = get_exec_cmd_result("dmidecode -t 17 | grep 'Size.*MB' ")
		results = result.split('\n')
		for tmp_result in results:
			cpu_total += int( tmp_result.strip().split(':')[-1].strip().split()[0] )
	except Exception,e:
		logging.error("%s"%e)
		cpu_total = "unknown"
	return cpu_total

#如果网卡有IP地址，则返回；不存在，则返回空
def get_ip_address(ifname):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
		return socket.inet_ntoa(fcntl.ioctl( s.fileno(), 0x8915,struct.pack('256s', ifname[:15]) )[20:24])
	except:
		return ""

def get_open_fd_max_num():
	open_fd_max_num = get_exec_cmd_result("cat /proc/sys/fs/file-max")
	return open_fd_max_num
	
def get_system_version():
	try:
		versio = get_exec_cmd_result("uname -a")
	except Exception,e:
		versio = "unknown"
	return versio		
		
#检测程序是否可以执行。返回0可以执行，返回非0则不能执行
def report_lock_check(id):
	id_time = ["0"]
	get_lock_id(id,id_time)
	
	#从配置文件中取得时间，然后比较
	time_2 = get_conf_by_name("interval_time")
	
	interval_time = float(time_2)
	last_time = float(id_time[0])
		
	if check_time_is_in_range(last_time, interval_time) == False :
		id[0] = id[0] + 1
		report_lock_modify(id[0])
		return 0
	else:
		#logging
		logging.error("the current:%s last:%s interval:%s" %(str(time.time()),str(last_time), str(interval_time)))
		return -1

		
#这个函数主要是修改report_lock文件，或者创建
def report_lock_modify(id):
	tmp_report = "%s/report.lock"%(LOG_PATH)
	f = open(tmp_report, 'w')
	str = "time="
	str_3 = '\r\n'
	time_str = time.time()
	str_1 = "%s%f%s"%(str, time_str, str_3)
	f.write(str_1)
	
	f.write('id=%d' % id)
	f.close()

def get_lock_id(id, id_time):
	id[0] = 0
	tmp_report = "%s/report.lock"%(LOG_PATH)
	if os.path.exists(tmp_report):
		f = open(tmp_report, "r")
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

def get_time_conf(cf,str_tmp):
	sections = cf.sections()
	if "last_time" not in sections:
		cf.add_section("last_time")
		set_time_conf(cf,str_tmp)
		return 0
	else:
		options = cf.options("last_time")
		if str_tmp not in options:
			set_time_conf(cf,str_tmp)
			return 0
		else:
			return cf.get("last_time", str_tmp)

def set_time_conf(cf,str_tmp):
	cf.set("last_time", str_tmp, str(int(time.time())))
	report_time = "%s/nn_report.time"%(LOG_PATH)
	f = open(report_time, "w")
	cf.write(f)
	f.close()

def check_time_is_in_range(last_time, interval_time):
	now_time = int(time.time())
	if now_time < int(last_time):
		return False
	if now_time - int(last_time) > int(interval_time):
		return False
	else:
		return True

#判断当前时间是否存在对应的文件,如果不存在则创建
def cur_time_file_check(id_report):
	utc = datetime.datetime.now()
	#首先检测年月日对应的文件
	y_m_d = utc.strftime("%Y%m%d")
	y_m_d_path = ("%s/%s")%(id_report, y_m_d)
	dir_path_check(y_m_d_path)
	
	#检测对应小时的文件是否存在
	h_dir = utc.strftime("%H")
	h_path = ("%s/%s")%(y_m_d_path,h_dir)
	dir_path_check(h_path)
	
	#最后将h_path的路径下当前utc时间对应的文件的路径返回
	file_name = utc.strftime("%Y%m%d%H%M%S")
	filename = ("%s/%s.txt")%(h_path,file_name)
	return filename	

#将保存为json格式的字典保存到指定的文件中
def save_json_into_file(data, file_name):
	f = open(file_name,"w")
	f.write(data)
	f.close()

def encode_json_data(report_info):
  return json.dumps(report_info, encoding='utf-8')

def create_info(url_list):
	logging.info("create_info is calling %d"%(len(total_info)))
	
	json_data = {}
	for i in range(len(total_info)):
		last_time = get_time_conf(cf,total_info[i][0])
		interval_time = total_info[i][1]
		logging.info("name:%s  last:%s interval:%s"%(total_info[i][0],last_time, str(interval_time)))
		if check_time_is_in_range(last_time, interval_time) == False:
			
			#调用json的生成函数
			json_data = total_info[i][4](i)
			json_data = encode_json_data(json_data)
			logging.info(json_data)
			
			#存文件
			for j in range(len(url_list)):
					tmp_report_dir = "%s/%s/%d"%(LOG_PATH,total_info[i][0],j)
					filename = cur_time_file_check(tmp_report_dir)
					logging.info("The file name: %s"%filename)
					save_json_into_file(json_data, filename)
					
			set_time_conf(cf,total_info[i][0])
			
		else:
			logging.error("wait %s"%total_info[i][0])

def get_ret_from_xml(xml_text):
	ret_list = []
	root = ElementTree.fromstring(xml_text)
	
	lst_node = root.getiterator("result")
	if lst_node[0].attrib.has_key("ret") > 0 :
		ret = lst_node[0].attrib['ret']
		reason = lst_node[0].attrib['reason']
	ret_list.append(ret)
	ret_list.append(reason)
	return ret_list
	
def post_file_list(file_list, url, max_upload_time):
	#设置超时时间
	upload_count = 0
	success_count = 0
	logging.info("-------------The url is-------------\r\n%s (%d)"%(url, len(file_list)))
	for i in file_list:
		if check_time_is_in_range(START_TIME, max_upload_time) == False:
			logging.info("upload time is bigger than the max upload time")
			return upload_count
			
		logging.info("post:%s"%i)
		if not os.path.exists(i):
			logging.warning("the file %s is not exists"%i)
			continue
		
		f = open(i)
		json_info = f.read()
		f.close()
		logging.info("the json_info is %s"%json_info)
		
		#发送总次数+1
		upload_count += 1
		
		request = urllib2.Request(url, json_info)
		try:
			response = urllib2.urlopen(request,timeout=60)
			http_code = response.code
			html = response.read() 
			logging.info("get the http code is %d"%http_code)
			logging.info("get the html is %s"%html)
			
			if http_code == 200:
				ret_xml_list = get_ret_from_xml(html)
				xml_ret = int(ret_xml_list[0])
			
				logging.info("the ret is %d,reason is %s"%(xml_ret,ret_xml_list[1]))
				if xml_ret == 0:
					success_count += 1
					logging.info("post ok,then remove the %s"%i)
					if os.path.exists(i):
						#需要将文件删除
						os.remove(i)
				elif xml_ret == 3:
					logging.info("unsupport,so delete file:%s"%i)
					if os.path.exists(i):
						#需要将文件删除
						os.remove(i)
			else:
				logging.error("post not ok")
			response.close()
		
		except Exception,e:
			logging.error("%s"%e)
			
	return upload_count

def get_upload_file_list(report_dir,max_count):
	file_list = []
	if not os.path.exists(report_dir):
		return file_list
	y_m_d = os.listdir(report_dir)
	y_m_d.sort()
	y_m_d.reverse()
	
	for i in y_m_d:
		day_path = "%s/%s"%(report_dir,i)
		#logging.info("day_path:%s"%day_path)
		
		if not os.path.exists(day_path):
			return file_list
			
		y_m_d_h = os.listdir(day_path)
		y_m_d_h.sort()
		y_m_d_h.reverse()
		
		for j in y_m_d_h:
			hour_path = "%s/%s"%(day_path, j)
			#logging.info("hour_path:%s"%hour_path)
			
			if not os.path.exists(hour_path):
				return file_list
				
			y_m_d_h_file = os.listdir(hour_path)
			y_m_d_h_file.sort()
			y_m_d_h_file.reverse()
			
			for k in y_m_d_h_file:
				file_path = "%s/%s"%(hour_path,k)
				file_list.append(file_path)
				#logging.info("file_path:%s file_count:%d,max_count:%d"%(file_path,len(file_list),max_count))
				if len(file_list) >= max_count:
					return file_list
				
	return file_list

def upload_info(url_list):
	file_list = []
	upload_count = []
	max_count = int( get_conf_by_name("max_upload_count"))
	
	max_upload_time = int( get_conf_by_name("max_upload_time"))
	
	for j in range(len(url_list)):
		upload_count.append(0)
	
	for i in range(len(total_info)):
		for j in range(len(url_list)):
			if check_time_is_in_range(START_TIME, max_upload_time) == False:
				logging.info("upload time is bigger than the max upload time")
				return
			if upload_count[j] < max_count:
				tmp_report_dir = "%s/%s/%d"%(LOG_PATH,total_info[i][0],j)
				url = url_list[j]
				logging.info("check_upload:%s, url:%s"%(tmp_report_dir, url))
				
				file_list = get_upload_file_list(tmp_report_dir, max_count-upload_count[j])
				url =  "%s?func=report_stat_hardware&hardware_id=%s&data_type=xml&report_version=%s"%(url_list[j],get_conf_by_name("server.id"),SERVER_VERSION)
				num = post_file_list(file_list, url, max_upload_time)
				logging.info("-----------this url post end,num:%d-----------------"%num)
				upload_count[j] += num

def rm_json_dir():
	logging.info("rm_json_dir run")
	
	for i in range(len(total_info)):
		path = "%s/%s"%(LOG_PATH,total_info[i][0])
		
		valid_time_m = int(total_info[i][2])/60
		if valid_time_m < 1:
			valid_time_m = 1
		logging.info("check_over_time_info:%s valid_time:%d(min)"%(path,valid_time_m))
		
		if not os.path.exists( path):
			continue
		
		#先删除过时文件
		try:
			cmd_str = "find %s/ -name '*.txt' -type f -cmin +%d -exec rm -f {} \;"%(path,valid_time_m)
			logging.info("delete the file's cmd is: %s"%cmd_str)
			os.system(cmd_str)
		except Exception, e:
			logging.error("%s"%e)
		
		#再删除一些空目录
		try:
			cmd_str_1 = "find  %s/ -depth -empty -type d -cmin +%d -exec rmdir {} \;"%(path,valid_time_m)
			logging.info("delete the empty path's cmd is: %s"%cmd_str_1)
			os.system(cmd_str_1)
		except Exception, e:
			logging.error("%s"%e)

def rm_log():
	path = "%s/log"%(LOG_PATH)
	t1 = (int(get_conf_by_name("log_time")))*60
	if t1 < 1:
		t1 = 1
	try:
		cmd_str = "find %s/ -name '*.log.txt' -type f -cmin +%d -exec rm -f {} \;"%(path,t1)
		logging.info("delete the log file:%s"%cmd_str)
		os.system(cmd_str)
	except Exception, e:
		logging.error("%s"%e)

if __name__ == '__main__':
	server_id = get_conf_by_name("server.id")
	LOG_PATH = "%s/%s.report"%(CUR_PATH,server_id)
	
	#检测对应设备ID的日志路径是否存在，不存在则创建
	logdir = "%s/log"%(LOG_PATH)
	dir_path_check(logdir)
	
	#初始化配置文件模块
	cf = ConfigParser.ConfigParser()
	report_time = "%s/nn_report.time"%(LOG_PATH)
	cf.read(report_time)
	
	#初始化日志系统
	logging.basicConfig(filename='%s/%s.log.txt' % (logdir, strftime("%Y%m%d%H")),
						format='%(asctime)s - %(levelname)s - %(message)s',
						datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "d",["debug"])
		if len(opts) == 1:
			#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
			console = logging.StreamHandler()
			console.setLevel(logging.INFO)
			formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
			console.setFormatter(formatter)
			logging.getLogger('').addHandler(console)
	except:
		logging.error("run getopt.getopt failed")
	
	
	logging.info("VERSION:%s begin run"%SERVER_VERSION)
	timer_id = [0]
	if report_lock_check(timer_id) != 0:
		logging.error("The time is too short")
		exit(0)
	
	#得到上传地址列表
	logging.info("get the post url")
	url_list = get_conf_list("report.url")
	
	rm_json_dir()
	rm_log()
	
	create_info(url_list)
	upload_info(url_list)
	
	tmp = timer_id[0]
	tmp_id_time = ["0"]
	get_lock_id(timer_id,tmp_id_time)
	if tmp == timer_id[0]:
		tmp_report = "%s/report.lock"%(LOG_PATH)
		os.remove(tmp_report)
		logging.info("delete the lock file")
	else:
		logging.error("delete the lock file failed")
	
	