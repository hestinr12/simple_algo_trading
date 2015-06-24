from lib.contract import *
from lib.base_class.position_base import Position
from ib.opt import ibConnection, Connection, message


class TwsManager():
	''' Helper class for TWS interactions '''

	def __init__(self, tws_port, tws_client_id, default_order_id):
		''' Pass in the TWS connection object and be responsible for it''' 
		self._tws = Connection.create(port=tws_port, clientId=tws_client_id)
		self.connected = False
		self._order_id = default_order_id
		self._data_router = {} # order_id:position

	def get_order_id(self):
		old_id = self._order_id
		self._order_id += 1
		return old_id

	def connect(self):
		self._tws.registerAll(self.route_message)
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

	def route_message(self, msg):
		self._data_router[msg.tickerId](msg)

	def request_market_data_stock(self, position):
		''' Open data spouts for each index past, fitted with appropriate
		data to craft TWS Contract objects (for example, see examples/contract.py)
		
		Returns: order id of the data stream

		WARNING - Data will begin pouring in immediately to any register handlers. Handlers
		should be established BEFORE this is called!!!
		'''

		if not self.connected:
			raise RuntimeError

		if not isinstance(position, Position):
			raise ValueError
			
		new_contract = None
		sec_type = position.index['info']['security_type']

		if sec_type == 'STK':
			new_contract = craft_contract_stock(index)
		else:
			raise ValueError

		order_id = self.get_order_id()
		self._tws.reqMktData(order_id, new_contract, '', False)
		self._data_contracts[order_id] = position.data_handler

		return order_id

	def request_market_data_option(self, position):
		''' Open data spouts for each index past, fitted with appropriate
		data to craft TWS Contract objects (for example, see examples/contract.py)

		Returns: order id of the data stream

		WARNING - Should be called for all positions before 'connect()'
		'''

		if not self.connected:
			raise RuntimeError

		if not isinstance(position, Position):
			raise ValueError
			
		new_contract = None
		sec_type = position.get_security_type()
		index = position.get_index_descrption()

		if sec_type == 'OPT':
			new_contract = craft_contract_option(index, strike, expiry)
		else:
			raise ValueError

		order_id = self.get_order_id()
		self._tws.reqMktData(order_id, new_contract, '', False)
		self._data_contracts[order_id] = position.data_handler

		return order_id

