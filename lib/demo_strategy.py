import math

import requests
from bs4 import BeautifulSoup

from lib.base_class.strategy_base import Strategy
from lib.contract import *




class SvxyStrategy(Strategy): # Scraper, Listener
	def __init__(self, index, trade_queue):
		super().__init__(index, trade_queue)	

	def is_closed(self):
		return self.__closed

	def set_index(self, new):
		'''Convenience for testing'''
		self.__index = new

	def premarket_check(self):
		try:
			info = self.__index['premarket']
			value = self.fetch_value_from_url_with_scrape_id(info)
			self.__premarket_decision = True

			if value >= 3.0: # TAG:NotGeneric
				return True
		finally:
			return False

	def initialize_order(self):
		'''
		Just getting the value necessary to finish order when live

		For example: Stocks don't need anything initialized,
		they just set their flag and return

		WE ROUND BEFORE OFFSET #TAG: NotGeneric

		Do you always round a stike?
		'''

		if self.__premarket_decision:
			try:
				info = self.__index['initialize']
				value = self.fetch_value_from_url_with_scrape_id(info)
				strike = value
				should_round = info['round_strike']
				should_offset = info['strike_offset']

				if should_round:
					round_type = info['round_type']
					rounder = None

					if round_type is 'ceil':
						rounder = math.ceil
					elif round_type is 'floor':
						rounder = math.floor
					else:
						print('Invalid round type in:\n{}'.format(self.__index))
						raise ValueError

					strike = rounder(strike)

				if should_offset:
					strike += info['strike_offset_value']

				self.__strike = strike


				date = datetime.date.today()
				today = datetime.date.today().ctime()
				offset = 4
				week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
				# expiry date is the nearest friday from now

				for day in week_days:
					if day in today:
						self.__expiry = '{}{}{}'.format(today.year, today.month, today.day+offset)
						break
					offset -= 1

				self.__initialized = True
			finally:
				pass

	def live(self):
		'''if self.__premarket_decision and not self.__initialized:
			# try again?
			return None
		'''

		if self.__premarket_decision and self.__initialized:
			'''Returns order to craft'''
			option_info = self.__index['live']['info']
			order_details = self.__index['live']['order']

			contract = create_contract_option(option_info, self.__strike, self.__expiry)
			order = create_order(order_details)

			self.__contract = contract
			self.__live_order = order

			return (contract, order)

		return None

	def data_handler(self, msg):
		if self.__trigger_pulled:
			return

		if self.__trigger_set and not self.__trigger_pulled:
			# check if we should close
			if msg.typeName is 'tickOptionComputation':
				if msg.optPrice > self.__trigger:
					self.close()
					self.__trigger_pulled = True
		else:
			if msg.typeName is 'updatePortfolio' and not self.__trigger_set and not self.__trigger_pulled:
				# if contract is my contract
				#   price paid?
				#   set trigger

				is_match = False
				try:
					is_match = compare_option_contract(self.__contract, msg.contract)
				except:
					return

				if is_match:
					#determine trigger
					trigger_info = self.__index['trigger']
					trigger_type = trigger_info['type']
					#the idea is that there would potentially be many types...
					if trigger_type is 'profit_ratio':
						modifier_ratio = trigger_info['ratio']
						self.__trigger = msg.averageCost * modifier_ratio / float(self.__contract.m_multiplier)
						self.__trigger_set = True

	def close(self):
		'''called from handler as exit'''
		trade_contract = self.__contract

		order_info = self.__index['close']['order']
		
		action = order_info['action']
		quantity = order_info['quantity']
		otype = order_info['type']

		self.__close_order = create_order(action, quantity, otype)

		#Protocol - (<Contract>, <Order>)
		self.__trade_queue.put((self.__contract, self.__close_order))
		self.__closed = True

	@staticmethod
	def fetch_value_from_url_with_scrape_id(info):
		
		url = info['url']
		scrape_id = info['scrape_id']
		inverse_modifier_from_class = None
		
		if 'inverse_modifier_from_class' in info:
			inverse_modifier_from_class = info['inverse_modifier_from_class']

		result = requests.get(url)
		assert result.status == 200
		body = result.text
		
		soup = BeautifulSoup(body)
		scraped_element = soup.find(id=scrape_id)

		# so bad...
		found_value = scraped_element.text #trim the % symbol...this is terrible logic btw
		number_set = [str(i) for i in range(0,10)] + ['.', '-']

		if found_value[-1] not in number_set:
			found_value = found_value[:-1]

		if found_value[0] not in number_set:
			found_value = found_value[1:]

		found_value = round(float(found_value), 2)

		if inverse_modifier_from_class is not None:	
			if inverse_modifier_from_class in scraped_element['class']:
				found_value *= -1

		return found_value
