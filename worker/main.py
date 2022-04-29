from celery import Celery
import requests
from celery.signals import after_setup_task_logger
from celery.app.log import TaskFormatter
from celery.utils.log import get_task_logger


BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)


@after_setup_task_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    for handler in logger.handlers:
        handler.setFormatter(TaskFormatter('%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s'))

logger = get_task_logger(__name__)
logger.setLevel('DEBUG')


@app.task(name='add_long')
def long_task(x, y):
    logger.debug('Executing long task...')
    # Time consuming request
    response = requests.get('https://www1.ncdc.noaa.gov/pub/data/cdo/samples/PRECIP_HLY_sample_csv.csv')
    logger.debug(f'Long task finished! Response: {response}')
    return x + y


@app.task(name='add_short')
def short_task(x, y):
    logger.debug('Executing short task...')
    # Fast request
    response = requests.get('https://www.google.com')
    logger.debug(f'Short task finished! Response: {response}')
    return x + y
