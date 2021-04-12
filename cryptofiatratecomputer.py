import os
import pandas as pd
import numpy as np

from pandasdatacomputer import PandasDataComputer

class CryptoFiatRateComputer(PandasDataComputer):
	def __init__(self, cryptoFiatCsvFilePathName):
		"""
		Currently, the configMgr is not used. Constants are used in place.
		
		:param cryptoFiatCsvFilePathName:
		"""
		super().__init__()
		self.cryptoFiatCsvFilePathName = cryptoFiatCsvFilePathName
	
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

		for index, row in unitFiatDf.iterrows():
			cryptoUnitDf = cryptoFiatDf.loc[(cryptoFiatDf['CRYPTO'] == crypto) & (cryptoFiatDf['UNIT'] == row['CRYPTO'])]
			if not cryptoUnitDf.empty:
				unitFiatDf = unitFiatDf.loc[(unitFiatDf['CRYPTO'] == cryptoUnitDf['UNIT'].values[0])]
				intermediateExchangeRateRequestLst.append(
					[cryptoUnitDf.iloc[0]['CRYPTO'], cryptoUnitDf.iloc[0]['UNIT'], cryptoUnitDf.iloc[0]['EXCHANGE']])
				intermediateExchangeRateRequestLst.append([unitFiatDf.iloc[0]['CRYPTO'], unitFiatDf.iloc[0]['UNIT'], unitFiatDf.iloc[0]['EXCHANGE']])

		return intermediateExchangeRateRequestLst


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