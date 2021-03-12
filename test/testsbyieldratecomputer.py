import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from configmanager import ConfigManager
from sbyieldratecomputer import *

class TestSBYieldRateComputer(unittest.TestCase):
	def setUp(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc.csv'

		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
			sbAccountSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + sbAccountSheetFileName
			depositSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + depositSheetFileName
		else:
			configPath = 'c:\\temp\\sbyield.ini'
			sbAccountSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + sbAccountSheetFileName
			depositSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + depositSheetFileName

		configMgr = ConfigManager(configPath)
		self.yieldRateComputer = SBYieldRateComputer(configMgr,
		                                             sbAccountSheetFilePathName,
		                                             depositSheetFilePathName)

	def test_loadSBEarningSheetUSDC(self):
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(yieldCrypto)
		self.assertEqual((9, 5), sbEarningsDf.shape)
		
		print('\nsbEarningsDf')
		print(sbEarningsDf.info())
		print(sbEarningsDf)
	
	def test_loadSBEarningSheetCHSB(self):
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
		
		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(yieldCrypto)
		self.assertEqual((1, 5), sbEarningsDf.shape)
		
		print('\nsbEarningsDf')
		print(sbEarningsDf.info())
		print(sbEarningsDf)
	
	def test_loadDepositSheet(self):
		depositDf = self.yieldRateComputer._loadDepositSheet()
		self.assertEqual((5, 2), depositDf.shape)
		
		print('\ndepositDf')
		print(depositDf.info())
		print(depositDf)
		
	def test_mergeEarningAndDeposit(self):
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(yieldCrypto)
		depositDf = self.yieldRateComputer._loadDepositSheet()
		
		mergedEarningDeposit = self.yieldRateComputer._mergeEarningAndDeposit(sbEarningsDf, depositDf)
		self.assertEqual((14, 5), mergedEarningDeposit.shape)

		print('\nmergedEarningDeposit')
		print(mergedEarningDeposit.info())
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(mergedEarningDeposit, {MERGED_SHEET_HEADER_YIELD_RATE: '.8f'}))

	def testGetDepositsAndDailyYieldRatesDataframes(self):
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		depositDataFrame, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		self.assertEqual((5, 2), depositDataFrame.shape)
		self.assertEqual((9, 1), yieldRatesDataframe.shape)

		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositDataFrame, {DEPOSIT_SHEET_HEADER_DEPOSIT_WITHDRAW: '.2f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRatesDataframe, {MERGED_SHEET_HEADER_YIELD_RATE: '.8f'}))

if __name__ == '__main__':
	#unittest.main()
	tst = TestSBYieldRateComputer()
	tst.setUp()
	tst.testGetDepositsAndDailyYieldRatesDataframes()
