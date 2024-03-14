import requests as rq
import pandas as pd
import json
from bs4 import BeautifulSoup
from datetime import datetime

pairs = ('AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CHFJPY',
         'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD',
         'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD',
         'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD',
         'USDCHF', 'USDJPY', 'XAGUSD', 'XAUUSD')


def myfxbook_extract():
    r = rq.get('https://www.myfxbook.com/community/outlook')
    soup = BeautifulSoup(r.content, "html.parser")

    # -------------------------- price range --------------------------
    price_tbl = soup.find(id="outlookSymbolsTable")
    price_df = pd.read_html(price_tbl.prettify(), index_col=0)[0]

    drop_cols = ['Community Trend (Shorts vs Longs)',
                 'Symbol Popularity', 'Unnamed: 6']
    price_df.drop(drop_cols, axis=1, inplace=True)
    for item in price_df.index.tolist():
        if item not in pairs:
            price_df.drop(item, inplace=True)

    price_df.rename(columns={'Avg. Short Price /  Distance From Price': 'Short_Distance',
                             'Avg. Long Price /  Distance From Price': 'Long_Distance',
                             'Current Price': 'Current_Price'}, inplace=True)
    distance = price_df.iloc[:, 0:2].copy()
    distance.Short_Distance = distance.Short_Distance.map(lambda x: x.rstrip(' pips'))
    distance.Long_Distance = distance.Long_Distance.map(lambda x: x.rstrip(' pips'))
    
    tmp_s = distance.Short_Distance.str.split(' ', expand=True).iloc[:, [0, 2]].copy()
    tmp_s.rename(columns={tmp_s.columns[0]: 'Short_Price', tmp_s.columns[1]: 'Short_Distance'}, inplace=True)
        
    tmp_l = distance.Long_Distance.str.split(' ', expand=True).iloc[:, [0, 2]].copy()
    tmp_l.rename(columns={tmp_l.columns[0]: 'Long_Price', tmp_l.columns[1]: 'Long_Distance'}, inplace=True)

    result_price_df = pd.concat([tmp_s, tmp_l, price_df.Current_Price], axis=1).apply(pd.to_numeric)
    result_price_df.sort_values(by=['Short_Distance'], ascending=False, key=abs, inplace=True)

    # -------------------------- retail sentiment --------------------------
    tag = "table table-bordered table-vertical-middle text-center margin-top-5"
    sent_table = soup.find_all("table", {"class": tag})
    sent_df = pd.DataFrame()
    for elem in sent_table:
        for pair in pairs:
            if pair in elem.text:
                df = pd.read_html(elem.prettify(), index_col=0)[0]
                sent_df = df if sent_df.empty else pd.concat([sent_df, df])
            else:
                continue

    sent_df.Volume = sent_df.Volume.map(lambda x: x.rstrip(' lots'))
    sent_df.Percentage = sent_df.Percentage.map(lambda x: x.rstrip('%'))
    numeric_sentiments = sent_df.iloc[:, 1:4].apply(pd.to_numeric)
    result_sentiments = pd.concat([sent_df.Action, numeric_sentiments], axis=1)
    result_sentiments.sort_values(by=['Percentage'], ascending=False, inplace=True)

    # -------------------------- traders percentage --------------------------
    tag = "text-center margin-top-5"
    sent_div = soup.find_all("div", {"class": tag})
    rows, indices = [], []
    for elem in sent_div:
        for pair in pairs:
            if pair in elem.text:
                temp = ''.join( c for c in elem.text if  c not in 'of traders are currently trading.' )
                rows.append(temp.split("%")[0])
                indices.append(temp.split("%")[1])
            else:
                continue
    sent_div_df = pd.DataFrame(rows, columns=['Percentage_traders'], index=indices).apply(pd.to_numeric)
    sent_div_df.sort_values(by=['Percentage_traders'], ascending=False, inplace=True)

    return result_price_df, result_sentiments, sent_div_df


# def currency_strength_extract(timestamp):
def currency_strength_extract():
    # print(timestamp)
    # r = rq.get(f'https://currency-strength.com/php/chart1d.json?id={timestamp}')
    r = rq.get('https://currency-strength.com/php/chart1d.json')
    currency_json = r.content.decode('utf8')
    data = json.loads(currency_json)

    list_df = list()
    for i in range(len(data)):
        df = pd.DataFrame.from_dict(data[i])
        new_df = pd.DataFrame(df['values'].to_list(), columns=['Date', data[i]['key']])
        new_df['Date'] = new_df['Date'].apply(lambda d: datetime.fromtimestamp(d/1000.0))
        new_df.set_index('Date', inplace=True)
        list_df.append(new_df)

    currency_strength_df = pd.concat(list_df, axis=1, ignore_index=False).apply(pd.to_numeric)
    return currency_strength_df


def fxstreet_extract():
    r = rq.get('https://currency-strength.com/php/chart1d.json')
    print(r.status_code)
    # return