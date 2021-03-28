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
	def initializeComputerClasses(self, sbAccountSheetFileName, depositSheetFileName):
		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
			self.testDataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/'
			sbAccountSheetFilePathName = self.testDataPath + sbAccountSheetFileName
			depositSheetFilePathName = self.testDataPath + depositSheetFileName
		else:
			configPath = 'c:\\temp\\sbyield.ini'
			self.testDataPath = 'D:\\Development\\Python\\SByield\\test\\testData\\'
			sbAccountSheetFilePathName = self.testDataPath + sbAccountSheetFileName
			depositSheetFilePathName = self.testDataPath + depositSheetFileName

		configMgr = ConfigManager(configPath)
		self.yieldRateComputer = SBYieldRateComputer(configMgr,
		                                             sbAccountSheetFilePathName,
		                                             depositSheetFilePathName)

	def test_loadSBEarningSheetUSDC(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

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
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
		
		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(yieldCrypto)
		self.assertEqual((1, 3), sbEarningsDf.shape)

		expectedStrDataframe = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2020-12-24 09:00:00  Earnings     CHSB         2.1'''
		
		if PRINT:
			print(sbEarningsDf)
		else:
			self.assertEqual(expectedStrDataframe, sbEarningsDf.to_string())

	def testGetSBEarningSheetTotalDfUSDC(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		sbEarningsTotals = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		self.assertEqual((10, 3), sbEarningsTotals.shape)

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
		
		if PRINT:
			print(sbEarningsTotals)
		else:
			self.assertEqual(expectedStrDataframe, sbEarningsTotals.to_string())
		
	def testGetSBEarningSheetTotalDfCHSB(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		sbEarningsTotals = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_CHSB)
		
		self.assertEqual((2, 3), sbEarningsTotals.shape)

		expectedStrDataframe = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2020-12-24 09:00:00  Earnings     CHSB         2.1
TOTAL                                          2.1'''
		
		if PRINT:
			print(sbEarningsTotals)
		else:
			self.assertEqual(expectedStrDataframe, sbEarningsTotals.to_string())

	def test_loadDepositSheet(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		depositDf = self.yieldRateComputer._loadDepositSheet()
		self.assertEqual((5, 2), depositDf.shape)

		expectedStrDataframe = \
'                    OWNER  DEP/WITHDR\n' + \
'DATE                                 ' + \
'''
2020-11-21 10:00:00   JPS      2000.0
2020-12-25 10:00:00  Papa      4000.0
2020-12-25 10:00:01   Béa      1000.0
2020-12-27 10:00:01  Papa      -500.0
2020-12-28 10:00:00   JPS      3000.0'''
		
		if PRINT:
			print(depositDf)
		else:
			self.assertEqual(expectedStrDataframe, depositDf.to_string())
		
	def test_mergeEarningAndDeposit(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(yieldCrypto)
		depositDf = self.yieldRateComputer._loadDepositSheet()
		
		mergedEarningDeposit = self.yieldRateComputer._mergeEarningAndDeposit(sbEarningsDf, depositDf)
		self.assertEqual((14, 6), mergedEarningDeposit.shape)
		
		expectedStrDataframe = \
'                   DATE  DEP/WITHDR  EARNING CAP  EARNINGS  D YIELD RATE  Y YIELD RATE\n' + \
'IDX                                                                                   ' + \
'''
1   2020-11-21 10:00:00      2000.0      2000.00      0.00      0.000000      0.000000
2   2020-12-22 09:00:00         0.0      2000.00      0.80      1.000400      1.157162
3   2020-12-23 09:00:00         0.0      2000.80      0.81      1.000405      1.159207
4   2020-12-24 09:00:00         0.0      2001.61      0.82      1.000410      1.161252
5   2020-12-25 09:00:00         0.0      2002.43      0.78      1.000390      1.152749
6   2020-12-25 10:00:00      4000.0      6003.21      0.00      0.000000      0.000000
7   2020-12-25 10:00:01      1000.0      7003.21      0.00      0.000000      0.000000
8   2020-12-26 09:00:00         0.0      7003.21      2.80      1.000400      1.157085
9   2020-12-27 09:00:00         0.0      7006.01      2.70      1.000385      1.151008
10  2020-12-27 10:00:01      -500.0      6508.71      0.00      0.000000      0.000000
11  2020-12-28 09:00:00         0.0      6508.71      2.75      1.000423      1.166705
12  2020-12-28 10:00:00      3000.0      9511.46      0.00      0.000000      0.000000
13  2020-12-29 09:00:00         0.0      9511.46      4.00      1.000421      1.165869
14  2020-12-30 09:00:00         0.0      9515.46      4.10      1.000431      1.170272'''
		
		if PRINT:
			print(mergedEarningDeposit)
		else:
			self.assertEqual(expectedStrDataframe, mergedEarningDeposit.to_string())
		
	def testGetDepositsAndDailyYieldRatesDataframes(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		depositDataFrame, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		self.assertEqual((5, 2), depositDataFrame.shape)
		self.assertEqual((9, 3), yieldRatesDataframe.shape)
		
		expectedDepositStrDataframe = \
'                    OWNER  DEP/WITHDR\n' + \
'DATE                                 ' + \
'''
2020-11-21 10:00:00   JPS      2000.0
2020-12-25 10:00:00  Papa      4000.0
2020-12-25 10:00:01   Béa      1000.0
2020-12-27 10:00:01  Papa      -500.0
2020-12-28 10:00:00   JPS      3000.0'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositDataFrame, {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f'}))
		else:
			self.assertEqual(expectedDepositStrDataframe, depositDataFrame.to_string())
		
		expectedYieldRatesStrDataframe = \
'            EARNINGS  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                            ' + \
'''
2020-12-22      0.80      1.000400      1.157162
2020-12-23      0.81      1.000405      1.159207
2020-12-24      0.82      1.000410      1.161252
2020-12-25      0.78      1.000390      1.152749
2020-12-26      2.80      1.000400      1.157085
2020-12-27      2.70      1.000385      1.151008
2020-12-28      2.75      1.000423      1.166705
2020-12-29      4.00      1.000421      1.165869
2020-12-30      4.10      1.000431      1.170272'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRatesDataframe, {MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.8f'}))
		else:
			self.assertEqual(expectedYieldRatesStrDataframe, yieldRatesDataframe.to_string())
		
	def testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_2_deposit(self):
		PRINT = True
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_2_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_2_deposit.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		depositDataFrame, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(
			yieldCrypto)
		
		if not PRINT:
			self.assertEqual((2, 2), depositDataFrame.shape)
			self.assertEqual((5, 3), yieldRatesDataframe.shape)
		
		expectedDepositStrDataframe = \
'           OWNER  DEP/WITHDR\n' + \
'DATE                        ' + \
'''
2020-01-01   JPS     20000.0
2020-01-03   JPS    -10000.0'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositDataFrame, {
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f'}))
		else:
			self.assertEqual(expectedDepositStrDataframe, depositDataFrame.to_string())
		
		expectedYieldRatesStrDataframe = \
'            EARNINGS  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                            ' + \
'''
2021-01-01  9.623818      1.000962      1.420630
2021-01-02  7.945745      1.000794      1.335928
2021-01-03  9.958172      1.000994      1.437141
2021-01-04  4.677371      1.000466      1.185561
2021-01-05  6.025685      1.000601      1.245038'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRatesDataframe, {
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.8f'}))
		else:
			self.assertEqual(expectedYieldRatesStrDataframe, yieldRatesDataframe.to_string())
	
	def testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_1_deposit_1_partial_withdr(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_1_partial_withdr.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_1_partial_withdr.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		depositDataFrame, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(
			yieldCrypto)

		if not PRINT:
			self.assertEqual((2, 2), depositDataFrame.shape)
			self.assertEqual((5, 3), yieldRatesDataframe.shape)
		
		expectedDepositStrDataframe = \
'           OWNER  DEP/WITHDR\n' + \
'DATE                        ' + \
'''
2021-01-01   JPS     20000.0
2021-01-04   JPS    -10000.0'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositDataFrame, {
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f'}))
		else:
			self.assertEqual(expectedDepositStrDataframe, depositDataFrame.to_string())
		
		expectedYieldRatesStrDataframe = \
'             EARNINGS  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                             ' + \
'''
2021-01-01  11.111261      1.000556      1.224735
2021-01-02   8.607416      1.000430      1.169954
2021-01-03   9.240537      1.000462      1.183451
2021-01-04   5.596533      1.000558      1.225841
2021-01-05   5.224288      1.000521      1.209226'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRatesDataframe, {
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.8f'}))
		else:
			self.assertEqual(expectedYieldRatesStrDataframe, yieldRatesDataframe.to_string())
	
	def testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_1_deposit_1_almost_full_withdr(self):
		PRINT = True
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_1_almost_full_withdr.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_1_almost_full_withdr.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		depositDataFrame, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(
			yieldCrypto)
		
		if not PRINT:
			self.assertEqual((2, 2), depositDataFrame.shape)
			self.assertEqual((5, 3), yieldRatesDataframe.shape)
		
		expectedDepositStrDataframe = \
'           OWNER  DEP/WITHDR\n' + \
'DATE                        ' + \
'''
2020-01-01   JPS     20000.0
2020-01-03   JPS    -10000.0'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositDataFrame, {
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f'}))
		else:
			self.assertEqual(expectedDepositStrDataframe, depositDataFrame.to_string())
		
		expectedYieldRatesStrDataframe = \
'            EARNINGS  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                            ' + \
'''
2021-01-01  9.623818      1.000962      1.420630
2021-01-02  7.945745      1.000794      1.335928
2021-01-03  9.958172      1.000994      1.437141
2021-01-04  4.677371      1.000466      1.185561
2021-01-05  6.025685      1.000601      1.245038'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRatesDataframe, {
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.8f'}))
		else:
			self.assertEqual(expectedYieldRatesStrDataframe, yieldRatesDataframe.to_string())


if __name__ == '__main__':
	#unittest.main()
	tst = TestSBYieldRateComputer()
	tst.setUp()
#	tst.test_mergeEarningAndDeposit()
#	tst.testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_2_deposit()
	tst.testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_1_deposit_1_partial_withdr()
#	tst.testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_1_deposit_1_almost_full_withdr()
