import numpy as np

class Indicators:

	def __init__(self):
		pass

	def sma(self, data, window):
		n = len(data) - window + 1
		sma_array = np.zeros(n)
		sma_array[0] = sum(data[:window]) / float(window)
		for i in range(n-1):
			sma_array[i+1] = sma_array[i] + (data[i+window] - data[i])/float(window)
		return sma_array

	def ema(self, data, window):
		n = len(data)
		alpha = 2.0 / (window + 1)
		ema_array = np.zeros(n)
		ema_array[0] = data[0]
		for i in range(1, n):
			ema_array[i] = alpha * data[i] + (1.0 - alpha) * ema_array[i-1]
		return ema_array