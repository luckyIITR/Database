import pandas as pd
import os
import datetime as dt

cwd = r"F:\Database\drive\Data\IntradayData_2018\IntradayData_2018"
all = os.listdir(cwd)
stocks_list_found = os.listdir(cwd)
# print(os.listdir(iwd))

stocks_list_found = sorted(list(set(stocks_list_found)))

for filename in stocks_list_found:
    if filename[-3:] != "txt":
        stocks_list_found.remove(filename)

for filename in stocks_list_found:
    # filename = stocks_list_found[0]
    # month = months[0]
    loc = os.path.join(cwd,filename)
    data = pd.read_csv(loc, sep=",", header=0,
                       names=['Symbol', 'date', 'time', 'Open', 'High', 'Low', 'Close', 'Volume','x'])
    data = data[['date', 'time', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')
    data['time'] = pd.to_datetime(data['time'], format='%H:%M')
    data['Time'] = [dt.datetime.combine(data.loc[e, 'date'], data.loc[e, 'time'].time()) for e in data.index]
    data = data[['Time', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    data.set_index('Time', inplace=True, drop=True)
    data.to_csv("F:\Database\drive\Data\\2018\\"+filename[:-4]+".csv")
