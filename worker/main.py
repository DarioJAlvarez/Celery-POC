from pkgutil import get_loader
from celery import Celery
from celery.signals import setup_logging
import requests
from task_formatter import TaskFormatter
import logging
import logging.config
import yaml


BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)


@setup_logging.connect
def setup_task_logger(**_):
    with open('./log_conf.yaml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    print(config)
    logging.config.dictConfig(config)
        

logger = logging.getLogger('celery_override')  # Name defined in log_conf.yaml


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
