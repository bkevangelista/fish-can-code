import time

async def timer(secs):
    print("Start timer")
    for i in range(secs):
        time.sleep(1)
    print("Timer up!")