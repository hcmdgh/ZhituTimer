from util import *
from config import * 
from collections import defaultdict

LAST_DAYS = 999

TASK_NAMES = get_config('valid_task_names')


def main():
    if get_saved_pid(delete_after=False):
        print("Busy......")
    else:
        print("Free.")
        
    client = pymongo.MongoClient()
    db = client.zhitu_timer 
    collection = db.record 
    punch_collection = db.punch_record 
    
    date2records: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for record in collection.find():
        _date = record['date']
        minutes = record['duration_minutes']
        task_name = record['task_name']
        
        assert task_name in TASK_NAMES 
        
        date2records[_date][task_name] += minutes
        
    items = list(date2records.items())
    items.sort(key=lambda x: x[0], reverse=True)
    items = items[:LAST_DAYS]

    entries = [] 

    for _date, records in items:
        punch_record = punch_collection.find_one({'_id': _date})
        
        if punch_record:
            punch_start_time = punch_record['start_time']
            punch_end_time = punch_record['end_time']
            
            if punch_start_time and punch_end_time:
                punch_duration = calc_time_delta(punch_start_time, punch_end_time)
            else:
                punch_duration = None 
        else:
            punch_start_time = punch_end_time = punch_duration = None 
        
        entry = {
            'Date': _date,
            'Punch In': datetime2mstr(punch_start_time),
            'Punch Out': datetime2mstr(punch_end_time),
        }
        
        other_duration = 0 
        
        for task_name in TASK_NAMES:
            duration = records.get(task_name, 0)
            titled_task_name = task_name.title()
            entry[titled_task_name] = format_minutes(duration)
            other_duration += duration
            
        if punch_duration:
            entry.update({
                'Total': format_minutes(punch_duration),
                'Online': format_minutes(punch_duration - other_duration),
                'Offline': format_minutes(other_duration),
            })
        else:
            entry.update({
                'Total': '-',
                'Online': '-',
                'Offline': format_minutes(other_duration),
            })
        
        entries.append(entry)
        
    draw_table(entries)
    

if __name__ == '__main__':
    main()
