from celery import Celery
import time 

celery = Celery('tasks', backend='redis://:juchongai@127.0.0.1:6379/1', broker='redis://:juchongai@127.0.0.1:6379/1')


@celery.task
def test(strs):
    return strs
    
