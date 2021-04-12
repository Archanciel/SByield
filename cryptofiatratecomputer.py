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