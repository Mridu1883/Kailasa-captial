import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("NF_60.csv")
df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

def calc_atr(df,period = 14):
    high = df['High']
    low = df['Low']
    close = df['Close']
    sumoftr = 0 
    df["ATR"] = None
    for i in range(0,period):
        sumoftr = df['High'].iloc[i]-df["Low"].iloc[i]
    df["ATR"].iloc[period-1] = sumoftr/period
    starter = 0
    for i in range(period,len(df)):
        sumoftr = sumoftr - (df['High'].iloc[starter]-df["Low"].iloc[starter]) + df['High'].iloc[i]-df["Low"].iloc[i]
        starter = starter + 1
        df["ATR"].iloc[i] = sumoftr/period
calc_atr(df,period=14)
print(df)


