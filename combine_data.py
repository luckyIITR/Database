import os
import pandas as pd
import datetime as dt
import mplfinance as mpf
import yfinance as yf


def get_dir():
    cwd = r"F:\Database\option-drice\2019-banknifty"
    all = os.listdir(cwd)
    fold = []
    for element in all:
        if element[-4:] != ".zip":
            fold.append(element)
    for i in range(len(fold)):
        x = os.path.join(cwd, fold[i])
        fold[i] = os.path.join(x, fold[i])
    for i in range(len(fold)):
        for element in os.listdir(fold[i]):
            if element[-4:] != ".zip":
                fold[i] = os.path.join(fold[i], element)
    return fold


def get_data(dbd, contract):
    loc = os.path.join(dbd, contract)

    data = pd.read_csv(loc, sep=",", header=0,
                       names=['Symbol', 'date', 'time', 'Open', 'High', 'Low', 'Close', 'x'])
    data = data[['date', 'time', 'Open', 'Low', 'High', 'Close']].copy()
    data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d')
    data['time'] = pd.to_datetime(data['time'], format='%H:%M')
    data['Time'] = [dt.datetime.combine(data.loc[e, 'date'], data.loc[e, 'time'].time()) for e in data.index]
    data = data[['Time', 'Open', 'Low', 'High', 'Close']].copy()
    data.set_index('Time', inplace=True, drop=True)
    ohlc_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}
    data = data.resample('5T').agg({'Open': 'first',
                                    'High': 'max',
                                    'Low': 'min',
                                    'Close': 'last'})
    data = data[data.index.month == data.index.date[-1].month]
    data.dropna(inplace=True)
    return data


def extract_dates(dbd):
    contract = os.listdir(dbd)[0]
    loc = os.path.join(dbd, contract)

    data = pd.read_csv(loc, sep=",", header=0,
                       names=['Symbol', 'date', 'time', 'Open', 'High', 'Low', 'Close', 'x'])
    data = data[['date', 'time', 'Open', 'Low', 'High', 'Close']].copy()
    data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d')
    data['time'] = pd.to_datetime(data['time'], format='%H:%M')
    data['Time'] = [dt.datetime.combine(data.loc[e, 'date'], data.loc[e, 'time'].time()) for e in data.index]
    data = data[['Time', 'Open', 'Low', 'High', 'Close']].copy()
    data.set_index('Time', inplace=True, drop=True)
    ohlc_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}
    data = data.resample('5T').agg({'Open': 'first',
                                    'High': 'max',
                                    'Low': 'min',
                                    'Close': 'last'})
    data = data[data.index.month == data.index.date[-1].month]
    data.dropna(inplace=True)
    return sorted(list(set(data.index.date)))


def banknify(date):
    df = yf.download('^NSEBANK', start=date, end=date + dt.timedelta(days=1))
    return df['Open'].iloc[-1]


def check(x):
    global bnf_ltp
    if int(x[9:14]) < bnf_ltp and x[14:16] == "PE":
        return True
    elif int(x[9:14]) > bnf_ltp and x[14:16] == 'CE':
        return True
    return False


# mpf.plot(data)

dirs = get_dir()
get_data(dirs)

for dir in dirs:
    # extracted dates inside a month
    dates = extract_dates(dir)
    for date in dates:
        bnf_ltp = banknify(date)
        contracts = os.listdir(dir)
        contracts = list(filter(check, contracts))
        for contract in contracts:
            df_5min = get_data(dir, contract)
