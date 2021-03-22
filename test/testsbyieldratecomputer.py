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
		depositSheetFileName = 'testDepositUsdc_1.csv'

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
		self.assertEqual((9, 3), sbEarningsDf.shape)
		#expectedStrDataframe = sbEarningsDf.to_string()
		expectedStrDataframe = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2020-12-22 09:00:00  Earnings     USDC        0.80
2020-12-23 09:00:00  Earnings     USDC        0.81
2020-12-24 09:00:00  Earnings     USDC        0.82
2020-12-25 09:00:00  Earnings     USDC        0.78
2020-12-26 09:00:00  Earnings     USDC        2.80
2020-12-27 09:00:00  Earnings     USDC        2.70
2020-12-28 09:00:00  Earnings     USDC        2.75
2020-12-29 09:00:00  Earnings     USDC        4.00
2020-12-30 09:00:00  Earnings     USDC        4.10'''
		self.assertEqual(expectedStrDataframe, sbEarningsDf.to_string())
	
	def test_loadSBEarningSheetCHSB(self):
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
		
		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(yieldCrypto)
		self.assertEqual((1, 3), sbEarningsDf.shape)
		#expectedStrDataframe = sbEarningsDf.to_string()
		expectedStrDataframe = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2020-12-24 09:00:00  Earnings     CHSB         2.1'''
		self.assertEqual(expectedStrDataframe, sbEarningsDf.to_string())

	def testGetSBEarningSheetTotalDfUSDC(self):
		sbEarningsTotals = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		self.assertEqual((10, 3), sbEarningsTotals.shape)
		# expectedStrDataframe = sbEarningsTotals.to_string()
		expectedStrDataframe = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2020-12-22 09:00:00  Earnings     USDC        0.80
2020-12-23 09:00:00  Earnings     USDC        0.81
2020-12-24 09:00:00  Earnings     USDC        0.82
2020-12-25 09:00:00  Earnings     USDC        0.78
2020-12-26 09:00:00  Earnings     USDC        2.80
2020-12-27 09:00:00  Earnings     USDC        2.70
2020-12-28 09:00:00  Earnings     USDC        2.75
2020-12-29 09:00:00  Earnings     USDC        4.00
2020-12-30 09:00:00  Earnings     USDC        4.10
TOTAL                                        19.56'''
		self.assertEqual(expectedStrDataframe, sbEarningsTotals.to_string())
		
	def testGetSBEarningSheetTotalDfCHSB(self):
		sbEarningsTotals = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_CHSB)
		
		self.assertEqual((2, 3), sbEarningsTotals.shape)
		# expectedStrDataframe = sbEarningsTotals.to_string()
		expectedStrDataframe = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2020-12-24 09:00:00  Earnings     CHSB         2.1
TOTAL                                          2.1'''
		self.assertEqual(expectedStrDataframe, sbEarningsTotals.to_string())

	def test_loadDepositSheet(self):
		depositDf = self.yieldRateComputer._loadDepositSheet()
		self.assertEqual((5, 2), depositDf.shape)
		#expectedStrDataframe = depositDf.to_string()
		expectedStrDataframe = \
'                    OWNER  DEP/WITHDR\n' + \
'DATE                                 ' + \
'''
2020-11-21 10:00:00   JPS      2000.0
2020-12-25 10:00:00  Papa      4000.0
2020-12-25 10:00:01   Béa      1000.0
2020-12-27 10:00:01  Papa      -500.0
2020-12-28 10:00:00   JPS      3000.0'''
		self.assertEqual(expectedStrDataframe, depositDf.to_string())
		
	def test_mergeEarningAndDeposit(self):
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(yieldCrypto)
		depositDf = self.yieldRateComputer._loadDepositSheet()
		
		mergedEarningDeposit = self.yieldRateComputer._mergeEarningAndDeposit(sbEarningsDf, depositDf)
		self.assertEqual((14, 5), mergedEarningDeposit.shape)
		
		#expectedStrDataframe = mergedEarningDeposit.to_string()
		expectedStrDataframe = \
'                   DATE  DEP/WITHDR  EARNING CAP  EARNINGS  DAILY YIELD RATE\n' + \
'IDX                                                                         ' + \
'''
1   2020-12-21 10:00:00      2000.0         0.00      0.00          0.000000
2   2020-12-22 09:00:00         0.0      2000.00      0.80          1.000400
3   2020-12-23 09:00:00         0.0      2000.80      0.81          1.000405
4   2020-12-24 09:00:00         0.0      2001.61      0.82          1.000410
5   2020-12-25 09:00:00         0.0      2002.43      0.78          1.000390
6   2020-12-25 10:00:00      4000.0      2003.21      0.00          0.000000
7   2020-12-25 10:00:01      1000.0      6003.21      0.00          0.000000
8   2020-12-26 09:00:00         0.0      7003.21      2.80          1.000400
9   2020-12-27 09:00:00         0.0      7006.01      2.70          1.000385
10  2020-12-27 10:00:01      -500.0      7008.71      0.00          0.000000
11  2020-12-28 09:00:00         0.0      6508.71      2.75          1.000423
12  2020-12-28 10:00:00      3000.0      6511.46      0.00          0.000000
13  2020-12-29 09:00:00         0.0      9511.46      4.00          1.000421
14  2020-12-30 09:00:00         0.0      9515.46      4.10          1.000431'''
		#self.assertEqual(expectedStrDataframe, mergedEarningDeposit.to_string())
		print(mergedEarningDeposit)
		
	def testGetDepositsAndDailyYieldRatesDataframes(self):
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		depositDataFrame, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		self.assertEqual((5, 2), depositDataFrame.shape)
		self.assertEqual((9, 1), yieldRatesDataframe.shape)
		
		# expectedStrDataframe = depositDataFrame.to_string()
		expectedDepositStrDataframe = \
'                    OWNER  DEP/WITHDR\n' + \
'DATE                                 ' + \
'''
2020-11-21 10:00:00   JPS      2000.0
2020-12-25 10:00:00  Papa      4000.0
2020-12-25 10:00:01   Béa      1000.0
2020-12-27 10:00:01  Papa      -500.0
2020-12-28 10:00:00   JPS      3000.0'''
		self.assertEqual(expectedDepositStrDataframe, depositDataFrame.to_string())
		
		#expectedStrDataframe = yieldRatesDataframe.to_string()
		expectedYieldRatesStrDataframe = \
			'            DAILY YIELD RATE\n' + \
			'DATE                        ' + \
'''
2020-12-22          1.000400
2020-12-23          1.000405
2020-12-24          1.000410
2020-12-25          1.000390
2020-12-26          1.000400
2020-12-27          1.000385
2020-12-28          1.000423
2020-12-29          1.000421
2020-12-30          1.000431'''
		self.assertEqual(expectedYieldRatesStrDataframe, yieldRatesDataframe.to_string())
		
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositDataFrame, {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRatesDataframe, {MERGED_SHEET_HEADER_YIELD_RATE: '.8f'}))
	
if __name__ == '__main__':
	#unittest.main()
	tst = TestSBYieldRateComputer()
	tst.setUp()
	tst.testGetDepositsAndDailyYieldRatesDataframes()
