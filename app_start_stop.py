from util import *
import signal 
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
        
    get_and_delete_saved_pid()
    
    exit(0)
        
        
def get_and_delete_saved_pid() -> int:
    try:
        with open('./state.yaml', 'r', encoding='utf-8') as fp:
            obj = yaml.safe_load(fp)
            
        return obj['pid']

    except Exception:
        return -1 
    
    finally:
        with open('./state.yaml', 'w', encoding='utf-8') as fp:
            pass 
    
    
def save_pid():
    obj = { 'pid': os.getpid() }
        
    with open('./state.yaml', 'w', encoding='utf-8') as fp:
        obj = yaml.safe_dump(obj, fp)


def main():
    saved_pid = get_and_delete_saved_pid()
    if saved_pid > -1:
        os.kill(saved_pid, signal.SIGTERM)
        exit(0)

    global task_name        
    task_name = inputbox(title='你好，知兔', prompt='请输入任务名称：')
    if not task_name:
        exit(0)
    
    save_pid()
    
    global start_time 
    start_time = datetime.now() 

    signal.signal(signal.SIGTERM, signal_handler)
    
    send_mac_notification('Now take a good journey of Zhitu!')
    
    total_minutes = 0
    
    while True:
        for _ in range(NOTIFICATION_DURATION):
            time.sleep(60)
            total_minutes += 1
            
        send_mac_notification(f'{total_minutes // 60}:{total_minutes % 60}')
        
        
if __name__ == '__main__':
    main() 
