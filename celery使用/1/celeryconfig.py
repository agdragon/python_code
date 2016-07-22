#!/usr/bin/env python
# coding=utf-8

from kombu import Exchange,Queue

BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

CELERY_QUEUES = (
		Queue("default",Exchange("default"),routing_key="default"), 
		Queue("for_task_A",Exchange("for_task_A"),routing_key="task_a"),
		Queue("for_task_B",Exchange("for_task_B"),routing_key="task_a"),
	)
    
CELERY_ROUTES = {
	'tasks.taskA':{"queue":"for_task_A","routing_key":"task_a"},
	'tasks.taskB':{"queue":"for_task_B","routing_key":"task_b"},
}