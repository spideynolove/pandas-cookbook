from pathlib import Path
from sys import path

SITE = Path(__file__).resolve().parent.parent
PROJECT = SITE.parent
path.append(str(PROJECT.absolute()))
from libs.c_helpers import *

SQLITE3_PATH = "/home/hung/sqlite3/database"
fxsb_mapping = {
    "EURAUD": "EUR/AUD", "EURCAD": "EUR/CAD", "EURCHF": "EUR/CHF", "EURGBP": "EUR/GBP", "EURJPY": "EUR/JPY", "EURNZD": "EUR/NZD", "EURUSD": "EUR/USD",
    "GBPAUD": "GBP/AUD", "GBPCAD": "GBP/CAD", "GBPCHF": "GBP/CHF", "GBPJPY": "GBP/JPY", "GBPNZD": "GBP/NZD", "GBPUSD": "GBP/USD",
    "AUDCAD": "AUD/CAD", "AUDCHF": "AUD/CHF", "AUDJPY": "AUD/JPY", "AUDNZD": "AUD/NZD", "AUDUSD": "AUD/USD",
    "NZDCAD": "NZD/CAD", "NZDCHF": "NZD/CHF", "NZDJPY": "NZD/JPY", "NZDUSD": "NZD/USD",
    "USDCAD": "USD/CAD", "USDCHF": "USD/CHF", "USDJPY": "USD/JPY",
    "CADCHF": "CAD/CHF", "CADJPY": "CAD/JPY", "CHFJPY": "CHF/JPY",
    "XAGUSD": "XAG/USD", "XAUUSD": "XAU/USD", "BRENTCMDUSD": "Brent_Oil",
    # "USA30IDXUSD": "US30", "USA500IDXUSD": "SPX500", "USACOMIDXUSD": "NAS100",
    # "DAX": "GER30", "GBRIDXGBP": "UK100",
}
tf_mapping = {"1": "M1", "5": "M5", "15": "M15", "30": "M30", "60": "H1", "240": "H4", "1440": "D1"}


def calculate_id(ticker_, timeframe_, time_):
    to_hash = f"{ticker_}_{timeframe_}_{time_}"
    hashed = md5(to_hash.encode()).hexdigest()
    return hashed[:24]


# from ast import literal_eval
# from boltons.iterutils import remap
# from calendar import monthrange
# from configparser import ConfigParser
# from datetime import datetime, timezone, timedelta, date
# from dateparser import parse
# from dateutil import parser
# from dateutil.relativedelta import relativedelta
# from fake_useragent import VERSION, UserAgent
# from json import dump, dumps, load, loads
# from pathlib import Path
# from pydantic.v1.utils import deep_update
# from pymongo import MongoClient
# from unicodedata import normalize
# from urllib.parse import urlencode, quote_plus
# from itertools import product
# from random import randint
# from re import sub, findall, search, compile, split
# # from redis import from_url
# from requests import get, post, Session
# from scrapy import Spider, Request, FormRequest
# from scrapy.exceptions import CloseSpider
# from scrapy.http import JsonRequest
# from scrapy.selector import Selector
# from sys import path


# CURRENT_PATH = Path(__file__).resolve().parent
# SITE = CURRENT_PATH.parent
# # PROJECT = SITE.parent
# NOW = datetime.now()
# UNIXTIME = str(datetime.timestamp(NOW)*1000).split('.')[0]
# CRAWL_DATE = NOW.strftime('%Y-%m-%d')
# LOG_TIME = NOW.strftime('%d%m%Y')
# IGNORES = ['google',]


# # =========================================== COMMONS ============================================
# def load_info(user="OBJECTROCKET") -> dict:
#     config = ConfigParser()
#     config.read(f"{CURRENT_PATH}/_login-tasks/accounts/mongo.ini")
#     try:
#         return config[user]
#     except:
#         print("User not found!")
#         exit(0)


# def connect_db(is_local: bool = False):
#     if is_local:
#         return MongoClient('mongodb://127.0.0.1:27017')
#     else:
#         config_data = load_info()
#         settings = {
#             'host': 'lon5-c15-1.mongo.objectrocket.com:43848,lon5-c15-2.mongo.objectrocket.com:43848,lon5-c15-0.mongo.objectrocket.com:43848',
#             'username': quote_plus(config_data['username']),
#             'password': quote_plus(config_data['password']),
#             'options': f"?authSource={config_data['db']}&replicaSet=e58c7b5541b04b3bb6c0dbfa399c5f80".format(**locals())
#         }
#         try:
#             mongodb_uri = "mongodb://{username}:{password}@{host}/{options}"
#             return MongoClient(mongodb_uri.format(**settings))
#         except Exception as ex:
#             print("Error: {}".format(ex))
#             exit('Failed to connect, terminating.')


# def handle_item(collection, item, filters):
#     documents = collection.find_one(filters)
#     if documents:
#         new_data = None
#         if isinstance(documents.get('data_'), list):
#             # add new data to old data
#             new_data = item.get('data_') + documents.get('data_')
#             new_data = [dict(t) for t in {tuple(d.items()) for d in new_data}]

#             # modify dict item of a list: t.b.d
#         else:
#             new_data = {**documents.get('data_'), **item.get('data_')}
#         collection.update_one({'_id': documents.get('_id')}, {'$set': {'data_': new_data}})
#     else:
#         collection.insert_one(dict(item))


# def random_user_agent():
#     # VERSION==1.1.3
#     ua_loc = f'{CURRENT_PATH}/fake_useragent{VERSION}.json'
#     ua = UserAgent(use_external_data=True, cache_path=ua_loc)
#     # ua = UserAgent(min_percentage=1.3)
#     return ua.random


# def rand_timeout(min: int = 8, max: int = 13) -> int:
#     return 100*randint(min, max)


# def get_time(days: str = None, isfuzzy: bool = False, divide: int = 1, have_hour: bool = False) -> str:
#     hour = ' %H:%M' if have_hour else ''
#     return parser.parse(days, fuzzy=isfuzzy).strftime(f'%Y-%m-%d{hour}') if days else ""


# def get_unixtime(timestamp: str = None, divide: int = 1000, have_hour: bool = False) -> str:
#     hour = ' %H:%M' if have_hour else ''
#     return datetime.fromtimestamp(int(timestamp)/divide).strftime(f'%Y-%m-%d{hour}') if timestamp else ""


# def get_unixdt(dt: datetime = None, multiple: int = 1000):
#     return str(datetime.timestamp(dt)*multiple).split('.')[0]

# def get_tztime(delta: int = 0):
#     tz_time = datetime.now(timezone.utc) + timedelta(delta)
#     return tz_time.replace(tzinfo=None).isoformat(timespec="seconds") + 'Z'


# def check_dirs(folder: str = None):
#     if not Path(folder).exists():
#         Path(folder).mkdir(parents=True, exist_ok=True)


# def fill_quote(string: str = None, base: str = 'https://shit/{}') -> str:
#     return base.format(string) if string else ""


# def get_num(string: str = None,
#             filter_: str = r"([^0-9.-])") -> str:
#     return sub(filter_, "", str(string).strip()) if string else ""


# def checknull(string: str = None) -> str:
#     return string if string else ""


# def clean_str(string: str = None) -> str:
#     return string.replace('“', '').replace('”', '').strip() if string else ""


# def clean_lst(lst: list = None) -> list:
#     lst = [clean_str(normalize('NFKD', ''.join(item)))
#            for item in lst if 'Also read:' not in ''.join(item)]
#     return list(filter(None, lst))


# def flatten_lst_dct(lst: list = None):
#     return {k: v for d in lst for k, v in d.items()}


# def sort_dict(dct: dict = None) -> dict:
#     return {k: v for k, v in sorted(dct.items(), key=lambda item: item[1], reverse=True)}


# def clear_dict(dct: dict = None) -> dict:
#     return {k: v for k, v in dct.items() if v}


# def lst_to_dict(items: list = None) -> dict:
#     # convert list of list to dict
#     return {item[0]: item[1] for item in items}


# def flatten(l):
#     return [item for sublist in l for item in sublist]


# def should_abort_request(request):
#     IGNORES = (
#         'google', 
#         # 'education',
#         'sbcharts', 
#         'forexpros', 
#         'ad-score', 
#         'krxd',
#         'doubleclick',
#     )
#     if any(item in request.url for item in IGNORES):
#         return True
#     if request.resource_type in ("image", "media", "other"):
#         return True
#     # if request.resource_type == "script":
#     #     return True
#     # if request.resource_type == "xhr":    # need
#     #     return True
#     # if request.resource_type == "stylesheet": # slow
#     #     return True
#     # if request.method.lower() == 'post':
#     #     # logging.log(logging.INFO, f"Ignoring {request.method} {request.url} ")
#     #     return True
#     return False


# def get_chunks(lst: list = None, n: int = 2) -> list:
#     return [lst[i:i + n] for i in range(0, len(lst), n)]


# def del_dictkeys(dict_: dict = None, keys: set = None):
#     '''  https://stackoverflow.com/questions/3405715/elegant-way-to-remove-fields-from-nested-dictionaries '''
#     def drop_keys(path, key, value): return key not in keys
#     return remap(dict_, visit=drop_keys)


# def cvtime_dict(dict_: dict = None, key: str = None, func: object = get_time, hour=False):
#     return deep_update(dict_, {key: func(dict_[key], divide=1, have_hour=hour)})


# def del_nul_ldict(data: list = None):
#     return [{k: v for k, v in item.items() if v} for item in data]


# def get_cursor(uri: str = None, db: str = None, collection: str = None):
#     client = MongoClient(uri)
#     return client[db][collection]


# def get_lday(time_: datetime = None):
#     return monthrange(time_.year, time_.month)[1]


# def transform_time(time_str: str = None, format_: str = '%Y-%m-%d'):
#     return datetime.strptime(time_str, '%d/%m/%Y').strftime(format_) if time_str else ""


# def gen_productwo(tup_one, tup_two, start=1):
#     return {i: item for i, item in enumerate(list(product(tup_one, tup_two)), start=start)}


# def connect_sen(lst: list) -> str:
#     return ' '.join(clean_lst(lst))
# # ========================================== END COMMONS =========================================


# # =========================================== BABYPIPS ===========================================
# # headers = {'User-Agent': random_user_agent(), 'Accept-Language': 'en-US,en;q=0.5','Referer': 'https://www.babypips.com/'}
# check_dirs(f"{SITE}/log/")
# new_types = ('news', 'trading/technical-analysis', 'trading/trade-ideas')



# # '5m': 'FIVE_MINUTE',
# SVP_PERIODS = {'15m': 'FIFTEEN_MINUTE', '30m': 'THIRTY_MINUTE', '1h': 'ONE_HOUR', '4h': 'FOUR_HOUR', '1d': 'ONE_DAY', '1w': 'ONE_WEEK', '1m': 'ONE_MONTH'}

# # 'FIVE_MINUTE': '5m', 'THIRTY_MINUTE': '30m',
# PRICES_PERIODS = {'ONE_MINUTE': '1m','FIFTEEN_MINUTE': '15m', 'ONE_HOUR': '1h', 'FOUR_HOUR': '4h', 'ONE_DAY': '1d', 'ONE_WEEK': '1w'}


# def query_data(qstring: str = 'StrengthHistory'):
#     if qstring == 'StrengthHistory':
#         return 'query StrengthHistory($period: Period!, $windowStr: ID!) {\n  fxcmAUD: symbol(id: "fxcm:AUD") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "ohlc", params: [], period: $period}\n      key: "close"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmCAD: symbol(id: "fxcm:CAD") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "ohlc", params: [], period: $period}\n      key: "close"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmCHF: symbol(id: "fxcm:CHF") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "ohlc", params: [], period: $period}\n      key: "close"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmEUR: symbol(id: "fxcm:EUR") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "ohlc", params: [], period: $period}\n      key: "close"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmGBP: symbol(id: "fxcm:GBP") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "ohlc", params: [], period: $period}\n      key: "close"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmJPY: symbol(id: "fxcm:JPY") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "ohlc", params: [], period: $period}\n      key: "close"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmNZD: symbol(id: "fxcm:NZD") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "ohlc", params: [], period: $period}\n      key: "close"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmUSD: symbol(id: "fxcm:USD") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "ohlc", params: [], period: $period}\n      key: "close"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n}'
#     elif qstring == 'VolatilityHistory':
#         return 'query VolatilityHistory($period: Period!, $lookbackStr: ID!, $windowStr: ID!) {\n  fxcmAUD: symbol(id: "fxcm:AUD") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "volatility", params: [$lookbackStr], period: $period}\n      key: "pct"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmCAD: symbol(id: "fxcm:CAD") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "volatility", params: [$lookbackStr], period: $period}\n      key: "pct"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmCHF: symbol(id: "fxcm:CHF") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "volatility", params: [$lookbackStr], period: $period}\n      key: "pct"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmEUR: symbol(id: "fxcm:EUR") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "volatility", params: [$lookbackStr], period: $period}\n      key: "pct"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmGBP: symbol(id: "fxcm:GBP") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "volatility", params: [$lookbackStr], period: $period}\n      key: "pct"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmJPY: symbol(id: "fxcm:JPY") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "volatility", params: [$lookbackStr], period: $period}\n      key: "pct"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmNZD: symbol(id: "fxcm:NZD") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "volatility", params: [$lookbackStr], period: $period}\n      key: "pct"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n  fxcmUSD: symbol(id: "fxcm:USD") {\n    id\n    precision\n    minPrecision\n    aggregate\n    values: sparkLine(\n      indicator: {name: "volatility", params: [$lookbackStr], period: $period}\n      key: "pct"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n}'
#     else:
#         return 'query PriceHistory($symbolId: ID!, $windowStr: ID!) {\n  symbol(id: $symbolId) {\n    id\n    precision\n    minPrecision\n    aggregate\n    nextUpdateAt: nextSparkLineUpdateAt(window: $windowStr)\n    prices: sparkLine(\n      indicator: {name: "ohlc", params: []}\n      key: "close"\n      window: $windowStr\n    ) {\n      period\n      minTime\n      maxTime\n      minValue\n      maxValue\n      values\n      __typename\n    }\n    __typename\n  }\n}'


# def get_calendar(dtime: datetime = None) -> str:
#     # return f"{dtime.isocalendar().year}-W{dtime.isocalendar().week}"  # 3.11 
#     year, week, _ = dtime.isocalendar()                                 # 3.8
#     return f"{year}-W{week}" if week > 9 else f"{year}-W0{week}"
# # ========================================= END BABYPIPS =========================================


# # =========================================== BARCHART ===========================================
# # T.B.D
# symbol_lists = {
#     # fx
#     '1': ('major-rates', 'forex.markets.all'),
#     '2': ('us-dollar', 'forex.markets.usd'),
#     '3': ('euro-fx', 'forex.markets.eur'),
#     '4': ('british-pound', 'forex.markets.gbp'),
#     '5': ('canadian-dollar', 'forex.markets.cad'),
#     '6': ('japanese-yen', 'forex.markets.jpy'),
#     '7': ('swiss-franc', 'forex.markets.chf'),
#     '8': ('australian-dollar', 'forex.markets.aud'),
#     '9': ('metals-rates', 'forex.markets.metals'),
#     '10': ('newzealand-dollar', 'forex.rates.NZD'),
#     '11': ('china-chn', 'forex.rates.CNH'), 
#     '12': ('china-cny', 'forex.rates.CNY'),
#     '13': ('gold-xau', 'forex.rates.XAU'),
#     '14': ('silver-xag', 'forex.rates.XAG'),
#     # coins
#     '15': ('major-coins', 'cryptos.all'),
#     '16': ('btc-coins', 'cryptos.rates(BTC)'),
#     '17': ('eth-coins', 'cryptos.rates(ETH)'),

#     # futures
#     # '18': ('futures-currencies', 'futures.category.us.currencies'), # fields and meta are different from fx and coins
#     # '19': ('futures-energies', 'futures.category.us.energies'),
#     # '20': ('futures-financials', 'futures.category.us.financials'),
#     # '21': ('futures-grains', 'futures.category.us.grains'),
#     # '22': ('futures-indicies', 'futures.category.us.indices'),
#     # '23': ('futures-meats', 'futures.category.us.meats'),
#     # '24': ('futures-metals', 'futures.category.us.metals'),
#     # '25': ('futures-softs', 'futures.category.us.softs'),
#     '18': ('us-major-commodities', 'futures.category.us.all'),
#     '19': ('eu-major-commodities', 'futures.category.euro.all'),

#     # etfs
#     '20': ('etfs-percent-change', 'etfs.us.percent.advances.unleveraged'),
#     '21': ('etfs-price-change', 'etfs.us.price.advances.overall'),
#     '22': ('etfs-range', 'etfs.us.range.advances.overall'),
#     '23': ('etfs-gainers', 'etfs.us.five_day.advances.unleveraged'),

#     # coins
#     # coins
# }


# def bypass_proxies(filepath=f'{SITE}/barchart_bypass.json'):
#     headers = {'User-Agent': random_user_agent(),}
#     data = {}
#     if Path(filepath).exists():
#         with open(filepath) as f:
#             data = load(f)
#     else:
#         session = Session()
#         response = session.get('https://www.barchart.com/forex', headers=headers)
#         if response.status_code != 200:
#             raise Exception("Failed to get https://www.barchart.com/forex")
#         else:
#             cookies = session.cookies.get_dict()
#             headers.setdefault('X-XSRF-TOKEN', f"{session.cookies.get('XSRF-TOKEN')[:-3]}=")
#             data = {'cookies': cookies, 'headers': headers}
#             with open(filepath, 'w', encoding='utf-8') as f:
#                 dump(data, f)
#     return data


# def gen_unixtime(dt: datetime = None) -> str:
#     return str(datetime.timestamp(dt)).split('.')[0]
# # ========================================= END BARCHART==========================================


# # ====================================== TRADINGECONOMICS ========================================

# countries_ = ('usa', 'gbr', 'emu', 'chn', 'deu', 'jpn', 'aus', 'nzl', 'can', 'che')
# importances = ('2', '3')

# # 'Spain', 'France', 'Italy', 'India', 'Hong Kong', 'Taiwan', 'South Korea', 'Saudi Arabia', 'Mexico', 'Russia', 'IMF', 'G7', 'G20', 'OPEC', 
# news_topics = ('Commodity', 'Canada', 'New Zealand', 'China', 'Australia', 'Euro Area', 'Japan', 'United States', 'United Kingdom', 'Germany', 'Switzerland', 'Currency')
# countries = {'jp': 'japan', 'au': 'australia', 'us': 'united states', 'eu': 'euro area', 'ge': 'germany', 'uk': 'united kingdom', 'cn': 'china', 'nz': 'new zealand', 'ca': 'canada', 'sw': 'switzerland'}

# # 'MN': 'span=max', # d1=2013-01-01
# intervals = {'D1': 'd1=2023-10-03&d2=2023-10-14&interval=1d', 'W1': 'd1=2023-10-03&d2=2023-10-14&interval=1w', 'MN': 'd1=2023-10-03&d2=2023-10-14&interval=1month'}

# currencies = (
#     'euraud:cur', 'eurnzd:cur', 'eurcad:cur', 'eurusd:cur', 'eurchf:cur', 'eurjpy:cur', 'eurgbp:cur',
#     'gbpaud:cur', 'gbpnzd:cur', 'gbpcad:cur', 'gbpusd:cur', 'gbpchf:cur', 'gbpjpy:cur',
#     'usdjpy:cur', 'usdchf:cur', 'usdcad:cur', 'dxy:cur', 'xauusd:cur', 'xagusd:cur',
#     'audusd:cur', 'audnzd:cur', 'audcad:cur', 'audchf:cur', 'audjpy:cur',
#     'nzdusd:cur', 'nzdcad:cur', 'nzdchf:cur', 'nzdjpy:cur',
#     'cadchf:cur', 'cadjpy:cur', 'chfjpy:cur',
# )

# bonds = ('USGG10YR:IND', 'GUKG10:IND', 'GJGB10:IND', 'GACGB10:IND', 'GCAN10YR:IND', 'GSWISS10:IND', 'GNZGB10:IND', 'GDBR10:IND', 'GCNY10YR:GOV')

# commodities = (
#     "CL1:COM", "CO1:COM", "NG1:COM", "XB1:COM", 
#     "HO1:COM", "XAL1:COM", "NGEU:COM", "NGUK:COM", 
#     "XAUUSD:CUR", "XAGUSD:CUR", "HG1:COM", "JBP:COM", "SCO:COM", 
#     "S 1:COM", "W 1:COM", "LB1:COM", "PLO:COM", "CHE:COM", 
#     "DA:COM", "JN1:COM", "JO1:COM", "KC1:COM", "CT1:COM",
#     "CC1:COM", "RR1:COM", "RS1:COM", "O 1:COM", "OL1:COM", 
#     "SB1:COM", "TEA:COM", "SUNF:COM", "RSO:COM", "FABT:COM", 
#     "FAPP:COM", "C 1:COM",
#     "FC1:COM", "LC1:COM", "LH1:COM", 
#     "CRYTR:IND", "LME:IND", "SPGSCITR:IND", "SSECC:COM", 

#     # "DL1:COM", "MOB:COM", "UXA:COM", "PNL:COM", "CMA:COM", "URDB:COM",
#     # "LC:COM", "XPTUSD:CUR", "TTSG:COM", "HRC:COM",
#     # "BIT:COM", "LCO1:COM", "LL1:COM", "LMAHDS03:COM", "LMSNDS03:COM", 
#     # "LMZSDS03:COM", "LN1:COM", "MOLYBDEN:COM", "XPDUSD:CUR", "XRH:COM",
#     # "POL:COM", "PVC:COM", "PYL:COM", "SODASH:COM", "SREMNDM:COM", 
#     # "TEC:COM", "TIOC:COM", "UANEU:COM", "UFB:COM", "UFI:COM", 
#     # "MACN:COM", "GAC:COM", "GECNYBGQ:COM", "IMR:COM", "IUC:COM", "KSP:COM",
#     # "BEEF:COM", "POUL:COM", "WEGGS:COM", "DCE:COM", "NOSMFZ:COM",
#     # "SPSCFI:COM", "MVNLRTR:IND", "SOLARNTR:IND", "EECXM:IND", "GWETR:IND",
#     # "GBRELEPRI:COM", "DEUELEPRI:COM", "FRAELEPRI:COM", "ITAELEPRI:COM", "ESPELEPRI:COM",
# )

# indices = (
#     "SPX:IND", "INDU:IND", "NDX:IND",
#     "UKX:IND", "DAX:IND", "SMI:IND", 
#     "SPE350:IND", "SX5E:IND", "N100:IND", "SX7E:IND", "STOXX:IND",
#     "NKY:IND", "SHCOMP:IND", "SHSZ300:IND", "SSE50:IND", "HSI:IND",
#     "VXJ:IND", "AS30:IND", "AS51:IND", "AS52:IND", "NZSE50FG:IND",

#     # "CAC:IND", "FTSEMIB:IND", "IBEX:IND", "INDEXCF:IND",
#     # "AEX:IND", "XU100:IND", 

#     # "OMX:IND", "WIG:IND", "BEL20:IND", "OSEAX:IND", "ATX:IND",
#     # "KFX:IND", "HEX:IND", "HEX25:IND", "ISEQ:IND", "ASE:IND",
#     # "BVLX:IND", "PSI20:IND", "PX:IND", "BET:IND", "BUX:IND",
#     # "PFTS:IND", "SKSM:IND", "LUXXX:IND", "CRO:IND", "SOFIX:IND",  
#     # "SBITOP:IND", "VILSE:IND", "BELEX15:IND", "SASX10:IND", "TALSE:IND", 
#     # "CYSMMAPA:IND", "MBI:IND", "MALTEX:IND", "ICEXI:IND", "RIGSE:IND", "MONEX:IND", 

#     # "BVQA:IND", "SPTSX:IND", "IBOV:IND", "MEXBOL:IND", "SPBLPGPT:IND",
#     # "MERVAL:IND", "IBVC:IND", "COLCAP:IND", "IGPA:IND", "BVPSBVPS:IND",
#     # "BSX:IND", "JMSMX:IND", "XIN9:IND", "SENSEX:IND", "DSEX:IND",
#     # "JCI:IND", "SASEIDX:IND", "TWSE:IND", "ADSMI:IND", "SET50:IND",
#     # "FBMKLCI:IND", "FSSTI:IND", "TA-125:IND", "PCOMP:IND", "KSE100:IND",
#     # "KZKAK:IND", "DSM:IND", "VHINDEX:IND", "VNINDEX:IND", "MSM30:IND",
#     # "CSEALL:IND", "BLOM:IND", "JOSMGNFF:IND", "LSXC:IND", "MSETOP:IND",
#     # "DFMGI:IND", "BKA:IND", "NIFTY:IND", "BHSEEI:IND", "NGSEINDX:IND",
#     # "TOP40:IND", "JALSH:IND", "CASE:IND", "MOSENEW:IND", "KNSMIDX:IND",
#     # "NSEASI:IND", "DARSDSEI:IND", "TUSISE:IND", "GGSECI:IND", "SEMDEX:IND",
#     # "ALSIUG:IND", "FTN098:IND", "BGSMDC:IND", "INDZI:IND",
# )


# def handle_lst(lst: list) -> str:
#     return ' '.join(clean_lst(lst))
# # =================================== END TRADINGECONOMICS =======================================


# # =========================================== DAILYFX ============================================
# MAJORS = ('USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD', 'CNY')
# nationToCheck = ('Japan', 'United States', 'United Kingdom', 'European Union', 'European Area', 'Australia', 'New Zealand', 'Canada', 'Switzerland', 'China', 'Germany')


# def transform_dict(input_dict, keyword):
#     """
#     # Example usage:
#     output_dict = {'Change in longs': ['-3.97% ', 'Daily', '-11.84% ', 'Weekly']}
#     transformed_dict = transform_dict(output_dict)
#     print(transformed_dict)
#     """
#     transformed_dict = {}
#     for key, value in input_dict.items():
#         if keyword in key:
#             # Transformation logic for values associated with keys containing the specified keyword
#             transformed_values = {}
#             for i in range(0, len(value), 2):
#                 new_key = f"{key.replace(' ', '-').capitalize()}-{value[i+1].strip().lower()}"
#                 transformed_values[new_key] = float(value[i].strip('% '))
#             transformed_dict.update(transformed_values)
#         else:
#             transformed_dict[key] = value
#     return transformed_dict


# # ============================================ END DAILYFX =======================================


# # ======================================== FOREXFACTORY ==========================================
# calendar_params = {
#     'impacts': (3, 2),
#     'event_types': (1, 2, 3, 4, 5, 7, 8, 9, 10, 11),
#     'currencies': ('6', '9'),
# }

# NEWS = {
#     'lastest': '-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="securitytoken"\r\n\r\nguest\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="do"\r\n\r\nsaveoptions\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="setdefault"\r\n\r\nno\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="ignoreinput"\r\n\r\nno\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][idSuffix]"\r\n\r\n{}\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][_flexForm_]"\r\n\r\nflexForm\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][modelData]"\r\n\r\neyJwYV9sYXlvdXRfaWQiOiJuZXdzIiwicGFfY29tcG9uZW50X2lkIjoiTmV3c0xlZnRPbmUiLCJwYV9jb250cm9scyI6Im5ld3N8TmV3c0xlZnRPbmUiLCJwYV9pbmplY3RyZXZlcnNlIjpmYWxzZSwicGFfaGFyZGluamVjdGlvbiI6ZmFsc2UsInBhX2luamVjdGF0IjpmYWxzZX0=\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][stream][]"\r\n\r\n1\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][news]"\r\n\r\nall\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][format]"\r\n\r\nheadline\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][items]"\r\n\r\n15\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][sort]"\r\n\r\nlatest\r\n-----------------------------48222048032047603611657549096--\r\n',
#     'hottest': '-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="securitytoken"\r\n\r\nguest\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="do"\r\n\r\nsaveoptions\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="setdefault"\r\n\r\nno\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="ignoreinput"\r\n\r\nno\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight1][idSuffix]"\r\n\r\n{}\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight1][_flexForm_]"\r\n\r\nflexForm\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight1][modelData]"\r\n\r\neyJwYV9sYXlvdXRfaWQiOiJuZXdzIiwicGFfY29tcG9uZW50X2lkIjoiTmV3c1JpZ2h0T25lIiwicGFfY29udHJvbHMiOiJuZXdzfE5ld3NSaWdodE9uZSIsInBhX2luamVjdHJldmVyc2UiOmZhbHNlLCJwYV9oYXJkaW5qZWN0aW9uIjpmYWxzZSwicGFfaW5qZWN0YXQiOmZhbHNlfQ==\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight1][news]"\r\n\r\nall\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight1][format]"\r\n\r\nlarge\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight1][items]"\r\n\r\n3\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight1][sort]"\r\n\r\nhottest\r\n-----------------------------48222048032047603611657549096--\r\n',
#     'most12h': '-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="securitytoken"\r\n\r\nguest\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="do"\r\n\r\nsaveoptions\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="setdefault"\r\n\r\nno\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="ignoreinput"\r\n\r\nno\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight3][idSuffix]"\r\n\r\n{}\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight3][_flexForm_]"\r\n\r\nflexForm\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight3][modelData]"\r\n\r\neyJwYV9sYXlvdXRfaWQiOiJuZXdzIiwicGFfY29tcG9uZW50X2lkIjoiTmV3c1JpZ2h0VGhyZWUiLCJwYV9jb250cm9scyI6Im5ld3N8TmV3c1JpZ2h0VGhyZWUiLCJwYV9pbmplY3RyZXZlcnNlIjpmYWxzZSwicGFfaGFyZGluamVjdGlvbiI6ZmFsc2UsInBhX2luamVjdGF0IjpmYWxzZX0=\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight3][news]"\r\n\r\n8\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight3][format]"\r\n\r\nthreads\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight3][items]"\r\n\r\n3\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight3][sort]"\r\n\r\nmostviewed\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight3][period]"\r\n\r\nlast12h\r\n-----------------------------48222048032047603611657549096--\r\n',
#     'lastFA': '-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="securitytoken"\r\n\r\nguest\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="do"\r\n\r\nsaveoptions\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="setdefault"\r\n\r\nno\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="ignoreinput"\r\n\r\nno\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight2][idSuffix]"\r\n\r\n{}\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight2][_flexForm_]"\r\n\r\nflexForm\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight2][modelData]"\r\n\r\neyJwYV9sYXlvdXRfaWQiOiJuZXdzIiwicGFfY29tcG9uZW50X2lkIjoiTmV3c1JpZ2h0VHdvIiwicGFfY29udHJvbHMiOiJuZXdzfE5ld3NSaWdodFR3byIsInBhX2luamVjdHJldmVyc2UiOmZhbHNlLCJwYV9oYXJkaW5qZWN0aW9uIjpmYWxzZSwicGFfaW5qZWN0YXQiOmZhbHNlfQ==\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight2][news]"\r\n\r\n107\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight2][format]"\r\n\r\nthreads\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight2][items]"\r\n\r\n3\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight2][sort]"\r\n\r\nmostviewed\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight2][period]"\r\n\r\nlast12h\r\n-----------------------------48222048032047603611657549096--\r\n',
#     'lastTA': '-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="securitytoken"\r\n\r\nguest\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="do"\r\n\r\nsaveoptions\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="setdefault"\r\n\r\nno\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="ignoreinput"\r\n\r\nno\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight4][idSuffix]"\r\n\r\n{}\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight4][_flexForm_]"\r\n\r\nflexForm\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight4][modelData]"\r\n\r\neyJwYV9sYXlvdXRfaWQiOiJuZXdzIiwicGFfY29tcG9uZW50X2lkIjoiTmV3c1JpZ2h0Rm91ciIsInBhX2NvbnRyb2xzIjoibmV3c3xOZXdzUmlnaHRGb3VyIiwicGFfaW5qZWN0cmV2ZXJzZSI6ZmFsc2UsInBhX2hhcmRpbmplY3Rpb24iOmZhbHNlLCJwYV9pbmplY3RhdCI6ZmFsc2V9\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight4][news]"\r\n\r\n89\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight4][format]"\r\n\r\nlarge\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight4][items]"\r\n\r\n2\r\n-----------------------------48222048032047603611657549096\r\nContent-Disposition: form-data; name="flex[News_newsRight4][sort]"\r\n\r\nlatest\r\n-----------------------------48222048032047603611657549096--\r\n',
# }

# calendata = '-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="securitytoken"\r\n\r\nguest\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="do"\r\n\r\nsaveoptions\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="setdefault"\r\n\r\nno\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="ignoreinput"\r\n\r\nno\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][idSuffix]"\r\n\r\n\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][_flexForm_]"\r\n\r\nflexForm\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][modelData]"\r\n\r\neyJwYV9sYXlvdXRfaWQiOiJob21lcGFnZSIsInBhX2NvbXBvbmVudF9pZCI6IkNhbGVuZGFyX0NvcHkxIiwicGFfY29udHJvbHMiOiJob21lcGFnZXxDYWxlbmRhcl9Db3B5MSIsInBhX2luamVjdHJldmVyc2UiOmZhbHNlLCJwYV9oYXJkaW5qZWN0aW9uIjpmYWxzZSwicGFfaW5qZWN0YXQiOmZhbHNlLCJob21lQ2FsZW5kYXIiOnRydWUsInZpZXdpbmdUb2RheSI6ZmFsc2UsInRvZGF5RGF0ZSI6Ik1heTI0LjIwMjMiLCJ0b21vcnJvd0RhdGUiOiJNYXkyNS4yMDIzIiwicHJldkNhbExpbmsiOiJyYW5nZT1tYXkxNi4yMDIzLW1heTIzLjIwMjMiLCJuZXh0Q2FsTGluayI6InJhbmdlPWp1bjEuMjAyMy1qdW44LjIwMjMiLCJwcmV2QWx0IjoiTWF5IDE2LCAyMDIzIC0gTWF5IDIyLCAyMDIzIiwibmV4dEFsdCI6Ikp1biAxLCAyMDIzIC0gSnVuIDcsIDIwMjMiLCJuZXh0SGlkZGVuIjpmYWxzZSwicHJldkhpZGRlbiI6ZmFsc2UsInJpZ2h0TGluayI6dHJ1ZX0=\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][begindate]"\r\n\r\n{}\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][enddate]"\r\n\r\n{}\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][calendardefault]"\r\n\r\ntoday\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][impacts][high]"\r\n\r\nhigh\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][impacts][medium]"\r\n\r\nmedium\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][_cbarray_]"\r\n\r\n1\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][eventtypes][growth]"\r\n\r\ngrowth\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][eventtypes][inflation]"\r\n\r\ninflation\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][eventtypes][employment]"\r\n\r\nemployment\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][eventtypes][centralbank]"\r\n\r\ncentralbank\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][eventtypes][bonds]"\r\n\r\nbonds\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][eventtypes][housing]"\r\n\r\nhousing\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][eventtypes][sentiment]"\r\n\r\nsentiment\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][eventtypes][pmi]"\r\n\r\npmi\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][eventtypes][speeches]"\r\n\r\nspeeches\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][eventtypes][misc]"\r\n\r\nmisc\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][_cbarray_]"\r\n\r\n1\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][currencies][aud]"\r\n\r\naud\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][currencies][cad]"\r\n\r\ncad\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][currencies][chf]"\r\n\r\nchf\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][currencies][cny]"\r\n\r\ncny\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][currencies][eur]"\r\n\r\neur\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][currencies][gbp]"\r\n\r\ngbp\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][currencies][jpy]"\r\n\r\njpy\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][currencies][nzd]"\r\n\r\nnzd\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][currencies][usd]"\r\n\r\nusd\r\n-----------------------------41566770301618672087425875231\r\nContent-Disposition: form-data; name="flex[Calendar_mainCalCopy1][_cbarray_]"\r\n\r\n1\r\n-----------------------------41566770301618672087425875231--\r\n'
# specials = {'nikkei': 'Nikkei225/USD', 'gold': 'Gold/USD'}
# # ====================================== END FOREXFACTORY ========================================


# # =========================================== FINVIZ =============================================
# # def get_aspxauth():
# #     with open(f'{SITE}/_login_tasks/saved-states/finviz.json') as f:
# #         parsed_json = loads(f.read())
# #     for item in parsed_json.get('cookies'):
# #         if item.get('name') == '.ASPXAUTH':
# #             return item.get('value')
# #     return None


# # cookies = {'.ASPXAUTH': get_aspxauth(),}

# rtparams = dict()
# quoteparams = {'instrument': 'futures','rev': '1686712055254','ticker': '6A','timeframe': 'w','type': 'new'}


# def get_ftime(days: str = None, iform: str = '%d/%m/%Y', oform: str = '%Y-%m-%d') -> str:
#     return datetime.strptime(days, iform).strftime(oform) if days else ""
# # ============================================ END FINVIZ =========================================


# # =========================================== FOREXSB =============================================
# pairs = (
#     "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD",
#     "CADCHF", "CADJPY", "CHFJPY",
#     "EURAUD", "EURCAD", "EURCHF", "EURGBP", "EURJPY", "EURNZD",
#     "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD",
#     "NZDCAD", "NZDCHF", "NZDJPY",
#     "XAGUSD", "XAUUSD", "AUDUSD", "EURUSD", "GBPUSD", "NZDUSD", "USDCAD", "USDCHF", "USDJPY",
#     "BRENTCMDUSD", "DEUIDXEUR", "USA30IDXUSD", "USA500IDXUSD", "USATECHIDXUSD", "GBRIDXGBP"
# )

# timeframes = {
#     '1440': 'D1', '240': 'H4', '60': 'H1',
#     '30': 'M30', '15': 'M15', '5': 'M5', '1': 'M1',
# }
# # ============================================ END FOREXSB ========================================


# # =========================================== FXEMPIRE ============================================
# artparams = {
#     'tags': '',
#     'mustContainAll': '',
#     'exclude': 'ignore',
#     'page': '1',
#     'mode': '',
#     'strict': 'false',
#     'isRecent': 'false',
#     'ids': '',
#     'instrumentType': '',
# }

# names = {
#     'cad': 'canada', 'usd': 'united-states',
#     'eur': 'euro-area,germany', 'gbp': 'united-kingdom',
#     'jpy': 'japan', 'chf': 'switzerland',
#     'aud': 'australia', 'nzd': 'new-zealand', 'chn': 'china',
#     # 'all': 'euro-area,canada,china,germany,japan,united-kingdom,united-states,switzerland,new-zealand',
#     # 'com': 'canada,new-zealand,australia',
#     # 'saf': 'japan,switzerland',
# }

# calparams = {
#     'page': '1',
#     'timezone': 'Asia/Ho_Chi_Minh',
#     'impact': '2,3',
#     'categoryGroup': 'gdp,markets,business,government,climate,money,housing,calendar,taxes,prices,consumer,labour,trade,health',
#     # 'country': 'all',
#     # 'dateFrom': '2023-07-08',
#     # 'dateTo': '2023-08-08',
# }
# # =========================================== END FXEMPIRE ========================================


# # =========================================== FXSTREET ============================================
# # -------------------- new code --------------------
# NEWSPAGE = 2
# symbols = {
#     'eurusd': 'fxs-3212164', 'gbpusd': 'fxs-3212166', 'audusd': 'fxs-3212322',
#     'nzdusd': 'fxs-3212173', 'usdcad': 'fxs-3212172', 'usdjpy': 'fxs-3212155',
#     'usdchf': 'fxs-3212167', 'eurgbp': 'fxs-3212168', 'gbpjpy': 'fxs-3212160',
#     'eurjpy': 'fxs-3212165', 'xauusd': 'fxs-3230110', 'usoil': 'fxs-52559005',
# }
# # -------------------- new code --------------------
# COMMODITIES = {'gold': 'fxs-3230110', 'oil': 'fxs-52559005'}

# INDICATORS = {
#     'cpi': {
#         'hoursToShowActual': 6,
#         'timezone': 'UTC',
#         'mainEvent': '9ae5cf07-55da-4f0f-b21d-f6f0835731d9',
#         'otherEvents': '6f846eaa-9a12-43ab-930d-f059069c6646,720115f6-77ca-424b-8f85-04f1faecd275,4abee304-9984-47cf-80ab-dca1114165f5,c28721ec-1bde-4fa5-bba7-86a3755288ca',
#     },
#     'nfp': {
#         'hoursToShowActual': 240,
#         'timezone': 'UTC',
#         'mainEvent': '9cdf56fd-99e4-4026-aa99-2b6c0ca92811',
#         'otherEvents': 'f9978a1f-510f-4a64-895c-6ca8f13d4522,9e9442d9-8a6b-4c9b-960d-78e9adf21aea,aec78791-08e0-4e06-b331-bbe5b34f879b,932c21fa-f664-40e1-a921-dbeb452f0081,b7abce59-89c3-42cc-8696-c4b6877cdee3',
#     },
# }

# BANKS = {
#     'fed': 'Federal Reserve', 'ecb': 'European Central Bank',
#     'boj': 'Bank of Japan', 'boe': 'Bank of England',
#     'snb': 'Swiss National Bank', 'rba': 'Reserve Bank of Australia',
#     'boc': 'Bank of Canada', 'rbnz': 'Reserve Bank of New Zealand'
# }

# PAIRS = (
#     'EURAUD', 'EURNZD', 'EURCAD', 'EURUSD', 'EURCHF', 'EURJPY', 'EURGBP',
#     'GBPAUD', 'GBPNZD', 'GBPCAD', 'GBPUSD', 'GBPCHF', 'GBPJPY',
#     'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD',
#     'XAUUSD', 'XAGUSD',
#     'USDCNH',

#     # 'AUDNZD', 'AUDCAD', 'AUDCHF', 'AUDJPY',
#     # 'NZDCAD', 'NZDCHF', 'NZDJPY',
#     # 'CADCHF', 'CADJPY', 'CHFJPY',
#     # 'XAUEUR', 'XAUGBP', 'XAUAUD', 'XAUCHF', 'XAUJPY',
#     # 'XAGEUR', 'XAGAUD'
# )

# COUNTRY_LST = ('Japan', 'Australia', 'United States', 'Euro Area', 'Germany',
#                'United Kingdom', 'China', 'New Zealand', 'Canada', 'Switzerland')

# FORELST = (
#     'fxs-3212164', 'fxs-3212166', 'fxs-3212155', 'fxs-3212167', 'fxs-3212322',
#     'fxs-3212173', 'fxs-3212172', 'fxs-3212160', 'fxs-3212165', 'fxs-3212168',
#     'fxs-129095728', 'fxs-3230110', 'fxs-52559005'
# )

# TECHLST = (
#     'fxs-3212164', 'fxs-3212168', 'fxs-3212165', 'fxs-3212215', 'fxs-3212169',
#     'fxs-3212247', 'fxs-3212183', 'fxs-3212166', 'fxs-3212155', 'fxs-3212322',
#     'fxs-3212172', 'fxs-3212173', 'fxs-3212167', 'fxs-3216797', 'fxs-3212163',
#     'fxs-3212157', 'fxs-3212182', 'fxs-3212216', 'fxs-3212166', 'fxs-3212158',
#     'fxs-3212160', 'fxs-3212162', 'fxs-3212246', 'fxs-3212155', 'fxs-3212200',
#     'fxs-3212171', 'fxs-3212268', 'fxs-898974', 'fxs-394990', 'fxs-751307',
#     'fxs-18922968', 'fxs-76597546', 'fxs-76593384', 'fxs-51399523', 'fxs-514562',
#     'fxs-5130908', 'fxs-402482', 'fxs-52559005', 'fxs-36354178', 'fxs-52559017',
#     'fxs-52559008', 'fxs-3230110', 'fxs-3230120', 'fxs-52559026'
# )

# RATESLST = (
#     'fxs-3212164', 'fxs-3212168', 'fxs-3212165', 'fxs-3212215', 'fxs-3212169',
#     'fxs-3212247', 'fxs-3212183', 'fxs-3212166', 'fxs-3212155', 'fxs-3212167',
#     'fxs-3212322', 'fxs-3212173', 'fxs-3212172', 'fxs-3216797', 'fxs-3212163',
#     'fxs-3212157', 'fxs-3212177', 'fxs-3212182', 'fxs-3212216', 'fxs-3212158',
#     'fxs-3212160', 'fxs-3212162', 'fxs-3212246', 'fxs-3212200', 'fxs-3212171',
#     'fxs-3212268', 'fxs-898974', 'fxs-394990', 'fxs-751307', 'fxs-18922968',
#     'fxs-76597546', 'fxs-514562', 'fxs-5130908', 'fxs-402482', 'fxs-2325578',
#     'fxs-51399239', 'fxs-51399237', 'fxs-51399541', 'fxs-3230110', 'fxs-3230120',
#     'fxs-52559005', 'fxs-36354178', 'fxs-52559017', 'fxs-52559008', 'fxs-3212170',
#     'fxs-3212180', 'fxs-3212259',
#     # 'fxs-178511545', 'fxs-178511528', 'fxs-178511546', 'fxs-170453004',
# )

# def getnum(string: str = None) -> str:
#     return "0" if string == "As Expected" else sub(r"([^0-9.-])", "", str(string).strip()) if string else ""

# def handle_tech(dct: dict = None) -> dict:
#     if 'Date' in dct:
#         del dct['Date']
#     for k, v in dct.items():
#         if k == 'PeriodType':
#             continue
#         dct[k] = get_num(v)
#     return dct

# def get_bearer():
#     with open(f'{SITE}/_login_tasks/saved-states/fxstreet.json') as f:
#         parsed_json = loads(f.read())
#     data = loads(parsed_json.get('origins')[0].get('localStorage')[0].get('value'))
#     return data.get('access_token')

# def handle_central(dct: dict = None) -> dict:
#     if 'EventId' in dct:
#         del dct['EventId']
#     for k, v in dct.items():
#         if k == 'CentralBankName':
#             continue
#         elif k in ('LastMeeting', 'NextMeeting'):
#             dct[k] = get_time(v)
#         else:
#             dct[k] = get_num(v)
#     return dct

# def extract_events(data: dict = None) -> dict:
#     return {
#         'name': data.get('EventName'),
#         'country': data.get('CountryName'),
#         'event_time': get_time(data.get('EventDate').get('DateUTC')),
#         'isBetter': data.get('IsBetter'),
#         'consensus': data.get('EventDate').get('Consensus'),
#         'previous': data.get('EventDate').get('Previous'),
#         'actual': data.get('EventDate').get('Actual'),
#         'revised': data.get('EventDate').get('Revised'),
#         'isBetter': data.get('IsBetter'),
#     }

# def convert_minago():
#     '''21 minutes ago'''
#     pass
# # =========================================== END FXSTREET ========================================


# # =========================================== MYFXBOOK ============================================
# COOKIES_FILE = f'{SITE}/myfxbook.json'
# MYFXBOOK_MAX_DAY = 90
# importances = {'2': 'medium',  '3': 'high'}

# # '240': 'H4', '60': 'H1', '30': 'M30', '15': 'M15', '5': 'M5'
# timeframes = {'43200': 'MN', '10080': 'W1', '1440': 'D1'}

# # '4': 'M30', '3': 'M15', '2': 'M5',
# indi_tfs = {'9': 'MN', '8': 'W1', '7': 'D1', '6': 'H4', '5': 'H1'}
# COTS_CURRENCIES = ('AUD', 'CAD', 'CHF', 'EU R', 'GBP', 'JPY', 'NZD')
# # =========================================== END MYFXBOOK ========================================
