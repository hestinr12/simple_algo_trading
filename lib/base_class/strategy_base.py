from abc import ABCMeta, abstractmethod

class Strategy(metaclass=ABCMeta):
	'''
	An implemented Strategy is a handcrafted tool, that details 
	how, when, and how a position should be executed 

	'''

	def __init__(self, index, trade_queue):
		pass
		'''
		self.__premarket_decision = False
		self.__initialized = False
		self.__threshold_set = False
		self.__opened = False
		self.__live = False
		self.__closed = False
		'''
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
