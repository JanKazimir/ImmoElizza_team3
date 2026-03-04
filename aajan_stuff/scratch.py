import time
from datetime import datetime

start_time = datetime.now()
print(f"starting at: {datetime.now()}")
time.sleep(1)
finished_time = datetime.now()
print(f"finished at: {datetime.now()}. Total time: {finished_time - start_time}")
print(datetime.now())