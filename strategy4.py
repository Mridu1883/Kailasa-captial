
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data and clean up column names just in case
df = pd.read_csv("NF_60.csv")
df.columns = df.columns.str.strip().str.lower()  # make all lowercase for consistency

# Combine date and time into a datetime column
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Sort by datetime (just in case)
df = df.sort_values('datetime').reset_index(drop=True)

def generate_renko(df, brick_size):
    renko = []
    dates = []
    last_price = df['close'].iloc[0]  # using lowercase column name
    renko.append(last_price)
    dates.append(df['datetime'].iloc[0])
    
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



def plot_renko(renko_df, window=300):
    plt.figure(figsize=(14, 6))

    # Use only the last 'window' bricks
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

# Run everything
brick_size = 10
renko_df = generate_renko(df, brick_size)
print(renko_df.head())
print(f"Renko bricks generated: {len(renko_df)}")
plot_renko(renko_df)
