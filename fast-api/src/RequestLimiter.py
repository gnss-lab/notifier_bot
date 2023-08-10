import time

from fastapi import HTTPException, status


class RequestLimiter:
    def __init__(self, times=1, seconds=1):
        self.last_time = 0
        self.times_per_second = times/seconds
        # 1 / self.times_per_second
        self.min_delay = seconds/times

    def __call__(self):
        print(self.last_time)
        now = time.time()
        if now - self.last_time < self.min_delay:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"The API can process only {self.times_per_second} requests per second"
            )
        self.last_time = now
