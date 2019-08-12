import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import talib


class IndicatorMarks():
	
	
	def __init__(self):
		pass
		
		
	def macd_marks(self, MACD):
		periods = len(MACD)
		temp = ['hold'] * periods
		for i in range(1, periods):
			if (MACD[i] > 0 and MACD[i-1] < 0):
				temp[i] = 'buy'
			elif (MACD[i] < 0 and MACD[i-1] > 0):
				temp[i] = 'sell'
		return temp
	
	
	def rsi_marks(self, rsi, buy_threshold=30, sell_threshold=70):
		periods = len(rsi)
		temp = ['hold'] * periods
		for i in range(1, periods):
			if (rsi[i] < buy_threshold):
				temp[i] = 'buy'
			elif (rsi[i] > sell_threshold):
				temp[i] = 'sell'
		return temp


class SingleInstrumentBacktest:
	
	df = None #dataframe
	price = None #open or close
	periods = None #number of periods
	balance = None #balance on current period of time
	fee = None #taker/maker fee
	stoploss = None
	takeprofit = None
	hold = 0 #current balance of an instrument
	i = 0 #current period index
	balance_on_buy = None #balance when bought to know current loss/profit
	wait = 0 #no action for "10" (e.g.) periods after stoploss/takeprofit
	use_custom_signal = None
	
	
	def __init__(self, df, initial_balance=100, fee=0.1, stoploss=0.03, takeprofit=0.05):
		self.df = df.copy()
		self.price = self.df['open'].values
		self.periods = df.shape[0]
		self.df.index = pd.RangeIndex(self.periods) #refresh index
		self.balance = np.zeros(self.periods)
		self.balance[0] = initial_balance
		self.fee = fee
		self.stoploss = stoploss
		self.takeprofit = takeprofit
		self.add_indicator_marks()
		
		
	def add_indicator_marks(self):
		im = IndicatorMarks()
		self.df['macd'] = talib.EMA(self.price, timeperiod=13) - talib.EMA(self.price, timeperiod=26)
		self.df['macd_mark'] = im.macd_marks(self.df['macd'].values)
		self.df['rsi_14'] = talib.RSI(self.price, timeperiod=14)
		self.df['rsi_14_mark'] = im.rsi_marks(self.df['rsi_14'].values, 30, 70)
	
	
	def buy_condition(self):
		#if (self.df['rsi_14_mark'][self.i] == 'buy' and self.wait == 0):
		if (self.df['custom_signal'][self.i] == 'buy' and self.wait == 0):
			return True
		if (self.wait > 0):
			self.wait -= 1
		return False
	
	
	def sell_condition(self):
		#if (self.df['rsi_14_mark'][self.i] == 'sell'):
		if (self.df['custom_signal'][self.i] == 'sell'):
			return True
		#stoploss/takeprofit
		current_trade_loss = 1.0 - self.balance[self.i] / self.balance_on_buy
		if (current_trade_loss >= self.stoploss or -1.0 * current_trade_loss >= self.takeprofit):
			self.wait = 8
			return True
		return False
	
	
	def step(self):
		if self.hold == 0:
			if (self.buy_condition() == True):
				self.hold = self.balance[self.i-1] / self.price[self.i] * (1.0 - self.fee/100.0)
				self.balance_on_buy = self.balance[self.i-1]
			self.balance[self.i] = self.balance[self.i-1]
		else:
			self.balance[self.i] = self.hold * self.price[self.i] * (1.0 - self.fee/100.0)
			if (self.sell_condition() == True):
				self.hold = 0
		
		
	def full_backtest(self, print_metrics=True, show_balance=True):
		for _ in range(1, self.periods):
			self.i += 1
			self.step()
		if print_metrics == True:
			print(self.get_metrics())
		if show_balance == True:
			self.show_balance()
		return self.balance
	
	
	def show_balance(self):
		plt.plot(range(self.periods), self.balance)
		
		
	def get_metrics(self, digits=3):
		risk_free_return = 0
		self.df['return'] = self.balance / self.balance[0]
		max_drawdown = 1.0 - min(self.df['return'].values)
		self.df['return'] = self.df['return'].pct_change(1)
		sharpe = (self.df['return'].mean() - risk_free_return) / self.df['return'].std()
		sharpe *= self.periods ** 0.5 #annualize
		#sharpe = np.mean(ret) / np.std(ret)
		return {"profit factor" : round(self.balance[self.periods-1]/self.balance[0], digits), 
				"sharpe ratio" : round(sharpe, digits),
				"max drawdown" : str(round(max_drawdown * 100, digits-2)) + "%"}