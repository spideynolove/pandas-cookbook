from own_utils.crawl_sentiment import myfxbook_extract as de
from own_utils.economic_calendar import get_calendar as gc
from datetime import datetime, timedelta, date
from own_utils.crawl_sentiment import currency_strength_extract as ce
from own_utils.crawl_sentiment import fxstreet_extract as fe
import matplotlib.pyplot as plt
import pandas as pd

'''

pairs = ('AUD/CAD', 'AUD/CHF', 'AUD/JPY', 'AUD/NZD', 'AUD/USD', 'CHF/JPY',
         'EUR/AUD', 'EUR/CAD', 'EUR/CHF', 'EUR/GBP', 'EUR/JPY', 'EUR/NZD',
         'EUR/USD', 'GBP/AUD', 'GBP/CAD', 'GBP/CHF', 'GBP/JPY', 'GBP/NZD',
         'GBP/USD', 'NZD/CAD', 'NZD/CHF', 'NZD/JPY', 'NZD/USD', 'USD/CAD',
         'USD/CHF', 'USD/CNH', 'USD/JPY', 'XAG/USD',  'XAU/USD')

news = list()
for pair in pairs:
    news.append(pair.replace('/', ''))

print(news)

# -------------------------------------------------------------------------------
# '''

# -------------------------------------------------------------------------------
'''
countries = ['united states', 'united kingdom', 'australia', 'canada',
             'switzerland', 'germany', 'japan', 'new zealand', 'china']

for i in range(1, 6):
    gc(times=[i, 2022], countries=countries,
       filepath=f'cookbook_data//owndata//economic_calendar_{i}.csv')
# __Content__</span>
# '''
# -------------------------------------------------------------------------------
# # de()
# price_df, sent_df, sent_div_df = de()
# price_df.to_csv('cookbook_data/owndata/price0904_df.csv')
# sent_df.to_csv('cookbook_data/owndata/sent0904_df.csv')

# price_df = pd.read_csv('cookbook_data/owndata/price0904_df.csv')
# sent_df = pd.read_csv('cookbook_data/owndata/sent0904_df.csv')
# print(sent_df.tail())

# -------------------------------------------------------------------------------

# timestamp = str(datetime.now().timestamp() * 1000).split('.')[0]
# df = ce(timestamp)

# df = ce()
# df.to_csv('cookbook_data/owndata/currency_strength1404_df.csv')

df = pd.read_csv('cookbook_data/owndata/currency_strength0904_df.csv')

# df.plot(figsize=(12,8))
# plt.show()
print(df.head())

# -------------------------------------------------------------------------------
# fe()

'''
rate detail: pips - money
10 - 10.88: GBPCHF, 10.86: EURCHF, 10.87: USDCHF
20 - 15.81: GBPCAD, 20:15.78: EURCAD, USDCAD
15 - 11: GBPAUD, 15 - 10.98: EURAUD
10 -10: GBPUSD, EURUSD, AUDUSD, NZDUSD, XAGUSD
100 - 10: XAUUSD
10 -6.8: GBPNZD, EURNZD
10 - 8.65: GBPJPY, USDJPY , 8.66: EJPY
# '''
