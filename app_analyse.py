import schema
from util import *
from collections import defaultdict
import numpy as np


def main():
    if get_start_time(delete=False):
        print("Busy......")
    else:
        print("Free.")
    
    date2records = defaultdict(list)

    for record in schema.Record.select().order_by(schema.Record.start_time):
        date_ = get_date(record.start_time)
        date2records[date_].append(record.duration_minutes)
        
    items = list(date2records.items())
    items.sort(key=lambda x: x[0], reverse=True)

    for date_, records in items:
        records.sort()
        total_minutes = int(np.sum(records))
        # avg_minutes = int(np.mean(records[1:-1]) if len(records) >= 2 else np.mean(records))

        # print(f"[{date_}] 总时长：{total_minutes // 60}:{total_minutes % 60} 平均时长：{avg_minutes // 60}:{avg_minutes % 60}")
        print(f"[{date_}]\t{total_minutes // 60}:{total_minutes % 60}")


if __name__ == '__main__':
    main()
