from util import *
import signal 
from typing import Optional, Any 
import time 
import yaml 

NOTIFICATION_DURATION = 10

TASK_NAMES = config.get_config('valid_task_names')

task_name = None 

client = pymongo.MongoClient()
db = client.zhitu_timer 
collection = db.record 


def signal_handler(signalnum, frame):
    stop_time = datetime.now()
    duration = int((stop_time - start_time).total_seconds())
    minutes = duration // 60

    send_mac_notification(f"The journey comes to an end! {minutes // 60}:{minutes % 60}")

    collection.insert_one({
        'date': date2str(get_real_date(start_time)),
        'task_name': task_name,
        'start_time': datetime2str(start_time),
        'duration_minutes': minutes,
    })
        
    get_saved_pid(delete_after=True)
    
    exit(0)
        
        
def main():
    saved_pid = get_saved_pid(delete_after=True)
    if saved_pid:
        os.kill(saved_pid, signal.SIGTERM)
        exit(0)

    last_task_name = config.get_config('last_task_name')

    global task_name    
        
    while True:
        task_name = inputbox(title='Hello, Zhituer!', prompt='Task name:', init_content=last_task_name)

        if not task_name:
            exit(0)
        elif task_name not in TASK_NAMES:
            pass 
        else:
            break 

    config.set_config('last_task_name', task_name)
    
    save_pid()
    
    global start_time 
    start_time = datetime.now() 

    signal.signal(signal.SIGTERM, signal_handler)
    
    send_mac_notification('Now take a good journey of Zhitu!')
    
    next_alert_minute = NOTIFICATION_DURATION
    
    while True:
        time.sleep(60)

        elapsed_minutes = (datetime.now() - start_time).total_seconds() // 60
        
        if elapsed_minutes >= next_alert_minute:
            send_mac_notification(f'{next_alert_minute // 60}:{next_alert_minute % 60}')
            next_alert_minute += NOTIFICATION_DURATION
        
        
if __name__ == '__main__':
    main() 
