import os
import pandas as pd

from pandasdatacomputer import PandasDataComputer
from pricerequester import PriceRequester
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
		self.priceReuester = priceRequester

	def _loadCryptoFiatCsvFile(self):
		"""
		Creates a Pandas data frame from the crypto fiat exchange csv file.

		:return: crypto fiat data frame
		"""
		cryptoFiatSheetSkipRows, \
		_ = self._determineDepositSheetSkipRowsAndCrypto(self.cryptoFiatCsvFilePathName,
															 'CRYPTO')

		cryptoFiatDf = pd.read_csv(self.cryptoFiatCsvFilePathName,
								   skiprows=cryptoFiatSheetSkipRows)
		
		return cryptoFiatDf

	def _getIntermediateExchangeRateRequests(self, crypto, fiat):
		cryptoFiatDf = self._loadCryptoFiatCsvFile()

		intermediateExchangeRateRequestLst = []

		unitFiatDf = cryptoFiatDf.loc[cryptoFiatDf['UNIT'] == fiat]

		cryptoUnitDf = cryptoFiatDf.loc[(cryptoFiatDf['CRYPTO'] == crypto) & (cryptoFiatDf['UNIT'] == fiat)]

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
			cryptoUnitDf = cryptoFiatDf.loc[(cryptoFiatDf['CRYPTO'] == crypto) & (cryptoFiatDf['UNIT'] == row['CRYPTO'])]
			if not cryptoUnitDf.empty:
				unitFiatDf = unitFiatDf.loc[(unitFiatDf['CRYPTO'] == cryptoUnitDf.iloc[0]['UNIT'])]
				intermediateExchangeRateRequestLst.append(
					[cryptoUnitDf.iloc[0]['CRYPTO'], cryptoUnitDf.iloc[0]['UNIT'], cryptoUnitDf.iloc[0]['EXCHANGE']])
				intermediateExchangeRateRequestLst.append([unitFiatDf.iloc[0]['CRYPTO'], unitFiatDf.iloc[0]['UNIT'], unitFiatDf.iloc[0]['EXCHANGE']])

		return intermediateExchangeRateRequestLst

	def computeCryptoFiatCurrentRate(self, crypto, fiat):
		'''
		:raise UnsupportedCryptoFiatPairError in case the crypto fiat exchange
		 	   CSV file does not have the necessary information to compute the
		 	   crypto/fiat pair rate.

		:return crypto/fiat pair current rate
		'''
		intermediateExchangeRateRequestLst = self._getIntermediateExchangeRateRequests(crypto, fiat)

		rateRequestNumber = len(intermediateExchangeRateRequestLst)

		if rateRequestNumber == 1:
			exchange = intermediateExchangeRateRequestLst[0][2]
			resultData = self.priceReuester.getCurrentPrice(crypto, fiat, exchange)
			if not self.checkIfProblem(resultData):
				return resultData.getValue(resultData.RESULT_KEY_PRICE)
		elif rateRequestNumber == 2:
				crypto = intermediateExchangeRateRequestLst[0][0]
				unit = intermediateExchangeRateRequestLst[0][1]
				exchange = intermediateExchangeRateRequestLst[0][2]
				resultData = self.priceReuester.getCurrentPrice(crypto, unit, exchange)
				if not self.checkIfProblem(resultData):
					firstRate = resultData.getValue(resultData.RESULT_KEY_PRICE)
					crypto = intermediateExchangeRateRequestLst[1][0]
					fiat = intermediateExchangeRateRequestLst[1][1]
					exchange = intermediateExchangeRateRequestLst[1][2]
					resultData = self.priceReuester.getCurrentPrice(crypto, fiat, exchange)
					if not self.checkIfProblem(resultData):
						secondRate = resultData.getValue(resultData.RESULT_KEY_PRICE)
						return firstRate * secondRate
		else:
			raise UnsupportedCryptoFiatPairError(crypto, fiat, self.cryptoFiatCsvFilePathName)

	def checkIfProblem(self, resultData):
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

	cfc = CryptoFiatRateComputer(cryptoFiatCsvFilePathName)
	cryptoFiatDf = cfc._loadCryptoFiatCsvFile()
	
	print(cryptoFiatDf)

	crypto = 'CHSB'
	fiat = 'CHF'

	unitFiatDf = cryptoFiatDf.loc[cryptoFiatDf['UNIT'] == fiat]
	print('Available unitFiatDf')
	print(unitFiatDf)

	for index, row in unitFiatDf.iterrows():
		cryptoUnitDf = cryptoFiatDf.loc[(cryptoFiatDf['CRYPTO'] == crypto) & (cryptoFiatDf['UNIT'] == row['CRYPTO'])]
		if not cryptoUnitDf.empty:
			print('cryptoUnitDf')
			print(cryptoUnitDf)
			unitFiatDf = unitFiatDf.loc[(unitFiatDf['CRYPTO'] == cryptoUnitDf.iloc[0]['UNIT'])]
			print('Final unitFiatDf')
			print(unitFiatDf)

	lst = cfc._getIntermediateExchangeRateRequests(crypto, fiat)
	print(lst)