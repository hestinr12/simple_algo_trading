from ib.ext.Contract import Contract



def craft_contract_stock(data):
	if isinstance(data, dict):
		try:
			details = data['info']
			
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

def craft_contract_option(data, strike, expiry):
	if isinstance(data, dict):
		try:
			details = data['info']
			
			newContract = Contract()
			newContract.m_symbol = details['symbol']
			newContract.m_secType = details['security_type']
			newContract.m_primaryExch = details['primary_exchange']
			newContract.m_exchange = details['exchange']
			newContract.m_currency = details['currency']
			newContract.m_multiplier = details['multiplier']
			newContract.m_right = details['right']
			newContract.m_expiry = expiry
			newOptContract.m_strike = strike # not sure how comfortable I am with float representation...anyway...
			return newContract
		except:
			raise TypeError
	else:
		raise TypeError