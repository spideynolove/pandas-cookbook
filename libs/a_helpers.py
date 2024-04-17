import sys


class LazyCallable(object):
    def __init__(self, name):
        self.n, self.f = name, None
    
    def __call__(self, *a, **k):
        if self.f is None:
            modn, funcn = self.n.rsplit('.', 1)
            if modn not in sys.modules:
                __import__(modn)
                self.f = getattr(sys.modules[modn], funcn)
            else:
                self.f = getattr(sys.modules[modn], funcn)
        return self.f(*a, **k)


def add_percentage_change(df, column_name, periods):
    period_map = {'W': 5,'M': 21, 'Y': 252, '3Y': 252 * 3}
    for period in periods:
        if period == 'YTD':
            df['YTD'] = df[column_name] / df.iloc[0][column_name] - 1
        else:
            period_value = period_map.get(period, period)
            new_column_name = f'Chg{period}'
            df[new_column_name] = df[column_name].pct_change(periods=period_value) * 100
            
    return df


def add_rolling_functions(df, column_names, window_sizes, functions):
    for column_name in column_names:
        for window_size in window_sizes:
            if isinstance(window_size, str):
                window = window_size
            elif isinstance(window_size, int):
                window = window_size
            else:
                raise ValueError("Window size must be either a string (e.g., '8D') or an integer (e.g., 8)")
            
            for func in functions:
                if func == 'mean':
                    df[f'{column_name}Mean{window}'] = df[column_name].rolling(window=window).mean()
                elif func == 'sum':
                    df[f'{column_name}Sum{window}'] = df[column_name].rolling(window=window).sum()
                elif func == 'max':
                    df[f'{column_name}Max{window}'] = df[column_name].rolling(window=window).max()
                elif func == 'min':
                    df[f'{column_name}Min{window}'] = df[column_name].rolling(window=window).min()                
                elif func == 'var':
                    df[f'{column_name}Var{window}'] = df[column_name].rolling(window=window).var()
                elif func == 'std':
                    df[f'{column_name}Std{window}'] = df[column_name].rolling(window=window).std()
                elif func == 'skew':
                    df[f'{column_name}Skew{window}'] = df[column_name].rolling(window=window).skew()
                elif func == 'kurt':
                    df[f'{column_name}Kurt{window}'] = df[column_name].rolling(window=window).kurt()
                elif func == 'shift':
                    df[f'{column_name}Shift{window}'] = df[column_name].rolling(window=window).shift()
                elif func == 'diff':
                    df[f'{column_name}Diff{window}'] = df[column_name].rolling(window=window).diff()
                else:
                    raise ValueError(f"Unsupported function: {func}")
                    
    return df


def add_technical_indicators(df, indicators):
    for indicator, params in indicators.items():
        time_periods = params.get('time_periods', [])
        input_columns = params.get('input_columns', [])
        if isinstance(input_columns, str):
            input_columns = [input_columns]  # Convert single input column to list

        if not isinstance(time_periods, list) or time_periods == "":
            time_periods = [""]

        for time_period in time_periods:
            column_name = f'{indicator}{time_period}'
            indicator_func = LazyCallable(f'talib.{indicator}')
            if time_period:
                df[column_name] = indicator_func(*[df[col] for col in input_columns], timeperiod=time_period)
            else:
                df[column_name] = indicator_func(*[df[col] for col in input_columns])
    
    return df