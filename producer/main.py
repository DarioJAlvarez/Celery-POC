from celery import Celery
import time

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)


# Send 3 tasks to Celery
print('Sending short task...')
short_result = app.send_task("add_short", (1, 2), apply_async=True, task_id="custom_task_id")
print('Sending long task...')
long_result = app.send_task("add_long", (3, 4), apply_async=True)
print('Sending another short task...')
start = time.time()
another_short_result = app.send_task("add_short", (5, 6), apply_async=True)


# Wait for the last task sended to finish and check for elapsed time.
# Check previous tasks do not block the main thread.
response = another_short_result.get()
print(f'Last task finished in: {time.time() - start :.2f} seconds')
response = long_result.get()
print(f'Response: {response} {long_result.task_id}')
