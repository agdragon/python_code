import Queue
import sys

queue = Queue.Queue(2)

print "put a data into queue"
queue.put(1)
queue.put(None)

# print "put a data into queue again"
# queue.put(1)

a = queue.get()
print a

a = queue.get()
print a

queue.task_done()

# b = queue.get()
# print b

print sys.exc_info()