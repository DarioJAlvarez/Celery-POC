from celery import Celery

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6380/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)

print('Sending short task...')
short_result = app.send_task("add_short", (1, 2))
print('Sending long task...')
long_result = app.send_task("add_long", (3, 4))
print('Sending another short task...')
another_short_result = app.send_task("add_short", (5, 6))

response = short_result.get()  # Expected 3
print(f'Response: {response}')

response = another_short_result.get()  # Expected 7
print(f'Response: {response}')

response = long_result.get()  # Expected 7
print(f'Response: {response}')