# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
import pandas_ta as pta
# Load data
df = pd.read_csv("NF_60.csv")
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# === Heikin Ashi Calculation ===
def heikin_ashi(df):
    ha_df = df.copy()
    ha_df['HA_Close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha_open = [(df['open'][0] + df['close'][0]) / 2]
    for i in range(1, len(df)):
        ha_open.append((ha_open[i-1] + ha_df['HA_Close'][i-1]) / 2)
    ha_df['HA_Open'] = ha_open
    ha_df['HA_High'] = ha_df[['high', 'HA_Open', 'HA_Close']].max(axis=1)
    ha_df['HA_Low'] = ha_df[['low', 'HA_Open', 'HA_Close']].min(axis=1)
    return ha_df

df = heikin_ashi(df)

df['RSI'] = RSIIndicator(close=df['HA_Close'], window=14).rsi()

# === Supertrend Calculation ===
df['Supertrend'] = pta.supertrend(high = df['HA_High'],low=df['HA_Low'],close=df['HA_Close'],length=10,multiplier=3)["SUPERTd_10_3.0"]
#def calculate_supertrend(df, period=10, multiplier=3):
#    hl2 = (df['HA_High'] + df['HA_Low']) / 2
#    tr = pd.concat([
#        df['HA_High'] - df['HA_Low'],
#        abs(df['HA_High'] - df['HA_Close'].shift()),
#        abs(df['HA_Low'] - df['HA_Close'].shift())
#    ], axis=1).max(axis=1)
#    atr = tr.rolling(period).mean()
#
#    upperband = hl2 + multiplier * atr
#    lowerband = hl2 - multiplier * atr
#    supertrend = [True] * len(df)
#
#    for i in range(1, len(df)):
#        if df['HA_Close'][i] > upperband[i-1]:
#            supertrend[i] = True
#        elif df['HA_Close'][i] < lowerband[i-1]:
#            supertrend[i] = False
#        else:
#            supertrend[i] = supertrend[i-1]
#
#    # print(supertrend)
#    df['Supertrend'] = supertrend
#    return df
#
# df = calculate_supertrend(df)

# === Strategy Logic ===
initial_capital = 2_00_00_00
capital = 2000000 
slippage_pct = 0.0001
target = 300
stoploss = 50

positions = []
in_position = False
position_type = None
entry_price = None
capital_curve = []
trades = []
stoplosslength = 50
targetlength = 300
print(df.info())
for i in range(1,len(df)):
    row = df.iloc[i]
    prev_row= df.iloc[i-1]
    price = row["HA_Close"]

    if in_position:
        if position_type == "long" and (price>=target or price<=stoploss):
            exit_price = price
            pnl = exit_price-entry_price
            capital = capital+pnl

        if position_type == "short" and (price<=target or price >=stoploss):
            exit_price = price
            pnl = entry_price-exit_price
            capital = capital+pnl
    else:
        if row["Supertrend"] and row["RSI"]>60:
            in_position = True
            entry_price = price
            position_type = "long"
            stoploss = entry_price - stoplosslength
            target = entry_price+targetlength
            continue
        elif not row["Supertrend"] and row["RSI"]<40:
            in_position = True
            entry_price = price
            position_type = "short"
            stoploss = entry_price+stoplosslength
            target = entry_price-targetlength
            continue
    capital_curve.append(capital)
df["datatime"] = df["date"]+df["time"]
print(capital)
#print(len(capital_curve),len(df["datetime"]))
#plt.figure(figsize=(12,6))
#number = len(df["datetime"])
#plt.plot(capital_curve,df["datatime"][1:number-1], label='Equity Curve', color='green')
#plt.title("Equity Curve")
#plt.xlabel("Time")
#plt.ylabel("Capital")
#plt.legend()
#plt.grid(True)
#plt.show()

#
#for i in range(1, len(df)):
#    row = df.iloc[i]
#    prev_row = df.iloc[i - 1]
#    price = row['HA_Close']
#
#    # Exit logic
#    if in_position:
#        move = price - entry_price if position_type == 'long' else entry_price - price
#        if move >= target or move <= -stoploss:
#            exit_price = price * (1 - slippage_pct if position_type == 'long' else 1 + slippage_pct)
#            profit = (exit_price - entry_price) if position_type == 'long' else (entry_price - exit_price)
#            capital += profit
#            positions.append(profit)
#            in_position = False
#            capital_curve.append(capital)
#            continue
#
#    # Entry logic
#    if not in_position:
#        if row['Supertrend'] and row['RSI'] > 60:
#            entry_price = price * (1 + slippage_pct)
#            position_type = 'long'
#            in_position = True
#        elif not row['Supertrend'] and row['RSI'] < 40:
#            entry_price = price * (1 - slippage_pct)
#            position_type = 'short'
#            in_position = True
#
#    capital_curve.append(capital)
#
## === Performance Metrics ===
#returns = pd.Series(positions)
#daily_returns = returns / initial_capital
#sharpe_ratio = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252) if len(daily_returns) > 1 else 0
#max_drawdown = np.max(np.maximum.accumulate(capital_curve) - capital_curve)
#calmar_ratio = (capital_curve[-1] - initial_capital) / max_drawdown if max_drawdown != 0 else 0
#
## === Plot Equity Curve ===
#plt.figure(figsize=(12,6))
#plt.plot(capital_curve, label='Equity Curve', color='green')
#plt.title("Equity Curve")
#plt.xlabel("Time")
#plt.ylabel("Capital")
#plt.legend()
#plt.grid(True)
#plt.show()
#
## === Print Metrics ===
#print(f"Final Capital: ₹{capital:,.2f}")
#print(f"Total Trades: {len(positions)}")
#print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
#print(f"Calmar Ratio: {calmar_ratio:.2f}")
#print(f"Max Draw Down: {max_drawdown:.2f}")
#

# %%

# %%
