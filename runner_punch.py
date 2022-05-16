from util import * 
import yaml 
import argparse
from datetime import datetime, timedelta, date 
import os 
from collections import defaultdict


def main():
    client = pymongo.MongoClient()
    db = client.zhitu_timer 
    punch_collection = db.punch_record 

    _date: str = date2str(get_real_date())
    now = datetime.now() 

    punch_record = punch_collection.find_one({'_id': _date})
    
    if not punch_record:  # 第一次打卡
        punch_record = {
            '_id': _date,
            'date': _date,
            'start_time': datetime2str(now),
            'end_time': None,
        }
        
        punch_collection.insert_one(punch_record)
    else:  # 第二次打卡
        punch_record['end_time'] = datetime2str(now)

        punch_collection.replace_one(
            { '_id': punch_record['_id'] },
            punch_record,
            upsert=True,
        )
    
    all_records: list[dict[str, Any]] = list(punch_collection.find())

    all_records.sort(key=lambda x: x['_id'], reverse=True)
    
    entries = [] 
    
    for record in all_records:
        start_time = record['start_time']
        end_time = record['end_time']
        
        entry = {
            'Date': record['_id'],
            'Punch In': datetime2mstr(start_time),
            'Punch Out': datetime2mstr(end_time),
            'Duration': format_minutes(calc_time_delta(start_time, end_time)) if start_time and end_time else '-',
        }
        
        entries.append(entry)
    
    draw_table(entries)
    

if __name__ == '__main__':
    main() 
