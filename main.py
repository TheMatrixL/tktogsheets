from keep_alive import keep_alive
from sendgs import send_to_gs
from datetime import date, datetime
from pytz import timezone    
import time
import multiprocessing

import os
global_label = os.environ['global_label']
big_brand_drop = os.environ['big_brand_drop']
today_arrivals = os.environ['today_arrivals']
clearance = os.environ['clearance']

def current_time():
  now = datetime.now(timezone('Europe/London'))
  current_time = now.strftime("%H:%M:%S")
  return current_time

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]
  
keep_alive()


while True :

  if is_between(current_time(), ("12:00", "12:30")) or is_between(current_time(), ("08:00", "08:30")) or is_between(current_time(), ("16:00", "16:30")):
    
    process1 = multiprocessing.Process(target=send_to_gs(global_label, "Global Label"))
    process2 = multiprocessing.Process(target=send_to_gs(big_brand_drop, "Big Brand Drop"))
    process3 = multiprocessing.Process(target=send_to_gs(today_arrivals, "Today Arrivals"))
    process4 = multiprocessing.Process(target=send_to_gs(clearance, "Clearance"))    

    process1.start(), process2.start(), process3.start(), process4.start()
    process1.join(), process2.join(), process3.join(), process4.join()
    
    # send_to_gs(global_label, "Global Label")
    # send_to_gs(big_brand_drop, "Big Brand Drop")
    # send_to_gs(today_arrivals, "Today Arrivals")
    # send_to_gs(clearance, "Clearance")
    time.sleep(1800)
  else:
    time.sleep(1800)


