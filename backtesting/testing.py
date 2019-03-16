import matplotlib.pyplot as plt
from tools import Indicators
import pandas as pd
import os

PATH_TO_DATA = os.getcwd()
PATH_TO_DATA = PATH_TO_DATA[:-PATH_TO_DATA[::-1].find("/")]
PATH_TO_DATA += "data/12-months/"

btc_df = pd.read_csv(PATH_TO_DATA + "Binance_BTCUSDT_1h_1 Mar, 2018-1 Mar, 2019.csv", sep='\t')
print(btc_df.head())

from strategies import MovingAverage
balance = MovingAverage().ma_cross_strategy(btc_df["open"].values, 13, 25)
plt.plot(range(len(balance)), balance)
plt.show()