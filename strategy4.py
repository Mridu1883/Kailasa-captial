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
    renko_prices = []
    renko_dates = []
    renko_directions = []

    last_price = df['close'].iloc[0]
    last_direction = 0
    renko_prices.append(last_price)
    renko_dates.append(df['datetime'].iloc[0])
    renko_directions.append(0)

    # Use final ATR as static brick size
    brick_size = atr.iloc[-1] * atr_factor

    for i in range(1, len(df)):
        price = df['close'].iloc[i]
        datetime = df['datetime'].iloc[i]
        diff = price - last_price
        bricks = int(diff / brick_size)  # number of bricks to add

        while abs(bricks) >= 1:
            direction = int(np.sign(bricks))
            last_price += direction * brick_size
            renko_prices.append(last_price)
            renko_dates.append(datetime)
            renko_directions.append(direction)
            bricks -= direction  # reduce brick count

    renko_df = pd.DataFrame({
        'datetime': renko_dates,
        'price': renko_prices,
        'direction': renko_directions
    })

    return renko_df
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
