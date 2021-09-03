import unittest
import os, sys, inspect
from dfConstants import *
from afternowpricerequestdatetimeerror import AfterNowPriceRequestDateError

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from cryptofiatratecomputer import CryptoFiatRateComputer
from pricerequester import PriceRequester
from unsupportedcryptofiatpairerror import UnsupportedCryptoFiatPairError
from datetimeutil import DateTimeUtil
from dfConstants import LOCAL_TIME_ZONE

class TestCryptoFiatRateComputer(unittest.TestCase):
	def initializeComputerClasses(self, cryptoFiatCsvFileName):
		if os.name == 'posix':
			dataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/data/'
			cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName
		else:
			dataPath = 'D:\\Development\\Python\\SByield\\data\\'
			cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName

		self.cryptoFiatRateComputer = CryptoFiatRateComputer(PriceRequester(), cryptoFiatCsvFilePathName)

	def test_loadCryptoFiatCsvFile(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)
		sbEarningsDf = self.cryptoFiatRateComputer._loadCryptoFiatCsvFile(self.cryptoFiatRateComputer.cryptoFiatCsvFilePathName)

		if not PRINT:
			self.assertEqual((12, 3), sbEarningsDf.shape)

		expectedStrDataframe = \
'''   CRYPTO UNIT EXCHANGE
0    USDC  USD        1
1    CHSB  BTC   HitBTC
2     BTC  USD   Kraken
3     BTC  CHF   Kraken
4     BTC  EUR   Kraken
5     ETH  USD   Kraken
6     ETH  CHF   Kraken
7     USD  CHF   CCCAGG
8     USD  EUR   CCCAGG
9     CHF  USD   CCCAGG
10    EUR  USD   CCCAGG
11    BNB  CHF   CCCAGG'''

		if PRINT:
			print(sbEarningsDf)
		else:
			self.assertEqual(expectedStrDataframe, sbEarningsDf.to_string())

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

	def test_getIntermediateExchangeRateRequests_USDC_CHF(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'USDC'
		fiat = 'CHF'

		actualIntermediateExchangeRateRequestLst = self.cryptoFiatRateComputer._getIntermediateExchangeRateRequests(crypto, fiat)

		expectedIntermediateExchangeRateRequestLst = [['USDC', 'USD', '1'], ['USD', 'CHF', 'CCCAGG']]

		if PRINT:
			print(actualIntermediateExchangeRateRequestLst)
		else:
			self.assertEqual(expectedIntermediateExchangeRateRequestLst, actualIntermediateExchangeRateRequestLst)

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

	def test_getIntermediateExchangeRateRequests_CHSB_USD(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		fiat = 'USD'

		actualIntermediateExchangeRateRequestLst = self.cryptoFiatRateComputer._getIntermediateExchangeRateRequests(crypto, fiat)

		expectedIntermediateExchangeRateRequestLst = [['CHSB', 'BTC', 'HitBTC'], ['BTC', 'USD', 'Kraken']]

		if PRINT:
			print(actualIntermediateExchangeRateRequestLst)
		else:
			self.assertEqual(expectedIntermediateExchangeRateRequestLst, actualIntermediateExchangeRateRequestLst)

	def test_getIntermediateExchangeRateRequestsUnsupportedCryptoFiatPair(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'ETH'
		fiat = 'YEN'

		actualIntermediateExchangeRateRequestLst = self.cryptoFiatRateComputer._getIntermediateExchangeRateRequests(crypto, fiat)

		expectedIntermediateExchangeRateRequestLst = []

		if PRINT:
			print(actualIntermediateExchangeRateRequestLst)
		else:
			self.assertEqual(expectedIntermediateExchangeRateRequestLst, actualIntermediateExchangeRateRequestLst)

	def testComputeCryptoFiatRate_current_ETH_USD(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'ETH'
		fiat = 'USD'
		exchange = 'Kraken'
		priceRequester = PriceRequester()

		actualCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat)
		resultData = priceRequester.getCurrentPrice(crypto, fiat, exchange)
		expectedCryptoFiatRate = resultData.getValue(resultData.RESULT_KEY_PRICE)

		if PRINT:
			print(actualCryptoFiatRate)
		else:
			self.assertAlmostEqual(expectedCryptoFiatRate, actualCryptoFiatRate, 1)

	def testComputeCryptoFiatRate_current_CHSB_USD(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		unit = 'BTC'
		fiat = 'USD'
		exchange1 = 'HitBTC'
		exchange2 = 'Kraken'
		priceRequester = PriceRequester()

		actualCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat)

		resultData = priceRequester.getCurrentPrice(crypto, unit, exchange1)
		cryptoUnitRate = resultData.getValue(resultData.RESULT_KEY_PRICE)
		resultData = priceRequester.getCurrentPrice(unit, fiat, exchange2)
		unitFiatRate = resultData.getValue(resultData.RESULT_KEY_PRICE)
		expectedCryptoFiatRate = cryptoUnitRate * unitFiatRate

		if PRINT:
			print(actualCryptoFiatRate)
		else:
			self.assertAlmostEqual(expectedCryptoFiatRate, actualCryptoFiatRate, 3)

	def testComputeCryptoFiatRate_historical_CHSB_USD(self):
		'''
		Test obtaining historical rate for a date more than 7 days before.
		'''
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		fiat = 'USD'
		dateStr = '2021-01-01'

		histoCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat, dateStr)

		if PRINT:
			print(histoCryptoFiatRate)
		else:
			self.assertAlmostEqual(0.260474254, histoCryptoFiatRate, 3)

	def testComputeCryptoFiatRate_historical_USD_CHF(self):
		'''
		Test obtaining historical rate for a date more than 7 days before.
		'''
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'USD'
		fiat = 'CHF'
		dateStr = '2021-01-01'

		histoCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat, dateStr)

		if PRINT:
			print(histoCryptoFiatRate)
		else:
			self.assertAlmostEqual(0.8906, histoCryptoFiatRate, 3)

	def testComputeCryptoFiatRate_historical_1_day_before_CHSB_USD(self):
		'''
		Ensuring that getting historical rate for a one day ago date does work too.
		'''
		PRINT = False

		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		oneDaysBeforeArrowDate = now.shift(days=-1).date()

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		fiat = 'USD'
		dateStr = str(oneDaysBeforeArrowDate)

		histoCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat, dateStr)

		if PRINT:
			print(histoCryptoFiatRate)
		else:
			self.assertTrue(isinstance(histoCryptoFiatRate, float))

	def testComputeCryptoFiatRate_historical_1_day_before_USD_CHF(self):
		'''
		Ensuring that getting historical rate for a one day ago date does work too.
		'''
		PRINT = False

		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		oneDaysBeforeArrowDate = now.shift(days=-1).date()

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'USD'
		fiat = 'CHF'
		dateStr = str(oneDaysBeforeArrowDate)

		histoCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat, dateStr)

		if PRINT:
			print(histoCryptoFiatRate)
		else:
			self.assertTrue(isinstance(histoCryptoFiatRate, float))

	def testComputeCryptoFiatRate_historical_ETH_USD(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'ETH'
		fiat = 'USD'
		dateStr = '2021-01-01'

		histoCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat, dateStr)

		if PRINT:
			print(histoCryptoFiatRate)
		else:
			self.assertAlmostEqual(730.85, histoCryptoFiatRate, 3)

	def testComputeCryptoFiatRate_current_USDC_CHF(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'USDC'
		unit = 'USD'
		fiat = 'CHF'
		exchange2 = 'CCCAGG'
		priceRequester = PriceRequester()

		actualCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat)
		resultData = priceRequester.getCurrentPrice(unit, fiat, exchange2)
		unitFiatRate = resultData.getValue(resultData.RESULT_KEY_PRICE)
		expectedCryptoFiatRate = unitFiatRate

		if PRINT:
			print(actualCryptoFiatRate)
		else:
			self.assertAlmostEqual(expectedCryptoFiatRate, actualCryptoFiatRate, 3)

	def testComputeCryptoFiatRate_current_USDC_USD(self):
		PRINT = False

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'USDC'
		fiat = 'USD'

		actualCryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat)
		expectedCryptoFiatRate = 1

		if PRINT:
			print(actualCryptoFiatRate)
		else:
			self.assertEqual(expectedCryptoFiatRate, actualCryptoFiatRate)

	def testComputeCryptoFiatRate_current_unsupported_cryptoFiatPair(self):
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		fiat = 'YEN'

		with self.assertRaises(UnsupportedCryptoFiatPairError) as e:
			self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat)

		self.assertEqual(
			'{}/{} pair not supported. Add adequate information to {} and retry.'.format(crypto, fiat, self.cryptoFiatRateComputer.cryptoFiatCsvFilePathName), e.exception.message)

	def testComputeCryptoFiatRate_historical_unsupported_cryptoFiatPair(self):
		'''
		Ensuring that getting historical rate for a one day ago for an unsupported crypto
		fiat pair raises the expected exception.
		'''
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		fiat = 'YEN'
		dateStr = '2021-01-01'

		with self.assertRaises(UnsupportedCryptoFiatPairError) as e:
			self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat, dateStr)

		self.assertEqual(
			'{}/{} pair not supported. Add adequate information to {} and retry.'.format(crypto, fiat, self.cryptoFiatRateComputer.cryptoFiatCsvFilePathName), e.exception.message)

	def testComputeCryptoFiatRate_requestDateAfterNow(self):
		'''
		Ensuring that asking a rate for a date in the future raises the expected
		exception.
		'''
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		fiat = 'EUR'
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		oneDayAfterNow = now.shift(days=1)
		oneDayAfterNowDateStr = oneDayAfterNow.format(DATE_FORMAT)

		with self.assertRaises(AfterNowPriceRequestDateError) as e:
			self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat, oneDayAfterNowDateStr)

		self.assertEqual(
			'Price request date {} is after now, which is not acceptable !'.format(oneDayAfterNowDateStr), e.exception.message)

	def testComputeCryptoFiatRate_historical_1_day_before_unsupported_cryptoFiatPair(self):
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		oneDaysBeforeArrowDate = now.shift(days=-1).date()

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		self.initializeComputerClasses(cryptoFiatCsvFileName)

		crypto = 'CHSB'
		fiat = 'YEN'
		dateStr = str(oneDaysBeforeArrowDate)

		with self.assertRaises(UnsupportedCryptoFiatPairError) as e:
			self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat, dateStr)

		self.assertEqual(
			'{}/{} pair not supported. Add adequate information to {} and retry.'.format(crypto, fiat, self.cryptoFiatRateComputer.cryptoFiatCsvFilePathName), e.exception.message)

if __name__ == '__main__':
	if os.name == 'posix':
		unittest.main()
	else:	
		tst = TestCryptoFiatRateComputer()
		tst.testComputeCryptoFiatRate_historical_1_day_before_USD_CHF()
