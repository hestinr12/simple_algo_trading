

class Position():
	'''

	The process of initialization is:
		- Collect data of interest*
		- For each data point
			- is my threshold met?
				- Execute
			- else
				- Pass

	*Should be noted that we can short circuit this process by
	collecting data in interation with each interested value


	An implemented position is a handcrafted tool, that details 
	how it should retrieve its premarket data and what data it
	wants from the data feed. The connection objet should be 

	Is a threshhold always bounded about 0? aka - can it be 
	measured in "differential from 0"
	'''

	def __init__(self, index):
		pass
		'''
		self.__premarket_decision = False
		self.__initialized = False
		self.__threshold_set = False
		self.__opened = False
		self.__live = False
		self.__closed = False
		'''

	def premarket_check(self):
		raise NotImplementedError

	def initialize_order(self):
		raise NotImplementedError

	def live(self):
		raise NotImplementedError

	def acquire_target(self):
		raise NotImplementedError

	def close(self):
		raise NotImplementedError

	def data_handler(self, msg):
		raise NotImplementedError

