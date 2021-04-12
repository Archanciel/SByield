import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from cryptofiatratecomputer import CryptoFiatRateComputer
from pricerequester import PriceRequester
from unsupportedcryptofiatpairerror import UnsupportedCryptoFiatPairError

class TestCryptoFiatRateComputer(unittest.TestCase):
	def initializeComputerClasses(self, cryptoFiatCsvFileName):
		if os.name == 'posix':
			dataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/data/'
			cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName
		else:
			dataPath = 'D:\\Development\\Python\\SByield\\data\\'
			cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName

		self.cryptoFiatRateComputer = CryptoFiatRateComputer(cryptoFiatCsvFilePathName)

	def test_loadCryptoFiatCsvFile(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)
		sbEarningsDf = self.cryptoFiatRateComputer._loadCryptoFiatCsvFile()

		if not PRINT:
			self.assertEqual((6, 3), sbEarningsDf.shape)

		expectedStrDataframe = \
'  CRYPTO UNIT EXCHANGE' + \
'''
0   USDC  USD        1
1   CHSB  BTC   HitBTC
2    BTC  USD   Kraken
3    BTC  CHF   Kraken
4    ETH  USD   Kraken
5    ETH  CHF   Kraken'''

		if PRINT:
			print(sbEarningsDf)
		else:
			self.assertEqual(expectedStrDataframe, sbEarningsDf.to_string())

	def test_getIntermediateExchangeRateRequests_CHSB_CHF(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		fiat = 'CHF'

		actualIntermediateExchangeRateRequestLst = self.cryptoFiatRateComputer._getIntermediateExchangeRateRequests(crypto, fiat)

		expectedIntermediateExchangeRateRequestLst = [['CHSB', 'BTC', 'HitBTC'], ['BTC', 'CHF', 'Kraken']]

		if PRINT:
			print(actualIntermediateExchangeRateRequestLst)
		else:
			self.assertEqual(expectedIntermediateExchangeRateRequestLst, actualIntermediateExchangeRateRequestLst)

	def test_getIntermediateExchangeRateRequests_ETH_CHF(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'ETH'
		fiat = 'CHF'

		actualIntermediateExchangeRateRequestLst = self.cryptoFiatRateComputer._getIntermediateExchangeRateRequests(crypto, fiat)

		expectedIntermediateExchangeRateRequestLst = [['ETH', 'CHF', 'Kraken']]

		if PRINT:
			print(actualIntermediateExchangeRateRequestLst)
		else:
			self.assertEqual(expectedIntermediateExchangeRateRequestLst, actualIntermediateExchangeRateRequestLst)

	def test_getIntermediateExchangeRateRequestsUnsupportedCryptoFiatPair(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'ETH'
		fiat = 'EUR'

		actualIntermediateExchangeRateRequestLst = self.cryptoFiatRateComputer._getIntermediateExchangeRateRequests(crypto, fiat)

		expectedIntermediateExchangeRateRequestLst = []

		if PRINT:
			print(actualIntermediateExchangeRateRequestLst)
		else:
			self.assertEqual(expectedIntermediateExchangeRateRequestLst, actualIntermediateExchangeRateRequestLst)

	def testComputeCryptoFiatCurrentRate_ETH_USD(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'ETH'
		fiat = 'USD'
		exchange = 'Kraken'
		priceRequester = PriceRequester()

		actualCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatCurrentRate(crypto, fiat)
		resultData = priceRequester.getCurrentPrice(crypto, fiat, exchange)
		expectedCryptoFiatRate = resultData.getValue(resultData.RESULT_KEY_PRICE)

		if PRINT:
			print(actualCryptoFiatRate)
		else:
			self.assertEqual(expectedCryptoFiatRate, actualCryptoFiatRate)

	def testComputeCryptoFiatCurrentRate_CHSB_USD(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		unit = 'BTC'
		fiat = 'USD'
		exchange1 = 'HitBTC'
		exchange2 = 'Kraken'
		priceRequester = PriceRequester()

		actualCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatCurrentRate(crypto, fiat)

		resultData = priceRequester.getCurrentPrice(crypto, unit, exchange1)
		cryptoUnitRate = resultData.getValue(resultData.RESULT_KEY_PRICE)
		resultData = priceRequester.getCurrentPrice(unit, fiat, exchange2)
		unitFiatRate = resultData.getValue(resultData.RESULT_KEY_PRICE)
		expectedCryptoFiatRate = cryptoUnitRate * unitFiatRate

		if PRINT:
			print(actualCryptoFiatRate)
		else:
			self.assertEqual(expectedCryptoFiatRate, actualCryptoFiatRate)

	def testComputeCryptoFiatCurrentRate_unsupported_cryptoFiatPair(self):
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		fiat = 'EUR'

		with self.assertRaises(UnsupportedCryptoFiatPairError) as e:
			self.cryptoFiatRateComputer.computeCryptoFiatCurrentRate(crypto, fiat)

		self.assertEqual(
			'{}/{} pair not supported. Add adequate information to {} and retry.'.format(crypto, fiat, self.cryptoFiatRateComputer.cryptoFiatCsvFilePathName), e.exception.message)

if __name__ == '__main__':
	#unittest.main()
	tst = TestCryptoFiatRateComputer()
	tst.test_getIntermediateExchangeRateRequestsUnsupportedCryptoFiatPair_()
