import pandas as pd
from crawldata.functions import *
from crawldata.items import PriceItem


class CrawlerSpider(Spider):
    name = 'read_fxsb_prices'
    custom_settings = {'LOG_FILE': f"{SITE}/log/{name}_{LOG_TIME}.log",}

    def start_requests(self):
        folder_path = Path(f'{SITE}/data/test/')
        foldernames = [f for f in folder_path.iterdir() if f.is_dir()]
        for foldername in foldernames:
            filenames = [f for f in Path(foldername).iterdir() if f.is_file()]
            for filename in filenames:
                ticker, time_ = str(filename).split('.')[0].split('/')[-1].split('_')
                df = pd.read_csv(filename, parse_dates=['time'], infer_datetime_format=True)
                records = df.to_dict('records')
                yield Request(f"file://{PROJECT}/ultilities/sample.html", dont_filter=True, meta={'data': (ticker, time_, records)})   
          
    def parse(self, response):
        ticker, time_, records = response.meta.get('data')
        for record in records:
            timeframe = tf_mapping.get(time_, time_)
            record_item = {
                '_id': calculate_id(ticker, timeframe, str(record.get('time'))),
                'ticker_': ticker, 
                'name_': fxsb_mapping.get(ticker, ticker),
                'time_entered_': CRAWL_DATE,
                'timeframe_': timeframe,
                'time_': record.get('time'),
                'close_': record.get('close'),
                'open_': record.get('open'),
                'high_': record.get('high'),
                'low_': record.get('low'),
                'volume_': record.get('volume'),
            }
            print(record_item)
            yield PriceItem(record_item)