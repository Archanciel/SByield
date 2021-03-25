import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from configmanager import ConfigManager
from ownerdeposityieldcomputer import *
from invaliddepositdateerror import InvalidDepositDateError


class TestOwnerDepositYieldComputer(unittest.TestCase):
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
		self.ownerDepositYieldComputer = OwnerDepositYieldComputer(configMgr, self.yieldRateComputer)
		
		def testComputeDepositsYieldsSeveralOwners(self):
			"""
			The deposit csv file causes the deposits sorted by owner and then by deposit date
			to start with an owner having only one deposit. The other owners have each one two
			deposits.
			"""
			sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
			depositSheetFileName = 'testDepositUsdc_1.csv'
			
			self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
			
			yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
			
			yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(
				yieldCrypto)
			
			print(depositSheetFileName)
			_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
			print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
			                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
			
			print(depositSheetFileName)
			
			sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
			
			sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
				sbEarningsTotalDf,
				{
					DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
			sbEarningsTotalDfExpectedStr = \
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
			
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
			
			yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
				yieldOwnerSummaryTotals,
				{
					DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
					DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
			yieldOwnerSummaryTotalsExpectedStr = \
				'      DEP/WITHDR YIELD AMOUNT\n' + \
				'OWNER                        ' + \
				'''
				Béa     1,000.00   2.45115938
				JPS     5,000.00  11.15560351
				Papa    3,500.00   8.96921943
				TOTAL   9,500.00  22.57598231'''
			
			self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
			
			yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
				yieldOwnerDetailTotals,
				{
					DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
					DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
					DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
			
			yieldOwnerDetailTotalsExpectedStr = \
				'      OWNER DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS YIELD AMOUNT\n' + \
				'IDX                                                                            ' + \
				'''
				1       Béa   1,000.00 1,000.00  2020-12-25  2020-12-30          6   2.45115938
				2       JPS   2,000.00 2,000.00  2020-12-22  2020-12-27          6   4.78322928
				3       JPS   3,000.00 5,000.00  2020-12-28  2020-12-30          3   6.37237423
				4      Papa   4,000.00 4,000.00  2020-12-25  2020-12-26          2   3.15799648
				5      Papa    -500.00 3,500.00  2020-12-27  2020-12-30          4   5.81122295
				TOTAL         9,500.00                                              22.57598231'''
			self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
	
	def testComputeDepositsYieldsSeveralOwners(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to start with an owner having only one deposit. The other owners have each one two
		deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)

		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		sbEarningsTotalDfExpectedStr = \
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
		
		self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerSummaryTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR YIELD AMOUNT\n' + \
'OWNER                        ' + \
'''
Béa     1,000.00   2.45115938
JPS     5,000.00  11.15560351
Papa    3,500.00   8.96921943
TOTAL   9,500.00  22.57598231'''
		
		self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerDetailTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerDetailTotalsExpectedStr = \
'      OWNER DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS YIELD AMOUNT\n' + \
'IDX                                                                            ' + \
'''
1       Béa   1,000.00 1,000.00  2020-12-25  2020-12-30          6   2.45115938
2       JPS   2,000.00 2,000.00  2020-12-22  2020-12-27          6   4.78322928
3       JPS   3,000.00 5,000.00  2020-12-28  2020-12-30          3   6.37237423
4      Papa   4,000.00 4,000.00  2020-12-25  2020-12-26          2   3.15799648
5      Papa    -500.00 3,500.00  2020-12-27  2020-12-30          4   5.81122295
TOTAL         9,500.00                                              22.57598231'''
		self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
	
	def testComputeDepositsYieldsLastDepositRowUniqueOwnerTwoDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. The other owners have each one two
		deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_2.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsMiddleDepositRowUniqueOwnerTwoDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to have the owner having only one deposit to be located in the middle of the
		deposit table. The other owners have each one two deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_3.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsFirstDepositRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to start with an owner having only one deposit. The other owners have each one three
		deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_4.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsLastDepositRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. The other owners have each one three
		deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_5.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsMiddleDepositRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to have the owner having only one deposit to be located in the middle of the
		deposit table. The other owners have each one three deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_6.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsFirstDepositDateFromIsMaxRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to start with an owner having only one deposit. This unique deposit is done on the
		date of the last yield payment and so will have a 0 yield day number and a 0 yield
		amount. The other owners have each one three deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_7.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsLastDepositDateFromIsMaxRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to have the owner having only one deposit to be located in the middle of the
		deposit table. This unique deposit is done on the date of the last yield payment
		and so will have a 0 yield day number and a 0 yield	amount. The other owners have
		each one three deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_8.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsMiddleDepositDateFromIsMaxRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. This unique deposit is done on the
		date of the last yield payment and so will have a 0 yield day number and a 0 yield
		amount. The other owners have each one three deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_9.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsFirstDepositDateFromIsMaxRowUniqueOwnerThreeDepositsDepositDateFromIsMax(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to start with an owner having only one deposit. This unique deposit is done on the
		date of the last yield payment and so will have a 0 yield day number and a 0 yield
		amount. The other owners have each one three deposits, one of them done on the
		date of the last yield payment.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_10.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsLastDepositDateFromIsMaxRowUniqueOwnerThreeDepositsDepositDateFromIsMax(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to have the owner having only one deposit to be located in the middle of the
		deposit table. This unique deposit is done on the date of the last yield payment
		and so will have a 0 yield day number and a 0 yield	amount. The other owners have
		each one three deposits, one of them done on the date of the last yield payment.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_11.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsMiddleDepositDateFromIsMaxRowUniqueOwnerThreeDepositsDepositDateFromIsMax(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. This unique deposit is done on the
		date of the last yield payment and so will have a 0 yield day number and a 0 yield
		amount. The other owners have each one three deposits, one of them done on the
		date of the last yield payment.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_12.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
	
	def testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_1(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. This unique deposit is done on a
		date after the last yield payment. This will cause an exception and interrupt the
		deposit yield computation.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_13.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		with self.assertRaises(InvalidDepositDateError) as e:
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
			
		self.assertEqual('CSV file {}testDepositUsdc_13.csv contains a deposit of 100.0 for owner JPS with a deposit date 2020-12-31 after the last payment date 2020-12-30'.format(self.testDataPath), e.exception.message)
	
	def testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_2(
			self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. This unique deposit is done on a
		date after the last yield payment. This will cause an exception and interrupt the
		deposit yield computation.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_14.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		with self.assertRaises(InvalidDepositDateError) as e:
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		self.assertEqual(
			'CSV file {}testDepositUsdc_14.csv contains a deposit of 100.0 for owner JPS with a deposit date 2020-12-31 after the last payment date 2020-12-30'.format(
				self.testDataPath), e.exception.message)
	
	def testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_3(
			self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. This unique deposit is done on a
		date after the last yield payment. This will cause an exception and interrupt the
		deposit yield computation.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_15.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		with self.assertRaises(InvalidDepositDateError) as e:
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		self.assertEqual(
			'CSV file {}testDepositUsdc_15.csv contains a deposit of 1000.0 for owner Loan with a deposit date 2020-12-31 after the last payment date 2020-12-30'.format(
				self.testDataPath), e.exception.message)
	
	def testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_4(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. This unique deposit is done on a
		date after the last yield payment. This will cause an exception and interrupt the
		deposit yield computation.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_16.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		with self.assertRaises(InvalidDepositDateError) as e:
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		self.assertEqual(
			'CSV file {}testDepositUsdc_16.csv contains a deposit of 300.0 for owner Papa with a deposit date 2020-12-31 after the last payment date 2020-12-30'.format(
				self.testDataPath), e.exception.message)
	
	def testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_5(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. This unique deposit is done on a
		date after the last yield payment. This will cause an exception and interrupt the
		deposit yield computation.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_17.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		with self.assertRaises(InvalidDepositDateError) as e:
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		self.assertEqual(
			'CSV file {}testDepositUsdc_17.csv contains a deposit of 1000.0 for owner Béa with a deposit date 2020-12-31 after the last payment date 2020-12-30'.format(
				self.testDataPath), e.exception.message)
	
	def testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_6(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. This unique deposit is done on a
		date after the last yield payment. This will cause an exception and interrupt the
		deposit yield computation.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_18.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		with self.assertRaises(InvalidDepositDateError) as e:
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		self.assertEqual(
			'CSV file {}testDepositUsdc_18.csv contains a deposit of 1000.0 for owner Zoé with a deposit date 2020-12-31 after the last payment date 2020-12-30'.format(
				self.testDataPath), e.exception.message)
	
	def testComputeDepositsYieldsLastDepositRowUniqueOwnerTwoDepositsOnFirstDepositDate(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. The other owners have each one two
		deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_19.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(yieldOwnerDetailTotals)
		print(yieldOwnerSummaryTotals)
	
	def testAndAnalyseComputeDepositsYields_dep_1(self):
		"""
		Only one owner with one deposit.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc_analysis_dep_1_2.xlsx'
		depositSheetFileName = 'testDepositUsdc_analysis_dep_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)

		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(sbEarningsTotalDf,
		                                                                                        {
			                                                                                        DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2020-12-22 09:00:00  Earnings     USDC    9.379352
2020-12-23 09:00:00  Earnings     USDC    8.904065
2020-12-24 09:00:00  Earnings     USDC    9.347525
2020-12-25 09:00:00  Earnings     USDC    9.392593
2020-12-26 09:00:00  Earnings     USDC    8.592407
2020-12-27 09:00:00  Earnings     USDC    8.292884
2020-12-28 09:00:00  Earnings     USDC    8.310218
2020-12-29 09:00:00  Earnings     USDC    8.313737
2020-12-30 09:00:00  Earnings     USDC    8.455467
2020-12-31 09:00:00  Earnings     USDC    8.403842
TOTAL                                    87.392090'''
		
		self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		#print(sbEarningsTotalDfActualStr)
				
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(yieldOwnerSummaryTotals,
		                                                                                        {
			                                                                                        DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
			                                                                                        DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR YIELD AMOUNT\n' + \
'OWNER                        ' + \
'''
JPS    19,571.69  87.39209000
TOTAL  19,571.69  87.39209000'''

		self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerDetailTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerDetailTotalsExpectedStr = \
'      OWNER DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS YIELD AMOUNT\n' + \
'IDX                                                                             ' + \
'''
1       JPS  19,571.69 19,571.69  2020-12-22  2020-12-31         10  87.39209000
TOTAL        19,571.69                                               87.39209000'''
		self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
		
	def testAndAnalyseComputeDepositsYields_dep_2(self):
		"""
		Two owners with one deposit each starting at same date.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc_analysis_dep_1_2.xlsx'
		depositSheetFileName = 'testDepositUsdc_analysis_dep_2.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2020-12-22 09:00:00  Earnings     USDC    9.379352
2020-12-23 09:00:00  Earnings     USDC    8.904065
2020-12-24 09:00:00  Earnings     USDC    9.347525
2020-12-25 09:00:00  Earnings     USDC    9.392593
2020-12-26 09:00:00  Earnings     USDC    8.592407
2020-12-27 09:00:00  Earnings     USDC    8.292884
2020-12-28 09:00:00  Earnings     USDC    8.310218
2020-12-29 09:00:00  Earnings     USDC    8.313737
2020-12-30 09:00:00  Earnings     USDC    8.455467
2020-12-31 09:00:00  Earnings     USDC    8.403842
TOTAL                                    87.392090'''
		
		self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		# print(sbEarningsTotalDfActualStr)
		
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerSummaryTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR YIELD AMOUNT\n' + \
'OWNER                        ' + \
'''
JPS     4,975.64  22.21737513
Papa   14,596.05  65.17471487
TOTAL  19,571.69  87.39209000'''
		
		self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerDetailTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})

		yieldOwnerDetailTotalsExpectedStr = \
'      OWNER DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS YIELD AMOUNT\n' + \
'IDX                                                                             ' + \
'''
1       JPS   4,975.64  4,975.64  2020-12-22  2020-12-31         10  22.21737513
2      Papa  14,596.05 14,596.05  2020-12-22  2020-12-31         10  65.17471487
TOTAL        19,571.69                                               87.39209000'''
		# print(yieldOwnerDetailTotalsActualStr)
		# print(yieldOwnerDetailTotalsExpectedStr)
		self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
	
	def testAndAnalyseComputeDepositsYields_dep_3(self):
		"""
		Two owners, the first with two deposits, the second with one deposit.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc_analysis_dep_3_a.xlsx'
		depositSheetFileName = 'testDepositUsdc_analysis_dep_3.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2020-12-22 09:00:00  Earnings     USDC    8.309086
2020-12-23 09:00:00  Earnings     USDC    8.904065
2020-12-24 09:00:00  Earnings     USDC    9.347525
2020-12-25 09:00:00  Earnings     USDC    9.392593
2020-12-26 09:00:00  Earnings     USDC    8.592407
2020-12-27 09:00:00  Earnings     USDC    8.292884
2020-12-28 09:00:00  Earnings     USDC    8.310218
2020-12-29 09:00:00  Earnings     USDC    8.313737
2020-12-30 09:00:00  Earnings     USDC    8.455467
2020-12-31 09:00:00  Earnings     USDC    8.403842
TOTAL                                    86.321824'''
		
		self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		#print(sbEarningsTotalDfActualStr)
		
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerSummaryTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR YIELD AMOUNT\n' + \
'OWNER                        ' + \
'''
JPS     4,975.64  21.13866487
Papa   14,596.05  65.17792340
TOTAL  19,571.69  86.31658827'''
		
		self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		#print(yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerDetailTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerDetailTotalsExpectedStr = \
'      OWNER DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS YIELD AMOUNT\n' + \
'IDX                                                                             ' + \
'''
1       JPS   2,742.27  2,742.27  2020-12-22  2020-12-22          1   1.31418490
2       JPS   2,233.37  4,975.64  2020-12-23  2020-12-31          9  19.82447997
3      Papa  14,596.05 14,596.05  2020-12-22  2020-12-31         10  65.17792340
TOTAL        19,571.69                                               86.31658827'''
		#print(yieldOwnerDetailTotalsActualStr)
		#print(yieldOwnerDetailTotalsExpectedStr)
		self.maxDiffr=None
		self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
	
	def testAndAnalyseComputeDepositsYields(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. The other owners have each one two
		deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc_analysis.xlsx'
		depositSheetFileName = 'testDepositUsdc_analysis.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(
			yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2020-12-22 09:00:00  Earnings     USDC        2.40
2020-12-23 09:00:00  Earnings     USDC        2.30
2020-12-24 09:00:00  Earnings     USDC        2.25
2020-12-25 09:00:00  Earnings     USDC        2.50
2020-12-26 09:00:00  Earnings     USDC        2.43
2020-12-27 09:00:00  Earnings     USDC        2.43
2020-12-28 09:00:00  Earnings     USDC        3.40
2020-12-29 09:00:00  Earnings     USDC        3.50
2020-12-30 09:00:00  Earnings     USDC        4.00
TOTAL                                        25.21'''
		
		#self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		print(sbEarningsTotalDfActualStr)
		
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerSummaryTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR YIELD AMOUNT\n' + \
'OWNER                        ' + \
'''
Béa     1,000.00   0.40317663
JPS     5,100.00  11.33751104
Papa    3,800.00  13.44900699
TOTAL   9,900.00  25.18969467'''
		
		# self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		print(yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = yieldOwnerDetailTotals.to_string()
		
		if os.name == 'posix':
			yieldOwnerDetailTotalsExpectedStr = \
'      OWNER  DEP/WITHDR CAPITAL        FROM          TO YIELD DAYS  YIELD AMOUNT\n' + \
'IDX                                                                             ' + \
'''
1       Béa      1000.0    1000  2020-12-29  2020-12-30          1      0.686957
2       JPS      2000.0    2000  2020-12-22  2020-12-21          1      0.800000
3       JPS       100.0    2100  2020-12-23  2020-12-27          5      4.464337
4       JPS      3000.0    5100  2020-12-28  2020-12-30          3      6.073174
5      Papa      4000.0    4000  2020-12-22  2020-12-22          1      1.600000
6      Papa      -500.0    3500  2020-12-23  2020-12-28          6      8.824920
7      Papa       300.0    3800  2020-12-29  2020-12-30          2      3.024087
TOTAL            9900.0                                                25.189695'''
		else:
			yieldOwnerDetailTotalsExpectedStr = \
'      OWNER  DEP/WITHDR CAPITAL        FROM          TO YIELD DAYS  YIELD AMOUNT\n' + \
'IDX                                                                             ' + \
'''
1       Béa      1000.0  1000.0  2020-12-30  2020-12-30          1      0.403177
2       JPS      2000.0  2000.0  2020-12-22  2020-12-22          1      0.800000
3       JPS       100.0  2100.0  2020-12-23  2020-12-27          5      4.464337
4       JPS      3000.0  5100.0  2020-12-28  2020-12-30          3      6.073174
5      Papa      4000.0  4000.0  2020-12-22  2020-12-22          1      1.600000
6      Papa      -500.0  3500.0  2020-12-23  2020-12-28          6      8.824920
7      Papa       300.0  3800.0  2020-12-29  2020-12-30          2      3.024087
TOTAL            9900.0                                                25.189695'''
		print(yieldOwnerDetailTotalsActualStr)
		print(yieldOwnerDetailTotalsExpectedStr)
		#self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
	
	def testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_before_first_yield(self):
		"""
		Only one owner with 1 deposit done on date before the first paid yield. The case
		when running the app on a Swissborg account statement spreadsheet required
		with a date from after the first yield farming deposit(s).
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_before_first_yield.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2021-01-01 09:00:00  Earnings     USDC  8.32237146
2021-01-02 09:00:00  Earnings     USDC  9.03544811
2021-01-03 09:00:00  Earnings     USDC  9.79285984
2021-01-04 09:00:00  Earnings     USDC  7.78065008
2021-01-05 09:00:00  Earnings     USDC 10.84835651
TOTAL                                  45.77968601'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerSummaryTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR YIELD AMOUNT\n' + \
'OWNER                        ' + \
'''
JPS    19,571.69  45.77968601
TOTAL  19,571.69  45.77968601'''
		
		if PRINT:
			print(yieldOwnerSummaryTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerDetailTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerDetailTotalsExpectedStr = \
'      OWNER DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS YIELD AMOUNT\n' + \
'IDX                                                                             ' + \
'''
1       JPS  19,571.69 19,571.69  2021-01-01  2021-01-05          5  45.77968601
TOTAL        19,571.69                                               45.77968601'''

		if PRINT:
			print(yieldOwnerDetailTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
	
	def testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_on_first_yield(self):
		"""
		Only one owner with 1 deposit done on same date as date of the first paid
		yield.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_on_first_yield.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2021-01-01 09:00:00  Earnings     USDC  8.32237146
2021-01-02 09:00:00  Earnings     USDC  9.03544811
2021-01-03 09:00:00  Earnings     USDC  9.79285984
2021-01-04 09:00:00  Earnings     USDC  7.78065008
2021-01-05 09:00:00  Earnings     USDC 10.84835651
TOTAL                                  45.77968601'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerSummaryTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR YIELD AMOUNT\n' + \
'OWNER                        ' + \
'''
JPS    19,571.69  45.77968601
TOTAL  19,571.69  45.77968601'''
		
		if PRINT:
			print(yieldOwnerSummaryTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerDetailTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerDetailTotalsExpectedStr = \
'      OWNER DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS YIELD AMOUNT\n' + \
'IDX                                                                             ' + \
'''
1       JPS  19,571.69 19,571.69  2021-01-01  2021-01-05          5  45.77968601
TOTAL        19,571.69                                               45.77968601'''
		
		if PRINT:
			print(yieldOwnerDetailTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
		
	def testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_after_first_yield(self):
		"""
		Only one owner with 1 deposit done on date after the first paid yield. The case
		when running the app on a Swissborg account statement spreadsheet required
		with a date from after the first yield farming deposits.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_after_first_yield.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_after_first_yield.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.14f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency        Net amount\n' + \
'Local time                                              ' + \
'''
2021-01-01 09:00:00  Earnings     USDC  0.00000000000000
2021-01-02 09:00:00  Earnings     USDC  0.00000000000000
2021-01-03 09:00:00  Earnings     USDC 11.72113358800560
2021-01-04 09:00:00  Earnings     USDC  8.58611000467863
2021-01-05 09:00:00  Earnings     USDC 11.58738852718670
TOTAL                                  31.89463211987093'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerSummaryTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR      YIELD AMOUNT\n' + \
'OWNER                             ' + \
'''
JPS    19,571.69 31.89463211987095
TOTAL  19,571.69 31.89463211987095'''
		
		if PRINT:
			print(yieldOwnerSummaryTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerDetailTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		
		yieldOwnerDetailTotalsExpectedStr = \
'      OWNER DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS      YIELD AMOUNT\n' + \
'IDX                                                                                  ' + \
'''
1       JPS  19,571.69 19,571.69  2021-01-03  2021-01-05          3 31.89463211987095
TOTAL        19,571.69                                              31.89463211987095'''
		
		if PRINT:
			print(yieldOwnerDetailTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
	
	def testAndAnalyseComputeDepositsYields_uniqueOwner_2_deposit(self):
		"""
		Only one owner with 2 deposits.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_2_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_2_deposit.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.14f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency        Net amount\n' + \
'Local time                                              ' + \
'''
2021-01-01 09:00:00  Earnings     USDC 10.98076808766560
2021-01-02 09:00:00  Earnings     USDC 14.96650972927810
2021-01-03 09:00:00  Earnings     USDC 12.64753912157900
2021-01-04 09:00:00  Earnings     USDC  9.83496631365051
2021-01-05 09:00:00  Earnings     USDC 14.99462415730880
TOTAL                                  63.42440740948201'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerSummaryTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR      YIELD AMOUNT\n' + \
'OWNER                             ' + \
'''
JPS    24,571.69 63.42440740948223
TOTAL  24,571.69 63.42440740948223'''
		
		if PRINT:
			print(yieldOwnerSummaryTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerDetailTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		
		yieldOwnerDetailTotalsExpectedStr = \
'      OWNER DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS      YIELD AMOUNT\n' + \
'IDX                                                                                  ' + \
'''
1       JPS  19,571.69 19,571.69  2021-01-01  2021-01-01          1 10.98076808766564
2       JPS   5,000.00 24,582.67  2021-01-02  2021-01-05          4 52.44363932181659
TOTAL        24,571.69                                              63.42440740948223'''
		
		if PRINT:
			print(yieldOwnerDetailTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
		
	def testAndAnalyseComputeDepositsYields_uniqueOwner_3_deposit(self):
		"""
		Only one owner with 3 deposits.
		"""
		PRINT = True
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_3_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_3_deposit.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.14f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency        Net amount\n' + \
'Local time                                              ' + \
'''
2021-01-01 09:00:00  Earnings     USDC 10.98076808766560
2021-01-02 09:00:00  Earnings     USDC 14.96650972927810
2021-01-03 09:00:00  Earnings     USDC 12.64753912157900
2021-01-04 09:00:00  Earnings     USDC  9.83496631365051
2021-01-05 09:00:00  Earnings     USDC 14.99462415730880
TOTAL                                  63.42440740948201'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerSummaryTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR      YIELD AMOUNT\n' + \
'OWNER                             ' + \
'''
JPS    24,571.69 63.42440740948223
TOTAL  24,571.69 63.42440740948223'''
		
		if PRINT:
			print(yieldOwnerSummaryTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerDetailTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		
		yieldOwnerDetailTotalsExpectedStr = \
'      OWNER DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS      YIELD AMOUNT\n' + \
'IDX                                                                                  ' + \
'''
1       JPS  19,571.69 19,571.69  2021-01-01  2021-01-01          1 10.98076808766564
2       JPS   5,000.00 24,582.67  2021-01-02  2021-01-05          4 52.44363932181659
TOTAL        24,571.69                                              63.42440740948223'''
		
		if PRINT:
			print(yieldOwnerDetailTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)
	
	def testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_1_withdr(self):
		"""
		Only one owner with 1 deposit and 1 withdrawal.
		"""
		PRINT = True
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_1_withdr.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_1_withdr.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		yieldOwnerSummaryTotals, yieldOwnerDetailTotals = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2021-01-01 09:00:00  Earnings     USDC  8.32237146
2021-01-02 09:00:00  Earnings     USDC  9.03544811
2021-01-03 09:00:00  Earnings     USDC  9.79285984
2021-01-04 09:00:00  Earnings     USDC  7.78065008
2021-01-05 09:00:00  Earnings     USDC 10.84835651
TOTAL                                  45.77968601'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerSummaryTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerSummaryTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerSummaryTotalsExpectedStr = \
'      DEP/WITHDR YIELD AMOUNT\n' + \
'OWNER                        ' + \
'''
JPS    19,571.69  45.77968601
TOTAL  19,571.69  45.77968601'''
		
		if PRINT:
			print(yieldOwnerSummaryTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerSummaryTotalsExpectedStr, yieldOwnerSummaryTotalsActualStr)
		
		yieldOwnerDetailTotalsActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerDetailTotals,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerDetailTotalsExpectedStr = \
'      OWNER DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS YIELD AMOUNT\n' + \
'IDX                                                                             ' + \
'''
1       JPS  19,571.69 19,571.69  2021-01-01  2021-05-01        121  45.77968601
TOTAL        19,571.69                                               45.77968601'''

		if PRINT:
			print(yieldOwnerDetailTotalsActualStr)
		else:
			self.assertEqual(yieldOwnerDetailTotalsExpectedStr, yieldOwnerDetailTotalsActualStr)

if __name__ == '__main__':
	# unittest.main()
	tst = TestOwnerDepositYieldComputer()
	# tst.testComputeDepositsYieldsSeveralOwners()
	# tst.testComputeDepositsYieldsLastDepositRowUniqueOwnerTwoDeposits()
	# tst.testComputeDepositsYieldsMiddleDepositRowUniqueOwnerTwoDeposits()
	# tst.testComputeDepositsYieldsFirstDepositRowUniqueOwnerThreeDeposits()
	# tst.testComputeDepositsYieldsLastDepositRowUniqueOwnerThreeDeposits()
	# tst.testComputeDepositsYieldsMiddleDepositRowUniqueOwnerThreeDeposits()
	# tst.testComputeDepositsYieldsFirstDepositDateFromIsMaxRowUniqueOwnerThreeDeposits()
	# tst.testComputeDepositsYieldsLastDepositDateFromIsMaxRowUniqueOwnerThreeDeposits()
	# tst.testComputeDepositsYieldsMiddleDepositDateFromIsMaxRowUniqueOwnerThreeDeposits()
	# tst.testComputeDepositsYieldsFirstDepositDateFromIsMaxRowUniqueOwnerThreeDepositsDepositDateFromIsMax()
	# tst.testComputeDepositsYieldsLastDepositDateFromIsMaxRowUniqueOwnerThreeDepositsDepositDateFromIsMax()
	# tst.testComputeDepositsYieldsMiddleDepositDateFromIsMaxRowUniqueOwnerThreeDepositsDepositDateFromIsMax()
	# tst.testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_1()
	# tst.testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_2()
	# tst.testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_3()
	# tst.testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_4()
	# tst.testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_5()
	# tst.testComputeDepositsYieldsMiddleDepositDateFromIsAfterMaxRowUniqueOwnerThreeDepositsDepositDateFromAfterMax_6()
	# tst.testAndAnalyseComputeDepositsYields()
	# tst.testAndAnalyseComputeDepositsYields_dep_1()
	# tst.testAndAnalyseComputeDepositsYields_dep_2()
	# tst.testAndAnalyseComputeDepositsYields_dep_3()
	# tst.testAndAnalyseComputeDepositsYields_dep_2()
	# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_before_first_yield()
	# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_on_first_yield()
	# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_after_first_yield()
	# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_2_deposit()
	tst.testAndAnalyseComputeDepositsYields_uniqueOwner_3_deposit()
	# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_1_withdr()

