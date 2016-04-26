#coding=utf-8
import threading
# 创建全局ThreadLocal对象:
localVal = threading.local()
localVal.val = "Main-Thread"
def process_student():
    print '%s (in %s)' % (localVal.val, threading.current_thread().name)

def process_thread(name):
    #赋值
    localVal.val = name
    process_student()
    
t1 = threading.Thread(target= process_thread, args=('One',), name='Thread-A')
t2 = threading.Thread(target= process_thread, args=('Two',), name='Thread-B')

t1.start()
t2.start()
t1.join()
t2.join()
print localVal.val
# 打印结果：
# One (in Thread-A)
# Two (in Thread-B)
# Main-Thread