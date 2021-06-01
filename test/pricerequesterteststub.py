import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from pricerequester import PriceRequester
from resultdata import ResultData
from ratedictionary import RateDictionary


if os.name == 'posix':
	RATE_DIC_FILE_PATH = '/sdcard/rateDic.txt'
else:
	RATE_DIC_FILE_PATH = 'D:\\Development\\Python\\SByield\\test\\rateDicSavedData.txt'

MINUTE_PRICE_DAY_NUMBER_LIMIT = 7   # if the request date is older than current time - this value,
									# the price returned is a day close price, not a minute price !

IDX_DATA_ENTRY_TO = 1

class PriceRequesterTestStub(PriceRequester):
	'''
	This class is used for testing purposes only to solve the fact that sometimes requesting
	a fiat/fiat (USD/CHF for example) historical price does not return a correct price.
	'''

	def __init__(self):
		super(PriceRequesterTestStub, self).__init__()
		self.rateDic = RateDictionary()

	# NO INTEREST TO CACHE RATES FOR DATE TIMES WHICH CHANGES AT EACH UNIT TEST
	# EXECUTION !
	#
	# def _getHistoMinutePriceAtUTCTimeStamp(self, crypto, unit, timeStampUTC, exchange, resultData):
	# 	rate = self.rateDic.getRate(crypto, unit, timeStampUTC, exchange)
	#
	# 	if not rate:
	# 		# the rate is not cached and is queried for the first time
	# 		resultData = super()._getHistoMinutePriceAtUTCTimeStamp(crypto, unit, timeStampUTC, exchange, resultData)
	# 		rate = resultData.getValue(resultData.RESULT_KEY_PRICE)
	#
	# 		if rate:
	# 			# no exception indicating that the coin pair is not supported was raised
	# 			self.rateDic.saveRate(crypto, unit, timeStampUTC, exchange, rate)
	# 	else:
	# 		resultData.setValue(ResultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
	# 		resultData.setValue(ResultData.RESULT_KEY_PRICE_TIME_STAMP, timeStampUTC)
	# 		resultData.setValue(ResultData.RESULT_KEY_PRICE, rate)
	#
	# 	return resultData

	def _getHistoDayPriceAtUTCTimeStamp(self, crypto, unit, timeStampUTC, exchange, resultData):
		# fed up with this fucking provider which regurlarly return an invalid value of 1.06
		# for USD/CHF on CCCAGG on 12/9/17 !
		if crypto == 'USD' and unit == 'CHF' and exchange == 'CCCAGG' and timeStampUTC == 1536710400:
			rate = 0.9728
			resultData.setValue(resultData.RESULT_KEY_PRICE, rate)
		elif crypto == 'USD' and unit == 'CHF' and exchange == 'CCCAGG' and timeStampUTC == 1505174400:
			rate = 1.001
			resultData.setValue(resultData.RESULT_KEY_PRICE, rate)
		elif crypto == 'USD' and unit == 'EUR' and exchange == 'CCCAGG' and timeStampUTC == 1505174400:
			rate = 0.8346
			resultData.setValue(resultData.RESULT_KEY_PRICE, rate)
		else:
			rate = self.rateDic.getRate(crypto, unit, timeStampUTC, exchange)

		if not rate:
			# the rate is not cached and is queried for the first time
			resultData = super()._getHistoDayPriceAtUTCTimeStamp(crypto, unit, timeStampUTC, exchange, resultData)
			rate = resultData.getValue(resultData.RESULT_KEY_PRICE)

			if rate != None and rate > 0:
				# no exception indicating that the coin pair is not supported was raised
				self.rateDic.saveRate(crypto, unit, timeStampUTC, exchange, rate)
		else:
			resultData.setValue(ResultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
			resultData.setValue(ResultData.RESULT_KEY_PRICE_TIME_STAMP, timeStampUTC)
			resultData.setValue(ResultData.RESULT_KEY_PRICE, rate)

		return resultData

	def getCurrentPrice(self,
						crypto,
						unit,
						exchange):
		resultData = ResultData()

		if crypto == 'CHSB' and unit == 'BTC':
			rate = 0.000015 # causes CHSB/CHF to be 1.5
		elif crypto == 'BTC' and unit == 'CHF':
			rate = 100000 # causes CHSB/CHF to be 1.5
		elif crypto == 'BTC' and unit == 'USD':
			rate = 113333.3333  # causes CHSB/USD to be 1.7
		elif crypto == 'BTC' and unit == 'EUR':
			rate = 44250  # causes CHSB/EUR to be 0.66 since CHSB/BTC is set to 0.000015, a value which is not conform to reality but causes CHSB/CHF to be 1.5 !
		elif crypto == 'USD' and unit == 'CHF':
			rate = 0.9105
		elif crypto == 'CHF' and unit == 'USD':
			rate = 1 / 0.9105
		elif crypto == 'USD' and unit == 'EUR':
			rate = 0.8
		elif crypto == 'USDC' and unit == 'CHF':
			rate = 0.9105
		elif crypto == 'ETH' and unit == 'CHF':
			rate = 4000
		elif crypto == 'ETH' and unit == 'USD':
			rate = 4400 # coherent with USD/CHF value of 0.90909090
		else:
			raise ValueError('Crypto {}/{} pair not supported by PriceRequesterTestStub. Complete PriceRequesterTestStub.getCurrentPrice() method and retry !'.format(crypto, unit))

		resultData.setValue(resultData.RESULT_KEY_PRICE, rate)

		return resultData

if __name__ == '__main__':
	pr = PriceRequesterTestStub()
	rd = pr.getCurrentPrice('CHSB', 'CHF','CCAGG')
	print(rd.getValue(rd.RESULT_KEY_PRICE))

