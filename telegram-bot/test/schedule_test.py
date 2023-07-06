import schedule
import time
from datetime import datetime

def job_that_executes_once():

    print("I'm working")

# schedule.every(3).seconds.do(job_that_executes_once)

def sh(text):
    def some_job():
        print("hi", text)

    schedule.every(3).seconds.do(some_job)

import schedule
import asyncio


async def my_async_function():
    # Your asynchronous logic here
    await asyncio.sleep(1)
    print("Async function executed")

async def main_async():
    while True:
        print("main_async")
        await asyncio.sleep(1)

def run_async_function():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(my_async_function())


schedule.every(1).seconds.do(run_async_function)

while True:
    schedule.run_pending()
