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
		Creates a Pandas data frame from the Deposit/Withdrawal sheet.
		
		:param sbDepositSheetFilePathName:

		:raise ValueError in case the deposit CSV file does not contain the
			   crypto definition (CRYPTO-crypto_symbol)
		:return: deposits data frame, deposit file defined crypto
		"""
		cryptoFiatSheetSkipRows, \
		_, \
		_, \
		_ = self._determineDepositSheetSkipRowsAndCrypto(self.cryptoFiatCsvFilePathName,
															 'CRYPTO',
															 'not used',
															 'not used',
															 'not used')

		cryptoFiatDf = pd.read_csv(self.cryptoFiatCsvFilePathName,
								 skiprows=cryptoFiatSheetSkipRows)
		
		return cryptoFiatDf


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