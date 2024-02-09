from celery import Celery

from config import Settings


celeryApp: Celery = Celery('tasks', broker=Settings.REDIS_DSN, backend=Settings.REDIS_DSN, include=['routers.arithmetic.tasks'])
    