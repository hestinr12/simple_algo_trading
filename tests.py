import unittest
import examples
import json
import time
import yaml

import lib.router as router
from lib.demo_strategy import SvxyStrategy



class SvxyStrategyTests(unittest.TestCase):

	def setUp(self):
		with open('./tests/test_data.yml', 'r') as fl:
			data = yaml.load(fl)['strategy']
			self.s = SvxyStrategy(data, None)

	@staticmethod
	def stub_fetch(value):
		return lambda x: value

	def stub_exception(self):
		raise Exception

	def test_premarket_check_pass(self):
		self.s.fetch_value_from_url_with_scrape_id = self.stub_fetch(5.0)
		result = self.s.premarket_check()
		print(result)
		assert result is True

	def test_premarket_check_fail(self):
		self.s.fetch_value_from_url_with_scrape_id = self.stub_fetch(2.0)
		result = self.s.premarket_check()
		assert result is False

	def test_premarket_check_exception(self):
		self.s.fetch_value_from_url_with_scrape_id = self.stub_exception
		result = self.s.premarket_check()
		assert result is False

	# TODO: needs good tests for data_handler


# these are junk...
'''
class TwsManagerTests(unittest.TestCase):
	
	def setUp(self):
		tws_port = 7496
		tws_client_id = 1234
		default_order_id = 1
		self.data_oids = []
		self.msgs = []

		self.tws_manager = router.TwsManager(tws_port, tws_client_id, default_order_id)
		self.tws_manager.connect()

		config = {}
		
		with open('./examples/data_config.json', 'r') as fl:
			config = json.load(fl)
		
		self.test_data = config['strategies']['goog']


	def tearDown(self):
		for oid in self.data_oids:
			self.tws_manager.cancel_market_data(oid)
		self.tws_manager.disconnect()

	def basicHandler(self, msg):
		self.msgs.append(msg)

	def dummy_handler(self, msg):
		return

	def error_handler(self, msg):
		assert False

	def basic_data_pull(self, handler, events=None):
		#fills self.msgs with some stuff
		if events is None:
			self.tws_manager.register_all(handler)
		else:
			for e in events:
				self.tws_manager.register(handler, e)

		oid = self.tws_manager.request_market_data_stock(self.test_data)
		self.data_oids.append(oid)
		
		time.sleep(3)

		if events is None:
			self.tws_manager.unregister_all(handler)
		else:
			for e in events:
				self.tws_manager.unregister(handler, e)

		self.tws_manager.cancel_market_data(oid)
		self.tws_manager.disconnect()

	def get_msg_types(self):
		return [m.typeName for m in self.msgs]

	def test_register_all(self):
		self.basic_data_pull(self.basicHandler)
		assert len(set(self.get_msg_types())) > 1

	def test_register(self):
		test_events = ['TickPrice']
		self.basic_data_pull(self.basicHandler, events=test_events)
		assert len(set(self.get_msg_types())) is 1

	def test_connection(self):
		raise NotImplementedError

	def test_stock_data_req(self):
		test_events = ['TickPrice']		
		self.basic_data_pull(self.basicHandler, test_events)
		assert len(self.msgs) > 0
'''

if __name__ == '__main__':
	unittest.main()
