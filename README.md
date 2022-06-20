# Celery async

## What is Celery
Celery is a task queue that is used to distribute work along threads or machines.  
A task's queue input is an unit of work called task.  
Celery communicates via messages, usually using a broker to mediate between clients and workers.  
Someone demanding the execution of a task is the 'producer' and the executor is the 'worker'.

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
```
python -m celery -A main worker --loglevel=INFO  --pool=gevent
```


## Celery client
```py
from celery import Celery

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)

result = app.send_task("add", args=(4, 5))
response = result.get()  # Expected 9
```

## Run redis container

### Backend
```
docker run --name redis-backend -p 6380:6379 -d redis
```

### Broker
```
docker run --name redis-broker -p 6379:6379 -d redis
```

## Execution pools
When you start a Celery worker on the command line via ```celery --app=...```, you just start a supervisor process. The Celery worker itself does not process any tasks. It spawns child processes (or threads) and deals with all the book keeping stuff. The child processes (or threads) execute the actual tasks. These child processes (or threads) are also known as the execution pool.

### Pool options
- solo: single process which runs inside worker process. Interesting for CPU bound tasks in microservices environment using K8s for example.
- gevent: useful for I/O bound tasks. By specifiying a number of threads, Celery creates child processes to switch between tasks when a processed stay at idle state.
- eventlet: same as __gevent__.
- prefork: based on multiprocessing package, it's usefull for executing CPU bound tasks in parallel.


## Concurrency
Allows to set the number of processes/threads to be started by the worker. To enable concurrency we must start celery app with this command:
```
python -m celery -A main worker --loglevel=INFO  --pool=gevent --concurrency=10
```


## Log traceability (correlation-id propagation)
When working in a microservice application, it's mandatory for log traceability 
that microservices propagate a correlation id which will be printed in logging.

Celery provides a built-in tool to achive this, so we don't have to create our tasks
with an extra parameter. By just sending an extra argument to the task call, the logger
will be able to print the correlation id passed with no extra configuration.
```python
task_call = app.send_task("add_long", (3, 4), apply_async=True, task_id=correlation_id.get())
```