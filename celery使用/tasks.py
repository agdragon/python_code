#!/usr/bin/env python
# coding=utf-8

from celery import Celery, platforms

app = Celery("tasks")

platforms.C_FORCE_ROOT = True

app.config_from_object("celeryconfig")

@app.task
def taskA(x,y):
    return x + y

@app.task
def taskB(x,y,z):
     return x + y + z

@app.task
def add(x,y):
    return x + y