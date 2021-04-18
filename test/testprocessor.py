import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from cryptofiatratecomputer import CryptoFiatRateComputer
from processor import *

class TestProcessor(unittest.TestCase):
	def initializeComputerClasses(self, sbAccountSheetFileName, depositSheetFileName, cryptoFiatCsvFileName):
		if os.name == 'posix':
			self.testDataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/'
			dataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/data/'
			sbAccountSheetFilePathName = self.testDataPath + sbAccountSheetFileName
			depositSheetFilePathName = self.testDataPath + depositSheetFileName
			cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName
		else:
			self.testDataPath = 'D:\\Development\\Python\\SByield\\test\\testData\\'
			dataPath = 'D:\\Development\\Python\\SByield\\data\\'
			sbAccountSheetFilePathName = self.testDataPath + sbAccountSheetFileName
			depositSheetFilePathName = self.testDataPath + depositSheetFileName
			cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName
		self.yieldRateComputer = SBYieldRateComputer(sbAccountSheetFilePathName,
		                                             depositSheetFilePathName)
		self.ownerDepositYieldComputer = OwnerDepositYieldComputer(self.yieldRateComputer)
		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(cryptoFiatCsvFilePathName))

	def testAddFiatConversionInfo(self):
		"""
		"""
		PRINT = True

		sbAccountSheetFileName = 'testSwissborg_account_statement_20201218_20210408.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_usd_chf.csv'
		#depositSheetFileName = 'testDepositChsb_fiat_usd.csv'
		#depositSheetFileName = 'testDepositChsb_no_fiat.csv'
		depositSheetFileName = 'testDepositChsb_fiat_chf.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)

		# resetting the pandas global float format so that the other unit test
		# are not impacted by the previous global float format setting
		pd.reset_option('display.float_format')

	def testAddFiatConversionInfo(self):
		"""
		"""
		PRINT = True

		sbAccountSheetFileName = 'testSwissborg_account_statement_20201218_20210408.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_usd_chf.csv'
		#depositSheetFileName = 'testDepositChsb_fiat_usd.csv'
		#depositSheetFileName = 'testDepositChsb_no_fiat.csv'
		depositSheetFileName = 'testDepositChsb_fiat_chf.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)

		# resetting the pandas global float format so that the other unit test
		# are not impacted by the previous global float format setting
		pd.reset_option('display.float_format')

if __name__ == '__main__':
	if os.name == 'posix':
		unittest.main()
	else:
		tst = TestProcessor()
		tst.testAddFiatConversionInfo()
