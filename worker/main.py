from celery import Celery
import requests

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)



@app.task(name='add_long')
def long_task(x, y):
    print('Executing long task...')
    # Time consuming request
    response = requests.get('https://www1.ncdc.noaa.gov/pub/data/cdo/samples/PRECIP_HLY_sample_csv.csv')
    print(f'Long task finished!. Status code: {response.status_code}')
    return x + y


@app.task(name='add_short')
def short_task(x, y):
    print('Executing short task...')
    # Fast request
    response = requests.get('https://www.google.com')
    print(f'Short task finished!. Status code: {response.status_code}')
    return x + y
