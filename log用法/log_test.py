import logging
import sys

log_1 = None
log_2 =None

def log_init(logger,tmp):
	logger = logging.getLogger("1")
	formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
	file_handler = logging.FileHandler(tmp)
	file_handler.setFormatter(formatter)
	stream_handler = logging.StreamHandler(sys.stderr)
	logger.addHandler(file_handler)
	logger.addHandler(stream_handler)
	logger.setLevel(logging.ERROR)
	logger.error("fuckgfw")
	logger.removeHandler(stream_handler)
	logger.error("fuckgov")
	
if __name__ == "__main__":
	log_init(log_1,"1.txt")
	log_init(log_2,"2.txt")
	