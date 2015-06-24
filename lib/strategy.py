from .base_class.strategy_base import TradingStrategy


class DemoStrategy(TradingStrategy):
'''
A TradingStrategy is a collection of positions, and the actions you
can do on those positions.

This class implements the TradingStrategy base class, defining what
the details of these actions are. 

The intention is for this class to be able to automate its positions
from a collection of user definied configuration data.

For now, for simplicity, time, and base necessity, these functions will
be hard wired. 



Mitigate risk  by distributing percentages of any given position across
many servers, which will minimize error and losses. Can be autoamted :)
'''


	def premarket(self):
		pass

	def live(self):
		pass

	def close(self):
		pass