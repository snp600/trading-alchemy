import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns;
sns.set()

class Viewer:

	def __init__(self):
		pass
	
	def joint_distribution(self, x, y, normalized=True, percents=True):

		def get_index(value, a = 2.0, b = 5.0):
			index = 2
			if value > a:
				index = (4 if value > b else 3)
			elif value < -a:
				index = (0 if value < -b else 1)
			return index

		digits = 2
		res = np.zeros((5,5))
		for k in range(len(x)):
			i = get_index(x[k])
			j = get_index(y[k])
			res[i,j] += 1
		if normalized:
			res /= len(x)
			digits = 3
		if percents:
			res *= 100
			digits = 1
		return res.round(digits)


	def joint_distribution_view(self, cur_1, cur_2, 
		normalized=True, percents=True, 
		title=None, xlabel=None, ylabel=None):

		mm = self.joint_distribution(cur_1, cur_2, normalized=normalized, percents=percents)
		ax = sns.heatmap(mm, annot=True, square=True, fmt='g', cmap='cool')
		ax.xaxis.tick_top()
		plt.text(0.5, -0.1, title,
			horizontalalignment='center',
			fontsize=15,
			transform = ax.transAxes,
			fontweight='bold')
		plt.text(0.5, 1.1, xlabel, horizontalalignment='center', fontsize=12, 
			transform = ax.transAxes, fontweight='bold')
		plt.text(-0.25, 0.487, ylabel, horizontalalignment='center', fontsize=12, 
			transform = ax.transAxes, fontweight='bold')

		ax.xaxis.set_ticks_position('none')
		ax.set_xticklabels(["fall (>5%)", "down (2-5%)","flat", "up (2-5%)", "surge (>5%)"], size=10)
		ax.set_yticklabels(["fall (>5%)", "down (2-5%)","flat", "up (2-5%)", "surge (>5%)"], rotation=0, size=10)
		return ax


	def correlate(self, x, y):
		jd = self.joint_distribution(x, y)
		diag1 = sum(np.diag(jd))
		diag3 = sum(np.diag(jd)) + sum(np.diag(jd, k=1)) + sum(np.diag(jd, k=-1))
		return (round(diag1, 1), round(diag3, 1))