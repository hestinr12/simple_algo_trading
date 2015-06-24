
class TradingStrategy():
	'''
	This is the base class/ghetto interface for a trading strategy. The subclass
	of this base should implement these methods as appropriate in order to execute
	the stretegy.

	...isn't this why they made ABCs? Or, you know...
	'''

	def fetch(self):
		raise NotImplementedError

	def live(self):
		raise NotImplementedError

	def end(self):
		raise NotImplementedError
