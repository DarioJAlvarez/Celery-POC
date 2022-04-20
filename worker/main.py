from celery import Celery
import time
from asgiref.sync import async_to_sync

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)



@app.task(name='add_long')
def long_task(x, y):
    print('Executing long task...')
    time.sleep(10)
    print('Long task finished!')
    return x + y


@app.task(name='add_short')
def short_task(x, y):
    print('Executing short task...')
    time.sleep(10)
    print('Short task finished!')
    return x + y
