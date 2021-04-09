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
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f',
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.14f',
				MERGED_SHEET_HEADER_YEARLY_YIELD_RATE: '.14f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'            EARNING CAP           EARNING     D YIELD RATE     Y YIELD RATE\n' + \
'DATE                                                                       ' + \
'''
2020-12-22      2000.00  0.80000000000000 1.00040000000000 1.15716240742315
2020-12-23      2000.80  0.81000000000000 1.00040483806477 1.15920681502544
2020-12-24      2001.61  0.82000000000000 1.00040967021548 1.16125231895822
2020-12-25      7002.43  0.78000000000000 1.00011138990322 1.04149278109388
2020-12-26      7003.21  2.80000000000000 1.00039981665551 1.15708500280257
2020-12-27      6506.01  2.70000000000000 1.00041500089917 1.16351303351960
2020-12-28      9508.71  2.75000000000000 1.00028920852566 1.11131705748685
2020-12-29      9511.46  4.00000000000000 1.00042054532112 1.16586905001583
2020-12-30      9515.46  4.10000000000000 1.00043087775052 1.17027235821340
TOTAL           9519.56 19.56000000000000                                  '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
Béa     1,000.00  2.06858041  1002.068580
JPS     5,000.00  9.99536474  5009.995365
Papa    3,500.00  7.49605486  3507.496055
TOTAL   9,500.00 19.56000000  9519.560000'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
Béa       1,000.00 1,000.00  2020-12-25  2020-12-30          6  2.06858041     0.206858  13.395176
TOTAL     1,002.07                                              2.06858041                        ''' \
'''
JPS       2,000.00 2,000.00  2020-12-22  2020-12-27          6  4.28517963     0.214259  13.905782
JPS       3,000.00 5,004.29  2020-12-28  2020-12-30          3  5.71018510     0.114106  14.883652
TOTAL     5,010.00                                              9.99536474                        ''' + \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-26          2  2.04500438     0.051125   9.776850
Papa       -500.00 3,502.05  2020-12-27  2020-12-30          4  5.45105048     0.155653  15.248820
TOTAL     3,507.50                                              7.49605486                        ''' + \
'''
G TOTAL   9,519.56                                             19.56000000                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsLastDepositRowUniqueOwnerTwoDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. The other owners have each one two
		deposits.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_2.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
JPS     5,000.00  9.99536474  5009.995365
Papa    3,500.00  7.49605486  3507.496055
Zoé     1,000.00  2.06858041  1002.068580
TOTAL   9,500.00 19.56000000  9519.560000'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
JPS       2,000.00 2,000.00  2020-12-22  2020-12-27          6  4.28517963     0.214259  13.905782
JPS       3,000.00 5,004.29  2020-12-28  2020-12-30          3  5.71018510     0.114106  14.883652
TOTAL     5,010.00                                              9.99536474                        ''' \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-26          2  2.04500438     0.051125   9.776850
Papa       -500.00 3,502.05  2020-12-27  2020-12-30          4  5.45105048     0.155653  15.248820
TOTAL     3,507.50                                              7.49605486                        ''' + \
'''
Zoé       1,000.00 1,000.00  2020-12-25  2020-12-30          6  2.06858041     0.206858  13.395176
TOTAL     1,002.07                                              2.06858041                        ''' + \
'''
G TOTAL   9,519.56                                             19.56000000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsMiddleDepositRowUniqueOwnerTwoDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to have the owner having only one deposit to be located in the middle of the
		deposit table. The other owners have each one two deposits.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_3.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
JPS     5,000.00  9.99536474  5009.995365
Loan    1,000.00  2.06858041  1002.068580
Papa    3,500.00  7.49605486  3507.496055
TOTAL   9,500.00 19.56000000  9519.560000'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
JPS       2,000.00 2,000.00  2020-12-22  2020-12-27          6  4.28517963     0.214259  13.905782
JPS       3,000.00 5,004.29  2020-12-28  2020-12-30          3  5.71018510     0.114106  14.883652
TOTAL     5,010.00                                              9.99536474                        ''' \
'''
Loan      1,000.00 1,000.00  2020-12-25  2020-12-30          6  2.06858041     0.206858  13.395176
TOTAL     1,002.07                                              2.06858041                        ''' + \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-26          2  2.04500438     0.051125   9.776850
Papa       -500.00 3,502.05  2020-12-27  2020-12-30          4  5.45105048     0.155653  15.248820
TOTAL     3,507.50                                              7.49605486                        ''' + \
'''
G TOTAL   9,519.56                                             19.56000000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsFirstDepositRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to start with an owner having only one deposit. The other owners have each one three
		deposits.
		
		The first JPS deposit date is one day before he first yield payment date.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_4.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
Béa     1,000.00  2.04755022  1002.047550
JPS     5,100.00 10.04583610  5110.045836
Papa    3,800.00  7.46661368  3807.466614
TOTAL   9,900.00 19.56000000  9919.560000'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
Béa       1,000.00 1,000.00  2020-12-25  2020-12-30          6  2.04755022     0.204755  13.250496
TOTAL     1,002.05                                              2.04755022                        ''' \
'''
JPS       2,000.00 2,000.00  2020-12-21  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         100.00 2,100.00  2020-12-22  2020-12-27          6  4.41225777     0.210108  13.619086
JPS       3,000.00 5,104.41  2020-12-28  2020-12-30          3  5.63357833     0.110367  14.362793
TOTAL     5,110.05                                             10.04583610                        ''' + \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-25          1  0.43928627     0.010982   4.089682
Papa       -500.00 3,500.44  2020-12-26  2020-12-28          3  3.91827019     0.111937  14.581168
Papa        300.00 3,804.36  2020-12-29  2020-12-30          2  3.10905721     0.081724  16.077121
TOTAL     3,807.47                                              7.46661368                        ''' + \
'''
G TOTAL   9,919.56                                             19.56000000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsLastDepositRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. The JPS owner has three deposits
		with a date before the first yield payment date.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_5.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
JPS     5,650.00 10.65022348   5660.650223
Papa    3,800.00  6.99279015   3806.992790
Zoé     1,000.00  1.91698637   1001.916986
TOTAL  10,450.00 19.56000000  10469.560000'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
JPS       2,000.00 2,000.00  2020-11-15  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         300.00 2,300.00  2020-11-17  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         200.00 2,500.00  2020-11-19  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         100.00 2,600.00  2020-12-22  2020-12-22          1  0.80000000     0.030769  11.883774
JPS          50.00 2,650.80  2020-12-23  2020-12-27          5  3.93998101     0.148634  11.451799
JPS       3,000.00 5,654.74  2020-12-28  2020-12-30          3  5.91024247     0.104518  13.552786
TOTAL     5,660.65                                             10.65022348                        ''' + \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-25          1  0.40771363     0.010193   3.790263
Papa       -500.00 3,500.41  2020-12-26  2020-12-28          3  3.63971477     0.103980  13.478472
Papa        300.00 3,804.05  2020-12-29  2020-12-30          2  2.94536175     0.077427  15.171219
TOTAL     3,806.99                                              6.99279015                        ''' + \
'''
Zoé       1,000.00 1,000.00  2020-12-25  2020-12-30          6  1.91698637     0.191699  12.356317
TOTAL     1,001.92                                              1.91698637                        ''' \
'''
G TOTAL  10,469.56                                             19.56000000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsMiddleDepositRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to have the owner having only one deposit to be located in the middle of the
		deposit table. The other owners have each one three deposits.
		
		The first JPS deposit date is several days before he first yield payment date.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_6.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
JPS     5,100.00 10.04583610  5110.045836
Loan    1,000.00  2.04755022  1002.047550
Papa    3,800.00  7.46661368  3807.466614
TOTAL   9,900.00 19.56000000  9919.560000'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
JPS       2,000.00 2,000.00  2020-12-11  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         100.00 2,100.00  2020-12-22  2020-12-27          6  4.41225777     0.210108  13.619086
JPS       3,000.00 5,104.41  2020-12-28  2020-12-30          3  5.63357833     0.110367  14.362793
TOTAL     5,110.05                                             10.04583610                        ''' + \
'''
Loan      1,000.00 1,000.00  2020-12-25  2020-12-30          6  2.04755022     0.204755  13.250496
TOTAL     1,002.05                                              2.04755022                        ''' \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-25          1  0.43928627     0.010982   4.089682
Papa       -500.00 3,500.44  2020-12-26  2020-12-28          3  3.91827019     0.111937  14.581168
Papa        300.00 3,804.36  2020-12-29  2020-12-30          2  3.10905721     0.081724  16.077121
TOTAL     3,807.47                                              7.46661368                        ''' + \
'''
G TOTAL   9,919.56                                             19.56000000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsFirstDepositDateFromIsMaxRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to start with an owner having only one deposit. This unique deposit is done on the
		date of the last yield payment and so will have a 1 yield day number and a small
		yield amount. The other owners have each one three deposits.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_7.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(
			yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
Béa     1,000.00  0.36556682   1000.365567
JPS     5,000.00  7.89504282   5007.895043
Papa    5,200.00 11.29939037   5211.299390
TOTAL  11,200.00 19.56000000  11219.560000'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
Béa       1,000.00 1,000.00  2020-12-30  2020-12-30          1  0.36556682     0.036557  14.271557
TOTAL     1,000.37                                              0.36556682                        ''' + \
'''
JPS       2,000.00 2,000.00  2020-11-15  2020-12-21          0  0.00000000     0.000000   0.000000
JPS        -300.00 1,700.00  2020-11-17  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         200.00 1,900.00  2020-11-19  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         100.00 2,000.00  2020-12-22  2020-12-27          6  2.71637796     0.135819   8.607155
JPS       3,000.00 5,002.72  2020-12-28  2020-12-30          3  5.17866485     0.103517  13.414676
TOTAL     5,007.90                                              7.89504282                        ''' + \
'''
Papa      2,000.00 2,000.00  2020-11-15  2020-12-21          0  0.00000000     0.000000   0.000000
Papa       -300.00 1,700.00  2020-11-16  2020-12-21          0  0.00000000     0.000000   0.000000
Papa       -200.00 1,500.00  2020-11-19  2020-12-21          0  0.00000000     0.000000   0.000000
Papa       -100.00 1,400.00  2020-12-22  2020-12-22          1  0.32941176     0.023529   8.966712
Papa      4,000.00 5,400.33  2020-12-23  2020-12-25          3  1.75856581     0.032564   4.040821
Papa       -500.00 4,902.09  2020-12-26  2020-12-28          3  5.26722255     0.107449  13.957899
Papa        300.00 5,207.36  2020-12-29  2020-12-30          2  3.94419024     0.075743  14.817998
TOTAL     5,211.30                                             11.29939037                        ''' + \
'''
G TOTAL  11,219.56                                             19.56000000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
		
	def testComputeDepositsYieldsFirstOwner_1_only_depositBeforeFirstYieldDate(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to start with an owner having only one deposit. This unique deposit is done on
		date before the first yield payment.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_7_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(
			yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
Béa     1,000.00  2.14087863   1002.140879
JPS     5,000.00  7.20600518   5007.206005
Papa    5,200.00 10.21311619   5210.213116
TOTAL  11,200.00 19.56000000  11219.560000'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
Béa       1,000.00 1,000.00  2020-12-22  2020-12-30          9  2.14087863     0.214088   9.060405
TOTAL     1,002.14                                              2.14087863                        ''' + \
'''
JPS       2,000.00 2,000.00  2020-11-15  2020-12-21          0  0.00000000     0.000000   0.000000
JPS        -300.00 1,700.00  2020-11-17  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         200.00 1,900.00  2020-11-19  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         100.00 2,000.00  2020-12-22  2020-12-27          6  2.32998750     0.116499   7.339788
JPS       3,000.00 5,002.33  2020-12-28  2020-12-30          3  4.87601768     0.097475  12.584823
TOTAL     5,007.21                                              7.20600518                        ''' + \
'''
Papa      2,000.00 2,000.00  2020-11-15  2020-12-21          0  0.00000000     0.000000   0.000000
Papa       -300.00 1,700.00  2020-11-16  2020-12-21          0  0.00000000     0.000000   0.000000
Papa       -200.00 1,500.00  2020-11-19  2020-12-21          0  0.00000000     0.000000   0.000000
Papa       -100.00 1,400.00  2020-12-22  2020-12-22          1  0.25454545     0.018182   6.860879
Papa      4,000.00 5,400.25  2020-12-23  2020-12-25          3  1.54921120     0.028688   3.551451
Papa       -500.00 4,901.80  2020-12-26  2020-12-28          3  4.64782822     0.094819  12.221918
Papa        300.00 5,206.45  2020-12-29  2020-12-30          2  3.76153131     0.072248  14.088478
TOTAL     5,210.21                                             10.21311619                        ''' + \
'''
G TOTAL  11,219.56                                             19.56000000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
		
	def testComputeDepositsYieldsFirstOwner_1_depositBeforeAnd_1_aftertFirstYieldDate(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to start with an owner having one deposit on date before the first yield
		payment followed by 1 deposit after the first yield payment.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_7_2.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(
			yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
Béa     2,000.00  3.56803830   2003.568038
JPS     5,000.00  6.62768455   5006.627685
Papa    5,200.00  9.36427715   5209.364277
TOTAL  12,200.00 19.56000000  12219.560000'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
Béa       1,000.00 1,000.00  2020-12-22  2020-12-24          3  0.37588260     0.037588   4.678524
Béa       1,000.00 2,000.38  2020-12-25  2020-12-30          6  3.19215570     0.159578  10.185940
TOTAL     2,003.57                                              3.56803830                        ''' + \
'''
JPS       2,000.00 2,000.00  2020-11-15  2020-12-21          0  0.00000000     0.000000   0.000000
JPS        -300.00 1,700.00  2020-11-17  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         200.00 1,900.00  2020-11-19  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         100.00 2,000.00  2020-12-22  2020-12-27          6  2.15381850     0.107691   6.766789
JPS       3,000.00 5,002.15  2020-12-28  2020-12-30          3  4.47386605     0.089439  11.490429
TOTAL     5,006.63                                              6.62768455                        ''' + \
'''
Papa      2,000.00 2,000.00  2020-11-15  2020-12-21          0  0.00000000     0.000000   0.000000
Papa       -300.00 1,700.00  2020-11-16  2020-12-21          0  0.00000000     0.000000   0.000000
Papa       -200.00 1,500.00  2020-11-19  2020-12-21          0  0.00000000     0.000000   0.000000
Papa       -100.00 1,400.00  2020-12-22  2020-12-22          1  0.25454545     0.018182   6.860879
Papa      4,000.00 5,400.25  2020-12-23  2020-12-25          3  1.49588409     0.027700   3.427149
Papa       -500.00 4,901.75  2020-12-26  2020-12-28          3  4.16070767     0.084882  10.874572
Papa        300.00 5,205.91  2020-12-29  2020-12-30          2  3.45313994     0.066331  12.864093
TOTAL     5,209.36                                              9.36427715                        ''' + \
'''
G TOTAL  12,219.56                                             19.56000000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsLastDepositDateFromIsMaxRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to have the owner having only one deposit to be located in the end of the
		deposit table. This unique deposit is done on the date of the last yield payment
		and so will have a 1 yield day number and a small yield amount. The other owners
		have each one three deposits.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_8.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(
			yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
JPS     5,100.00 10.79785741  5110.797857
Papa    3,800.00  8.34864690  3808.348647
Zoé     1,000.00  0.41349569  1000.413496
TOTAL   9,900.00 19.56000000  9919.560000'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
JPS       2,000.00 2,000.00  2020-12-21  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         100.00 2,100.00  2020-12-22  2020-12-27          6  4.76269570     0.226795  14.775833
JPS       3,000.00 5,104.76  2020-12-28  2020-12-30          3  6.03516170     0.118226  15.460326
TOTAL     5,110.80                                             10.79785741                        ''' + \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-25          1  0.51127174     0.012782   4.775582
Papa       -500.00 3,500.51  2020-12-26  2020-12-28          3  4.55534719     0.130134  17.143148
Papa        300.00 3,805.07  2020-12-29  2020-12-30          2  3.28202797     0.086254  17.040048
TOTAL     3,808.35                                              8.34864690                        ''' + \
'''
Zoé       1,000.00 1,000.00  2020-12-30  2020-12-30          1  0.41349569     0.041350  16.287424
TOTAL     1,000.41                                              0.41349569                        ''' \
'''
G TOTAL   9,919.56                                             19.56000000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsMiddleDepositDateFromIsMaxRowUniqueOwnerThreeDeposits(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		with an owner having only one deposit in the middle. This unique deposit is done on the
		date of the last yield payment and so will have 1 yield day number and a small yield
		amount. The other owners have each one three deposits.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_9.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(
			yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
JPS     5,100.00 10.79785741  5110.797857
Loan    1,000.00  0.41349569  1000.413496
Papa    3,800.00  8.34864690  3808.348647
TOTAL   9,900.00 19.56000000  9919.560000'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
JPS       2,000.00 2,000.00  2020-12-21  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         100.00 2,100.00  2020-12-22  2020-12-27          6  4.76269570     0.226795  14.775833
JPS       3,000.00 5,104.76  2020-12-28  2020-12-30          3  6.03516170     0.118226  15.460326
TOTAL     5,110.80                                             10.79785741                        ''' + \
'''
Loan      1,000.00 1,000.00  2020-12-30  2020-12-30          1  0.41349569     0.041350  16.287424
TOTAL     1,000.41                                              0.41349569                        ''' \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-25          1  0.51127174     0.012782   4.775582
Papa       -500.00 3,500.51  2020-12-26  2020-12-28          3  4.55534719     0.130134  17.143148
Papa        300.00 3,805.07  2020-12-29  2020-12-30          2  3.28202797     0.086254  17.040048
TOTAL     3,808.35                                              8.34864690                        ''' + \
'''
G TOTAL   9,919.56                                             19.56000000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsFirstDepositDateFromIsMaxRowUniqueOwnerThreeDepositsDepositDateFromIsMax(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to start with an owner having only one deposit. This unique deposit is done on the
		date of the last yield payment and so will have 1 yield day number and a small yield
		amount. The other owners have each one three deposits, one of them done on the
		date of the last yield payment.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_10.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
			
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f',
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.14f',
				MERGED_SHEET_HEADER_YEARLY_YIELD_RATE: '.14f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'            EARNING CAP           EARNING     D YIELD RATE     Y YIELD RATE\n' + \
'DATE                                                                       ' + \
'''
2020-12-22      5000.00  0.80000000000000 1.00016000000000 1.06013401406762
2020-12-23      5000.80  0.81000000000000 1.00016197408415 1.06089803601031
2020-12-24      5001.61  0.82000000000000 1.00016394720900 1.06166223538982
2020-12-25      9002.43  0.78000000000000 1.00008664327298 1.03212875789612
2020-12-26      8503.21  2.80000000000000 1.00032928741028 1.12768867832013
2020-12-27      8506.01  2.70000000000000 1.00031742262236 1.12281718724729
2020-12-28      8508.71  2.75000000000000 1.00032319822864 1.12518593115677
2020-12-29      8511.46  4.00000000000000 1.00046995462588 1.18707600482800
2020-12-30      9915.46  4.10000000000000 1.00041349569259 1.16287423910268
TOTAL           9919.56 19.56000000000000                                  '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
Béa     1,000.00  0.41349569  1000.413496
JPS     5,100.00 12.18370638  5112.183706
Papa    3,800.00  6.96279792  3806.962798
TOTAL   9,900.00 19.56000000  9919.560000'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
Béa       1,000.00 1,000.00  2020-12-30  2020-12-30          1  0.41349569     0.041350  16.287424
TOTAL     1,000.41                                              0.41349569                        ''' \
'''
JPS       2,000.00 2,000.00  2020-12-21  2020-12-21          0  0.00000000     0.000000   0.000000
JPS       3,000.00 5,000.00  2020-12-22  2020-12-29          8 10.07071415     0.201414   9.614869
JPS         100.00 5,110.07  2020-12-30  2020-12-30          1  2.11299223     0.041350  16.287424
TOTAL     5,112.18                                             12.18370638                        ''' + \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-25          1  0.34657309     0.008664   3.212876
Papa       -500.00 3,500.35  2020-12-26  2020-12-29          4  5.04271275     0.144063  14.038179
Papa        300.00 3,805.39  2020-12-30  2020-12-30          1  1.57351208     0.041350  16.287424
TOTAL     3,806.96                                              6.96279792                        ''' + \
'''
G TOTAL   9,919.56                                             19.56000000                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsLastDepositDateFromIsMaxRowUniqueOwnerThreeDepositsDepositDateFromIsMax(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to have the owner having only one deposit to be located in the middle of the
		deposit table. This unique deposit is done on the date of the last yield payment
		and so will have 1 yield day number and a small yield	amount. The other owners have
		each one three deposits, one of them done on the date of the last yield payment.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_11.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f',
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.14f',
				MERGED_SHEET_HEADER_YEARLY_YIELD_RATE: '.14f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'            EARNING CAP           EARNING     D YIELD RATE     Y YIELD RATE\n' + \
'DATE                                                                       ' + \
'''
2020-12-22      5000.00  0.80000000000000 1.00016000000000 1.06013401406762
2020-12-23      5000.80  0.81000000000000 1.00016197408415 1.06089803601031
2020-12-24      5001.61  0.82000000000000 1.00016394720900 1.06166223538982
2020-12-25      9002.43  0.78000000000000 1.00008664327298 1.03212875789612
2020-12-26      8503.21  2.80000000000000 1.00032928741028 1.12768867832013
2020-12-27      8506.01  2.70000000000000 1.00031742262236 1.12281718724729
2020-12-28      8508.71  2.75000000000000 1.00032319822864 1.12518593115677
2020-12-29      8511.46  4.00000000000000 1.00046995462588 1.18707600482800
2020-12-30      9915.46  4.10000000000000 1.00041349569259 1.16287423910268
TOTAL           9919.56 19.56000000000000                                  '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
JPS     5,100.00 12.18370638  5112.183706
Papa    3,800.00  6.96279792  3806.962798
Zoé     1,000.00  0.41349569  1000.413496
TOTAL   9,900.00 19.56000000  9919.560000'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
JPS       2,000.00 2,000.00  2020-12-21  2020-12-21          0  0.00000000     0.000000   0.000000
JPS       3,000.00 5,000.00  2020-12-22  2020-12-29          8 10.07071415     0.201414   9.614869
JPS         100.00 5,110.07  2020-12-30  2020-12-30          1  2.11299223     0.041350  16.287424
TOTAL     5,112.18                                             12.18370638                        ''' + \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-25          1  0.34657309     0.008664   3.212876
Papa       -500.00 3,500.35  2020-12-26  2020-12-29          4  5.04271275     0.144063  14.038179
Papa        300.00 3,805.39  2020-12-30  2020-12-30          1  1.57351208     0.041350  16.287424
TOTAL     3,806.96                                              6.96279792                        ''' + \
'''
Zoé       1,000.00 1,000.00  2020-12-30  2020-12-30          1  0.41349569     0.041350  16.287424
TOTAL     1,000.41                                              0.41349569                        ''' \
'''
G TOTAL   9,919.56                                             19.56000000                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testComputeDepositsYieldsMiddleDepositDateFromIsMaxRowUniqueOwnerThreeDepositsDepositDateFromIsMax(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. This unique deposit is done on the
		date of the last yield payment and so will have 1 yield day number and a small yield
		amount. The other owners have each one three deposits, one of them done on the
		date of the last yield payment.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_12.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f',
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.14f',
				MERGED_SHEET_HEADER_YEARLY_YIELD_RATE: '.14f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'            EARNING CAP           EARNING     D YIELD RATE     Y YIELD RATE\n' + \
'DATE                                                                       ' + \
'''
2020-12-22      5000.00  0.80000000000000 1.00016000000000 1.06013401406762
2020-12-23      5000.80  0.81000000000000 1.00016197408415 1.06089803601031
2020-12-24      5001.61  0.82000000000000 1.00016394720900 1.06166223538982
2020-12-25      9002.43  0.78000000000000 1.00008664327298 1.03212875789612
2020-12-26      8503.21  2.80000000000000 1.00032928741028 1.12768867832013
2020-12-27      8506.01  2.70000000000000 1.00031742262236 1.12281718724729
2020-12-28      8508.71  2.75000000000000 1.00032319822864 1.12518593115677
2020-12-29      8511.46  4.00000000000000 1.00046995462588 1.18707600482800
2020-12-30      9915.46  4.10000000000000 1.00041349569259 1.16287423910268
TOTAL           9919.56 19.56000000000000                                  '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
JPS     5,100.00 12.18370638  5112.183706
Loan    1,000.00  0.41349569  1000.413496
Papa    3,800.00  6.96279792  3806.962798
TOTAL   9,900.00 19.56000000  9919.560000'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
JPS       2,000.00 2,000.00  2020-12-21  2020-12-21          0  0.00000000     0.000000   0.000000
JPS       3,000.00 5,000.00  2020-12-22  2020-12-29          8 10.07071415     0.201414   9.614869
JPS         100.00 5,110.07  2020-12-30  2020-12-30          1  2.11299223     0.041350  16.287424
TOTAL     5,112.18                                             12.18370638                        ''' + \
'''
Loan      1,000.00 1,000.00  2020-12-30  2020-12-30          1  0.41349569     0.041350  16.287424
TOTAL     1,000.41                                              0.41349569                        ''' + \
'''
Papa      4,000.00 4,000.00  2020-12-25  2020-12-25          1  0.34657309     0.008664   3.212876
Papa       -500.00 3,500.35  2020-12-26  2020-12-29          4  5.04271275     0.144063  14.038179
Papa        300.00 3,805.39  2020-12-30  2020-12-30          1  1.57351208     0.041350  16.287424
TOTAL     3,806.96                                              6.96279792                        ''' + \
'''
G TOTAL   9,919.56                                             19.56000000                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
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
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_19.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
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
2020-12-22 09:00:00  Earnings     USDC  0.80000000
2020-12-23 09:00:00  Earnings     USDC  0.81000000
2020-12-24 09:00:00  Earnings     USDC  0.82000000
2020-12-25 09:00:00  Earnings     USDC  0.78000000
2020-12-26 09:00:00  Earnings     USDC  2.80000000
2020-12-27 09:00:00  Earnings     USDC  2.70000000
2020-12-28 09:00:00  Earnings     USDC  2.75000000
2020-12-29 09:00:00  Earnings     USDC  4.00000000
2020-12-30 09:00:00  Earnings     USDC  4.10000000
TOTAL                                  19.56000000'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f',
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.14f',
				MERGED_SHEET_HEADER_YEARLY_YIELD_RATE: '.14f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'            EARNING CAP           EARNING     D YIELD RATE     Y YIELD RATE\n' + \
'DATE                                                                       ' + \
'''
2020-12-22      5600.00  0.80000000000000 1.00014285714286 1.05352231204482
2020-12-23      5600.80  0.81000000000000 1.00014462219683 1.05420115928152
2020-12-24      5601.61  0.82000000000000 1.00014638648531 1.05488014804745
2020-12-25      5602.43  0.78000000000000 1.00013922530045 1.05212686112719
2020-12-26      5603.21  2.80000000000000 1.00049971355705 1.20003400124187
2020-12-27      5606.01  2.70000000000000 1.00048162596927 1.19214136811120
2020-12-28      8608.71  2.75000000000000 1.00031944391204 1.12364561066504
2020-12-29      8911.46  4.00000000000000 1.00044886023166 1.17797542840651
2020-12-30      9915.46  4.10000000000000 1.00041349569259 1.16287423910268
TOTAL           9919.56 19.56000000000000                                  '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
Béa     1,000.00  0.41349569  1000.413496
JPS     5,100.00  9.29964252  5109.299643
Papa    3,800.00  9.84686179  3809.846862
TOTAL   9,900.00 19.56000000  9919.560000'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
Béa       1,000.00 1,000.00  2020-12-30  2020-12-30          1  0.41349569     0.041350  16.287424
TOTAL     1,000.41                                              0.41349569                        ''' + \
'''
JPS       2,000.00 2,000.00  2020-12-21  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         100.00 2,100.00  2020-12-22  2020-12-27          6  3.26625000     0.155536   9.915758
JPS       3,000.00 5,103.27  2020-12-28  2020-12-30          3  6.03339252     0.118226  15.460326
TOTAL     5,109.30                                              9.29964252                        ''' + \
'''
Papa      4,000.00 4,000.00  2020-12-21  2020-12-21          0  0.00000000     0.000000   0.000000
Papa       -500.00 3,500.00  2020-12-22  2020-12-28          7  6.56354266     0.187530  10.262292
Papa        300.00 3,806.56  2020-12-29  2020-12-30          2  3.28331913     0.086254  17.040048
TOTAL     3,809.85                                              9.84686179                        ''' + \
'''
G TOTAL   9,919.56                                             19.56000000                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testAndAnalyseComputeDepositsYields_dep_1(self):
		"""
		Only one owner with one deposit.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSBEarningUsdc_analysis_dep_1_2.xlsx'
		depositSheetFileName = 'testDepositUsdc_analysis_dep_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
		
		if PRINT:
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
			
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(yieldOwnerWithTotalsSummaryDf,
		                                                                                        {
			                                                                                        DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
			                                                                                        DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT        TOTAL\n' + \
'OWNER                                    ' + \
'''
JPS    19,571.69 87.39209000  19659.08209
TOTAL  19,571.69 87.39209000  19659.08209'''

		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                              ' + \
'''
JPS      19,571.69 19,571.69  2020-12-22  2020-12-31         10 87.39209000     0.446523  17.658725
TOTAL    19,659.08                                              87.39209000                        ''' + \
'''
G TOTAL  19,659.08                                              87.39209000                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testAndAnalyseComputeDepositsYields_dep_2(self):
		"""
		Two owners with one deposit each starting at same date.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSBEarningUsdc_analysis_dep_1_2.xlsx'
		depositSheetFileName = 'testDepositUsdc_analysis_dep_2.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
			
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f',
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.14f',
				MERGED_SHEET_HEADER_YEARLY_YIELD_RATE: '.14f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP           EARNING     D YIELD RATE     Y YIELD RATE\n' + \
'DATE                                                                        ' + \
'''
2020-12-22  19571.690000  9.37935200000000 1.00047923056210 1.19110000636782
2020-12-23  19581.069352  8.90406500000000 1.00045472822959 1.18050000088884
2020-12-24  19589.973417  9.34752500000000 1.00047715863626 1.19020000422810
2020-12-25  19599.320942  9.39259300000000 1.00047923053190 1.19109999324535
2020-12-26  19608.713535  8.59240700000000 1.00043819330547 1.17340000795736
2020-12-27  19617.305942  8.29288400000000 1.00042273307173 1.16680000935365
2020-12-28  19625.598826  8.31021800000000 1.00042343767819 1.16710000021616
2020-12-29  19633.909044  8.31373700000000 1.00042343768535 1.16710000326509
2020-12-30  19642.222781  8.45546700000000 1.00043047404025 1.17010000053656
2020-12-31  19650.678248  8.40384200000000 1.00042766167630 1.16890000874786
TOTAL       19659.082090 87.39209000000000                                  '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
	
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
JPS     4,975.64 22.21737513   4997.857375
Papa   14,596.05 65.17471487  14661.224715
TOTAL  19,571.69 87.39209000  19659.082090'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                              ' + \
'''
JPS       4,975.64  4,975.64  2020-12-22  2020-12-31         10 22.21737513     0.446523  17.658725
TOTAL     4,997.86                                              22.21737513                        ''' + \
'''
Papa     14,596.05 14,596.05  2020-12-22  2020-12-31         10 65.17471487     0.446523  17.658725
TOTAL    14,661.22                                              65.17471487                        ''' + \
'''
G TOTAL  19,659.08                                              87.39209000                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testAndAnalyseComputeDepositsYields_dep_3(self):
		"""
		Two owners, the first with two deposits, the second with one deposit.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSBEarningUsdc_analysis_dep_3_a.xlsx'
		depositSheetFileName = 'testDepositUsdc_analysis_dep_3.csv'

		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
			
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP    EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                           ' + \
'''
2020-12-22  17338.320000   8.309086      1.000479      1.191101
2020-12-23  19579.999086   8.904065      1.000455      1.180511
2020-12-24  19588.903151   9.347525      1.000477      1.190211
2020-12-25  19598.250676   9.392593      1.000479      1.191111
2020-12-26  19607.643269   8.592407      1.000438      1.173410
2020-12-27  19616.235676   8.292884      1.000423      1.166810
2020-12-28  19624.528560   8.310218      1.000423      1.167110
2020-12-29  19632.838778   8.313737      1.000423      1.167110
2020-12-30  19641.152515   8.455467      1.000430      1.170110
2020-12-31  19649.607982   8.403842      1.000428      1.168910
TOTAL       19658.011824  86.321824                            '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
JPS     4,975.64 21.14390099   4996.783901
Papa   14,596.05 65.17792340  14661.227923
TOTAL  19,571.69 86.32182439  19658.011824'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: '.14f',
				DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: '.14f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS   YIELD AMT      YIELD AMT %         Y YIELD %\n' + \
'OWNER                                                                                                         ' + \
'''
JPS       2,742.27  2,742.27  2020-12-22  2020-12-22          1  1.31418490 0.04792324971508 19.11008472302236
JPS       2,233.37  4,976.95  2020-12-23  2020-12-31          9 19.82971609 0.39843075403525 17.49960131498618
TOTAL     4,996.78                                              21.14390099                                   ''' + \
'''
Papa     14,596.05 14,596.05  2020-12-22  2020-12-31         10 65.17792340 0.44654494471553 17.65966487491983
TOTAL    14,661.23                                              65.17792340                                   ''' + \
'''
G TOTAL  19,658.01                                              86.32182439                                   '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testAndAnalyseComputeDepositsYields(self):
		"""
		The deposit csv file causes the deposits sorted by owner and then by deposit date
		to end with an owner having only one deposit. The other owners have each one two
		deposits.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSBEarningUsdc_analysis.xlsx'
		depositSheetFileName = 'testDepositUsdc_analysis.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = self.ownerDepositYieldComputer.computeDepositsYields(
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
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
			
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f',
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.14f',
				MERGED_SHEET_HEADER_YEARLY_YIELD_RATE: '.14f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'            EARNING CAP           EARNING     D YIELD RATE     Y YIELD RATE\n' + \
'DATE                                                                       ' + \
'''
2020-12-22      6600.00  2.40000000000000 1.00036363636364 1.14191096756715
2020-12-23      6602.40  2.30000000000000 1.00034835817279 1.13556303181785
2020-12-24      6604.70  2.25000000000000 1.00034066649507 1.13238054718992
2020-12-25      6606.95  2.50000000000000 1.00037838942326 1.14807429877768
2020-12-26      6609.45  2.43000000000000 1.00036765540249 1.14358670901265
2020-12-27      9611.88  2.43000000000000 1.00025281214497 1.09665514566168
2020-12-28      9914.31  3.40000000000000 1.00034293864122 1.13331973651396
2020-12-29     10917.71  3.50000000000000 1.00032058004838 1.12411152249952
2020-12-30     10921.21  4.00000000000000 1.00036625978257 1.14300452642022
TOTAL          10925.21 25.21000000000000                                  '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
Béa     1,000.00  0.68695725   1000.686957
JPS     5,100.00 10.32919115   5110.329191
Papa    4,800.00 14.19385160   4814.193852
TOTAL  10,900.00 25.21000000  10925.210000'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
			
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR  CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                             ' + \
'''
Béa       1,000.00 1,000.00  2020-12-29  2020-12-30          2  0.68695725     0.068696  13.351866
TOTAL     1,000.69                                              0.68695725                        ''' + \
'''
JPS       2,000.00 2,000.00  2020-12-21  2020-12-21          0  0.00000000     0.000000   0.000000
JPS         100.00 2,100.00  2020-12-22  2020-12-26          5  3.78000000     0.180000  14.028916
JPS       3,000.00 5,103.78  2020-12-27  2020-12-30          4  6.54919115     0.128320  12.413888
TOTAL     5,110.33                                             10.32919115                        ''' + \
'''
Papa      4,000.00 4,000.00  2020-12-21  2020-12-21          0  0.00000000     0.000000   0.000000
Papa        500.00 4,500.00  2020-12-22  2020-12-27          6  9.23970243     0.205327  13.289809
Papa        300.00 4,809.24  2020-12-28  2020-12-30          3  4.95414917     0.103013  13.345235
TOTAL     4,814.19                                             14.19385160                        ''' + \
'''
G TOTAL  10,925.21                                             25.21000000                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
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
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
JPS    19,571.69 45.77968601  19617.469686
TOTAL  19,571.69 45.77968601  19617.469686'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                              ' + \
'''
JPS      19,571.69 19,571.69  2021-01-01  2021-01-05          5 45.77968601     0.233908  18.596076
TOTAL    19,617.47                                              45.77968601                        ''' + \
'''
G TOTAL  19,617.47                                              45.77968601                        '''

		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
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
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
JPS    19,571.69 45.77968601  19617.469686
TOTAL  19,571.69 45.77968601  19617.469686'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                              ' + \
'''
JPS      19,571.69 19,571.69  2021-01-01  2021-01-05          5 45.77968601     0.233908  18.596076
TOTAL    19,617.47                                              45.77968601                        ''' + \
'''
G TOTAL  19,617.47                                              45.77968601                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
		
	def testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_after_first_yield(self):
		"""
		Only one owner with 1 deposit done on date after the first paid yield.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_after_first_yield.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_after_first_yield.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR         YIELD AMT         TOTAL\n' + \
'OWNER                                           ' + \
'''
JPS    19,571.69 31.89463211987095  19603.584632
TOTAL  19,571.69 31.89463211987095  19603.584632'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS         YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                                    ' + \
'''
JPS      19,571.69 19,571.69  2021-01-03  2021-01-05          3 31.89463211987095     0.162963  21.909696
TOTAL    19,603.58                                              31.89463211987095                        ''' + \
'''
G TOTAL  19,603.58                                              31.89463211987095                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
		
	def testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_on_last_yield(self):
		"""
		Only one owner with 3 deposits.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_on_last_yield.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_on_last_yield.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f',
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.14f',
				MERGED_SHEET_HEADER_YEARLY_YIELD_RATE: '.14f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP          EARNING     D YIELD RATE     Y YIELD RATE\n' + \
'DATE                                                                       ' + \
'''
2021-01-05  10000.000000 4.10938248077946 1.00041093824808 1.16178968743629
TOTAL       10004.109382 4.10938248077946                                  '''
		
		if PRINT:
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR        YIELD AMT         TOTAL\n' + \
'OWNER                                          ' + \
'''
JPS    10,000.00 4.10938248077946  10004.109382
TOTAL  10,000.00 4.10938248077946  10004.109382'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: '.14f',
				DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: '.14f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS        YIELD AMT      YIELD AMT %         Y YIELD %\n' + \
'OWNER                                                                                                              ' + \
'''
JPS      10,000.00 10,000.00  2021-01-05  2021-01-05          1 4.10938248077946 0.04109382480779 16.17896874362914
TOTAL    10,004.11                                              4.10938248077946                                   ''' + \
'''
G TOTAL  10,004.11                                              4.10938248077946                                   '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testAndAnalyseComputeDepositsYields_uniqueOwner_2_deposit(self):
		"""
		Only one owner with 2 deposits.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_2_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_2_deposit.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR         YIELD AMT         TOTAL\n' + \
'OWNER                                           ' + \
'''
JPS    24,571.69 63.42440740948223  24635.114407
TOTAL  24,571.69 63.42440740948223  24635.114407'''
		
		if PRINT:
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS         YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                                    ' + \
'''
JPS      19,571.69 19,571.69  2021-01-01  2021-01-01          1 10.98076808766564     0.056105  22.719019
JPS       5,000.00 24,582.67  2021-01-02  2021-01-05          4 52.44363932181659     0.213336  21.465680
TOTAL    24,635.11                                              63.42440740948223                        ''' + \
'''
G TOTAL  24,635.11                                              63.42440740948223                        '''
		
		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
		
	def testAndAnalyseComputeDepositsYields_uniqueOwner_3_deposit(self):
		"""
		Only one owner with 3 deposits.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_3_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_3_deposit.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
2021-01-01 09:00:00  Earnings     USDC  4.36774839
2021-01-02 09:00:00  Earnings     USDC  7.11332700
2021-01-03 09:00:00  Earnings     USDC  8.47797205
2021-01-04 09:00:00  Earnings     USDC 22.46701621
2021-01-05 09:00:00  Earnings     USDC 19.17963718
TOTAL                                  61.60570083'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f',
				MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.14f',
				MERGED_SHEET_HEADER_YEARLY_YIELD_RATE: '.14f'})

		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP           EARNING     D YIELD RATE     Y YIELD RATE\n' + \
'DATE                                                                        ' + \
'''
2021-01-01  10000.000000  4.36774838756355 1.00043677483876 1.17279291419006
2021-01-02  15004.367748  7.11332700382809 1.00047408375502 1.18886558873487
2021-01-03  15011.481075  8.47797205061397 1.00056476586208 1.22885316870567
2021-01-04  40019.959047 22.46701621233660 1.00056139528243 1.22734313720236
2021-01-05  40042.426064 19.17963717721430 1.00047898289546 1.19099238934721
TOTAL       40061.605701 61.60570083155650                                  '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR         YIELD AMT         TOTAL\n' + \
'OWNER                                           ' + \
'''
JPS    40,000.00 61.60570083155653  40061.605701
TOTAL  40,000.00 61.60570083155653  40061.605701'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: '.14f',
				DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: '.14f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS         YIELD AMT      YIELD AMT %         Y YIELD %\n' + \
'OWNER                                                                                                               ' + \
'''
JPS      10,000.00 10,000.00  2021-01-01  2021-01-01          1  4.36774838756355 0.04367748387564 17.27929141900555
JPS       5,000.00 15,004.37  2021-01-02  2021-01-03          2 15.59129905444206 0.10391173634169 20.86940249219460
JPS      25,000.00 40,019.96  2021-01-04  2021-01-05          2 41.64665338955092 0.10406470766295 20.90311557299003
TOTAL    40,061.61                                              61.60570083155653                                   ''' + \
'''
G TOTAL  40,061.61                                              61.60570083155653                                   '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_1_partial_withdr(self):
		"""
		Only one owner with 1 deposit and 1 partial withdrawal.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_1_partial_withdr.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_1_partial_withdr.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
2021-01-01 09:00:00  Earnings     USDC 11.11126149
2021-01-02 09:00:00  Earnings     USDC  8.60741640
2021-01-03 09:00:00  Earnings     USDC  9.24053714
2021-01-04 09:00:00  Earnings     USDC  5.59653333
2021-01-05 09:00:00  Earnings     USDC  5.22428781
TOTAL                                  39.78003617'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP    EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                           ' + \
'''
2021-01-01  20000.000000  11.111261      1.000556      1.224735
2021-01-02  20011.111261   8.607416      1.000430      1.169954
2021-01-03  20019.718678   9.240537      1.000462      1.183451
2021-01-04  10028.959215   5.596533      1.000558      1.225841
2021-01-05  10034.555748   5.224288      1.000521      1.209226
TOTAL       10039.780036  39.780036                            '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
JPS    10,000.00 39.78003617  10039.780036
TOTAL  10,000.00 39.78003617  10039.780036'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                              ' + \
'''
JPS      20,000.00 20,000.00  2021-01-01  2021-01-03          3 28.95921503     0.144796  19.248711
JPS     -10,000.00 10,028.96  2021-01-04  2021-01-05          2 10.82082114     0.107896  21.750490
TOTAL    10,039.78                                              39.78003617                        ''' + \
'''
G TOTAL  10,039.78                                              39.78003617                        '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_1_almost_full_withdr(self):
		"""
		Only one owner with 1 deposit and 1 almost full withdrawal. Since the deposit
		continues to generate earning on the yield redemption fulfilment date, the last
		earning will remain in the smart yield and continue to generate very small earnings.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_1_almost_full_withdr.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_1_almost_full_withdr.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
2021-01-01 09:00:00  Earnings     USDC  8.84728534
2021-01-02 09:00:00  Earnings     USDC 11.62354646
2021-01-03 09:00:00  Earnings     USDC 10.81679235
2021-01-04 09:00:00  Earnings     USDC  0.00983605
2021-01-05 09:00:00  Earnings     USDC  0.00942140
TOTAL                                  31.30688161'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP           EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                                  ' + \
'''
2021-01-01  20000.000000  8.84728534291207      1.000442      1.175187
2021-01-02  20008.847285 11.62354645871160      1.000581      1.236116
2021-01-03  20020.470832 10.81679235481710      1.000540      1.217928
2021-01-04     16.287624  0.00983605445532      1.000604      1.246520
2021-01-05     16.297460  0.00942140246999      1.000578      1.234841
TOTAL          16.306882 31.30688161336608                            '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR         YIELD AMT      TOTAL\n' + \
'OWNER                                        ' + \
'''
JPS       -15.00 31.30688161336618  16.306882
TOTAL     -15.00 31.30688161336618  16.306882'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.14f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR               CAPITAL        FROM          TO YIELD DAYS         YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                                                ' + \
'''
JPS      20,000.00 20,000.00000000000000  2021-01-01  2021-01-03          3 31.28762415644087     0.156438  20.947251
JPS     -20,015.00     16.28762415644087  2021-01-04  2021-01-05          2  0.01925745692531     0.118234  24.066683
TOTAL        16.31                                                          31.30688161336618                        ''' + \
'''
G TOTAL      16.31                                                          31.30688161336618                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_1_partial_withdr_fixed_yield_rate(self):
		"""
		Only one owner with 1 deposit and 1 partial withdrawal.
		"""
		PRINT = True

		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_1_partial_withdr_fixed_yield_rate.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_1_partial_withdr.csv'

		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
2021-01-01 09:00:00  Earnings     USDC 11.11126149
2021-01-02 09:00:00  Earnings     USDC  8.60741640
2021-01-03 09:00:00  Earnings     USDC  9.24053714
2021-01-04 09:00:00  Earnings     USDC  5.59653333
2021-01-05 09:00:00  Earnings     USDC  5.22428781
TOTAL                                  39.78003617'''

		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})

		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP    EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                           ' + \
'''
2021-01-01  20000.000000  11.111261      1.000556      1.224735
2021-01-02  20011.111261   8.607416      1.000430      1.169954
2021-01-03  20019.718678   9.240537      1.000462      1.183451
2021-01-04  10028.959215   5.596533      1.000558      1.225841
2021-01-05  10034.555748   5.224288      1.000521      1.209226
TOTAL       10039.780036  39.780036                            '''

		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)

		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.8f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.8f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
JPS    10,000.00 39.78003617  10039.780036
TOTAL  10,000.00 39.78003617  10039.780036'''

		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)

		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.8f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.8f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                              ' + \
'''
JPS      20,000.00 20,000.00  2021-01-01  2021-01-03          3 28.95921503     0.144796  19.248711
JPS     -10,000.00 10,028.96  2021-01-04  2021-01-05          2 10.82082114     0.107896  21.750490
TOTAL    10,039.78                                              39.78003617                        ''' + \
'''
G TOTAL  10,039.78                                              39.78003617                        '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_1_almost_full_withdr_fixed_yield_rate(self):
		"""
		Only one owner with 1 deposit and 1 almost full withdrawal. Since the deposit
		continues to generate earning on the yield redemption fulfilment date, the last
		earning will remain in the smart yield and continue to generate very small earnings.
		
		In this test case, the yield rate is identical on all days (20 % annually)
		"""
		PRINT = True
		
		sbAccountSheetFileName = 'testSBEarningUsdc_uniqueOwner_1_deposit_1_almost_full_withdr_fixed_yield_rate.xlsx'
		depositSheetFileName = 'testDepositUsdc_uniqueOwner_1_deposit_1_almost_full_withdr_fixed_yield_rate.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
2021-01-01 09:00:00  Earnings     USDC  8.84728534
2021-01-02 09:00:00  Earnings     USDC 11.62354646
2021-01-03 09:00:00  Earnings     USDC 10.81679235
2021-01-04 09:00:00  Earnings     USDC  0.00983605
2021-01-05 09:00:00  Earnings     USDC  0.00942140
TOTAL                                  31.30688161'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
		
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.8f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.8f',
				MERGED_SHEET_HEADER_EARNING_NEW_NAME: '.14f'})
		
		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP           EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                                  ' + \
'''
2021-01-01  20000.000000  8.84728534291207      1.000442      1.175187
2021-01-02  20008.847285 11.62354645871160      1.000581      1.236116
2021-01-03  20020.470832 10.81679235481710      1.000540      1.217928
2021-01-04     16.287624  0.00983605445532      1.000604      1.246520
2021-01-05     16.297460  0.00942140246999      1.000578      1.234841
TOTAL          16.306882 31.30688161336608                            '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.8f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.8f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR         YIELD AMT      TOTAL\n' + \
'OWNER                                        ' + \
'''
JPS       -15.00 31.30688161336618  16.306882
TOTAL     -15.00 31.30688161336618  16.306882'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.8f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.14f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.14f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR               CAPITAL        FROM          TO YIELD DAYS         YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                                                ' + \
'''
JPS      20,000.00 20,000.00000000000000  2021-01-01  2021-01-03          3 31.28762415644087     0.156438  20.947251
JPS     -20,015.00     16.28762415644087  2021-01-04  2021-01-05          2  0.01925745692531     0.118234  24.066683
TOTAL        16.31                                                          31.30688161336618                        ''' + \
'''
G TOTAL      16.31                                                          31.30688161336618                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testAndAnalyseComputeDepositsYields_2_owner_1_deposit_before_first_yield(self):
		"""
		Two owners with 1 deposit for each done on date before the first paid yield.
		The case when running the app on a Swissborg account statement spreadsheet
		required with a date from after the first yield farming deposit(s).
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_2_owner_1_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_2_owner_1_deposit_before_first_yield.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
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
2021-01-01 09:00:00  Earnings     USDC 18.08315865
2021-01-02 09:00:00  Earnings     USDC 18.09283537
2021-01-03 09:00:00  Earnings     USDC 14.59114061
2021-01-04 09:00:00  Earnings     USDC 13.61595741
2021-01-05 09:00:00  Earnings     USDC 17.45808404
TOTAL                                  81.84117609'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
			
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP    EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                           ' + \
'''
2021-01-01  30000.000000  18.083159      1.000603      1.246009
2021-01-02  30018.083159  18.092835      1.000603      1.245990
2021-01-03  30036.175994  14.591141      1.000486      1.193952
2021-01-04  30050.767135  13.615957      1.000453      1.179798
2021-01-05  30064.383092  17.458084      1.000581      1.236012
TOTAL       30081.841176  81.841176                            '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR   YIELD AMT         TOTAL\n' + \
'OWNER                                     ' + \
'''
JPS    10,000.00 27.28039203  10027.280392
Papa   20,000.00 54.56078406  20054.560784
TOTAL  30,000.00 81.84117609  30081.841176'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                              ' + \
'''
JPS      10,000.00 10,000.00  2021-01-01  2021-01-05          5 27.28039203     0.272804  22.003032
TOTAL    10,027.28                                              27.28039203                        ''' + \
'''
Papa     20,000.00 20,000.00  2021-01-01  2021-01-05          5 54.56078406     0.272804  22.003032
TOTAL    20,054.56                                              54.56078406                        ''' + \
'''
G TOTAL  30,081.84                                              81.84117609                        '''
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
		
	def testAndAnalyseComputeDepositsYields_3_owner_1_multi_deposit(self):
		"""
		Three owners with only 1 owner with several deposits of which 1 withdrawal.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_3_owner_multi_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_3_owner_1_multi_deposit.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2021-01-01 09:00:00  Earnings     USDC  15.02363060
2021-01-02 09:00:00  Earnings     USDC  14.33714241
2021-01-03 09:00:00  Earnings     USDC  24.77659057
2021-01-04 09:00:00  Earnings     USDC  28.66457400
2021-01-05 09:00:00  Earnings     USDC  27.45068569
TOTAL                                  110.25262326'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
			
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP     EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                            ' + \
'''
2021-01-01  30000.000000   15.023631      1.000501      1.200504
2021-01-02  30015.023631   14.337142      1.000478      1.190420
2021-01-03  40029.360773   24.776591      1.000619      1.253388
2021-01-04  36054.137364   28.664574      1.000795      1.336528
2021-01-05  36082.801938   27.450686      1.000761      1.319925
TOTAL       36110.252623  110.252623                            '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
		
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR    YIELD AMT         TOTAL\n' + \
'OWNER                                      ' + \
'''
Béa     2,000.00   4.35268089   2004.352681
JPS    10,000.00  31.57162847  10031.571628
Papa   24,000.00  74.32831390  24074.328314
TOTAL  36,000.00 110.25262326  36110.252623'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS    YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                               ' + \
'''
Béa       2,000.00  2,000.00  2021-01-03  2021-01-05          3   4.35268089     0.217634  30.277991
TOTAL     2,004.35                                                4.35268089                        ''' \
'''
JPS      10,000.00 10,000.00  2021-01-01  2021-01-05          5  31.57162847     0.315716  25.873825
TOTAL    10,031.57                                               31.57162847                        ''' + \
'''
Papa     20,000.00 20,000.00  2021-01-01  2021-01-02          2  19.57384867     0.097869  19.545160
Papa      8,000.00 28,019.57  2021-01-03  2021-01-03          1  17.34300763     0.061896  25.338848
Papa     -4,000.00 24,036.92  2021-01-04  2021-01-05          2  37.41145760     0.155642  32.820077
TOTAL    24,074.33                                               74.32831390                        ''' + \
'''
G TOTAL  36,110.25                                              110.25262326                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)
	
	def testAndAnalyseComputeDepositsYields_3_owner_multi_deposit(self):
		"""
		Three owners with several deposits/withdrawals.
		"""
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc_3_owner_multi_deposit.xlsx'
		depositSheetFileName = 'testDepositUsdc_3_owner_multi_deposit.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		
		sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
			self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
		
		print(depositSheetFileName)
		
		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(SB_ACCOUNT_SHEET_CURRENCY_USDC)
		
		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2021-01-01 09:00:00  Earnings     USDC  15.02363060
2021-01-02 09:00:00  Earnings     USDC  14.33714241
2021-01-03 09:00:00  Earnings     USDC  24.77659057
2021-01-04 09:00:00  Earnings     USDC  28.66457400
2021-01-05 09:00:00  Earnings     USDC  27.45068569
TOTAL                                  110.25262326'''
		
		if PRINT:
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)
			
		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbYieldRatesWithTotalDfExpectedStr = \
'             EARNING CAP     EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                            ' + \
'''
2021-01-01  30000.000000   15.023631      1.000501      1.200504
2021-01-02  35015.023631   14.337142      1.000409      1.161162
2021-01-03  52029.360773   24.776591      1.000476      1.189786
2021-01-04  48054.137364   28.664574      1.000597      1.243164
2021-01-05  48082.801938   27.450686      1.000571      1.231608
TOTAL       48110.252623  110.252623                            '''
		
		if PRINT:
			print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)
	
		yieldOwnerWithTotalsSummaryDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsSummaryDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		yieldOwnerWithTotalsSummaryDfExpectedStr = \
'      DEP/WITHDR    YIELD AMT         TOTAL\n' + \
'OWNER                                      ' + \
'''
Béa     2,000.00   3.28902191   2003.289022
JPS    22,000.00  47.34936079  22047.349361
Papa   24,000.00  59.61424056  24059.614241
TOTAL  48,000.00 110.25262326  48110.252623'''
		
		if PRINT:
			print('\nOwner summary deposit/withdrawal yield totals ...')
			print(yieldOwnerWithTotalsSummaryDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsSummaryDfExpectedStr, yieldOwnerWithTotalsSummaryDfActualStr)
		
		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})
		
		yieldOwnerWithTotalsDetailDfExpectedStr = \
'        DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS    YIELD AMT  YIELD AMT %  Y YIELD %\n' + \
'OWNER                                                                                               ' + \
'''
Béa       2,000.00  2,000.00  2021-01-03  2021-01-05          3   3.28902191     0.164451  22.130240
TOTAL     2,003.29                                                3.28902191                        ''' \
'''
JPS      10,000.00 10,000.00  2021-01-01  2021-01-01          1   5.00787687     0.050079  20.050434
JPS       5,000.00 15,005.01  2021-01-02  2021-01-02          1   6.14390374     0.040946  16.116194
JPS       7,000.00 22,011.15  2021-01-03  2021-01-05          3  36.19758018     0.164451  22.130240
TOTAL    22,047.35                                               47.34936079                        ''' + \
'''
Papa     20,000.00 20,000.00  2021-01-01  2021-01-02          2  18.20899240     0.091045  18.066928
Papa      8,000.00 28,018.21  2021-01-03  2021-01-03          1  13.34238365     0.047620  18.978557
Papa     -4,000.00 24,031.55  2021-01-04  2021-01-05          2  28.06286451     0.116775  23.737252
TOTAL    24,059.61                                               59.61424056                        ''' + \
'''
G TOTAL  48,110.25                                              110.25262326                        '''
		
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)


if __name__ == '__main__':
	if os.name == 'posix':
		unittest.main()
	else:
		tst = TestOwnerDepositYieldComputer()
		# tst.testComputeDepositsYieldsSeveralOwners()
		# tst.testComputeDepositsYieldsLastDepositRowUniqueOwnerTwoDeposits()
		# tst.testComputeDepositsYieldsMiddleDepositRowUniqueOwnerTwoDeposits()
		# tst.testComputeDepositsYieldsFirstDepositRowUniqueOwnerThreeDeposits()
		# tst.testComputeDepositsYieldsLastDepositRowUniqueOwnerThreeDeposits()
		# tst.testComputeDepositsYieldsMiddleDepositRowUniqueOwnerThreeDeposits()
		# tst.testComputeDepositsYieldsFirstDepositDateFromIsMaxRowUniqueOwnerThreeDeposits()
		# tst.testComputeDepositsYieldsFirstOwner_1_only_depositBeforeFirstYieldDate()
		# tst.testComputeDepositsYieldsFirstOwner_1_depositBeforeAnd_1_aftertFirstYieldDate()
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
		# tst.testComputeDepositsYieldsLastDepositRowUniqueOwnerTwoDepositsOnFirstDepositDate()
		# tst.testAndAnalyseComputeDepositsYields()
		# tst.testAndAnalyseComputeDepositsYields_dep_1()
		# tst.testAndAnalyseComputeDepositsYields_dep_2()
		# tst.testAndAnalyseComputeDepositsYields_dep_3()
		# tst.testAndAnalyseComputeDepositsYields_dep_2()
		# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_before_first_yield()
		# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_on_first_yield()
		# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_after_first_yield()
		# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_on_last_yield()
		# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_2_deposit()
		# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_3_deposit()
		# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_1_partial_withdr()
		# tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_1_almost_full_withdr()
		# tst.testAndAnalyseComputeDepositsYields_2_owner_1_deposit_before_first_yield()
		# tst.testAndAnalyseComputeDepositsYields_3_owner_1_multi_deposit()
		# tst.testAndAnalyseComputeDepositsYields_3_owner_multi_deposit()
#		tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_1_partial_withdr_fixed_yield_rate()
#		tst.testAndAnalyseComputeDepositsYields_uniqueOwner_1_deposit_1_almost_full_withdr_fixed_yield_rate()