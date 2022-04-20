from celery import Celery
import asyncio
from asgiref.sync import async_to_sync

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)



##################################################################
### LONG TASK (10s)
##################################################################

async def long_task_async(x, y):
    await asyncio.sleep(10)
    return x + y

@app.task(name='add_long')
def long_task(x, y):
    print('Executing long task...')
    result = async_to_sync(long_task_async)(x, y)
    print('Long task finished!')
    return f'long task finished: {result}'


##################################################################
### SHORT TASK (1s)
##################################################################

async def short_task_async(x, y):
    await asyncio.sleep(1)
    return x + y

@app.task(name='add_short')
def short_task(x, y):
    print('Executing short task...')
    result = async_to_sync(short_task_async)(x, y)
    print('Short task finished!')
    return f'short task finished: {result}'
