
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


def plot_renko(renko_df):
    plt.figure(figsize=(12, 6))

    up = []
    down = []

    for i in range(1, len(renko_df)):
        if renko_df['price'].iloc[i] > renko_df['price'].iloc[i - 1]:
            up.append(i)
        else:
            down.append(i)

    up = np.array(up)
    down = np.array(down)

    # Calculate differences and bottoms
    up_heights = renko_df['price'].iloc[up].values - renko_df['price'].iloc[up - 1].values
    up_bottoms = renko_df['price'].iloc[up - 1].values

    down_heights = renko_df['price'].iloc[down].values - renko_df['price'].iloc[down - 1].values
    down_bottoms = renko_df['price'].iloc[down - 1].values

    # Plot
    plt.bar(up, up_heights, bottom=up_bottoms, color='green', label='Up')
    plt.bar(down, down_heights, bottom=down_bottoms, color='red', label='Down')

    plt.title("Renko Chart")
    plt.xlabel("Bricks")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()
# Run everything
brick_size = 10
renko_df = generate_renko(df, brick_size)
print(renko_df.head())
print(f"Renko bricks generated: {len(renko_df)}")
plot_renko(renko_df)
