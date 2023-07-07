from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time
from datetime import datetime
import asyncio

def job_that_executes_once():

    print("I'm working")

# schedule.every(3).seconds.do(job_that_executes_once)

def sh(text):
    def some_job():
        print("hi", text)

    # schedule.every(3).seconds.do(some_job)



async def my_async_function():
    # Your asynchronous logic here
    await asyncio.sleep(1)
    print("Async function executed")

async def main_async1(n):
    print(f"main_async1 start {n=}")
    await asyncio.sleep(.1)
    print(f"main_async1 end {n=}")

n = 0
scheduler = AsyncIOScheduler()


async def main_async2():
    while True:
        print("main_async2")
        await asyncio.sleep(.5)
        global n
        n+=1
        if n%3==0:
            scheduler.add_job(main_async1, 'interval', args=(n,), seconds=1)


async def gather():
    scheduler.start()
    await asyncio.gather(main_async2())


asyncio.run(gather())

# schedule.every(1).seconds.do(run_async_function)


asyncio.get_event_loop().run_forever()
