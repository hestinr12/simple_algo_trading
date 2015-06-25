import math

import requests
from bs4 import BeautifulSoup

from lib.base_class.position_base import Position
from lib.contract import *




class SvxyCallPosition(Position): # Scraper, Listener
	def __init__(self, index):
		self.__index = index

		self.__strike = None
		self.__expiry = None

		self.__premarket_decision = False
		self.__initialized = False
		self.__threshold_set = False
		self.__opened = False
		self.__live = False
		self.__executed_open = False
		self.__closed = False		

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

				### START HERE ###
				# Needs to calc expiry,
				# Set expiry
				# then set flag and return
				##################

				self.__initialized = True
			finally:
				pass


	def live(self):
		raise NotImplementedError

	def acquire_target(self):
		'''blocks live until we have target'''
		raise NotImplementedError

	def close(self):
		raise NotImplementedError

	def data_handler(self, msg):
		raise NotImplementedError




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
