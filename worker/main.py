from celery import Celery
from celery.signals import after_setup_task_logger, setup_logging, celeryd_init
from celery.utils.log import get_task_logger
import yaml
import time
import logging


BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)



@celeryd_init.connect
def setup_log_format(sender, conf, **kwargs):
    with open('log_conf.yaml') as f:
        config = yaml.full_load(f)
    conf.worker_log_format = config['worker_format']
    conf.worker_task_log_format = config['task_format']

print("Logging setup")

for h in logging.root.handlers:
    print(h)

logger = logging.getLogger('celery.task')
# logger = get_task_logger()  # also works


@app.task(name='add_long')
def long_task(x, y):
    logger.info('Executing long task...')
    # Time consuming request
    time.sleep(1)
    logger.info(f'Long task finished!')
    return x + y


@app.task(name='add_short')
def short_task(x, y):
    logger.info('Executing short task...')
    # Fast request
    time.sleep(0.1)
    logger.info(f'Short task finished!')
    return x + y
