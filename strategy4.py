import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("NF_60.csv")
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
def generate_renko(df, brick_size):
    renko = []
    dates = []
    last_price = df['Close'].iloc[0]
    renko.append(last_price)
    dates.append(df['Date'].iloc[0])
    
    for i in range(1, len(df)):
        price = df['Close'].iloc[i]
        diff = price - last_price

        while abs(diff) >= brick_size:
            direction = np.sign(diff)
            last_price += direction * brick_size
            renko.append(last_price)
            dates.append(df['Date'].iloc[i])
            diff = price - last_price

    return pd.DataFrame({'Date': dates, 'Price': renko})

def plot_renko(renko_df):
    plt.figure(figsize=(12, 6))

    up = []
    down = []

    for i in range(1, len(renko_df)):
        if renko_df['Price'].iloc[i] > renko_df['Price'].iloc[i-1]:
            up.append(i)
        else:
            down.append(i)

    plt.bar(up, renko_df['Price'].iloc[up] - renko_df['Price'].iloc[np.array(up)-1], 
            bottom=renko_df['Price'].iloc[np.array(up)-1], color='green', label='Up')
    plt.bar(down, renko_df['Price'].iloc[down] - renko_df['Price'].iloc[np.array(down)-1], 
            bottom=renko_df['Price'].iloc[np.array(down)-1], color='red', label='Down')

    plt.title("Renko Chart")
    plt.xlabel("Bricks")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()

brick_size = 10  # you can adjust this
renko_df = generate_renko(df, brick_size)
plot_renko(renko_df)
