from contract import *


class TwsManager():
	''' Helper class for TWS interactions '''

	def __init__(self, tws, default_order_id):
		''' Pass in the TWS connection object and be responsible for it''' 
		self._tws = Connection.create(port=tws_port, clientId=tws_client_id)
		self._order_id = default_order_id
		self._data_contracts = [] # order_ids associated with data requests

	def register_all(self, handler):
		''' Wrapper for TWS Connection handler registration '''
		self._tws.registerAll(handler)

	def register(self, handler, event):
		''' Wrapper for TWS Connection handler registration '''
		self._tws.register(handler, event)

	def request_market_data_stock(self, indicies):
		''' Open data spouts for each index past, fitted with appropriate
		data to craft TWS Contract objects (for example, see examples/contract.py)

		Expects 'indicies' to be a correctly formatted dict...see examples/data_config.json

		WARNING - Data will begin pouring in immediately to any register handlers. Handlers
		should be established BEFORE this is called!!!
		'''
		raise NotImplementedError

		for ind in indicies:
			
			new_contract = None
			sec_type = ind['info']['security_type']

			if sec_type is 'STK':
				new_contract = craft_contract_stock(ind)
			else:
				raise ValueError

			self._tws.reqMktData(self._order_id, new_contract, '', False)
			self._data_contracts.append(self._order_id)
			self._order_id += 1





