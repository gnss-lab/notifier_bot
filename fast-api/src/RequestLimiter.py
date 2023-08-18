import time

from fastapi import HTTPException, status
from loguru import logger

class RequestLimiter:
    def __init__(self, times=1, seconds=1):
        self.last_time = 0
        self.counter = 0
        self.times = times
        self.seconds = seconds

    def __call__(self):
        now = time.time()
        if now - self.last_time > self.seconds:
            self.last_time = now
            self.counter = 1
        else:
            self.counter+=1

        if self.counter > self.times:
            logger.error(f"More than {self.times} requests per {self.seconds} seconds")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"The API can process only {self.times} requests per {self.seconds} seconds"
            )