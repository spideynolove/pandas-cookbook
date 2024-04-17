# crawl_helpers
from ast import literal_eval
from boltons.iterutils import remap
from calendar import monthrange
from configparser import ConfigParser
from datetime import datetime, timezone, timedelta, date
from dateparser import parse
from dateutil import parser
from dateutil.relativedelta import relativedelta
from fake_useragent import VERSION, UserAgent
from json import dump, dumps, load, loads
from hashlib import md5
from pathlib import Path
from pydantic.v1.utils import deep_update
from pymongo import MongoClient, ASCENDING, DESCENDING
from unicodedata import normalize
from urllib.parse import urlencode, quote_plus
from itertools import product
from random import randint, choice
from re import sub, findall, search, compile, split, match
from redis import from_url
from requests import get, post, Session
from scrapy import Spider, Request, FormRequest
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from typing import Optional


NOW = datetime.now()
UNIXTIME = str(datetime.timestamp(NOW)*1000).split('.')[0]
CRAWL_DATE = NOW.strftime('%Y-%m-%d')
LOG_TIME = NOW.strftime('%d%m%Y')
CURRENT_PATH = Path(__file__).resolve().parent


def random_user_agent():
    ua_loc = f'{CURRENT_PATH}/fake_useragent{VERSION}.json'
    ua = UserAgent(use_external_data=True, cache_path=ua_loc)
    return ua.random


def rand_timeout(min: int = 7, max: int = 9) -> int:
    return 100*randint(min, max)


def get_time(days: str = None, isfuzzy: bool = False, have_hour: bool = False) -> str:
    hour = ' %H:%M' if have_hour else ''
    return parser.parse(days, fuzzy=isfuzzy).strftime(f'%Y-%m-%d{hour}') if days else ""


def get_unixtime(timestamp: str = None, divide: int = 1000, have_hour: bool = False) -> str:
    hour = ' %H:%M' if have_hour else ''
    return datetime.fromtimestamp(int(timestamp)/divide).strftime(f'%Y-%m-%d{hour}') if timestamp else ""


def get_tztime(delta: int = 0):
    tz_time = datetime.now(timezone.utc) + timedelta(delta)
    return tz_time.replace(tzinfo=None).isoformat(timespec="seconds") + 'Z'


def check_dirs(folder: str = None):
    if not Path(folder).exists():
        Path(folder).mkdir(parents=True, exist_ok=True)


def fill_quote(string: str = None, base: str = 'https://www.fxstreet.com/macroeconomics/central-banks/{}') -> str:
    return base.format(string) if string else ""


def get_num(string: str = None, filter_: str = r"([^0-9.])") -> str:
    return sub(filter_, "", str(string).strip()) if string else ""


def get_vp(string: Optional[str] = None) -> Optional[float]:
    string = str(string).strip()
    if '%' in string:
        return float(string.replace('%', ''))
    match_ = match(r'([0-9.]+)([KMB])', string)
    if match_:
        num, unit = match_.groups()
        multiplier = {'K': 1000, 'M': 1e6, 'B': 1e9}.get(unit, 1)
        return float(num) * multiplier
    try:
        return float(string)
    except ValueError:
        return 0


def checknull(string: str = None) -> str:
    return string if string else ""


def clean_str(string: str = None) -> str:
    return string.replace('“', '').replace('”', '').strip() if string else ""


def clean_lst(lst: list = None, unwanted: str = 'Also read:') -> list:
    lst = [clean_str(normalize('NFKD', ''.join(item)))
           for item in lst if unwanted not in ''.join(item)]
    return list(filter(None, lst))


def flatten_lst_dct(lst: list = None):
    return {k: v for d in lst for k, v in d.items()}


def sort_dict(dct: dict = None) -> dict:
    return {k: v for k, v in sorted(dct.items(), key=lambda item: item[1], reverse=True)}


def clear_dict(dct: dict = None) -> dict:
    return {k: v for k, v in dct.items() if v}


def lst_to_dict(items: list = None) -> dict:
    return {item[0]: item[1] for item in items}


def flatten(l):
    return [item for sublist in l for item in sublist]


def should_abort_request(request):
    IGNORES = ('google', 'sbcharts', 'forexpros',
               'ad-score', 'krxd', 'doubleclick')
    if any(item in request.url for item in IGNORES):
        return True
    # if request.resource_type in ("image", "media", "script", "xhr", "stylesheet"):
    #     return True
    # if request.method.lower() == 'post':
    #     return True
    return False


def get_chunks(lst: list = None, n: int = 2) -> list:
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def del_dictkeys(dict_: dict = None, keys: set = None):
    '''  https://stackoverflow.com/questions/3405715/elegant-way-to-remove-fields-from-nested-dictionaries '''
    def drop_keys(path, key, value): return key not in keys
    return remap(dict_, visit=drop_keys)


def cvtime_dict(dict_: dict = None, key: str = None, func: object = get_time, hour=False):
    return deep_update(dict_, {key: func(dict_[key], divide=1, have_hour=hour)})


def del_nul_ldict(data: list = None):
    return [{k: v for k, v in item.items() if v} for item in data]


def get_mongo(uri: str = None, db: str = None, collection: str = None):
    client = MongoClient(uri)
    return client[db][collection]


def get_lday(time_: datetime = None):
    return monthrange(time_.year, time_.month)[1]


def transform_time(time_str: str = None, format_: str = '%Y-%m-%d'):
    return datetime.strptime(time_str, '%d/%m/%Y').strftime(format_) if time_str else ""


def gen_productwo(tup_one, tup_two, start=1):
    return {i: item for i, item in enumerate(list(product(tup_one, tup_two)), start=start)}


def connect_sen(lst: list) -> str:
    return ' '.join(clean_lst(lst))


def add_urls_redis(redis_url: str = None, name: str = None, urls: object = None):
    ''' Example: add_urls_redis('redis://127.0.0.1:6379', 'quotes:start_urls', urls) '''
    redisClient = from_url(redis_url)
    for url in urls:
        redisClient.lpush(name, url)


def insert_unique_document(collection, new_record, unique_fields):
    query = {field: new_record[field] for field in unique_fields}
    existing_document = collection.find_one(query)
    if existing_document:
        print("Document already exists:", existing_document)
    else:
        collection.insert_one(new_record)
        print("Inserted new document:", new_record)


def preprocess_values(data_list):
    processed_list = []
    for _, item in enumerate(data_list):
        if isinstance(item, list):
            processed_item = [get_num(sub_item) if isinstance(sub_item, str) and any(
                char.isdigit() for char in sub_item) else sub_item for sub_item in item]
        elif isinstance(item, str) and any(char.isdigit() for char in item):
            processed_item = get_num(item)
        else:
            processed_item = item
        processed_list.append(processed_item)
    return processed_list


def extract_code(text: str) -> tuple:
    pattern = r'(.+)\(([^)]+)\)'
    match = search(pattern, text)
    if match:
        company_name = match.group(1).strip()
        ticker = match.group(2)
        return company_name, ticker
    else:
        return "", ""


def extract_id_from_url(url, pattern=r"\b(\d+)\b"):
    match_ = search(pattern, url)
    return match_.group(1) if match_ else None
