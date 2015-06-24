

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
	def __init__(self):
		pass
		'''
		self.__position = None
		self.__threshold = None
		self.__should_open = None
'''

	def open(self):
		''' returns True is the position is now open
			else False (reasons plenty)
		'''
		raise NotImplementedError

	def data_handler(self):
		raise NotImplementedError

	def triggered(self):
		''' returns True if threshold is met
			false otherwise

			Mostly just a wrapper for __threshold
		'''
		raise NotImplementedError

	def close(self):
		raise NotImplementedError

