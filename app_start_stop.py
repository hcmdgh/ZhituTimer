from util import *


def main():
    start_time = get_start_time()

    if not start_time:
        save_start_time()
        show_prompt('开始做知兔')
    else:
        stop_time = datetime.now()
        duration = int((stop_time - start_time).total_seconds())
        minutes = duration // 60

        if minutes >= 5:
            show_prompt(f"结束做知兔 {minutes}:{duration % 60}")

            schema.Record.create(
                date=start_time,
                start_time=start_time,
                end_time=stop_time,
                duration_minutes=minutes,
            )
        else:
            show_prompt("结束做知兔 记录无效")

        # today_minutes = count_day_minutes(datetime.now())
        # log(f"today {today_minutes // 60}:{today_minutes % 60}")
        
        
if __name__ == '__main__':
    main() 
