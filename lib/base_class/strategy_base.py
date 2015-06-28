from abc import ABCMeta, abstractmethod

class Strategy(metaclass=ABCMeta):
	'''
	An implemented Strategy is a handcrafted tool, that details 
	how, when, and how a position should be executed 

	'''

	def __init__(self):
		self._premarket_decision = False
		self._initialized = False
		self._threshold_set = False
		self._opened = False
		self._live = False
		self._trigger_set = False
		self._trigger_pulled = False
		self._closed = False
		
	@abstractmethod
	def premarket_check(self):
		raise NotImplementedError

	@abstractmethod
	def initialize_order(self):
		raise NotImplementedError

	@abstractmethod
	def live(self):
		raise NotImplementedError

	@abstractmethod
	def data_handler(self, msg):
		raise NotImplementedError

	@abstractmethod
	def close(self):
		raise NotImplementedError
