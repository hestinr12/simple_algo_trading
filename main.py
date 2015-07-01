import yaml
import sched
from time import sleep
import datetime
from multiprocessing import Queue
from lib.option_strategy import OptionStrategy
from lib.router import TwsManager



''' As offsets from midnight EST '''
# 9:28am
premarket_check = 2 #9 * 60 * 60 + 28 * 60 
# 9:30am
market_open = 8 #9 * 60 * 60 + 30 * 60
# 8:00pm
end_of_day = 15 #18 * 60 *60

# TWS default settings
tws_port = 7496
tws_client_id = 1234
default_order_id = 150  # not entirely safe...
default_account_id = '15076'

#default config
config_file = './data_config.yml'

#@asyncio.coroutine
def trade_worker(tws_manager, trader_queue):
	while True:
		trade = yield from trader_queue.get()
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

def start():
	''' Entry into basic market functionality '''
	# See examples/data_config.json for some example formats 
	try:
		config = yaml.load(open(config_file, 'r'))
	except:
		print('Config file not found')
		raise ValueError

	print(config)

	tws_manager = TwsManager(tws_port, tws_client_id, default_order_id, default_account_id) 

	trader_queue = Queue()
	#asyncio.async(trade_worker(tws_manager, trader_queue))
	
	demo_pos = OptionStrategy(config[0], tws_manager)

	'''
	Position Lifecycle:
	- decision to create
	- Created
	- initialized 
	- fed data
	- closed

	*Instructions derived from data in future...

	'''
	###START HERE
	# The process needs to be split 
	# so that the premarket is sync
	# and the live market is async

	check = demo_pos.premarket_check()

	print(check)

	if check:
		demo_pos.initialize_order()
		tws_manager.connect()
		sleep(5)
		pieces = demo_pos.live()
		tws_manager.register_all(demo_pos.data_handler)
		sleep(5)
		while not demo_pos.is_closed():
			sleep(1)

if __name__ == '__main__':
	print('main')
	start()