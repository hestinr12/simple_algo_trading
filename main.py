import yaml
import sched
import time
import datetime
from multiprocessing import Process, Queue
from lib.demo_strategy import SvxyStrategy



''' As offsets from midnight EST '''
# 9:28am
premarket_check = 9 * 60 * 60 + 28 * 60 
# 9:30am
market_open = 9 * 60 * 60 + 30 * 60
# 8:00pm
end_of_day = 18 * 60 *60

# TWS default settings
tws_port = 7496
tws_client_id = 1234
default_order_id = 1  # not entirely safe...

#default config
config_file = './data_config.yml'


def worker(tws_manager, trades):
	while True:
		trade = trades.get()
		if trade == None:
			break
		else:
			#Protocol - (<Contract>, <Order>)
			try:	
				contract = trade[0]
				order = trade[1]
				tws_manager.placeOrder(contract, order)
			except:
				raise RuntimeError

def main():
	''' Entry into basic market functionality '''
	
	# See examples/data_config.json for some example formats 
	try:
		config = yaml.load(open(config_file, 'r'))
	except:
		print('Config file not found')
		raise ValueError

	trader_queue = Queue()
	tws_manager = (tws_port, tws_client_id, default_order_id) 


	
	demo_pos = SvxyStrategy(config[0], trader_queue)

	'''
	Position Lifecycle:
	- decision to create
	- Created
	- initialized 
	- fed data
	- closed

	*Instructions derived from data in future...

	'''




	# This will be for the actual processes during active hours
	while True:
		break



if __name__ == '__main__':
	main()