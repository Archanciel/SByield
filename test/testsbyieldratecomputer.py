import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from configmanager import ConfigManager
from sbyieldratecomputer import *

class TestSByieldRateComputer(unittest.TestCase):
	def setUp(self):
		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
		else:
			configPath = 'c:\\temp\\sbyield.ini'

		configMgr = ConfigManager(configPath)
		self.sheetDataAccess = SByieldRateComputer(configMgr)

	def test_loadSBEarningSheetUSDC(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		if os.name == 'posix':
			sbAccountSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + sbAccountSheetFileName
		else:
			sbAccountSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + sbAccountSheetFileName

		sbEarningsDf = self.sheetDataAccess._loadSBEarningSheet(sbAccountSheetFilePathName, yieldCrypto)
		self.assertEqual((9, 5), sbEarningsDf.shape)
		
		print('\nsbEarningsDf')
		print(sbEarningsDf.info())
		print(sbEarningsDf)
	
	def test_loadSBEarningSheetCHSB(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
		
		if os.name == 'posix':
			sbAccountSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + sbAccountSheetFileName
		else:
			sbAccountSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + sbAccountSheetFileName
		
		sbEarningsDf = self.sheetDataAccess._loadSBEarningSheet(sbAccountSheetFilePathName, yieldCrypto)
		self.assertEqual((1, 5), sbEarningsDf.shape)
		
		print('\nsbEarningsDf')
		print(sbEarningsDf.info())
		print(sbEarningsDf)
	
	def test_loadDepositSheet(self):
		depositSheetFileName = 'testDepositUsdc.csv'

		if os.name == 'posix':
			depositSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + depositSheetFileName
		else:
			depositSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + depositSheetFileName

		depositDf = self.sheetDataAccess._loadDepositSheet(depositSheetFilePathName)
		self.assertEqual((5, 2), depositDf.shape)
		
		print('\ndepositDf')
		print(depositDf.info())
		print(depositDf)
		
	def test_mergeEarningAndDeposit(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc.csv'
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		if os.name == 'posix':
			sbAccountSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + sbAccountSheetFileName
			depositSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + depositSheetFileName
		else:
			sbAccountSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + sbAccountSheetFileName
			depositSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + depositSheetFileName

		sbEarningsDf = self.sheetDataAccess._loadSBEarningSheet(sbAccountSheetFilePathName, yieldCrypto)
		depositDf = self.sheetDataAccess._loadDepositSheet(depositSheetFilePathName)
		
		mergedEarningDeposit = self.sheetDataAccess._mergeEarningAndDeposit(sbEarningsDf, depositDf)
		self.assertEqual((14, 5), mergedEarningDeposit.shape)

		print('\nmergedEarningDeposit')
		print(mergedEarningDeposit.info())
		print(self.sheetDataAccess.getDataframeStrWithFormattedColumns(mergedEarningDeposit, {MERGED_SHEET_HEADER_YIELD_RATE: '.8f'}))

	def testGetDepositsAndDailyYieldRatesDataframes(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc.csv'
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		if os.name == 'posix':
			sbAccountSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + sbAccountSheetFileName
			depositSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + depositSheetFileName
		else:
			sbAccountSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + sbAccountSheetFileName
			depositSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + depositSheetFileName

		depositDataFrame, yieldRatesDataframe = self.sheetDataAccess.getDepositsAndDailyYieldRatesDataframes(sbAccountSheetFilePathName,
		                                                                                   depositSheetFilePathName,
		                                                                                   yieldCrypto)
		self.assertEqual((5, 2), depositDataFrame.shape)
		self.assertEqual((9, 1), yieldRatesDataframe.shape)

		print(self.sheetDataAccess.getDataframeStrWithFormattedColumns(depositDataFrame, {DEPOSIT_SHEET_HEADER_DEPOSIT_WITHDRAW: '.2f'}))
		print(self.sheetDataAccess.getDataframeStrWithFormattedColumns(yieldRatesDataframe, {MERGED_SHEET_HEADER_YIELD_RATE: '.8f'}))

if __name__ == '__main__':
	#unittest.main()
	tst = TestSByieldRateComputer()
	tst.setUp()
	tst.testGetDepositsAndDailyYieldRatesDataframes()
