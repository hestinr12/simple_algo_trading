
class TradingStrategy():
	'''
	This is the base class/ghetto interface for a trading strategy. The subclass
	of this base should implement these methods as appropriate in order to execute
	the stretegy.

	...isn't this why they made ABCs? Or, you know...
	'''

	def on_premarket(self, data):
		raise NotImplementedError

	def on_live_tick(self, msg):
		raise NotImplementedError
