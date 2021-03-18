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
	
	def testComputeDepositsYieldsFirstDepositRowUniqueOwnerTwoDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to start with an owner having only one deposit. The other owners have each one two
		deposits.
		"""
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)

		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
	                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
	                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		#		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)
		
		print(depositSheetFileName)
		_, yieldRateDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(yieldRateDataframe,
		                                                                 {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame,
		                                                                 {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                                                  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))
		print(yieldOwnerDetailTotals)
		print(yieldOwnerSummaryTotals)
	
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
		
		depositsYieldsDataFrame, yieldOwnerSummaryTotals, yieldOwnerDetailTotals = self.ownerDepositYieldComputer.computeDepositsYields(
			yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		actualStrDataframe = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(sbEarningsTotalDf,
		                                                                                        {
			                                                                                        DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		expectedStrDataframe = \
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
		
		self.assertEqual(expectedStrDataframe, actualStrDataframe)
		
		actualStrDataframe = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(yieldOwnerSummaryTotals,
		                                                                                        {
			                                                                                        DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
			                                                                                        DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		expectedStrDataframe = \
'      DEP/WITHDR YIELD AMOUNT\n' + \
'OWNER                        ' + \
'''
Béa     1,000.00   0.40317663
JPS     5,100.00  11.33751104
Papa    3,800.00  13.44900699
TOTAL   9,900.00  25.18969467'''

		self.assertEqual(expectedStrDataframe, actualStrDataframe)

		actualStrDataframe = yieldOwnerDetailTotals.to_string()
		
		if os.name == 'posix':
			expectedStrDataframe = \
'      OWNER  DEP/WITHDR CAPITAL        FROM          TO YIELD DAYS  YIELD AMOUNT\n' + \
'IDX                                                                             ' + \
'''
1       Béa      1000.0    1000  2020-12-30  2020-12-30          1      0.403177
2       JPS      2000.0    2000  2020-12-22  2020-12-22          1      0.800000
3       JPS       100.0    2100  2020-12-23  2020-12-27          5      4.464337
4       JPS      3000.0    5100  2020-12-28  2020-12-30          3      6.073174
5      Papa      4000.0    4000  2020-12-22  2020-12-22          1      1.600000
6      Papa      -500.0    3500  2020-12-23  2020-12-28          6      8.824920
7      Papa       300.0    3800  2020-12-29  2020-12-30          2      3.024087
TOTAL            9900.0                                                25.189695'''
		else:
			expectedStrDataframe = \
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
		self.assertEqual(expectedStrDataframe, actualStrDataframe)


if __name__ == '__main__':
	#unittest.main()
	tst = TestOwnerDepositYieldComputer()
	# tst.testComputeDepositsYieldsFirstDepositRowUniqueOwnerTwoDeposits()
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
	tst.testAndAnalyseComputeDepositsYields()
