from celery import Celery
import requests
from celery.signals import after_setup_task_logger, setup_logging
from celery.app.log import TaskFormatter
from celery.utils.log import get_task_logger
import yaml
import logging


BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)


@setup_logging.connect
def setup_task_logger(*args, **kwargs):
    from logging.config import dictConfig
    try:
        with open('log_conf.yaml', 'r') as f:
            config = yaml.full_load(f)
            dictConfig(config)
    except Exception as e:
        print(f'Error loading logging config: {e}')
    # print("ok")
    # x = config['formatters']
    # y = logger.handlers
    # for handler in logger.handlers:
    #     if True or handler.formatter:
    #         x = handler.formatter
    #         try:
    #             handler.setFormatter(TaskFormatter('%(task_id)s - %(task_name)s -_-_- %(message)s'))



    # print("ok")

    # for handler in logger.handlers:
    #     handler.setFormatter(config['formatters']['simple_format'])

logger = logging.getLogger('celery_override')
logger.setLevel('DEBUG')


@app.task(name='add_long')
def long_task(x, y):
    logger.info('Executing long task...')
    # Time consuming request
    response = requests.get('https://www1.ncdc.noaa.gov/pub/data/cdo/samples/PRECIP_HLY_sample_csv.csv')
    logger.info(f'Long task finished! Response: {response}')
    return x + y


@app.task(name='add_short')
def short_task(x, y):
    logger.info('Executing short task...')
    # Fast request
    response = requests.get('https://www.google.com')
    logger.info(f'Short task finished! Response: {response}')
    return x + y
