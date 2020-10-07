'''Stock parser'''
# import packages
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta

# var definitions
path = "/home/mlb/res/json/"
date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
cols = ["0050", "0051", "0052"]
dates = list()
df = pd.DataFrame(columns=cols)
feature = pd.DataFrame(columns=["open", "close", "max_volume"])
 
# function definitions
def past_n_dates(date, path, dates, n=3):   # store the past n trading dates
    while len(dates) < n:
        checked_date = date - timedelta(days=1)
        if os.path.isfile(path + checked_date.strftime("%Y-%m-%d") + ".json"):
            dates.append(checked_date)
        date = checked_date

def gen_df(dates, df):   # read in the file and generate dataframe
    for date in dates:
        date = date.strftime("%Y-%m-%d")
        sub_df = pd.read_json(path + date + ".json")
        df = pd.concat([df, sub_df[cols]])
    return df

def extract_features(df, feature):   # extract features from dataframe
    for col in df.columns:
        idx_groups = df.groupby(df.index)
        mean_open = idx_groups.get_group("open")[col].mean()
        mean_close = idx_groups.get_group("close")[col].mean()
        max_volume = idx_groups.get_group("volume")[col].max()
        f = {
            "open": mean_open,
            "close": mean_close,
            "max_volume": max_volume
        }
        feature = feature.append(f, ignore_index=True)
    feature = np.array(feature)
    return feature

past_n_dates(date, path, dates)
df = gen_df(dates, df)
feature = extract_features(df, feature)
print(feature)
