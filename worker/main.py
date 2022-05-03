from pkgutil import get_loader
from celery import Celery
from celery.signals import setup_logging
import requests
from task_formatter import TaskFormatter
# from celery.app.log import TaskFormatter
from celery.utils.log import get_task_logger
import logging


BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)


@setup_logging.connect
def setup_task_logger(**_):
    # logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger()
    sh = logging.StreamHandler()
    sh.setFormatter(TaskFormatter('%(asctime)s - %(task_id)s - %(levelname)s - %(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(sh)
        

# logger = get_task_logger(__name__)
logger = logging.getLogger(__name__)
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
