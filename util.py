import schema
import config 
from datetime import datetime, timedelta, date
from typing import Union, Optional, Any 
from tkinter import Tk, Label
import pymongo
import yaml 
import os 
from tkinter.simpledialog import askstring 
from tkinter import Tk 
import texttable
import prettytable


def show_prompt(msg: str, duration: int = 3):
    raise NotImplementedError
    def destroy():
        window.destroy()

    window = Tk()
    window.overrideredirect(True)
    # window.attributes('-alpha', 1)
    window.attributes('-topmost', True)
    # window.attributes('-transparent', True)

    label = Label(window,
                  text=msg,
                  font=('楷体', 25),
                  fg='red',
                  bg='black')
    label.pack(fill='x', anchor='center')

    window.geometry('+0+0')
    window.after(duration * 1000, destroy)

    window.mainloop()


def get_real_date(_datetime: Optional[datetime] = None) -> date:
    if not _datetime:
        _datetime = datetime.now()
    
    return (_datetime - timedelta(hours=7)).date()


def get_datetime_range(date_: Optional[date] = None) -> tuple[datetime, datetime]:
    raise DeprecationWarning
    if not date_:
        now = datetime.now()
        date_ = get_real_date(now)

    date_ = datetime.combine(date_, datetime.min.time())

    lower_bound = date_ + timedelta(hours=7)
    upper_bound = lower_bound + timedelta(days=1)

    return lower_bound, upper_bound


def count_day_minutes(date_: Union[None, datetime, date]) -> int:
    raise NotImplementedError
    if date_ is None:
        date_ = datetime.now()

    if type(date_) == datetime:
        lower_bound, upper_bound = get_datetime_range(get_real_date(date_))
    elif type(date_) == date:
        lower_bound, upper_bound = get_datetime_range(date_)
    else:
        raise AssertionError

    minutes = 0

    for record in schema.Record.select().where((schema.Record.date >= lower_bound) & (schema.Record.date < upper_bound)):
        minutes += record.duration_minutes

    return minutes


def get_start_time(delete: bool = True) -> Optional[datetime]:
    raise NotImplementedError
    try:
        with open('./state.yaml', 'r', encoding='utf-8') as fp:
            obj = yaml.safe_load(fp)

        if delete:
            with open('./state.yaml', 'w'):
                pass 
            
        return obj.get('start_time')
    except Exception:
        return None 


def save_start_time(start_time: Optional[datetime] = None):
    raise NotImplementedError
    if not start_time:
        start_time = datetime.now() 
        
    obj = { 'start_time': start_time }
        
    with open('./state.yaml', 'w', encoding='utf-8') as fp:
        obj = yaml.safe_dump(obj, fp)


def send_mac_notification(msg: str, title: str = 'Zhitu'):
    os.system(f''' osascript -e 'display notification "{msg}" with title "{title}"' ''')

    
def save_pid():
    pid = os.getpid()
        
    config.set_config('pid', pid)


def get_saved_pid(delete_after: bool) -> Optional[int]:
    pid = config.get_config('pid')
    
    if delete_after:
        config.set_config('pid', None)
        
    return pid  


def inputbox(title: str, prompt: str, init_content: Optional[str]) -> Optional[str]:
    app = Tk()
    app.withdraw()

    content = askstring(title=title, prompt=prompt, initialvalue=init_content)

    app.destroy()
    
    return content 


def draw_table(entries: list[dict[str, Any]]):
    assert entries 
    
    column_names = list(entries[0].keys())
    
    # table = texttable.Texttable()
    # table.header(column_names)
    
    table = prettytable.PrettyTable(column_names)
    
    for entry in entries:
        row = []
        
        for column_name in column_names:
            row.append(entry.get(column_name))
        
        table.add_row(row)
        
    print(table)
    
    
def format_minutes(minutes: int) -> str:
    if minutes < 5:
        return '-'
    
    h = minutes // 60 
    m = minutes % 60 
    
    return f"{h}:{m:0>2d}"


def calc_time_delta(start_time: Union[datetime, str],
                    end_time: Union[datetime, str]) -> int:
    """
    计算两个时间的时间差，以分钟数返回。
    """
    
    if isinstance(start_time, str):
        start_time = str2datetime(start_time)

    if isinstance(end_time, str):
        end_time = str2datetime(end_time)
    
    return int((end_time - start_time).total_seconds()) // 60


def date2str(_date: date) -> str:
    return _date.strftime('%Y-%m-%d')


def str2datetime(s: str) -> datetime:
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def str2datetime_(s: str) -> datetime:
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')

    
def datetime2str(_datetime: datetime) -> str:
    return _datetime.strftime('%Y-%m-%d %H:%M:%S')


def datetime2mstr(_datetime: Union[datetime, str, None]) -> str:
    if not _datetime:
        return '-'
    
    if isinstance(_datetime, str):
        _datetime = str2datetime(_datetime)
        
    return _datetime.strftime('%H:%M')
        

if __name__ == '__main__':
    draw_table([
        {'name': '耿皓', 'sex': True, 'birth': datetime.now().date()},
        {'name': '啊哈哈', 'sex': False, 'birth': datetime.now()},
    ])
