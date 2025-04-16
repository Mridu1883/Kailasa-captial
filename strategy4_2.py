import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("NF_60.csv")
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

def calc_atr(df,period = 14):
    high = df['high']
    low = df['low']
    close = df['close']
    sumoftr = 0 
    df["ATR"] = 0
    for i in range(0,period):
        sumoftr = sumoftr+ (df['high'].iloc[i]-df["low"].iloc[i])
    df["ATR"].iloc[(period-1)] = sumoftr/period
    starter = 0
    for i in range(period,len(df)):
        sumoftr = sumoftr - (df['high'].iloc[starter]-df["low"].iloc[starter]) + df['high'].iloc[i]-df["low"].iloc[i]
        starter = starter + 1
        df["ATR"].iloc[i] = sumoftr/period
calc_atr(df,period=14)
print(df)


