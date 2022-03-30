import yaml 
from typing import Optional, Any 

CONFIG_FILE = './config.yaml'

try:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as _fp:
        _config_dict = yaml.safe_load(_fp)
except Exception:
    _config_dict = dict() 
    
    
def get_config(key: str) -> Optional[Any]:
    if not _config_dict:
        return None 
    
    return _config_dict.get(key)


def set_config(key: str, value: Any):
    _config_dict[key] = value 
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as _fp:
        yaml.safe_dump(_config_dict, _fp, allow_unicode=True)


def clear_config():
    with open(CONFIG_FILE, 'w', encoding='utf-8') as _fp:
        pass 
