from util import *
import signal 
from typing import Optional, Any 
import time 
import yaml 

NOTIFICATION_DURATION = 10

task_name = None 


def signal_handler(signalnum, frame):
    stop_time = datetime.now()
    duration = int((stop_time - start_time).total_seconds())
    minutes = duration // 60

    if minutes >= 5 or True:
        send_mac_notification(f"The journey comes to an end! {minutes // 60}:{minutes % 60}")

        schema.Record.create(
            date=start_time,
            start_time=start_time,
            end_time=stop_time,
            duration_minutes=minutes,
            desc=task_name,
        )
    else:
        send_mac_notification("The journey comes to an end, but takes too short!")
        
    get_saved_pid(delete_after=True)
    
    exit(0)
        
        
def main():
    saved_pid = get_saved_pid(delete_after=True)
    if saved_pid:
        os.kill(saved_pid, signal.SIGTERM)
        exit(0)

    last_task_name = config.get_config('last_task_name')

    global task_name    
        
    task_name = inputbox(title='你好，知兔', prompt='请输入任务名称：', init_content=last_task_name)
    # task_name = '学习'

    if not task_name:
        exit(0)
    else:
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
