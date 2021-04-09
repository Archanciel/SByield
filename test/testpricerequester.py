import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pricerequester import PriceRequester
from resultdata import ResultData


class TestPriceRequester(unittest.TestCase):
	def setUp(self):
		if os.name == 'posix':
			FILE_PATH = '/sdcard/cryptopricer.ini'
		else:
			FILE_PATH = 'c:\\temp\\cryptopricer.ini'

		self.priceRequester = PriceRequester()


	def testGetCurrentPrice(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'CCCAGG'

		resultData = self.priceRequester.getCurrentPrice(crypto, unit, exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))

	def testGetCurrentPriceWrongExchange(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'unknown'

		resultData = self.priceRequester.getCurrentPrice(crypto, unit, exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - unknown market does not exist for this coin pair (BTC/USD).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetCurrentPriceWrongCrypto(self):
		crypto = 'BBB'
		unit = 'USD'
		exchange = 'all'

		resultData = self.priceRequester.getCurrentPrice(crypto, unit, exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
		self.assertEqual("PROVIDER ERROR - all market does not exist for this coin pair (BBB/USD).", resultData.getValue(resultData.RESULT_KEY_ERROR_MSG))
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetCurrentPriceWrongPair(self):
		crypto = 'BTA'
		unit = 'CHF'
		exchange = 'all'

		resultData = self.priceRequester.getCurrentPrice(crypto, unit, exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - all market does not exist for this coin pair (BTA/CHF).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetCurrentPriceWrongUnit(self):
		crypto = 'BTC'
		unit = 'USL'
		exchange = 'all'

		resultData = self.priceRequester.getCurrentPrice(crypto, unit, exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - all market does not exist for this coin pair (BTC/USL).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


if __name__ == '__main__':
	unittest.main()
