import investpy as iv
import pandas as pd
import numpy as np
import re
from datetime import date
from calendar import monthrange, month_abbr

# 9 most important currencies
curs = ('USD', 'GBP', 'AUD', 'EUR', 'JPY', 'CAD', 'NZD', 'CNY', 'CHF')


def find_days(month, year):
    today = date.today()
    first = today.replace(day=1, month=month, year=year)
    last = today.replace(day=monthrange(year, month)
                         [1], month=month, year=year)
    return first, last


def convert_date(dates):
    for date in dates:
        yield date.strftime("%d/%m/%Y")


def get_calendar(times, countries, filepath=None):
    start, end = find_days(*times)
    start, end = list(convert_date([start, end]))

    df = iv.economic_calendar(time_zone='GMT +7:00', time_filter='time_only',
                              countries=countries,
                              importances=['high', 'medium'],
                              categories=None,
                              from_date=start, to_date=end)

    df.to_csv(filepath, index=False)


def read_calendar(filename='economic_calendar_12'):
    df = pd.read_csv(f'Data/{filename}.csv', index_col=1,
                     parse_dates=True).drop('id', axis=1)

    # ------------------------ remove_shit ------------------------
    # fucking hardcode
    shits = ['Q1', 'Q2', 'Q3', 'Q4']
    for i in range(1, 13):
        shits.append(f'{month_abbr[i]}')

    # fucking logic loop --------- for events ---------
    exam = list()
    for item in df['event'].values:
        wordList = re.sub("[^\w]", " ",  item).split()
        for shit in shits:
            if shit in wordList:
                wordList.remove(shit)
        exam.append(" ".join(wordList))
    df['event'] = exam

    # fucking logic loop --------- for special text after number ---------
    special_txt = ('K', 'M', 'B', 'T', '%')
    for item in ['actual', 'forecast', 'previous']:
        for count, status in enumerate(df[item].notna().values):
            if status:
                df.iloc[count][item] = ''.join(
                    [n for n in df.iloc[count][item] if n not in special_txt])
            else:
                pass
    # ------------------------ end remove_shit ------------------------

    # 5 types of outcome: N ~ NaN and Not ~ NotNaN
    # N_N_N, N_N_Not, Not_N_Not, N_Not_Not, Not_Not_Not
    pre_Nan = df[df['previous'].isna()]
    pre_notNan = df[df['previous'].notna()]

    # case_1
    fore_Nan = pre_notNan[pre_notNan['forecast'].isna()]
    Not_N_Not = fore_Nan[fore_Nan['actual'].notna()]
    N_N_Not = fore_Nan[fore_Nan['actual'].isna()]

    # case_2
    fore_notNan = pre_notNan[pre_notNan['forecast'].notna()]
    Not_Not_Not = fore_notNan[fore_notNan['actual'].notna()]
    # most important
    N_Not_Not = fore_notNan[fore_notNan['actual'].isna()]

    return df, pre_Nan, (Not_N_Not, N_N_Not), (Not_Not_Not, N_Not_Not)
