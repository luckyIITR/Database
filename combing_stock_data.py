import os

import pandas as pd


def intersection(lst1, lst2):
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


cwd = r'F:\Database\drive\Data'
list1 = os.listdir(os.path.join(cwd, "2017"))
list2 = os.listdir(os.path.join(cwd, "2018"))
list3 = os.listdir(os.path.join(cwd, "2019"))
list4 = os.listdir(os.path.join(cwd, "2020"))

l1 = intersection(list1, list2)
l1 = intersection(l1, list3)
l1 = intersection(l1, list4)
# filename = l2[0]
for filename in l1:
    years = ["2017","2018", "2019", "2020"]
    main_data = pd.DataFrame()
    for year in years:
        # year = years[0]
        loc = os.path.join(cwd, year)
        loc = os.path.join(loc, filename)
        data = pd.read_csv(loc, header=0, index_col=0)
        main_data = pd.concat([main_data, data], axis=0)
    main_data.to_csv("F:\Database\drive\Data\\2017-2020\\"+filename)