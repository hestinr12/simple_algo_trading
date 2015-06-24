from lib.contract import *
from ib.opt import ibConnection, Connection, message


class TwsManager():
	''' Helper class for TWS interactions '''

	def __init__(self, tws_port, tws_client_id, default_order_id):
		''' Pass in the TWS connection object and be responsible for it''' 
		self._tws = Connection.create(port=tws_port, clientId=tws_client_id)
		self.connected = False
		self._order_id = default_order_id
		self._data_contracts = [] # order_ids associated with data requests

	def get_order_id(self):
		old_id = self._order_id
		self._order_id += 1
		return old_id

	def connect(self):
		self._tws.connect()
		self.connected = True

	def disconnect(self):
		self._tws.disconnect()
		self.connected = False
		
	def register_all(self, handler):
		''' Wrapper for TWS Connection handler registration '''
		self._tws.registerAll(handler)

	def unregister_all(self, handler):
		self._tws.unregisterAll(handler)

	def register(self, handler, event):
		''' Wrapper for TWS Connection handler registration '''
		self._tws.register(handler, event)

	def unregister(self, handler, event):
		self._tws.register(handler, event)

	def cancel_market_data(self, order_id):
		self._tws.cancelMktData(order_id)

	def request_market_data_stock(self, index):
		''' Open data spouts for each index past, fitted with appropriate
		data to craft TWS Contract objects (for example, see examples/contract.py)

		Expects 'index' to be a correctly formatted dict...see examples/data_config.json

		Returns: order id of the data stream

		WARNING - Data will begin pouring in immediately to any register handlers. Handlers
		should be established BEFORE this is called!!!
		'''

		if not self.connected:
			raise RuntimeError
			
		new_contract = None
		sec_type = index['info']['security_type']

		if sec_type == 'STK':
			new_contract = craft_contract_stock(index)
		else:
			raise ValueError

		order_id = self.get_order_id()
		self._tws.reqMktData(order_id, new_contract, '', False)
		self._data_contracts.append(order_id)

		return order_id




