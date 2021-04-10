import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from sbyieldratecomputer import *
from duplicatedepositdatetimeerror import DuplicateDepositDateTimeError
from invaliddeposittimeerror import InvalidDepositTimeError

class TestSBYieldRateComputer(unittest.TestCase):
	def initializeComputerClasses(self, sbAccountSheetFileName, depositSheetFileName):
		if os.name == 'posix':
			self.testDataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/'
			sbAccountSheetFilePathName = self.testDataPath + sbAccountSheetFileName
			depositSheetFilePathName = self.testDataPath + depositSheetFileName
		else:
			self.testDataPath = 'D:\\Development\\Python\\SByield\\test\\testData\\'
			sbAccountSheetFilePathName = self.testDataPath + sbAccountSheetFileName
			depositSheetFilePathName = self.testDataPath + depositSheetFileName

		self.yieldRateComputer = SBYieldRateComputer(sbAccountSheetFilePathName,
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

	def test_loadDepositCsvFile(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		depositDf, depositCrypto = self.yieldRateComputer._loadDepositCsvFile()

		if not PRINT:
			self.assertEqual((5, 2), depositDf.shape)
			self.assertEqual(expectedYieldCrypto, depositCrypto)

		expectedStrDataframe = \
'                    OWNER  DEP/WITHDR\n' + \
'DATE                                 ' + \
'''
2020-11-21 00:00:00   JPS      2000.0
2020-12-25 00:00:00  Papa      4000.0
2020-12-25 00:00:01   Béa      1000.0
2020-12-27 00:00:00  Papa      -500.0
2020-12-28 00:00:00   JPS      3000.0'''
		
		if PRINT:
			print(depositDf)
		else:
			self.assertEqual(expectedStrDataframe, depositDf.to_string())
	
	def test_loadDepositCsvFileWithDuplicateDatetime(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1_duplDatetime.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		with self.assertRaises(DuplicateDepositDateTimeError) as e:
			self.yieldRateComputer._loadDepositCsvFile()
		
		self.assertEqual(
			'CSV file {} contains a deposit of 1000.0 for owner Béa with a deposit date 2020-12-25 00:00:00 which is identical to another deposit date. Change the date by increasing the time second by 1 and retry.'.format(
				self.testDataPath + depositSheetFileName), e.exception.message)

	def test_loadDepositCsvFileWithoutCryptoDefinition(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1_noCryptoDefinition.csv'

		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		with self.assertRaises(ValueError) as e:
			self.yieldRateComputer._loadDepositCsvFile()

		self.assertEqual(
			'{} does not contain crypto currency definition. Add CRYPTO-crypto_symbol in the file before the CSV headers and retry.'.format(
				self.testDataPath + depositSheetFileName), str(e.exception))

	def test_loadDepositCsvFileWithInvalidTimeComponent(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1_invalidTimeComponent.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		with self.assertRaises(InvalidDepositTimeError) as e:
			self.yieldRateComputer._loadDepositCsvFile()
		
		self.assertEqual(
			'CSV file {} contains a deposit of 1000.0 for owner Béa with a deposit date 2020/12/25 00:00: whose time component is invalid. Correct the time component and retry.'.format(
				self.testDataPath + depositSheetFileName), e.exception.message)
	
	def test_loadDepositCsvFileWithTimeComponentAfterNineOClock(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1_timeComponentAfter9oclock.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		with self.assertRaises(InvalidDepositTimeError) as e:
			self.yieldRateComputer._loadDepositCsvFile()
		
		self.assertEqual(
			'CSV file {} contains a deposit of 1000.0 for owner Béa with a deposit date 2020-12-25 10:00:00 whose time component is later than the 09:00:00 Swissborg yield payment time. Set the time to a value before 09:00:00 and retry.'.format(
				self.testDataPath + depositSheetFileName), e.exception.message)
	
	def test_mergeEarningAndDeposit(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(expectedYieldCrypto)
		depositDf, depositCrypto = self.yieldRateComputer._loadDepositCsvFile()
		
		mergedEarningDeposit = self.yieldRateComputer._mergeEarningAndDeposit(sbEarningsDf, depositDf)

		if not PRINT:
			self.assertEqual((14, 6), mergedEarningDeposit.shape)
			self.assertEqual(expectedYieldCrypto, depositCrypto)

		expectedStrDataframe = \
'                   DATE  DEP/WITHDR  EARNING CAP  EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'IDX                                                                                  ' + \
'''
1   2020-11-21 00:00:00      2000.0      2000.00     0.00      0.000000      0.000000
2   2020-12-22 09:00:00         0.0      2000.00     0.80      1.000400      1.157162
3   2020-12-23 09:00:00         0.0      2000.80     0.81      1.000405      1.159207
4   2020-12-24 09:00:00         0.0      2001.61     0.82      1.000410      1.161252
5   2020-12-25 00:00:00      4000.0      6002.43     0.00      0.000000      0.000000
6   2020-12-25 00:00:01      1000.0      7002.43     0.00      0.000000      0.000000
7   2020-12-25 09:00:00         0.0      7002.43     0.78      1.000111      1.041493
8   2020-12-26 09:00:00         0.0      7003.21     2.80      1.000400      1.157085
9   2020-12-27 00:00:00      -500.0      6506.01     0.00      0.000000      0.000000
10  2020-12-27 09:00:00         0.0      6506.01     2.70      1.000415      1.163513
11  2020-12-28 00:00:00      3000.0      9508.71     0.00      0.000000      0.000000
12  2020-12-28 09:00:00         0.0      9508.71     2.75      1.000289      1.111317
13  2020-12-29 09:00:00         0.0      9511.46     4.00      1.000421      1.165869
14  2020-12-30 09:00:00         0.0      9515.46     4.10      1.000431      1.170272'''
		
		if PRINT:
			print(mergedEarningDeposit)
		else:
			self.assertEqual(expectedStrDataframe, mergedEarningDeposit.to_string())
		
	def testGetDepositsAndDailyYieldRatesDataframes(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		depositDataFrame, depositCrypto, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(expectedYieldCrypto)

		if not PRINT:
			self.assertEqual((5, 2), depositDataFrame.shape)
			self.assertEqual((9, 4), yieldRatesDataframe.shape)
			self.assertEqual(expectedYieldCrypto, depositCrypto)

		expectedDepositStrDataframe = \
'                    OWNER  DEP/WITHDR\n' + \
'DATE                                 ' + \
'''
2020-11-21 00:00:00   JPS      2000.0
2020-12-25 00:00:00  Papa      4000.0
2020-12-25 00:00:01   Béa      1000.0
2020-12-27 00:00:00  Papa      -500.0
2020-12-28 00:00:00   JPS      3000.0'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositDataFrame, {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f'}))
		else:
			self.assertEqual(expectedDepositStrDataframe, depositDataFrame.to_string())
		
		expectedYieldRatesStrDataframe = \
'            EARNING CAP  EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                        ' + \
'''
2020-12-22      2000.00     0.80      1.000400      1.157162
2020-12-23      2000.80     0.81      1.000405      1.159207
2020-12-24      2001.61     0.82      1.000410      1.161252
2020-12-25      7002.43     0.78      1.000111      1.041493
2020-12-26      7003.21     2.80      1.000400      1.157085
2020-12-27      6506.01     2.70      1.000415      1.163513
2020-12-28      9508.71     2.75      1.000289      1.111317
2020-12-29      9511.46     4.00      1.000421      1.165869
2020-12-30      9515.46     4.10      1.000431      1.170272'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRatesDataframe, {MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.8f'}))
		else:
			self.assertEqual(expectedYieldRatesStrDataframe, yieldRatesDataframe.to_string())
		
	def testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_2_deposit(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_2_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_2_deposit.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		depositDataFrame, depositCrypto, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(
			expectedYieldCrypto)
		
		if not PRINT:
			self.assertEqual((2, 2), depositDataFrame.shape)
			self.assertEqual((5, 4), yieldRatesDataframe.shape)
			self.assertEqual(expectedYieldCrypto, depositCrypto)

		expectedDepositStrDataframe = \
'           OWNER  DEP/WITHDR\n' + \
'DATE                        ' + \
'''
2021-01-01   JPS    19571.69
2021-01-02   JPS     5000.00'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositDataFrame, {
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f'}))
		else:
			self.assertEqual(expectedDepositStrDataframe, depositDataFrame.to_string())
		
		expectedYieldRatesStrDataframe = \
'             EARNING CAP    EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                           ' + \
'''
2021-01-01  19571.690000  10.980768      1.000561      1.227190
2021-01-02  24582.670768  14.966510      1.000609      1.248762
2021-01-03  24597.637278  12.647539      1.000514      1.206383
2021-01-04  24610.284817   9.834966      1.000400      1.157005
2021-01-05  24620.119783  14.994624      1.000609      1.248861'''
		
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
		
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		depositDataFrame, depositCrypto, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(
			expectedYieldCrypto)

		if not PRINT:
			self.assertEqual((2, 2), depositDataFrame.shape)
			self.assertEqual((5, 4), yieldRatesDataframe.shape)
			self.assertEqual(expectedYieldCrypto, depositCrypto)

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
'             EARNING CAP    EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                           ' + \
'''
2021-01-01  20000.000000  11.111261      1.000556      1.224735
2021-01-02  20011.111261   8.607416      1.000430      1.169954
2021-01-03  20019.718678   9.240537      1.000462      1.183451
2021-01-04  10028.959215   5.596533      1.000558      1.225841
2021-01-05  10034.555748   5.224288      1.000521      1.209226'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRatesDataframe, {
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.8f'}))
		else:
			self.assertEqual(expectedYieldRatesStrDataframe, yieldRatesDataframe.to_string())
	
	def testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_1_deposit_1_almost_full_withdr(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_1_almost_full_withdr.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_1_almost_full_withdr.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		depositDataFrame, depositCrypto, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(
			expectedYieldCrypto)
		
		if not PRINT:
			self.assertEqual((2, 2), depositDataFrame.shape)
			self.assertEqual((5, 4), yieldRatesDataframe.shape)
			self.assertEqual(expectedYieldCrypto, depositCrypto)

		expectedDepositStrDataframe = \
'           OWNER  DEP/WITHDR\n' + \
'DATE                        ' + \
'''
2021-01-01   JPS     20000.0
2021-01-04   JPS    -20015.0'''
		
		if PRINT:
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositDataFrame, {
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f'}))
		else:
			self.assertEqual(expectedDepositStrDataframe, depositDataFrame.to_string())
		
		expectedYieldRatesStrDataframe = \
'             EARNING CAP    EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                           ' + \
'''
2021-01-01  20000.000000   8.847285      1.000442      1.175187
2021-01-02  20008.847285  11.623546      1.000581      1.236116
2021-01-03  20020.470832  10.816792      1.000540      1.217928
2021-01-04     16.287624   0.009836      1.000604      1.246520
2021-01-05     16.297460   0.009421      1.000578      1.234841'''
		
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
#	tst.testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_1_deposit_1_partial_withdr()
	tst.test_mergeEarningAndDeposit()
