
import pandas as pd
import datetime
import dateutil
from stocktrends import Renko

# Modify this to your CSV file path
csv_file_path = 'NF_60.csv'

# Load the CSV file into a DataFrame
ohlc = pd.read_csv(csv_file_path, parse_dates=['Date'], index_col='Date')

# Function to convert ohlc data into renko bricks. Pass dataframe name and brick size
def df_to_renko(data, n):
    data.reset_index(inplace=True)
    data.columns = [i.lower() for i in data.columns]
    print(data.isnull().values.any())
    df = Renko(data)
    df.brick_size = n
    renko_df = df.get_ohlc_data()
    return renko_df

# Use a brick size of 50
r_bars = df_to_renko(ohlc, 50)
print('# of rows in DF:', len(r_bars))

# Save the Renko chart data to an Excel file
r_bars.to_excel("output.xlsx", index=False)

# Extract the open and close columns for the plot
new_df = r_bars[['open', 'close']]

import matplotlib.pyplot as plt
import matplotlib
plt.rcParams["figure.figsize"] = (18, 9)

# Create the figure
fig = plt.figure(1)
fig.clf()
axes = fig.gca()

# Add 10 extra spaces to the right
num_bars = 100
df = new_df.tail(num_bars)

renkos = zip(df['open'], df['close'])

# Plot the bars, green for 'up', red for 'down'
index = 1
for open_price, close_price in renkos:
    if open_price < close_price:
        renko = matplotlib.patches.Rectangle((index, open_price), 1, close_price - open_price, edgecolor='black', facecolor='green', alpha=0.5)
        axes.add_patch(renko)
    else:
        renko = matplotlib.patches.Rectangle((index, open_price), 1, close_price - open_price, edgecolor='black', facecolor='red', alpha=0.5)
        axes.add_patch(renko)
    index = index + 1

# Adjust the axes
plt.xlim([0, num_bars + 5])
plt.ylim([min(min(df['open']), min(df['close'])), max(max(df['open']), max(df['close']))])
plt.grid(True)
plt.show()
