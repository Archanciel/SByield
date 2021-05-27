import os
import pandas as pd

from dfConstants import LOCAL_TIME_ZONE, DATE_FORMAT
from pandasdatacomputer import PandasDataComputer
from resultdata import ResultData
from pricerequester import PriceRequester
from datetimeutil import DateTimeUtil
from unsupportedcryptofiatpairerror import UnsupportedCryptoFiatPairError


class CryptoFiatRateComputer(PandasDataComputer):
	def __init__(self,
				 priceRequester,
				 cryptoFiatCsvFilePathName):
		"""
		Currently, the configMgr is not used. Constants are used in place.
		
		:param cryptoFiatCsvFilePathName:
		"""
		super().__init__()
		self.cryptoFiatCsvFilePathName = cryptoFiatCsvFilePathName
		self.cryptoFiatDf = self._loadCryptoFiatCsvFile(cryptoFiatCsvFilePathName)
		self.priceRequester = priceRequester

	def _loadCryptoFiatCsvFile(self, cryptoFiatCsvFilePathName):
		"""
		Creates a Pandas data frame from the crypto fiat exchange csv file.

		:return: crypto fiat data frame
		"""
		cryptoFiatSheetSkipRows, \
		_ = self._determineDepositSheetSkipRowsAndCrypto(cryptoFiatCsvFilePathName,
														 'CRYPTO')

		cryptoFiatDf = pd.read_csv(cryptoFiatCsvFilePathName,
								   skiprows=cryptoFiatSheetSkipRows)
		
		return cryptoFiatDf

	def _getIntermediateExchangeRateRequests(self, crypto, fiat):
		intermediateExchangeRateRequestLst = []

		unitFiatDf = self.cryptoFiatDf.loc[self.cryptoFiatDf['UNIT'] == fiat]

		cryptoUnitDf = self.cryptoFiatDf.loc[(self.cryptoFiatDf['CRYPTO'] == crypto) & (self.cryptoFiatDf['UNIT'] == fiat)]

		if not cryptoUnitDf.empty:
			# means the cryptoFiatDf contains a row for the crypto/fiat pair, like
			# ETH/CHF for example. In this case, [['ETH', 'CHF', 'Kraken']]
			# will be returned.
			intermediateExchangeRateRequestLst.append(
				[cryptoUnitDf.iloc[0]['CRYPTO'], cryptoUnitDf.iloc[0]['UNIT'], cryptoUnitDf.iloc[0]['EXCHANGE']])
			return intermediateExchangeRateRequestLst

		# here, we are handling a crypto/fiat pair which is not directly available
		# in the cryptoFiatDf, like CHSB/CHF for example. In this case,
		# [['CHSB', 'BTC', 'HitBTC'], ['BTC', 'CHF', 'Kraken']] will be returned.
		for index, row in unitFiatDf.iterrows():
			cryptoUnitDf = self.cryptoFiatDf.loc[(self.cryptoFiatDf['CRYPTO'] == crypto) & (self.cryptoFiatDf['UNIT'] == row['CRYPTO'])]
			if not cryptoUnitDf.empty:
				unitFiatDf = unitFiatDf.loc[(unitFiatDf['CRYPTO'] == cryptoUnitDf.iloc[0]['UNIT'])]
				intermediateExchangeRateRequestLst.append(
					[cryptoUnitDf.iloc[0]['CRYPTO'], cryptoUnitDf.iloc[0]['UNIT'], cryptoUnitDf.iloc[0]['EXCHANGE']])
				intermediateExchangeRateRequestLst.append([unitFiatDf.iloc[0]['CRYPTO'], unitFiatDf.iloc[0]['UNIT'], unitFiatDf.iloc[0]['EXCHANGE']])

		return intermediateExchangeRateRequestLst

	def computeCryptoFiatRate(self,
							  crypto,
							  fiat,
							  dateStr=None):
		'''

		:raise UnsupportedCryptoFiatPairError in case the crypto fiat exchange
		 	   CSV file does not have the necessary information to compute the
		 	   crypto/fiat pair rate.

		@param crypto:
		@param fiat:
		@param dateStr: if not None, means that an historical rate must be
						obtained. Otherwise, a current rate is returned.

		:return crypto/fiat pair current rate
		'''
		intermediateExchangeRateRequestLst = self._getIntermediateExchangeRateRequests(crypto, fiat)

		rateRequestNumber = len(intermediateExchangeRateRequestLst)

		if rateRequestNumber == 1:
			exchange = intermediateExchangeRateRequestLst[0][2]
			if exchange == '1':
				# the case if the crypto/fiat pair is a stablecoin/ coin fiat pair,
				# like USDC/USD !
				return 1
			else:
				resultData = self._getCurrentOrHistoRate(crypto, dateStr, exchange, fiat)

				if not self._checkIfProblem(resultData):
					return resultData.getValue(resultData.RESULT_KEY_PRICE)
		elif rateRequestNumber == 2:
				crypto = intermediateExchangeRateRequestLst[0][0]
				unit = intermediateExchangeRateRequestLst[0][1]
				exchange = intermediateExchangeRateRequestLst[0][2]
				if exchange == '1':
					resultData = ResultData()
					resultData.setValue(resultData.RESULT_KEY_PRICE, 1)
				else:
					resultData = self._getCurrentOrHistoRate(crypto, dateStr, exchange, unit)
				if not self._checkIfProblem(resultData):
					firstRate = resultData.getValue(resultData.RESULT_KEY_PRICE)
					crypto = intermediateExchangeRateRequestLst[1][0]
					fiat = intermediateExchangeRateRequestLst[1][1]
					exchange = intermediateExchangeRateRequestLst[1][2]
					resultData = self._getCurrentOrHistoRate(crypto, dateStr, exchange, fiat)
					if not self._checkIfProblem(resultData):
						secondRate = resultData.getValue(resultData.RESULT_KEY_PRICE)
						return firstRate * secondRate

		raise UnsupportedCryptoFiatPairError(crypto, fiat, self.cryptoFiatCsvFilePathName)

	def _getCurrentOrHistoRate(self, crypto, dateStr, exchange, fiat):
		if dateStr is None:
			resultData = self.priceRequester.getCurrentPrice(crypto, fiat, exchange)
		else:
			timeStampLocalMidDay = DateTimeUtil.dateTimeStringToTimeStamp(dateStr,
																		  LOCAL_TIME_ZONE,
																		  "YYYY-MM-DD")
			timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp(dateStr,
																		"UTC",
																		DATE_FORMAT)
			resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																			  fiat,
																			  timeStampLocalMidDay,
																			  LOCAL_TIME_ZONE,
																			  timeStampUtcNoHHMM,
																			  exchange)
		return resultData

	def getHistoricalRate(self, crypto, fiat, dateStr):
		timeStampLocalMidDay = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", 'Europe/Zurich',
																"YYYY/MM/DD HH:mm:ss")
		timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
																	"YYYY/MM/DD HH:mm:ss")
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, unit,
																		  timeStampLocalMidDay,
																		  'Europe/Zurich',
																		  timeStampUtcNoHHMM,
																		  exchange)


		return self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																	fiat,
																	timeStampLocalForHistoMinute,
																	localTz,
																	timeStampUTCNoHHMMForHistoDay,
																	exchange)

	def _checkIfProblem(self, resultData):
		isProblem = False

		if not resultData.noError():
			isProblem = True
			print(resultData.getErrorMessage())
		if resultData.containsWarnings():
			isProblem = True
			print(resultData.getAllWarningMessages())

		return isProblem


if __name__ == "__main__":
	cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
	
	if os.name == 'posix':
		dataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/data/'
		cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName
	else:
		dataPath = 'D:\\Development\\Python\\SByield\\data\\'
		cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName

	cfc = CryptoFiatRateComputer(PriceRequester(),
								 cryptoFiatCsvFilePathName)

	print(cfc.cryptoFiatDf)

	crypto = 'CHSB'
	fiat = 'CHF'

	unitFiatDf = cfc.cryptoFiatDf.loc[cryptoFiatDf['UNIT'] == fiat]
	print('Available unitFiatDf')
	print(unitFiatDf)

	for index, row in unitFiatDf.iterrows():
		cfc.cryptoUnitDf = cfc.cryptoFiatDf.loc[(cfc.cryptoFiatDf['CRYPTO'] == crypto) & (cfc.cryptoFiatDf['UNIT'] == row['CRYPTO'])]
		if not cfc.cryptoUnitDf.empty:
			print('self.cryptoUnitDf')
			print(cfc.cryptoUnitDf)
			unitFiatDf = unitFiatDf.loc[(unitFiatDf['CRYPTO'] == cfc.cryptoUnitDf.iloc[0]['UNIT'])]
			print('Final unitFiatDf')
			print(unitFiatDf)

	lst = cfc._getIntermediateExchangeRateRequests(crypto, fiat)
	print(lst)