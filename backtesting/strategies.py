import numpy as np
from tools import Indicators

class MovingAverage:

	def __init__(self):
		pass


	def ma_cross_strategy(self, open_prices, 
		fast_h=6, slow_h=13, family="sma", 
		start_balance=1000, fee=0.1):

		if family == "sma":
			ma_fast = Indicators().sma(open_prices, fast_h)
			ma_fast = ma_fast[slow_h-fast_h:]
			ma_slow = Indicators().sma(open_prices, slow_h)
			open_prices = open_prices[slow_h-1:]
		elif family == "ema":
			ma_fast = Indicators().ema(open_prices, fast_h)
			ma_slow = Indicators().ema(open_prices, slow_h)

		balance = np.ones(len(open_prices))
		balance[0] = start_balance
		hold_btc  = 0

		for i in range(1, len(open_prices)):  
			if hold_btc == 0:
				if (ma_fast[i] > ma_slow[i] and ma_fast[i-1] < ma_slow[i-1]): #buy btc
					hold_btc = balance[i-1] / open_prices[i] * (1.0 - fee/100.0)
				balance[i] = balance[i-1]
			else:
				balance[i] = hold_btc * open_prices[i] * (1.0 - fee/100.0)
				if (ma_fast[i] < ma_slow[i] and ma_fast[i-1] > ma_slow[i-1]): #sell btc
					hold_btc = 0
				
		return balance


	def ma_cross_strategy_sltp(self, open_prices, 
		fast_h=6, slow_h=13, family="sma", 
		start_balance=1000, fee=0.1,
		stop_loss=0.05, take_profit=0.07):

		if family == "sma":
			ma_fast = Indicators().sma(open_prices, fast_h)
			ma_fast = ma_fast[slow_h-fast_h:]
			ma_slow = Indicators().sma(open_prices, slow_h)
			open_prices = open_prices[slow_h-1:]
		elif family == "ema":
			ma_fast = Indicators().ema(open_prices, fast_h)
			ma_slow = Indicators().ema(open_prices, slow_h)

		balance = np.ones(len(open_prices))
		balance[0] = start_balance
		hold_btc  = 0
		buy_price = 0

		for i in range(1, len(open_prices)):  
			if hold_btc == 0:
				if (ma_fast[i] > ma_slow[i] and ma_fast[i-1] < ma_slow[i-1]): #buy btc
					hold_btc = balance[i-1] / open_prices[i] * (1.0 - fee/100.0)
					buy_price = open_prices[i]
				balance[i] = balance[i-1]
			else:
				balance[i] = hold_btc * open_prices[i] * (1.0 - fee/100.0)
				if (ma_fast[i] < ma_slow[i] and ma_fast[i-1] > ma_slow[i-1]): #sell btc
					hold_btc = 0
				change = 1 - open_prices[i] / buy_price
				if (change > take_profit or -change > stop_loss):
					hold_btc = 0
				
		return balance