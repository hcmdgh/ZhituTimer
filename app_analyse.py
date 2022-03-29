import schema
from util import *
from collections import defaultdict
import numpy as np
import texttable

LAST_DAYS = 3


def main():
    if get_saved_pid() > -1:
        print("Busy......")
    else:
        print("Free.")
    
    date2records = defaultdict(lambda: defaultdict(int))

    for record in schema.Record.select():
        date_ = get_date(record.start_time)
        
        minutes = record.duration_minutes
        desc = record.desc 
        
        date2records[date_][desc] += minutes
        
    items = list(date2records.items())
    items.sort(key=lambda x: x[0], reverse=True)
    items = items[:LAST_DAYS]

    for date_, records in items:
        print(f"日期：{date_}")
        
        total_minutes = sum(records.values())
        records['总计'] = total_minutes
        
        table_data = [
            (desc, f"{minutes // 60}:{minutes % 60}")
            for desc, minutes in records.items()
        ]
        
        table = texttable.Texttable()
        table.header(('事项', '时长'))
        table.add_rows(table_data, header=False) 

        print(table.draw())
        
        print()

if __name__ == '__main__':
    main()
