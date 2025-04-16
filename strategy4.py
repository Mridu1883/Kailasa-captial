import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("NF_60.csv")
df.columns = df.columns.str.strip().str.lower()  # Normalize column names
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Compute ATR
def compute_atr(df, period=14):
    high = df['high']
    low = df['low']
    close = df['close']

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(window=period).mean()
    return atr

# Generate Renko using ATR for brick size
def generate_renko(df, atr, atr_factor=1.5):
    renko = []
    dates = []
    last_price = df['close'].iloc[0]
    renko.append(last_price)
    dates.append(df['datetime'].iloc[0])

    # Calculate the brick size based on the latest ATR value
    brick_size = atr.iloc[-1] * atr_factor

    for i in range(1, len(df)):
        price = df['close'].iloc[i]
        diff = price - last_price

        while abs(diff) >= brick_size:
            direction = np.sign(diff)
            last_price += direction * brick_size
            renko.append(last_price)
            dates.append(df['datetime'].iloc[i])
            diff = price - last_price

    return pd.DataFrame({'datetime': dates, 'price': renko})

# Plot Renko
def plot_renko(renko_df, window=300):
    plt.figure(figsize=(14, 6))

    renko_df = renko_df.iloc[-window:].reset_index(drop=True)

    prices = renko_df['price'].values
    indices = np.arange(len(prices))

    colors = ['green' if prices[i] > prices[i - 1] else 'red' for i in range(1, len(prices))]
    heights = prices[1:] - prices[:-1]
    bottoms = prices[:-1]

    plt.bar(indices[1:], heights, bottom=bottoms, color=colors, width=1.0)

    plt.title(f"Renko Chart (Last {window} Bricks)")
    plt.xlabel("Bricks")
    plt.ylabel("Price")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Compute ATR and Generate Renko
atr = compute_atr(df, period=14)
renko_df = generate_renko(df, atr)

# Plot the last 300 Renko bricks
plot_renko(renko_df, window=300)
