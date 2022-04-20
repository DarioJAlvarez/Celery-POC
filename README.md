# Celery async

## What is Celery
Celery is a task queue that is used to distribute work along threads or machines.  
A task's queue input is an unit of work called task.  
Celery communicates via messages, usually using a broker to mediate between clients and workers.

## Broker
Celery requires a solution to send and receive messages; usually this comes in the form of a separate service called a message broker.

## Backend
Results are not enabled by default. In order to do remote procedure calls or keep track of task results in a database, you will need to configure Celery to use a result backend.

## Celery worker
```py
from celery import Celery

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)

@app.task(name='add')
def add(x, y):
    return x + y
```

## Run Celery worker
```celery -A tasks worker --loglevel=INFO```


## Celery client
```py
from celery import Celery

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)

result = app.send_task("add", kwargs=(4, 5))
response = result.get()  # Expected 9
```