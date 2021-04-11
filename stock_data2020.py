import pandas as pd
import os
import datetime as dt

cwd = r"F:\Database\drive\2020-20210318T035736Z-001\2020"
months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
stocks_list_found = []
for month in months:
    iwd = os.path.join(cwd, month)
    iwd = os.path.join(iwd, "IntradayData_" + month + "2020")
    iwd = os.path.join(iwd, "IntradayData_" + month + "2020")
    if len(os.listdir(iwd)) == 1:
        iwd = os.path.join(iwd, "NIFTY50_" + month + "2017")
    stocks_list_found.extend(os.listdir(iwd))
    # print(os.listdir(iwd))

stocks_list_found = sorted(list(set(stocks_list_found)))

for filename in stocks_list_found:
    if filename[-3:] != "txt":
        stocks_list_found.remove(filename)

for filename in stocks_list_found:
    # filename = stocks_list_found[0]
    main_data = pd.DataFrame()
    for month in months:
        # month = months[0]
        iwd = os.path.join(cwd, month)
        iwd = os.path.join(iwd, "IntradayData_" + month + "2020")
        iwd = os.path.join(iwd, "IntradayData_" + month + "2020")
        loc = os.path.join(iwd, filename)
        try :
            data = pd.read_csv(loc, sep=",", header=0,
                               names=['Symbol', 'date', 'time', 'Open', 'High', 'Low', 'Close', 'Volume','x'])
            data = data[['date', 'time', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
            data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')
            data['time'] = pd.to_datetime(data['time'], format='%H:%M')
            data['Time'] = [dt.datetime.combine(data.loc[e, 'date'], data.loc[e, 'time'].time()) for e in data.index]
            data = data[['Time', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
            data.set_index('Time', inplace=True, drop=True)
            main_data = pd.concat([main_data, data], axis=0)
        except FileNotFoundError:
            continue
    main_data.to_csv("F:\Database\drive\\2020-20210318T035736Z-001\\2020\\2020\\"+filename[:-4]+".csv")
        # break
