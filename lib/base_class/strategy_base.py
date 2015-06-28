from abc import ABCMeta, abstractmethod

class Strategy(metaclass=ABCMeta):
	'''
	An implemented Strategy is a handcrafted tool, that details 
	how, when, and how a position should be executed 

	'''

	def __init__(self, index, trade_queue):
		self.__index = index
		self.__trade_queue = trade_queue

		self.__contract = None
		self.__live_order = None
		self.__close_order = None

		self.__strike = None
		self.__expiry = None
		self.__trigger = None

		self.__premarket_decision = False
		self.__initialized = False
		self.__threshold_set = False
		self.__opened = False
		self.__live = False
		self.__trigger_set = False
		self.__trigger_pulled = False
		self.__closed = False
		
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
