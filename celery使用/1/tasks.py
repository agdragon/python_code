#!/usr/bin/env python
# coding=utf-8

from celery import Celery, platforms

celery = Celery("tasks")

platforms.C_FORCE_ROOT = True

celery.config_from_object("celeryconfig")

@celery.task
def taskA(x,y):
    return x + y

@celery.task
def taskB(x,y,z):
     return x + y + z


@celery.task
def add(x, y):
	print "x" * 50
	return int(x) + int(y)