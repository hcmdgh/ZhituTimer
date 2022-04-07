import yaml 
import argparse
from datetime import datetime, timedelta, date 
import os 
from collections import defaultdict
import texttable

RECORD_PATH = './record/punch_record.yaml'


def main():
    record_dict: dict[date, list[datetime]] = dict()
    
    if os.path.isfile(RECORD_PATH):
        with open(RECORD_PATH, 'r', encoding='utf-8') as fp:
            record_dict = yaml.safe_load(fp)
    
    if args.punch:
        now = datetime.now()
        today = (now - timedelta(hours=7)).date() 

        if today in record_dict:
            today_records = record_dict[today]
        else:
            today_records = []
            record_dict[today] = today_records
        
        if len(today_records) < 2:
            today_records.append(now)
        elif len(today_records) == 2:
            today_records[1] = now 
        else:
            raise AssertionError
        
        with open(RECORD_PATH, 'w', encoding='utf-8') as fp:
            yaml.safe_dump(record_dict, fp)

    table = texttable.Texttable()
    table.header(['日期', '上班打卡', '下班打卡', '时长'])
    
    for date_ in sorted(record_dict.keys(), reverse=True):
        date_record = record_dict[date_]
        record1 = record2 = 'N/A'
        duration = 'N/A'
        
        if len(date_record) >= 1:
            record1 = date_record[0].strftime('%H:%M')
            
        if len(date_record) >= 2:
            record2 = date_record[1].strftime('%H:%M')

            duration_minutes = int((date_record[1] - date_record[0]).total_seconds()) // 60 
            
            duration = f"{duration_minutes // 60}:{duration_minutes % 60:0>2}"
        
        table.add_row([date_.strftime('%Y-%m-%d'),
                       record1,
                       record2,
                       duration,])

    print(table.draw())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--punch",
                        action='store_true')
    
    args = parser.parse_args()
    
    main() 
