from ib.ext.Contract import Contract
from ib.ext.Order import Order


def craft_contract_stock(details):
	if isinstance(details, dict):
		try:			
			newContract = Contract()
			newContract.m_symbol = details['symbol']
			newContract.m_secType = details['security_type']
			newContract.m_primaryExch = details['primary_exchange']
			newContract.m_exchange = details['exchange']
			newContract.m_currency = details['currency']
			return newContract
		except:
			raise TypeError
	else:
		raise TypeError

def craft_contract_option(details, strike, expiry):
	print(strike)
	print(expiry)
	if isinstance(details, dict):
		try:			
			newContract = Contract()
			newContract.m_symbol = details['symbol']
			newContract.m_secType = details['security_type']
			newContract.m_primaryExch = details['primary_exchange']
			newContract.m_exchange = details['exchange']
			newContract.m_currency = details['currency']
			newContract.m_multiplier = details['multiplier']
			newContract.m_right = details['right']
			newContract.m_expiry = expiry
			newContract.m_strike = strike # not sure how comfortable I am with float representation...anyway...
			return newContract
		except:
			raise TypeError
	else:
		raise TypeError


def create_order(data):
	if isinstance(data, dict):
		try:
			order = Order()
			order.m_orderType = data['type']
			order.m_totalQuantity = data['quantity']
			order.m_action = data['action']
			return order
		except:
			raise ValueError
	else:
		raise TypeError	

def compare_stock_contract(self, first, second):
	if isinstance(first, Contract) and isinstance(second, Contract):		
		try:
			assert first.m_symbol == second.m_symbol
			assert first.m_secType == second.m_secType
			assert first.m_primaryExch == second.m_primaryExch
			assert first.m_exchange == second.m_exchange
			assert first.m_currency == second.m_currency
			return True
		except:
			return False
	else:
		raise TypeError

def compare_option_contract(first, second):
	if isinstance(first, Contract) and isinstance(second, Contract):		
		try:
			print('first --> {}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(first.m_symbol, first.m_secType, first.m_primaryExch, first.m_exchange, first.m_currency, first.m_multiplier, first.m_right, first.m_expiry, first.m_strike))
			print('second --> {}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(second.m_symbol, second.m_secType, second.m_primaryExch, second.m_exchange, second.m_currency, second.m_multiplier, second.m_right, second.m_expiry, second.m_strike))
			assert first.m_symbol == second.m_symbol
			print('symbol match')
			assert first.m_secType == second.m_secType
			print('sec match')
			#assert first.m_primaryExch == second.m_primaryExch
			#assert first.m_exchange == second.m_exchange
			assert first.m_currency == second.m_currency
			print('currency match')
			assert int(first.m_multiplier) == int(second.m_multiplier)
			print('multiplier match')
			assert first.m_right == second.m_right
			print('right match')
			assert first.m_expiry == second.m_expiry
			print('expiry match')
			assert first.m_strike == second.m_strike
			print('strike match')
		except:
			return False
		return True
	else:
		raise TypeError
