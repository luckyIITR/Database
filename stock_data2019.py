import pandas as pd
import os
import datetime as dt

cwd = r"F:\Database\drive\Data"
all = os.listdir(cwd)
all = all[3:]


stock_files = []
for folder in all:
    loc = os.path.join(cwd, folder)
    loc = os.path.join(loc, folder)
    stock_files.extend(os.listdir(loc))

stock_files = sorted(list(set(stock_files)))


for filename in stock_files:
    # filename = stocks_list_found[0]
    main_data = pd.DataFrame()
    for folder in all:
        # month = months[0]
        loc = os.path.join(cwd, folder)
        loc = os.path.join(loc, folder)
        loc = os.path.join(loc, filename)
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
    main_data.to_csv("F:\Database\drive\Data\\2019\\"+filename[:-4]+".csv")
        # break