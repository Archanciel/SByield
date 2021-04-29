import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from cryptofiatratecomputer import CryptoFiatRateComputer
from pricerequester import PriceRequester
from pricerequesterteststub import PriceRequesterTestStub
from processor import *

PRINT_SB_EARNING_TOTALS = False

class TestProcessor(unittest.TestCase):
	def initializeComputerClasses(self,
								  sbAccountSheetFileName,
								  depositSheetFileName,
								  cryptoFiatCsvFileName,
								  language=GB):
		self.language = language

		if os.name == 'posix':
			self.testDataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/'
			dataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/data/'
			sbAccountSheetFilePathName = self.testDataPath + sbAccountSheetFileName
			depositSheetFilePathName = self.testDataPath + depositSheetFileName
			self.cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName
		else:
			self.testDataPath = 'D:\\Development\\Python\\SByield\\test\\testData\\'
			dataPath = 'D:\\Development\\Python\\SByield\\data\\'
			sbAccountSheetFilePathName = self.testDataPath + sbAccountSheetFileName
			depositSheetFilePathName = self.testDataPath + depositSheetFileName
			self.cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName
		self.yieldRateComputer = SBYieldRateComputer(sbAccountSheetFilePathName,
		                                             depositSheetFilePathName,
													 self.language)
		self.ownerDepositYieldComputer = OwnerDepositYieldComputer(self.yieldRateComputer,
																   self.language)
		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequester(),
														  self.cryptoFiatCsvFilePathName),
								   self.language)

	def testAddFiatConversionInfo_CHSB_2_fiats_2_owners_french_language(self):
		"""
		Two owners, two fiats, french language.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSwissborg_account_statement_20201218_20210408.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_usd_chf.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName,
									   language=FR)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(),
														  self.cryptoFiatCsvFilePathName),
								   language=FR)

		self.maxDiff=None

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto = self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2021-01-30 09:00:00  Earnings     CHSB   3.77500000
2021-01-31 09:00:00  Earnings     CHSB   3.10400000
2021-02-01 09:00:00  Earnings     CHSB   2.99900000
2021-02-02 09:00:00  Earnings     CHSB   2.95700000
2021-02-03 09:00:00  Earnings     CHSB   2.89400000
2021-02-04 09:00:00  Earnings     CHSB   3.64200000
2021-02-05 09:00:00  Earnings     CHSB   3.68000000
2021-02-06 09:00:00  Earnings     CHSB   3.68000000
2021-02-07 09:00:00  Earnings     CHSB   3.61300000
2021-02-08 09:00:00  Earnings     CHSB   3.61300000
2021-02-09 09:00:00  Earnings     CHSB   3.47200000
2021-02-10 09:00:00  Earnings     CHSB   3.47300000
2021-02-11 09:00:00  Earnings     CHSB   3.52600000
2021-02-12 09:00:00  Earnings     CHSB   3.52700000
2021-02-13 09:00:00  Earnings     CHSB   3.45900000
2021-02-14 09:00:00  Earnings     CHSB   3.37500000
2021-02-15 09:00:00  Earnings     CHSB   3.30700000
2021-02-16 09:00:00  Earnings     CHSB   3.33400000
2021-02-17 09:00:00  Earnings     CHSB   3.27700000
2021-02-18 09:00:00  Earnings     CHSB   3.19800000
2021-02-19 09:00:00  Earnings     CHSB   3.14300000
2021-02-20 09:00:00  Earnings     CHSB   3.14400000
2021-02-21 09:00:00  Earnings     CHSB   3.23100000
2021-02-22 09:00:00  Earnings     CHSB   3.23100000
2021-02-23 09:00:00  Earnings     CHSB   3.23200000
2021-02-24 09:00:00  Earnings     CHSB   3.23200000
2021-02-25 09:00:00  Earnings     CHSB   3.23300000
2021-02-26 09:00:00  Earnings     CHSB   3.40100000
2021-02-27 09:00:00  Earnings     CHSB   3.35900000
2021-02-28 09:00:00  Earnings     CHSB   3.35900000
2021-03-01 09:00:00  Earnings     CHSB   3.35400000
2021-03-02 09:00:00  Earnings     CHSB   3.34400000
2021-03-03 09:00:00  Earnings     CHSB   3.34500000
2021-03-04 09:00:00  Earnings     CHSB   3.34500000
2021-03-05 09:00:00  Earnings     CHSB   2.75700000
2021-03-06 09:00:00  Earnings     CHSB   2.75700000
2021-03-07 09:00:00  Earnings     CHSB   3.92000000
2021-03-08 09:00:00  Earnings     CHSB   4.07100000
2021-03-09 09:00:00  Earnings     CHSB   4.07200000
2021-03-10 09:00:00  Earnings     CHSB   3.98900000
2021-03-11 09:00:00  Earnings     CHSB   4.85200000
2021-03-12 09:00:00  Earnings     CHSB   4.85300000
2021-03-13 09:00:00  Earnings     CHSB   4.53400000
2021-03-14 09:00:00  Earnings     CHSB   4.51000000
2021-03-15 09:00:00  Earnings     CHSB   4.51000000
2021-03-16 09:00:00  Earnings     CHSB   4.51900000
2021-03-17 09:00:00  Earnings     CHSB   4.52000000
2021-03-18 09:00:00  Earnings     CHSB   4.84900000
2021-03-19 09:00:00  Earnings     CHSB   4.79100000
2021-03-20 09:00:00  Earnings     CHSB   4.79100000
2021-03-21 09:00:00  Earnings     CHSB   4.79200000
2021-03-22 09:00:00  Earnings     CHSB   4.62400000
2021-03-23 09:00:00  Earnings     CHSB   4.62500000
2021-03-24 09:00:00  Earnings     CHSB   4.62600000
2021-03-25 09:00:00  Earnings     CHSB   3.91600000
2021-03-26 09:00:00  Earnings     CHSB   3.91600000
2021-03-27 09:00:00  Earnings     CHSB   3.91700000
2021-03-28 10:00:00  Earnings     CHSB   3.82400000
2021-03-29 10:00:00  Earnings     CHSB   3.82400000
2021-03-30 10:00:00  Earnings     CHSB   3.82500000
2021-03-31 10:00:00  Earnings     CHSB   3.78200000
2021-04-01 10:00:00  Earnings     CHSB   3.78300000
2021-04-02 10:00:00  Earnings     CHSB   3.34800000
2021-04-03 10:00:00  Earnings     CHSB   3.34800000
2021-04-04 10:00:00  Earnings     CHSB   3.67300000
2021-04-05 10:00:00  Earnings     CHSB   3.67400000
2021-04-06 10:00:00  Earnings     CHSB   3.52900000
2021-04-07 10:00:00  Earnings     CHSB   3.52900000
2021-04-08 10:00:00  Earnings     CHSB   3.25600000
TOTAL                                  255.96400000'''

		if PRINT:
			# print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                                                                          DEPOTS/RETRAITS                                                                                                    \n' + \
'                     CHSB                                         USD                                                 CHF                       CAPITAL                    DATE                      INTERETS                \n' + \
'        Tot incl intérêts TX DAT DEP    TX ACT PLUS-VAL CAP P-V CAP %  TX DAT DEP    TX ACT  PLUS-VAL CAP       P-V CAP %      CHSB       USD       CHF          DE           A  JOURS   CHSB    USD      CHF INT % INT ANN %\n' + \
'PROPR                                                                                                                                                                                                                        ' + \
'''
JPS              4,422.80   2,479.76  7,518.77     5,039.01    203.21    2,212.10  6,634.20      4,422.10          199.91  4,422.80  7,518.77  6,634.20  2021-01-30  2021-02-18     20  14.75  25.07    22.12  0.33      6.26
JPS                511.33     456.60    869.26       412.66     90.38      408.04    767.00        358.95           87.97  4,948.88  8,413.10  7,423.32  2021-02-19  2021-03-07     17  12.81  21.78    19.22  0.26      5.71
JPS              2,047.89   2,401.13  3,481.41     1,080.28     44.99    2,239.89  3,071.84        831.95           37.14  7,009.58 11,916.29 10,514.37  2021-03-08  2021-03-10      3   2.66   4.51     3.98  0.04      4.72
JPS                300.48     430.55    510.82        80.27     18.64      397.92    450.72         52.80           13.27  7,312.72 12,431.62 10,969.08  2021-03-11  2021-04-08     29  27.26  46.35    40.89  0.37      4.79
TOTAL            7,339.98   5,768.04 12,477.97     6,612.22    114.64    5,257.95 11,009.97      5,665.80          107.76                                                               57.48  97.71    86.21                ''' + \
'''
Papa            15,941.63   8,938.09 27,100.76    18,162.67    203.21    7,973.32 23,912.44     15,939.12          199.91 15,941.63 27,100.76 23,912.44  2021-01-30  2021-03-06     36  92.46 157.19   138.69  0.58      6.04
Papa             8,973.34  10,421.37 15,254.68     4,833.31     46.38    9,712.37 13,460.01      3,747.64           38.59 25,007.43 42,512.63 37,511.14  2021-03-07  2021-04-08     33 106.02 180.24   159.04  0.42      4.79
TOTAL           25,113.45  19,359.46 42,692.87    22,995.98    118.78   17,685.69 37,670.18     19,686.76          111.31                                                              198.49 337.43   297.73                ''' + \
'''
G TOTAL         32,453.43            55,170.84                                    48,680.15                                                                                            255.96 435.14   383.95                '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_CHSB_2_fiats_2_owners(self):
		"""
		Two owners, two fiats, default english language.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSwissborg_account_statement_20201218_20210408.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_usd_chf.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		self.maxDiff = None

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto = self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2021-01-30 09:00:00  Earnings     CHSB   3.77500000
2021-01-31 09:00:00  Earnings     CHSB   3.10400000
2021-02-01 09:00:00  Earnings     CHSB   2.99900000
2021-02-02 09:00:00  Earnings     CHSB   2.95700000
2021-02-03 09:00:00  Earnings     CHSB   2.89400000
2021-02-04 09:00:00  Earnings     CHSB   3.64200000
2021-02-05 09:00:00  Earnings     CHSB   3.68000000
2021-02-06 09:00:00  Earnings     CHSB   3.68000000
2021-02-07 09:00:00  Earnings     CHSB   3.61300000
2021-02-08 09:00:00  Earnings     CHSB   3.61300000
2021-02-09 09:00:00  Earnings     CHSB   3.47200000
2021-02-10 09:00:00  Earnings     CHSB   3.47300000
2021-02-11 09:00:00  Earnings     CHSB   3.52600000
2021-02-12 09:00:00  Earnings     CHSB   3.52700000
2021-02-13 09:00:00  Earnings     CHSB   3.45900000
2021-02-14 09:00:00  Earnings     CHSB   3.37500000
2021-02-15 09:00:00  Earnings     CHSB   3.30700000
2021-02-16 09:00:00  Earnings     CHSB   3.33400000
2021-02-17 09:00:00  Earnings     CHSB   3.27700000
2021-02-18 09:00:00  Earnings     CHSB   3.19800000
2021-02-19 09:00:00  Earnings     CHSB   3.14300000
2021-02-20 09:00:00  Earnings     CHSB   3.14400000
2021-02-21 09:00:00  Earnings     CHSB   3.23100000
2021-02-22 09:00:00  Earnings     CHSB   3.23100000
2021-02-23 09:00:00  Earnings     CHSB   3.23200000
2021-02-24 09:00:00  Earnings     CHSB   3.23200000
2021-02-25 09:00:00  Earnings     CHSB   3.23300000
2021-02-26 09:00:00  Earnings     CHSB   3.40100000
2021-02-27 09:00:00  Earnings     CHSB   3.35900000
2021-02-28 09:00:00  Earnings     CHSB   3.35900000
2021-03-01 09:00:00  Earnings     CHSB   3.35400000
2021-03-02 09:00:00  Earnings     CHSB   3.34400000
2021-03-03 09:00:00  Earnings     CHSB   3.34500000
2021-03-04 09:00:00  Earnings     CHSB   3.34500000
2021-03-05 09:00:00  Earnings     CHSB   2.75700000
2021-03-06 09:00:00  Earnings     CHSB   2.75700000
2021-03-07 09:00:00  Earnings     CHSB   3.92000000
2021-03-08 09:00:00  Earnings     CHSB   4.07100000
2021-03-09 09:00:00  Earnings     CHSB   4.07200000
2021-03-10 09:00:00  Earnings     CHSB   3.98900000
2021-03-11 09:00:00  Earnings     CHSB   4.85200000
2021-03-12 09:00:00  Earnings     CHSB   4.85300000
2021-03-13 09:00:00  Earnings     CHSB   4.53400000
2021-03-14 09:00:00  Earnings     CHSB   4.51000000
2021-03-15 09:00:00  Earnings     CHSB   4.51000000
2021-03-16 09:00:00  Earnings     CHSB   4.51900000
2021-03-17 09:00:00  Earnings     CHSB   4.52000000
2021-03-18 09:00:00  Earnings     CHSB   4.84900000
2021-03-19 09:00:00  Earnings     CHSB   4.79100000
2021-03-20 09:00:00  Earnings     CHSB   4.79100000
2021-03-21 09:00:00  Earnings     CHSB   4.79200000
2021-03-22 09:00:00  Earnings     CHSB   4.62400000
2021-03-23 09:00:00  Earnings     CHSB   4.62500000
2021-03-24 09:00:00  Earnings     CHSB   4.62600000
2021-03-25 09:00:00  Earnings     CHSB   3.91600000
2021-03-26 09:00:00  Earnings     CHSB   3.91600000
2021-03-27 09:00:00  Earnings     CHSB   3.91700000
2021-03-28 10:00:00  Earnings     CHSB   3.82400000
2021-03-29 10:00:00  Earnings     CHSB   3.82400000
2021-03-30 10:00:00  Earnings     CHSB   3.82500000
2021-03-31 10:00:00  Earnings     CHSB   3.78200000
2021-04-01 10:00:00  Earnings     CHSB   3.78300000
2021-04-02 10:00:00  Earnings     CHSB   3.34800000
2021-04-03 10:00:00  Earnings     CHSB   3.34800000
2021-04-04 10:00:00  Earnings     CHSB   3.67300000
2021-04-05 10:00:00  Earnings     CHSB   3.67400000
2021-04-06 10:00:00  Earnings     CHSB   3.52900000
2021-04-07 10:00:00  Earnings     CHSB   3.52900000
2021-04-08 10:00:00  Earnings     CHSB   3.25600000
TOTAL                                  255.96400000'''

		if PRINT:
			# print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                                                               DEP/WITHDR                                                                                            \n' + \
'                  CHSB                                      USD                                       CHF                       CAPITAL                    DATE                     YIELD            \n' + \
'        Tot incl yield   DF RATE  CUR RATE  CAP GAIN CAP GAIN %   DF RATE  CUR RATE  CAP GAIN  CAP GAIN %      CHSB       USD       CHF        FROM          TO DAYS   CHSB    USD    CHF  Y % YR Y %\n' + \
'OWNER                                                                                                                                                                                                ' + \
'''
JPS           4,422.80  2,479.76  7,518.77  5,039.01     203.21  2,212.10  6,634.20  4,422.10      199.91  4,422.80  7,518.77  6,634.20  2021-01-30  2021-02-18   20  14.75  25.07  22.12 0.33   6.26
JPS             511.33    456.60    869.26    412.66      90.38    408.04    767.00    358.95       87.97  4,948.88  8,413.10  7,423.32  2021-02-19  2021-03-07   17  12.81  21.78  19.22 0.26   5.71
JPS           2,047.89  2,401.13  3,481.41  1,080.28      44.99  2,239.89  3,071.84    831.95       37.14  7,009.58 11,916.29 10,514.37  2021-03-08  2021-03-10    3   2.66   4.51   3.98 0.04   4.72
JPS             300.48    430.55    510.82     80.27      18.64    397.92    450.72     52.80       13.27  7,312.72 12,431.62 10,969.08  2021-03-11  2021-04-08   29  27.26  46.35  40.89 0.37   4.79
TOTAL         7,339.98  5,768.04 12,477.97  6,612.22     114.64  5,257.95 11,009.97  5,665.80      107.76                                                             57.48  97.71  86.21            ''' + \
'''
Papa         15,941.63  8,938.09 27,100.76 18,162.67     203.21  7,973.32 23,912.44 15,939.12      199.91 15,941.63 27,100.76 23,912.44  2021-01-30  2021-03-06   36  92.46 157.19 138.69 0.58   6.04
Papa          8,973.34 10,421.37 15,254.68  4,833.31      46.38  9,712.37 13,460.01  3,747.64       38.59 25,007.43 42,512.63 37,511.14  2021-03-07  2021-04-08   33 106.02 180.24 159.04 0.42   4.79
TOTAL        25,113.45 19,359.46 42,692.87 22,995.98     118.78 17,685.69 37,670.18 19,686.76      111.31                                                            198.49 337.43 297.73            ''' + \
'''
G TOTAL      32,453.43           55,170.84                                48,680.15                                                                                  255.96 435.14 383.95            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_USDC_1_fiat_4_owners(self):
		"""
		Four owners, one fiat, real Swiaaborg data, default english language.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSwissborg_account_statement_20201218_20210408.xlsx'
		depositSheetFileName = 'depositUsdc_fiat_chf.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)


		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		self.maxDiff = None

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto = self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2020-12-22 09:00:00  Earnings     USDC   9.37935200
2020-12-23 09:00:00  Earnings     USDC   8.90406500
2020-12-24 09:00:00  Earnings     USDC   9.34752500
2020-12-25 09:00:00  Earnings     USDC   9.39259300
2020-12-26 09:00:00  Earnings     USDC   8.59240700
2020-12-27 09:00:00  Earnings     USDC   8.29288400
2020-12-28 09:00:00  Earnings     USDC   8.31021800
2020-12-29 09:00:00  Earnings     USDC   8.31373700
2020-12-30 09:00:00  Earnings     USDC   8.45546700
2020-12-31 09:00:00  Earnings     USDC   8.40384200
2021-01-01 09:00:00  Earnings     USDC   8.94866800
2021-01-02 09:00:00  Earnings     USDC  10.13596200
2021-01-03 09:00:00  Earnings     USDC  10.30184400
2021-01-04 09:00:00  Earnings     USDC   9.83256800
2021-01-05 09:00:00  Earnings     USDC   8.47960700
2021-01-06 09:00:00  Earnings     USDC   8.55706700
2021-01-07 09:00:00  Earnings     USDC   9.84148300
2021-01-08 09:00:00  Earnings     USDC  10.16541400
2021-01-09 09:00:00  Earnings     USDC   9.81087500
2021-01-10 09:00:00  Earnings     USDC   9.30776900
2021-01-11 09:00:00  Earnings     USDC   9.90612600
2021-01-12 09:00:00  Earnings     USDC   9.47169000
2021-01-13 09:00:00  Earnings     USDC   9.42159500
2021-01-14 09:00:00  Earnings     USDC   9.68069300
2021-01-15 09:00:00  Earnings     USDC   9.37595600
2021-01-16 09:00:00  Earnings     USDC   9.64914000
2021-01-17 09:00:00  Earnings     USDC   9.41237200
2021-01-18 09:00:00  Earnings     USDC  10.54711600
2021-01-19 09:00:00  Earnings     USDC  10.25644900
2021-01-20 09:00:00  Earnings     USDC   9.88213100
2021-01-21 09:00:00  Earnings     USDC  10.01395100
2021-01-22 09:00:00  Earnings     USDC  11.07753700
2021-01-23 09:00:00  Earnings     USDC  10.76276400
2021-01-24 09:00:00  Earnings     USDC  11.28946700
2021-01-25 09:00:00  Earnings     USDC  11.42429200
2021-01-26 09:00:00  Earnings     USDC  12.96254200
2021-01-27 09:00:00  Earnings     USDC  12.22091600
2021-01-28 09:00:00  Earnings     USDC  11.74139100
2021-01-29 09:00:00  Earnings     USDC  11.14081800
2021-01-30 09:00:00  Earnings     USDC  10.85179700
2021-01-31 09:00:00  Earnings     USDC  10.88462000
2021-02-01 09:00:00  Earnings     USDC  11.62614800
2021-02-02 09:00:00  Earnings     USDC  12.66880200
2021-02-03 09:00:00  Earnings     USDC  13.14905700
2021-02-04 09:00:00  Earnings     USDC  11.74103200
2021-02-05 09:00:00  Earnings     USDC  12.64466700
2021-02-06 09:00:00  Earnings     USDC  13.50551700
2021-02-07 09:00:00  Earnings     USDC  12.88773900
2021-02-08 09:00:00  Earnings     USDC  11.87728900
2021-02-09 09:00:00  Earnings     USDC  13.60013400
2021-02-10 09:00:00  Earnings     USDC  11.87017900
2021-02-11 09:00:00  Earnings     USDC   0.01139700
2021-02-12 09:00:00  Earnings     USDC   0.01322200
2021-02-13 09:00:00  Earnings     USDC   0.01372400
2021-02-14 09:00:00  Earnings     USDC   0.01402200
2021-02-15 09:00:00  Earnings     USDC   0.01310700
2021-02-16 09:00:00  Earnings     USDC   0.01129500
2021-02-17 09:00:00  Earnings     USDC   0.00987800
2021-02-18 09:00:00  Earnings     USDC   0.00981400
2021-02-19 09:00:00  Earnings     USDC   0.01008000
2021-02-20 09:00:00  Earnings     USDC   2.37429000
2021-02-21 09:00:00  Earnings     USDC   2.13930100
2021-02-22 09:00:00  Earnings     USDC   2.13213200
2021-02-23 09:00:00  Earnings     USDC   2.13315300
2021-02-24 09:00:00  Earnings     USDC   2.22922100
2021-02-25 09:00:00  Earnings     USDC   1.90730500
2021-02-26 09:00:00  Earnings     USDC   1.94364000
2021-02-27 09:00:00  Earnings     USDC   1.73608600
2021-02-28 09:00:00  Earnings     USDC   1.82774900
2021-03-01 09:00:00  Earnings     USDC   1.61576000
2021-03-02 09:00:00  Earnings     USDC   1.72746800
2021-03-03 09:00:00  Earnings     USDC   1.77486700
2021-03-04 09:00:00  Earnings     USDC   1.82425600
2021-03-05 09:00:00  Earnings     USDC   1.81760100
2021-03-06 09:00:00  Earnings     USDC   1.70356600
2021-03-07 09:00:00  Earnings     USDC   1.74367100
2021-03-08 09:00:00  Earnings     USDC   1.73156200
2021-03-09 09:00:00  Earnings     USDC   2.03148300
2021-03-10 09:00:00  Earnings     USDC   2.04489600
2021-03-11 09:00:00  Earnings     USDC   2.39879500
2021-03-12 09:00:00  Earnings     USDC   2.74537200
2021-03-13 09:00:00  Earnings     USDC   2.53650500
2021-03-14 09:00:00  Earnings     USDC   2.41505600
2021-03-15 09:00:00  Earnings     USDC   2.23474800
2021-03-16 09:00:00  Earnings     USDC   1.98237200
2021-03-17 09:00:00  Earnings     USDC   2.13457600
2021-03-18 09:00:00  Earnings     USDC   2.16150600
2021-03-19 09:00:00  Earnings     USDC   2.27394200
2021-03-20 09:00:00  Earnings     USDC   2.05326200
2021-03-21 09:00:00  Earnings     USDC   2.00176700
2021-03-22 09:00:00  Earnings     USDC   2.14793200
2021-03-23 09:00:00  Earnings     USDC   2.25350700
2021-03-24 09:00:00  Earnings     USDC   2.26700200
2021-03-25 09:00:00  Earnings     USDC   2.72753000
2021-03-26 09:00:00  Earnings     USDC   2.25609400
2021-03-27 09:00:00  Earnings     USDC   2.47635600
2021-03-28 10:00:00  Earnings     USDC   2.71710100
2021-03-29 10:00:00  Earnings     USDC   2.36588800
2021-03-30 10:00:00  Earnings     USDC   2.30850400
2021-03-31 10:00:00  Earnings     USDC   2.36525100
2021-04-01 10:00:00  Earnings     USDC   2.29953000
2021-04-02 10:00:00  Earnings     USDC   2.18754400
2021-04-03 10:00:00  Earnings     USDC   2.77552300
2021-04-04 10:00:00  Earnings     USDC   3.96848500
2021-04-05 10:00:00  Earnings     USDC   3.00978000
2021-04-06 10:00:00  Earnings     USDC   2.68636300
2021-04-07 10:00:00  Earnings     USDC   2.85181000
2021-04-08 10:00:00  Earnings     USDC   2.67352200
TOTAL                                  638.13744300'''

		if PRINT:
			# print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		sbYieldRatesWithTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbYieldRatesWithTotalDf,
			{})

		sbYieldRatesWithTotalDfExpectedStr =  \
'             EARNING CAP     EARNING  D YIELD RATE  Y YIELD RATE\n' + \
'DATE                                                            ' + \
'''
2020-12-22  19571.690000    9.379352      1.000479      1.191100
2020-12-23  19581.069352    8.904065      1.000455      1.180500
2020-12-24  19589.973417    9.347525      1.000477      1.190200
2020-12-25  19599.320942    9.392593      1.000479      1.191100
2020-12-26  19608.713535    8.592407      1.000438      1.173400
2020-12-27  19617.305942    8.292884      1.000423      1.166800
2020-12-28  19625.598826    8.310218      1.000423      1.167100
2020-12-29  19633.909044    8.313737      1.000423      1.167100
2020-12-30  19642.222781    8.455467      1.000430      1.170100
2020-12-31  19650.678248    8.403842      1.000428      1.168900
2021-01-01  19659.082090    8.948668      1.000455      1.180700
2021-01-02  19668.030758   10.135962      1.000515      1.206900
2021-01-03  19678.166720   10.301844      1.000524      1.210500
2021-01-04  19688.468564    9.832568      1.000499      1.199900
2021-01-05  19698.301132    8.479607      1.000430      1.170100
2021-01-06  19706.780739    8.557067      1.000434      1.171700
2021-01-07  19715.337806    9.841483      1.000499      1.199800
2021-01-08  19725.179289   10.165414      1.000515      1.206900
2021-01-09  19735.344703    9.810875      1.000497      1.198900
2021-01-10  19745.155578    9.307769      1.000471      1.187700
2021-01-11  19754.463347    9.906126      1.000501      1.200800
2021-01-12  19764.369473    9.471690      1.000479      1.191100
2021-01-13  19773.841163    9.421595      1.000476      1.189900
2021-01-14  19783.262758    9.680693      1.000489      1.195500
2021-01-15  19792.943451    9.375956      1.000474      1.188700
2021-01-16  19802.319407    9.649140      1.000487      1.194600
2021-01-17  19811.968547    9.412372      1.000475      1.189300
2021-01-18  19821.380919   10.547116      1.000532      1.214300
2021-01-19  19831.928035   10.256449      1.000517      1.207700
2021-01-20  19842.184484    9.882131      1.000498      1.199300
2021-01-21  19852.066615   10.013951      1.000504      1.202100
2021-01-22  19862.080566   11.077537      1.000558      1.225700
2021-01-23  19873.158103   10.762764      1.000542      1.218500
2021-01-24  19883.920867   11.289467      1.000568      1.230200
2021-01-25  19895.210334   11.424292      1.000574      1.233100
2021-01-26  19906.634626   12.962542      1.000651      1.268200
2021-01-27  19919.597168   12.220916      1.000614      1.250900
2021-01-28  19931.818084   11.741391      1.000589      1.239800
2021-01-29  19943.559475   11.140818      1.000559      1.226100
2021-01-30  19954.700293   10.851797      1.000544      1.219500
2021-01-31  19965.552090   10.884620      1.000545      1.220100
2021-02-01  19976.436710   11.626148      1.000582      1.236600
2021-02-02  19988.062858   12.668802      1.000634      1.260200
2021-02-03  20000.731660   13.149057      1.000657      1.271100
2021-02-04  20013.880717   11.741032      1.000587      1.238700
2021-02-05  20025.621749   12.644667      1.000631      1.259100
2021-02-06  20038.266416   13.505517      1.000674      1.278800
2021-02-07  20051.771933   12.887739      1.000643      1.264300
2021-02-08  20064.659672   11.877289      1.000592      1.241100
2021-02-09  20076.536961   13.600134      1.000677      1.280400
2021-02-10  20090.137095   11.870179      1.000591      1.240600
2021-02-11     18.797274    0.011397      1.000606      1.247619
2021-02-12     18.808671    0.013222      1.000703      1.292393
2021-02-13     18.821893    0.013724      1.000729      1.304791
2021-02-14     18.835617    0.014022      1.000744      1.312088
2021-02-15     18.849639    0.013107      1.000695      1.288801
2021-02-16     18.862746    0.011295      1.000599      1.244204
2021-02-17     18.874041    0.009878      1.000523      1.210433
2021-02-18     18.883919    0.009814      1.000520      1.208816
2021-02-19     18.893733    0.010080      1.000534      1.214921
2021-02-20   4447.843813    2.374290      1.000534      1.215053
2021-02-21   4451.218103    2.139301      1.000481      1.191700
2021-02-22   4453.357404    2.132132      1.000479      1.190900
2021-02-23   4455.489536    2.133153      1.000479      1.190900
2021-02-24   4457.622689    2.229221      1.000500      1.200200
2021-02-25   4459.851910    1.907305      1.000428      1.168900
2021-02-26   4461.759215    1.943640      1.000436      1.172300
2021-02-27   4463.702855    1.736086      1.000389      1.152500
2021-02-28   4465.438941    1.827749      1.000409      1.161100
2021-03-01   4467.266690    1.615760      1.000362      1.141100
2021-03-02   4468.882450    1.727468      1.000387      1.151500
2021-03-03   4470.609918    1.774867      1.000397      1.155900
2021-03-04   4472.384785    1.824256      1.000408      1.160500
2021-03-05   4474.209041    1.817601      1.000406      1.159800
2021-03-06   4476.026642    1.703566      1.000381      1.149000
2021-03-07   4477.730208    1.743671      1.000389      1.152700
2021-03-08   4479.473879    1.731562      1.000387      1.151500
2021-03-09   4481.205441    2.031483      1.000453      1.179900
2021-03-10   4483.236924    2.044896      1.000456      1.181100
2021-03-11   4485.281820    2.398795      1.000535      1.215500
2021-03-12   4487.680615    2.745372      1.000612      1.250100
2021-03-13   4490.425987    2.536505      1.000565      1.228900
2021-03-14   4492.962492    2.415056      1.000538      1.216700
2021-03-15   4495.377548    2.234748      1.000497      1.198900
2021-03-16   4497.612296    1.982372      1.000441      1.174500
2021-03-17   4499.594668    2.134576      1.000474      1.189000
2021-03-18   4501.729244    2.161506      1.000480      1.191500
2021-03-19   4503.890750    2.273942      1.000505      1.202300
2021-03-20   4506.164692    2.053262      1.000456      1.180900
2021-03-21   4508.217954    2.001767      1.000444      1.175900
2021-03-22   4510.219721    2.147932      1.000476      1.189800
2021-03-23   4512.367653    2.253507      1.000499      1.199900
2021-03-24   4514.621160    2.267002      1.000502      1.201100
2021-03-25   4516.888162    2.727530      1.000604      1.246500
2021-03-26   4519.615692    2.256094      1.000499      1.199800
2021-03-27   4521.871786    2.476356      1.000548      1.221200
2021-03-28   4524.348142    2.717101      1.000601      1.245000
2021-03-29   4527.065243    2.365888      1.000523      1.210100
2021-03-30   4529.431131    2.308504      1.000510      1.204400
2021-03-31   4531.739635    2.365251      1.000522      1.209800
2021-04-01   4534.104886    2.299530      1.000507      1.203300
2021-04-02   4536.404416    2.187544      1.000482      1.192400
2021-04-03   4538.591960    2.775523      1.000612      1.250000
2021-04-04   4541.367483    3.968485      1.000874      1.375499
2021-04-05   4545.335968    3.009780      1.000662      1.273300
2021-04-06   4548.345748    2.686363      1.000591      1.240500
2021-04-07   4551.032111    2.851810      1.000627      1.256900
2021-04-08   4553.883921    2.673522      1.000587      1.238900
TOTAL        4556.557443  638.137443                            '''

		if PRINT:
			# print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
#			if PRINT_SB_EARNING_TOTALS:
			print(sbYieldRatesWithTotalDfActualStr)
		else:
			self.assertEqual(sbYieldRatesWithTotalDfExpectedStr, sbYieldRatesWithTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                       DEP/WITHDR                                                                           \n' + \
'                  USDC                                        CHF             CAPITAL                    DATE              YIELD            \n' + \
'        Tot incl yield   DF RATE   CUR RATE   CAP GAIN CAP GAIN %      USDC       CHF        FROM          TO DAYS   USDC    CHF  Y % YR Y %\n' + \
'OWNER                                                                                                                                       ' + \
'''
Béa           4,428.94  3,999.10   4,032.55      33.45       0.84  4,428.94  4,032.55  2021-02-20  2021-02-20    1   2.36   2.15 0.05  21.51
Béa               1.00      0.90       0.91       0.01       0.84  4,432.30  4,035.61  2021-02-21  2021-04-08   47 104.89  95.50 2.37  19.92
TOTAL         4,537.20  4,000.00   4,131.12      33.46       0.84                                                  107.26  97.66            ''' + \
'''
JPS           4,975.64  4,379.47   4,530.32     150.85       3.44  4,975.64  4,530.32  2020-12-22  2021-02-10   51 134.82 122.75 2.71  21.09
JPS          -5,105.68  4,563.05  -4,648.72  -9,211.77     201.88      4.78      4.35  2021-02-11  2021-04-08   57   0.14   0.13 3.00  20.85
TOTAL             4.92  8,942.52       4.48  -9,060.92    -101.32                                                  134.96 122.88            ''' + \
'''
Papa         14,596.05 12,854.78  13,289.70     434.92       3.38 14,596.05 13,289.70  2020-12-22  2021-02-10   51 395.50 360.10 2.71  21.09
Papa        -14,977.53 13,393.61 -13,637.04 -27,030.65     201.82     14.02     12.76  2021-02-11  2021-04-08   57   0.42   0.38 3.00  20.85
TOTAL            14.44 26,248.39      13.15 -26,595.73    -101.32                                                  395.92 360.48            ''' + \
'''
G TOTAL       4,556.56             4,148.75                                                                        638.14 581.02            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_1_fiat_simple_values_2_owners(self):
		"""
		CHSB crypto, 2 owners, 1 with 1 withdrawal, fixed yield rate,
		CHSB/CHF final rate of 1.5.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_2_owners.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_2_owners.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency     Net amount\n' + \
'Local time                                           ' + \
'''
2021-01-01 00:00:00  Earnings     CHSB     2.87273664
2021-01-02 00:00:00  Earnings     CHSB     2.87348687
2021-01-03 00:00:00  Earnings     CHSB     2.87423731
2021-01-04 00:00:00  Earnings     CHSB     2.87498794
2021-01-05 00:00:00  Earnings     CHSB     5.48731752
2021-01-06 00:00:00  Earnings     CHSB     7.05569784
2021-01-07 00:00:00  Earnings     CHSB     7.05754049
2021-01-08 00:00:00  Earnings     CHSB     7.05938362
2021-01-09 00:00:00  Earnings     CHSB     7.06122723
2021-01-10 00:00:00  Earnings     CHSB     6.93249239
2021-01-11 00:00:00  Earnings     CHSB     6.93611381
2021-01-12 00:00:00  Earnings     CHSB     6.93792523
2021-01-13 00:00:00  Earnings     CHSB     6.93973713
2021-01-14 00:00:00  Earnings     CHSB     6.94154950
2021-01-15 00:00:00  Earnings     CHSB     6.94336234
2021-01-16 00:00:00  Earnings     CHSB     6.94517565
2021-01-17 00:00:00  Earnings     CHSB     6.94698944
2021-01-18 00:00:00  Earnings     CHSB     6.94880370
2021-01-19 00:00:00  Earnings     CHSB     6.95061843
2021-01-20 00:00:00  Earnings     CHSB     6.95243364
2021-01-21 00:00:00  Earnings     CHSB     6.95424932
2021-01-22 00:00:00  Earnings     CHSB     6.95606548
2021-01-23 00:00:00  Earnings     CHSB     6.95788211
2021-01-24 00:00:00  Earnings     CHSB     6.95969922
2021-01-25 00:00:00  Earnings     CHSB     6.96151680
2021-01-26 00:00:00  Earnings     CHSB     6.96333485
2021-01-27 00:00:00  Earnings     CHSB     6.96515338
2021-01-28 00:00:00  Earnings     CHSB     6.96697239
2021-01-29 00:00:00  Earnings     CHSB     6.96879187
2021-01-30 00:00:00  Earnings     CHSB     6.97061182
2021-01-31 00:00:00  Earnings     CHSB     6.97243225
2021-02-01 00:00:00  Earnings     CHSB     6.97425316
2021-02-02 00:00:00  Earnings     CHSB     6.97607454
2021-02-03 00:00:00  Earnings     CHSB     6.97789640
2021-02-04 00:00:00  Earnings     CHSB     6.97971873
2021-02-05 00:00:00  Earnings     CHSB     6.98154154
2021-02-06 00:00:00  Earnings     CHSB     6.98336482
2021-02-07 00:00:00  Earnings     CHSB     6.98518858
2021-02-08 00:00:00  Earnings     CHSB     6.98701282
2021-02-09 00:00:00  Earnings     CHSB     6.98883753
2021-02-10 00:00:00  Earnings     CHSB     6.99066272
2021-02-11 00:00:00  Earnings     CHSB     6.99248839
2021-02-12 00:00:00  Earnings     CHSB     6.99431453
2021-02-13 00:00:00  Earnings     CHSB     6.99614115
2021-02-14 00:00:00  Earnings     CHSB     6.99796825
2021-02-15 00:00:00  Earnings     CHSB     6.99979583
2021-02-16 00:00:00  Earnings     CHSB     7.00162388
2021-02-17 00:00:00  Earnings     CHSB     7.00345241
2021-02-18 00:00:00  Earnings     CHSB     7.00528141
2021-02-19 00:00:00  Earnings     CHSB     7.00711090
2021-02-20 00:00:00  Earnings     CHSB     7.00894086
2021-02-21 00:00:00  Earnings     CHSB     7.01077130
2021-02-22 00:00:00  Earnings     CHSB     7.01260222
2021-02-23 00:00:00  Earnings     CHSB     7.01443361
2021-02-24 00:00:00  Earnings     CHSB     7.01626549
2021-02-25 00:00:00  Earnings     CHSB     7.01809784
2021-02-26 00:00:00  Earnings     CHSB     7.01993067
2021-02-27 00:00:00  Earnings     CHSB     7.02176398
2021-02-28 00:00:00  Earnings     CHSB     7.02359777
2021-03-01 00:00:00  Earnings     CHSB     7.02543204
2021-03-02 00:00:00  Earnings     CHSB     7.02726679
2021-03-03 00:00:00  Earnings     CHSB     7.02910201
2021-03-04 00:00:00  Earnings     CHSB     7.03093772
2021-03-05 00:00:00  Earnings     CHSB     7.03277390
2021-03-06 00:00:00  Earnings     CHSB     7.03461057
2021-03-07 00:00:00  Earnings     CHSB     7.03644771
2021-03-08 00:00:00  Earnings     CHSB     7.03828534
2021-03-09 00:00:00  Earnings     CHSB     7.04012344
2021-03-10 00:00:00  Earnings     CHSB     7.04196202
2021-03-11 00:00:00  Earnings     CHSB     7.04380109
2021-03-12 00:00:00  Earnings     CHSB     7.04564063
2021-03-13 00:00:00  Earnings     CHSB     7.04748066
2021-03-14 00:00:00  Earnings     CHSB     7.04932116
2021-03-15 00:00:00  Earnings     CHSB     7.05116215
2021-03-16 00:00:00  Earnings     CHSB     7.05300361
2021-03-17 00:00:00  Earnings     CHSB     7.05484556
2021-03-18 00:00:00  Earnings     CHSB     7.05668799
2021-03-19 00:00:00  Earnings     CHSB     7.05853090
2021-03-20 00:00:00  Earnings     CHSB     7.06037429
2021-03-21 00:00:00  Earnings     CHSB     7.06221816
2021-03-22 00:00:00  Earnings     CHSB     7.06406252
2021-03-23 00:00:00  Earnings     CHSB     7.06590735
2021-03-24 00:00:00  Earnings     CHSB     7.06775267
2021-03-25 00:00:00  Earnings     CHSB     7.06959847
2021-03-26 00:00:00  Earnings     CHSB     7.07144475
2021-03-27 00:00:00  Earnings     CHSB     7.07329151
2021-03-28 00:00:00  Earnings     CHSB     7.07513876
2021-03-29 00:00:00  Earnings     CHSB     7.07698649
2021-03-30 00:00:00  Earnings     CHSB     7.07883470
2021-03-31 00:00:00  Earnings     CHSB     7.08068339
2021-04-01 00:00:00  Earnings     CHSB     7.08253257
2021-04-02 00:00:00  Earnings     CHSB     7.08438223
2021-04-03 00:00:00  Earnings     CHSB     7.08623237
2021-04-04 00:00:00  Earnings     CHSB     7.08808299
2021-04-05 00:00:00  Earnings     CHSB     7.08993410
2021-04-06 00:00:00  Earnings     CHSB     7.09178569
2021-04-07 00:00:00  Earnings     CHSB     7.09363777
2021-04-08 00:00:00  Earnings     CHSB     7.09549033
2021-04-09 00:00:00  Earnings     CHSB     7.09734337
2021-04-10 00:00:00  Earnings     CHSB     7.09919690
2021-04-11 00:00:00  Earnings     CHSB     7.10105091
2021-04-12 00:00:00  Earnings     CHSB     7.10290541
2021-04-13 00:00:00  Earnings     CHSB     7.10476039
2021-04-14 00:00:00  Earnings     CHSB     7.10661585
2021-04-15 00:00:00  Earnings     CHSB     7.10847180
2021-04-16 00:00:00  Earnings     CHSB     7.11032823
2021-04-17 00:00:00  Earnings     CHSB     7.11218515
2021-04-18 00:00:00  Earnings     CHSB     7.11404255
2021-04-19 00:00:00  Earnings     CHSB     7.11590044
2021-04-20 00:00:00  Earnings     CHSB     7.11775882
2021-04-21 00:00:00  Earnings     CHSB     7.11961767
2021-04-22 00:00:00  Earnings     CHSB     7.12147702
2021-04-23 00:00:00  Earnings     CHSB     7.12333685
2021-04-24 00:00:00  Earnings     CHSB     7.12519716
2021-04-25 00:00:00  Earnings     CHSB     7.12705796
2021-04-26 00:00:00  Earnings     CHSB     7.12891925
2021-04-27 00:00:00  Earnings     CHSB     7.13078103
2021-04-28 00:00:00  Earnings     CHSB     7.13264329
2021-04-29 00:00:00  Earnings     CHSB     7.13450603
2021-04-30 00:00:00  Earnings     CHSB     7.13636926
2021-05-01 00:00:00  Earnings     CHSB     7.13823298
2021-05-02 00:00:00  Earnings     CHSB     7.14009719
2021-05-03 00:00:00  Earnings     CHSB     7.14196188
2021-05-04 00:00:00  Earnings     CHSB     7.14382706
2021-05-05 00:00:00  Earnings     CHSB     7.14569273
2021-05-06 00:00:00  Earnings     CHSB     7.14755888
2021-05-07 00:00:00  Earnings     CHSB     7.14942552
2021-05-08 00:00:00  Earnings     CHSB     7.15129265
2021-05-09 00:00:00  Earnings     CHSB     7.15316027
2021-05-10 00:00:00  Earnings     CHSB     7.15502837
2021-05-11 00:00:00  Earnings     CHSB     7.15689696
2021-05-12 00:00:00  Earnings     CHSB     7.15876604
2021-05-13 00:00:00  Earnings     CHSB     7.16063561
2021-05-14 00:00:00  Earnings     CHSB     7.16250567
2021-05-15 00:00:00  Earnings     CHSB     7.16437621
2021-05-16 00:00:00  Earnings     CHSB     7.16624725
2021-05-17 00:00:00  Earnings     CHSB     7.16811877
2021-05-18 00:00:00  Earnings     CHSB     7.16999078
2021-05-19 00:00:00  Earnings     CHSB     7.17186328
2021-05-20 00:00:00  Earnings     CHSB     7.17373627
2021-05-21 00:00:00  Earnings     CHSB     7.17560975
2021-05-22 00:00:00  Earnings     CHSB     7.17748371
2021-05-23 00:00:00  Earnings     CHSB     7.17935817
2021-05-24 00:00:00  Earnings     CHSB     7.18123311
2021-05-25 00:00:00  Earnings     CHSB     7.18310855
2021-05-26 00:00:00  Earnings     CHSB     7.18498448
2021-05-27 00:00:00  Earnings     CHSB     7.18686089
2021-05-28 00:00:00  Earnings     CHSB     7.18873780
2021-05-29 00:00:00  Earnings     CHSB     7.19061519
2021-05-30 00:00:00  Earnings     CHSB     7.19249308
2021-05-31 00:00:00  Earnings     CHSB     7.19437145
2021-06-01 00:00:00  Earnings     CHSB     7.19625032
2021-06-02 00:00:00  Earnings     CHSB     7.19812968
2021-06-03 00:00:00  Earnings     CHSB     7.20000953
2021-06-04 00:00:00  Earnings     CHSB     7.20188987
2021-06-05 00:00:00  Earnings     CHSB     7.20377070
2021-06-06 00:00:00  Earnings     CHSB     7.20565202
2021-06-07 00:00:00  Earnings     CHSB     7.20753383
2021-06-08 00:00:00  Earnings     CHSB     7.20941613
2021-06-09 00:00:00  Earnings     CHSB     7.21129893
2021-06-10 00:00:00  Earnings     CHSB     7.21318222
2021-06-11 00:00:00  Earnings     CHSB     7.21506600
2021-06-12 00:00:00  Earnings     CHSB     7.21695027
2021-06-13 00:00:00  Earnings     CHSB     7.21883503
2021-06-14 00:00:00  Earnings     CHSB     7.22072029
2021-06-15 00:00:00  Earnings     CHSB     7.22260603
2021-06-16 00:00:00  Earnings     CHSB     7.22449228
2021-06-17 00:00:00  Earnings     CHSB     7.22637901
2021-06-18 00:00:00  Earnings     CHSB     7.22826623
2021-06-19 00:00:00  Earnings     CHSB     7.23015395
2021-06-20 00:00:00  Earnings     CHSB     7.23204216
2021-06-21 00:00:00  Earnings     CHSB     7.23393087
2021-06-22 00:00:00  Earnings     CHSB     7.23582007
2021-06-23 00:00:00  Earnings     CHSB     7.23770976
2021-06-24 00:00:00  Earnings     CHSB     7.23959994
2021-06-25 00:00:00  Earnings     CHSB     7.24149062
2021-06-26 00:00:00  Earnings     CHSB     7.24338179
2021-06-27 00:00:00  Earnings     CHSB     7.24527346
2021-06-28 00:00:00  Earnings     CHSB     7.24716562
2021-06-29 00:00:00  Earnings     CHSB     7.24905828
2021-06-30 00:00:00  Earnings     CHSB     7.25095142
2021-07-01 00:00:00  Earnings     CHSB     7.25284507
2021-07-02 00:00:00  Earnings     CHSB     7.25473920
2021-07-03 00:00:00  Earnings     CHSB     7.25663384
2021-07-04 00:00:00  Earnings     CHSB     7.25852896
2021-07-05 00:00:00  Earnings     CHSB     7.26042459
2021-07-06 00:00:00  Earnings     CHSB     7.26232070
2021-07-07 00:00:00  Earnings     CHSB     7.26421732
2021-07-08 00:00:00  Earnings     CHSB     7.26611442
2021-07-09 00:00:00  Earnings     CHSB     7.26801203
2021-07-10 00:00:00  Earnings     CHSB     7.26991012
2021-07-11 00:00:00  Earnings     CHSB     7.27180872
2021-07-12 00:00:00  Earnings     CHSB     7.27370781
2021-07-13 00:00:00  Earnings     CHSB     7.27560739
2021-07-14 00:00:00  Earnings     CHSB     7.27750748
2021-07-15 00:00:00  Earnings     CHSB     7.27940806
2021-07-16 00:00:00  Earnings     CHSB     7.28130913
2021-07-17 00:00:00  Earnings     CHSB     7.28321070
2021-07-18 00:00:00  Earnings     CHSB     7.28511277
2021-07-19 00:00:00  Earnings     CHSB     7.28701533
2021-07-20 00:00:00  Earnings     CHSB     7.28891840
2021-07-21 00:00:00  Earnings     CHSB     7.29082195
2021-07-22 00:00:00  Earnings     CHSB     7.29272601
2021-07-23 00:00:00  Earnings     CHSB     7.29463056
2021-07-24 00:00:00  Earnings     CHSB     7.29653561
2021-07-25 00:00:00  Earnings     CHSB     7.29844116
2021-07-26 00:00:00  Earnings     CHSB     7.30034721
2021-07-27 00:00:00  Earnings     CHSB     7.30225375
2021-07-28 00:00:00  Earnings     CHSB     7.30416079
2021-07-29 00:00:00  Earnings     CHSB     7.30606833
2021-07-30 00:00:00  Earnings     CHSB     7.30797637
2021-07-31 00:00:00  Earnings     CHSB     7.30988490
2021-08-01 00:00:00  Earnings     CHSB     7.31179394
2021-08-02 00:00:00  Earnings     CHSB     7.31370347
2021-08-03 00:00:00  Earnings     CHSB     7.31561350
2021-08-04 00:00:00  Earnings     CHSB     7.31752403
2021-08-05 00:00:00  Earnings     CHSB     7.31943506
2021-08-06 00:00:00  Earnings     CHSB     7.32134659
2021-08-07 00:00:00  Earnings     CHSB     7.32325861
2021-08-08 00:00:00  Earnings     CHSB     7.32517114
2021-08-09 00:00:00  Earnings     CHSB     7.32708417
2021-08-10 00:00:00  Earnings     CHSB     7.32899769
2021-08-11 00:00:00  Earnings     CHSB     7.33091172
2021-08-12 00:00:00  Earnings     CHSB     7.33282624
2021-08-13 00:00:00  Earnings     CHSB     7.33474127
2021-08-14 00:00:00  Earnings     CHSB     7.33665679
2021-08-15 00:00:00  Earnings     CHSB     7.33857282
2021-08-16 00:00:00  Earnings     CHSB     7.34048935
2021-08-17 00:00:00  Earnings     CHSB     7.34240637
2021-08-18 00:00:00  Earnings     CHSB     7.34432390
2021-08-19 00:00:00  Earnings     CHSB     7.34624193
2021-08-20 00:00:00  Earnings     CHSB     7.34816046
2021-08-21 00:00:00  Earnings     CHSB     7.35007949
2021-08-22 00:00:00  Earnings     CHSB     7.35199902
2021-08-23 00:00:00  Earnings     CHSB     7.35391905
2021-08-24 00:00:00  Earnings     CHSB     7.35583958
2021-08-25 00:00:00  Earnings     CHSB     7.35776062
2021-08-26 00:00:00  Earnings     CHSB     7.35968216
2021-08-27 00:00:00  Earnings     CHSB     7.36160420
2021-08-28 00:00:00  Earnings     CHSB     7.36352674
2021-08-29 00:00:00  Earnings     CHSB     7.36544978
2021-08-30 00:00:00  Earnings     CHSB     7.36737333
2021-08-31 00:00:00  Earnings     CHSB     7.36929737
2021-09-01 00:00:00  Earnings     CHSB     7.37122192
2021-09-02 00:00:00  Earnings     CHSB     7.37314698
2021-09-03 00:00:00  Earnings     CHSB     7.37507253
2021-09-04 00:00:00  Earnings     CHSB     7.37699859
2021-09-05 00:00:00  Earnings     CHSB     7.37892515
2021-09-06 00:00:00  Earnings     CHSB     7.38085221
2021-09-07 00:00:00  Earnings     CHSB     7.38277978
2021-09-08 00:00:00  Earnings     CHSB     7.38470785
2021-09-09 00:00:00  Earnings     CHSB     7.38663643
2021-09-10 00:00:00  Earnings     CHSB     7.38856551
2021-09-11 00:00:00  Earnings     CHSB     7.39049509
2021-09-12 00:00:00  Earnings     CHSB     7.39242517
2021-09-13 00:00:00  Earnings     CHSB     7.39435576
2021-09-14 00:00:00  Earnings     CHSB     7.39628686
2021-09-15 00:00:00  Earnings     CHSB     7.39821846
2021-09-16 00:00:00  Earnings     CHSB     7.40015056
2021-09-17 00:00:00  Earnings     CHSB     7.40208317
2021-09-18 00:00:00  Earnings     CHSB     7.40401628
2021-09-19 00:00:00  Earnings     CHSB     7.40594990
2021-09-20 00:00:00  Earnings     CHSB     7.40788402
2021-09-21 00:00:00  Earnings     CHSB     7.40981865
2021-09-22 00:00:00  Earnings     CHSB     7.41175378
2021-09-23 00:00:00  Earnings     CHSB     7.41368942
2021-09-24 00:00:00  Earnings     CHSB     7.41562556
2021-09-25 00:00:00  Earnings     CHSB     7.41756221
2021-09-26 00:00:00  Earnings     CHSB     7.41949936
2021-09-27 00:00:00  Earnings     CHSB     7.42143703
2021-09-28 00:00:00  Earnings     CHSB     7.42337519
2021-09-29 00:00:00  Earnings     CHSB     7.42531386
2021-09-30 00:00:00  Earnings     CHSB     7.42725304
2021-10-01 00:00:00  Earnings     CHSB     7.42919273
2021-10-02 00:00:00  Earnings     CHSB     7.43113292
2021-10-03 00:00:00  Earnings     CHSB     7.43307362
2021-10-04 00:00:00  Earnings     CHSB     7.43501483
2021-10-05 00:00:00  Earnings     CHSB     7.43695654
2021-10-06 00:00:00  Earnings     CHSB     7.43889876
2021-10-07 00:00:00  Earnings     CHSB     7.44084149
2021-10-08 00:00:00  Earnings     CHSB     7.44278472
2021-10-09 00:00:00  Earnings     CHSB     7.44472846
2021-10-10 00:00:00  Earnings     CHSB     7.44667271
2021-10-11 00:00:00  Earnings     CHSB     7.44861747
2021-10-12 00:00:00  Earnings     CHSB     7.45056273
2021-10-13 00:00:00  Earnings     CHSB     7.45250851
2021-10-14 00:00:00  Earnings     CHSB     7.45445479
2021-10-15 00:00:00  Earnings     CHSB     7.45640158
2021-10-16 00:00:00  Earnings     CHSB     7.45834888
2021-10-17 00:00:00  Earnings     CHSB     7.46029668
2021-10-18 00:00:00  Earnings     CHSB     7.46224500
2021-10-19 00:00:00  Earnings     CHSB     7.46419382
2021-10-20 00:00:00  Earnings     CHSB     7.46614315
2021-10-21 00:00:00  Earnings     CHSB     7.46809300
2021-10-22 00:00:00  Earnings     CHSB     7.47004335
2021-10-23 00:00:00  Earnings     CHSB     7.47199421
2021-10-24 00:00:00  Earnings     CHSB     7.47394558
2021-10-25 00:00:00  Earnings     CHSB     7.47589746
2021-10-26 00:00:00  Earnings     CHSB     7.47784985
2021-10-27 00:00:00  Earnings     CHSB     7.47980275
2021-10-28 00:00:00  Earnings     CHSB     7.48175616
2021-10-29 00:00:00  Earnings     CHSB     7.48371008
2021-10-30 00:00:00  Earnings     CHSB     7.48566451
2021-10-31 00:00:00  Earnings     CHSB     7.48761945
2021-11-01 00:00:00  Earnings     CHSB     7.48957490
2021-11-02 00:00:00  Earnings     CHSB     7.49153086
2021-11-03 00:00:00  Earnings     CHSB     7.49348733
2021-11-04 00:00:00  Earnings     CHSB     7.49544431
2021-11-05 00:00:00  Earnings     CHSB     7.49740181
2021-11-06 00:00:00  Earnings     CHSB     7.49935981
2021-11-07 00:00:00  Earnings     CHSB     7.50131833
2021-11-08 00:00:00  Earnings     CHSB     7.50327736
2021-11-09 00:00:00  Earnings     CHSB     7.50523690
2021-11-10 00:00:00  Earnings     CHSB     7.50719695
2021-11-11 00:00:00  Earnings     CHSB     7.50915751
2021-11-12 00:00:00  Earnings     CHSB     7.51111859
2021-11-13 00:00:00  Earnings     CHSB     7.51308018
2021-11-14 00:00:00  Earnings     CHSB     7.51504228
2021-11-15 00:00:00  Earnings     CHSB     7.51700489
2021-11-16 00:00:00  Earnings     CHSB     7.51896802
2021-11-17 00:00:00  Earnings     CHSB     7.52093165
2021-11-18 00:00:00  Earnings     CHSB     7.52289580
2021-11-19 00:00:00  Earnings     CHSB     7.52486047
2021-11-20 00:00:00  Earnings     CHSB     7.52682564
2021-11-21 00:00:00  Earnings     CHSB     7.52879133
2021-11-22 00:00:00  Earnings     CHSB     7.53075754
2021-11-23 00:00:00  Earnings     CHSB     7.53272425
2021-11-24 00:00:00  Earnings     CHSB     7.53469148
2021-11-25 00:00:00  Earnings     CHSB     7.53665923
2021-11-26 00:00:00  Earnings     CHSB     7.53862749
2021-11-27 00:00:00  Earnings     CHSB     7.54059626
2021-11-28 00:00:00  Earnings     CHSB     7.54256554
2021-11-29 00:00:00  Earnings     CHSB     7.54453534
2021-11-30 00:00:00  Earnings     CHSB     7.54650566
2021-12-01 00:00:00  Earnings     CHSB     7.54847649
2021-12-02 00:00:00  Earnings     CHSB     7.55044783
2021-12-03 00:00:00  Earnings     CHSB     7.55241969
2021-12-04 00:00:00  Earnings     CHSB     7.55439207
2021-12-05 00:00:00  Earnings     CHSB     7.55636495
2021-12-06 00:00:00  Earnings     CHSB     7.55833836
2021-12-07 00:00:00  Earnings     CHSB     7.56031228
2021-12-08 00:00:00  Earnings     CHSB     7.56228671
2021-12-09 00:00:00  Earnings     CHSB     7.56426166
2021-12-10 00:00:00  Earnings     CHSB     7.56623713
2021-12-11 00:00:00  Earnings     CHSB     7.56821311
2021-12-12 00:00:00  Earnings     CHSB     7.57018961
2021-12-13 00:00:00  Earnings     CHSB     7.57216663
2021-12-14 00:00:00  Earnings     CHSB     7.57414416
2021-12-15 00:00:00  Earnings     CHSB     7.57612220
2021-12-16 00:00:00  Earnings     CHSB     7.57810077
2021-12-17 00:00:00  Earnings     CHSB     7.58007985
2021-12-18 00:00:00  Earnings     CHSB     7.58205945
2021-12-19 00:00:00  Earnings     CHSB     7.58403956
2021-12-20 00:00:00  Earnings     CHSB     7.58602019
2021-12-21 00:00:00  Earnings     CHSB     7.58800134
2021-12-22 00:00:00  Earnings     CHSB     7.58998301
2021-12-23 00:00:00  Earnings     CHSB     7.59196519
2021-12-24 00:00:00  Earnings     CHSB     7.59394789
2021-12-25 00:00:00  Earnings     CHSB     7.59593111
2021-12-26 00:00:00  Earnings     CHSB     7.59791485
2021-12-27 00:00:00  Earnings     CHSB     7.59989911
2021-12-28 00:00:00  Earnings     CHSB     7.60188388
2021-12-29 00:00:00  Earnings     CHSB     7.60386917
2021-12-30 00:00:00  Earnings     CHSB     7.60585498
2021-12-31 00:00:00  Earnings     CHSB     7.60784131
TOTAL                                  2,631.86967354'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                     DEP/WITHDR                                                                                \n' + \
'                  CHSB                                      CHF             CAPITAL                    DATE                  YIELD             \n' + \
'        Tot incl yield   DF RATE  CUR RATE  CAP GAIN CAP GAIN %      CHSB       CHF        FROM          TO DAYS     CHSB      CHF   Y % YR Y %\n' + \
'OWNER                                                                                                                                          ' + \
'''
JPS          10,000.00  5,000.00 15,000.00 10,000.00     200.00 10,000.00 15,000.00  2021-01-01  2021-01-04    4    10.45    15.68  0.10  10.00
JPS          10,000.00 10,000.00 15,000.00  5,000.00      50.00 20,010.45 30,015.68  2021-01-05  2021-01-05    1     5.23     7.84  0.03  10.00
JPS           1,000.00  2,000.00  1,500.00   -500.00     -25.00 21,015.68 31,523.51  2021-01-06  2021-01-09    4    24.71    37.06  0.12  11.32
JPS            -500.00   -500.00   -750.00   -250.00     -50.00 20,540.38 30,810.57  2021-01-10  2021-12-31  356 2,256.55 3,384.82 10.99  11.28
TOTAL        22,796.93 16,500.00 34,195.39 14,250.00      86.36                                                  2,296.93 3,445.39             ''' + \
'''
Papa          1,000.00    500.00  1,500.00  1,000.00     200.00  1,000.00  1,500.00  2021-01-01  2021-01-05    5     1.31     1.96  0.13  10.00
Papa          2,000.00  4,000.00  3,000.00 -1,000.00     -25.00  3,001.31  4,501.96  2021-01-06  2021-12-31  360   333.64   500.45 11.12  11.28
TOTAL         3,334.94  4,500.00  5,002.41      0.00       0.00                                                    334.94   502.41             ''' + \
'''
G TOTAL      26,131.87           39,197.80                                                                       2,631.87 3,947.80             '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_1_fiat_simple_values_2_owners_1_deposit(self):
		"""
		CHSB crypto, 2 owners with 1 deposit, fixed yield rate,
		CHSB/CHF final rate of 1.5.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_2_owners_1_deposit.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_2_owners_1_deposit.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto = self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2021-01-01 00:00:00  Earnings     CHSB   1.00026116
2021-01-02 00:00:00  Earnings     CHSB   1.00026116
2021-01-03 00:00:00  Earnings     CHSB   1.00026116
2021-01-04 00:00:00  Earnings     CHSB   1.00026116
2021-01-05 00:00:00  Earnings     CHSB   1.00026116
2021-01-06 00:00:00  Earnings     CHSB   1.00026116
2021-01-07 00:00:00  Earnings     CHSB   1.00026116
2021-01-08 00:00:00  Earnings     CHSB   1.00026116
2021-01-09 00:00:00  Earnings     CHSB   1.00026116
2021-01-10 00:00:00  Earnings     CHSB   1.00026116
2021-01-11 00:00:00  Earnings     CHSB   1.00026116
2021-01-12 00:00:00  Earnings     CHSB   1.00026116
2021-01-13 00:00:00  Earnings     CHSB   1.00026116
2021-01-14 00:00:00  Earnings     CHSB   1.00026116
2021-01-15 00:00:00  Earnings     CHSB   1.00026116
2021-01-16 00:00:00  Earnings     CHSB   1.00026116
2021-01-17 00:00:00  Earnings     CHSB   1.00026116
2021-01-18 00:00:00  Earnings     CHSB   1.00026116
2021-01-19 00:00:00  Earnings     CHSB   1.00026116
2021-01-20 00:00:00  Earnings     CHSB   1.00026116
2021-01-21 00:00:00  Earnings     CHSB   1.00026116
2021-01-22 00:00:00  Earnings     CHSB   1.00026116
2021-01-23 00:00:00  Earnings     CHSB   1.00026116
2021-01-24 00:00:00  Earnings     CHSB   1.00026116
2021-01-25 00:00:00  Earnings     CHSB   1.00026116
2021-01-26 00:00:00  Earnings     CHSB   1.00026116
2021-01-27 00:00:00  Earnings     CHSB   1.00026116
2021-01-28 00:00:00  Earnings     CHSB   1.00026116
2021-01-29 00:00:00  Earnings     CHSB   1.00026116
2021-01-30 00:00:00  Earnings     CHSB   1.00026116
2021-01-31 00:00:00  Earnings     CHSB   1.00026116
2021-02-01 00:00:00  Earnings     CHSB   1.00026116
2021-02-02 00:00:00  Earnings     CHSB   1.00026116
2021-02-03 00:00:00  Earnings     CHSB   1.00026116
2021-02-04 00:00:00  Earnings     CHSB   1.00026116
2021-02-05 00:00:00  Earnings     CHSB   1.00026116
2021-02-06 00:00:00  Earnings     CHSB   1.00026116
2021-02-07 00:00:00  Earnings     CHSB   1.00026116
2021-02-08 00:00:00  Earnings     CHSB   1.00026116
2021-02-09 00:00:00  Earnings     CHSB   1.00026116
2021-02-10 00:00:00  Earnings     CHSB   1.00026116
2021-02-11 00:00:00  Earnings     CHSB   1.00026116
2021-02-12 00:00:00  Earnings     CHSB   1.00026116
2021-02-13 00:00:00  Earnings     CHSB   1.00026116
2021-02-14 00:00:00  Earnings     CHSB   1.00026116
2021-02-15 00:00:00  Earnings     CHSB   1.00026116
2021-02-16 00:00:00  Earnings     CHSB   1.00026116
2021-02-17 00:00:00  Earnings     CHSB   1.00026116
2021-02-18 00:00:00  Earnings     CHSB   1.00026116
2021-02-19 00:00:00  Earnings     CHSB   1.00026116
2021-02-20 00:00:00  Earnings     CHSB   1.00026116
2021-02-21 00:00:00  Earnings     CHSB   1.00026116
2021-02-22 00:00:00  Earnings     CHSB   1.00026116
2021-02-23 00:00:00  Earnings     CHSB   1.00026116
2021-02-24 00:00:00  Earnings     CHSB   1.00026116
2021-02-25 00:00:00  Earnings     CHSB   1.00026116
2021-02-26 00:00:00  Earnings     CHSB   1.00026116
2021-02-27 00:00:00  Earnings     CHSB   1.00026116
2021-02-28 00:00:00  Earnings     CHSB   1.00026116
2021-03-01 00:00:00  Earnings     CHSB   1.00026116
2021-03-02 00:00:00  Earnings     CHSB   1.00026116
2021-03-03 00:00:00  Earnings     CHSB   1.00026116
2021-03-04 00:00:00  Earnings     CHSB   1.00026116
2021-03-05 00:00:00  Earnings     CHSB   1.00026116
2021-03-06 00:00:00  Earnings     CHSB   1.00026116
2021-03-07 00:00:00  Earnings     CHSB   1.00026116
2021-03-08 00:00:00  Earnings     CHSB   1.00026116
2021-03-09 00:00:00  Earnings     CHSB   1.00026116
2021-03-10 00:00:00  Earnings     CHSB   1.00026116
2021-03-11 00:00:00  Earnings     CHSB   1.00026116
2021-03-12 00:00:00  Earnings     CHSB   1.00026116
2021-03-13 00:00:00  Earnings     CHSB   1.00026116
2021-03-14 00:00:00  Earnings     CHSB   1.00026116
2021-03-15 00:00:00  Earnings     CHSB   1.00026116
2021-03-16 00:00:00  Earnings     CHSB   1.00026116
2021-03-17 00:00:00  Earnings     CHSB   1.00026116
2021-03-18 00:00:00  Earnings     CHSB   1.00026116
2021-03-19 00:00:00  Earnings     CHSB   1.00026116
2021-03-20 00:00:00  Earnings     CHSB   1.00026116
2021-03-21 00:00:00  Earnings     CHSB   1.00026116
2021-03-22 00:00:00  Earnings     CHSB   1.00026116
2021-03-23 00:00:00  Earnings     CHSB   1.00026116
2021-03-24 00:00:00  Earnings     CHSB   1.00026116
2021-03-25 00:00:00  Earnings     CHSB   1.00026116
2021-03-26 00:00:00  Earnings     CHSB   1.00026116
2021-03-27 00:00:00  Earnings     CHSB   1.00026116
2021-03-28 00:00:00  Earnings     CHSB   1.00026116
2021-03-29 00:00:00  Earnings     CHSB   1.00026116
2021-03-30 00:00:00  Earnings     CHSB   1.00026116
2021-03-31 00:00:00  Earnings     CHSB   1.00026116
2021-04-01 00:00:00  Earnings     CHSB   1.00026116
2021-04-02 00:00:00  Earnings     CHSB   1.00026116
2021-04-03 00:00:00  Earnings     CHSB   1.00026116
2021-04-04 00:00:00  Earnings     CHSB   1.00026116
2021-04-05 00:00:00  Earnings     CHSB   1.00026116
2021-04-06 00:00:00  Earnings     CHSB   1.00026116
2021-04-07 00:00:00  Earnings     CHSB   1.00026116
2021-04-08 00:00:00  Earnings     CHSB   1.00026116
2021-04-09 00:00:00  Earnings     CHSB   1.00026116
2021-04-10 00:00:00  Earnings     CHSB   1.00026116
2021-04-11 00:00:00  Earnings     CHSB   1.00026116
2021-04-12 00:00:00  Earnings     CHSB   1.00026116
2021-04-13 00:00:00  Earnings     CHSB   1.00026116
2021-04-14 00:00:00  Earnings     CHSB   1.00026116
2021-04-15 00:00:00  Earnings     CHSB   1.00026116
2021-04-16 00:00:00  Earnings     CHSB   1.00026116
2021-04-17 00:00:00  Earnings     CHSB   1.00026116
2021-04-18 00:00:00  Earnings     CHSB   1.00026116
2021-04-19 00:00:00  Earnings     CHSB   1.00026116
2021-04-20 00:00:00  Earnings     CHSB   1.00026116
2021-04-21 00:00:00  Earnings     CHSB   1.00026116
2021-04-22 00:00:00  Earnings     CHSB   1.00026116
2021-04-23 00:00:00  Earnings     CHSB   1.00026116
2021-04-24 00:00:00  Earnings     CHSB   1.00026116
2021-04-25 00:00:00  Earnings     CHSB   1.00026116
2021-04-26 00:00:00  Earnings     CHSB   1.00026116
2021-04-27 00:00:00  Earnings     CHSB   1.00026116
2021-04-28 00:00:00  Earnings     CHSB   1.00026116
2021-04-29 00:00:00  Earnings     CHSB   1.00026116
2021-04-30 00:00:00  Earnings     CHSB   1.00026116
2021-05-01 00:00:00  Earnings     CHSB   1.00026116
2021-05-02 00:00:00  Earnings     CHSB   1.00026116
2021-05-03 00:00:00  Earnings     CHSB   1.00026116
2021-05-04 00:00:00  Earnings     CHSB   1.00026116
2021-05-05 00:00:00  Earnings     CHSB   1.00026116
2021-05-06 00:00:00  Earnings     CHSB   1.00026116
2021-05-07 00:00:00  Earnings     CHSB   1.00026116
2021-05-08 00:00:00  Earnings     CHSB   1.00026116
2021-05-09 00:00:00  Earnings     CHSB   1.00026116
2021-05-10 00:00:00  Earnings     CHSB   1.00026116
2021-05-11 00:00:00  Earnings     CHSB   1.00026116
2021-05-12 00:00:00  Earnings     CHSB   1.00026116
2021-05-13 00:00:00  Earnings     CHSB   1.00026116
2021-05-14 00:00:00  Earnings     CHSB   1.00026116
2021-05-15 00:00:00  Earnings     CHSB   1.00026116
2021-05-16 00:00:00  Earnings     CHSB   1.00026116
2021-05-17 00:00:00  Earnings     CHSB   1.00026116
2021-05-18 00:00:00  Earnings     CHSB   1.00026116
2021-05-19 00:00:00  Earnings     CHSB   1.00026116
2021-05-20 00:00:00  Earnings     CHSB   1.00026116
2021-05-21 00:00:00  Earnings     CHSB   1.00026116
2021-05-22 00:00:00  Earnings     CHSB   1.00026116
2021-05-23 00:00:00  Earnings     CHSB   1.00026116
2021-05-24 00:00:00  Earnings     CHSB   1.00026116
2021-05-25 00:00:00  Earnings     CHSB   1.00026116
2021-05-26 00:00:00  Earnings     CHSB   1.00026116
2021-05-27 00:00:00  Earnings     CHSB   1.00026116
2021-05-28 00:00:00  Earnings     CHSB   1.00026116
2021-05-29 00:00:00  Earnings     CHSB   1.00026116
2021-05-30 00:00:00  Earnings     CHSB   1.00026116
2021-05-31 00:00:00  Earnings     CHSB   1.00026116
2021-06-01 00:00:00  Earnings     CHSB   1.00026116
2021-06-02 00:00:00  Earnings     CHSB   1.00026116
2021-06-03 00:00:00  Earnings     CHSB   1.00026116
2021-06-04 00:00:00  Earnings     CHSB   1.00026116
2021-06-05 00:00:00  Earnings     CHSB   1.00026116
2021-06-06 00:00:00  Earnings     CHSB   1.00026116
2021-06-07 00:00:00  Earnings     CHSB   1.00026116
2021-06-08 00:00:00  Earnings     CHSB   1.00026116
2021-06-09 00:00:00  Earnings     CHSB   1.00026116
2021-06-10 00:00:00  Earnings     CHSB   1.00026116
2021-06-11 00:00:00  Earnings     CHSB   1.00026116
2021-06-12 00:00:00  Earnings     CHSB   1.00026116
2021-06-13 00:00:00  Earnings     CHSB   1.00026116
2021-06-14 00:00:00  Earnings     CHSB   1.00026116
2021-06-15 00:00:00  Earnings     CHSB   1.00026116
2021-06-16 00:00:00  Earnings     CHSB   1.00026116
2021-06-17 00:00:00  Earnings     CHSB   1.00026116
2021-06-18 00:00:00  Earnings     CHSB   1.00026116
2021-06-19 00:00:00  Earnings     CHSB   1.00026116
2021-06-20 00:00:00  Earnings     CHSB   1.00026116
2021-06-21 00:00:00  Earnings     CHSB   1.00026116
2021-06-22 00:00:00  Earnings     CHSB   1.00026116
2021-06-23 00:00:00  Earnings     CHSB   1.00026116
2021-06-24 00:00:00  Earnings     CHSB   1.00026116
2021-06-25 00:00:00  Earnings     CHSB   1.00026116
2021-06-26 00:00:00  Earnings     CHSB   1.00026116
2021-06-27 00:00:00  Earnings     CHSB   1.00026116
2021-06-28 00:00:00  Earnings     CHSB   1.00026116
2021-06-29 00:00:00  Earnings     CHSB   1.00026116
2021-06-30 00:00:00  Earnings     CHSB   1.00026116
2021-07-01 00:00:00  Earnings     CHSB   1.00026116
2021-07-02 00:00:00  Earnings     CHSB   1.00026116
2021-07-03 00:00:00  Earnings     CHSB   1.00026116
2021-07-04 00:00:00  Earnings     CHSB   1.00026116
2021-07-05 00:00:00  Earnings     CHSB   1.00026116
2021-07-06 00:00:00  Earnings     CHSB   1.00026116
2021-07-07 00:00:00  Earnings     CHSB   1.00026116
2021-07-08 00:00:00  Earnings     CHSB   1.00026116
2021-07-09 00:00:00  Earnings     CHSB   1.00026116
2021-07-10 00:00:00  Earnings     CHSB   1.00026116
2021-07-11 00:00:00  Earnings     CHSB   1.00026116
2021-07-12 00:00:00  Earnings     CHSB   1.00026116
2021-07-13 00:00:00  Earnings     CHSB   1.00026116
2021-07-14 00:00:00  Earnings     CHSB   1.00026116
2021-07-15 00:00:00  Earnings     CHSB   1.00026116
2021-07-16 00:00:00  Earnings     CHSB   1.00026116
2021-07-17 00:00:00  Earnings     CHSB   1.00026116
2021-07-18 00:00:00  Earnings     CHSB   1.00026116
2021-07-19 00:00:00  Earnings     CHSB   1.00026116
2021-07-20 00:00:00  Earnings     CHSB   1.00026116
2021-07-21 00:00:00  Earnings     CHSB   1.00026116
2021-07-22 00:00:00  Earnings     CHSB   1.00026116
2021-07-23 00:00:00  Earnings     CHSB   1.00026116
2021-07-24 00:00:00  Earnings     CHSB   1.00026116
2021-07-25 00:00:00  Earnings     CHSB   1.00026116
2021-07-26 00:00:00  Earnings     CHSB   1.00026116
2021-07-27 00:00:00  Earnings     CHSB   1.00026116
2021-07-28 00:00:00  Earnings     CHSB   1.00026116
2021-07-29 00:00:00  Earnings     CHSB   1.00026116
2021-07-30 00:00:00  Earnings     CHSB   1.00026116
2021-07-31 00:00:00  Earnings     CHSB   1.00026116
2021-08-01 00:00:00  Earnings     CHSB   1.00026116
2021-08-02 00:00:00  Earnings     CHSB   1.00026116
2021-08-03 00:00:00  Earnings     CHSB   1.00026116
2021-08-04 00:00:00  Earnings     CHSB   1.00026116
2021-08-05 00:00:00  Earnings     CHSB   1.00026116
2021-08-06 00:00:00  Earnings     CHSB   1.00026116
2021-08-07 00:00:00  Earnings     CHSB   1.00026116
2021-08-08 00:00:00  Earnings     CHSB   1.00026116
2021-08-09 00:00:00  Earnings     CHSB   1.00026116
2021-08-10 00:00:00  Earnings     CHSB   1.00026116
2021-08-11 00:00:00  Earnings     CHSB   1.00026116
2021-08-12 00:00:00  Earnings     CHSB   1.00026116
2021-08-13 00:00:00  Earnings     CHSB   1.00026116
2021-08-14 00:00:00  Earnings     CHSB   1.00026116
2021-08-15 00:00:00  Earnings     CHSB   1.00026116
2021-08-16 00:00:00  Earnings     CHSB   1.00026116
2021-08-17 00:00:00  Earnings     CHSB   1.00026116
2021-08-18 00:00:00  Earnings     CHSB   1.00026116
2021-08-19 00:00:00  Earnings     CHSB   1.00026116
2021-08-20 00:00:00  Earnings     CHSB   1.00026116
2021-08-21 00:00:00  Earnings     CHSB   1.00026116
2021-08-22 00:00:00  Earnings     CHSB   1.00026116
2021-08-23 00:00:00  Earnings     CHSB   1.00026116
2021-08-24 00:00:00  Earnings     CHSB   1.00026116
2021-08-25 00:00:00  Earnings     CHSB   1.00026116
2021-08-26 00:00:00  Earnings     CHSB   1.00026116
2021-08-27 00:00:00  Earnings     CHSB   1.00026116
2021-08-28 00:00:00  Earnings     CHSB   1.00026116
2021-08-29 00:00:00  Earnings     CHSB   1.00026116
2021-08-30 00:00:00  Earnings     CHSB   1.00026116
2021-08-31 00:00:00  Earnings     CHSB   1.00026116
2021-09-01 00:00:00  Earnings     CHSB   1.00026116
2021-09-02 00:00:00  Earnings     CHSB   1.00026116
2021-09-03 00:00:00  Earnings     CHSB   1.00026116
2021-09-04 00:00:00  Earnings     CHSB   1.00026116
2021-09-05 00:00:00  Earnings     CHSB   1.00026116
2021-09-06 00:00:00  Earnings     CHSB   1.00026116
2021-09-07 00:00:00  Earnings     CHSB   1.00026116
2021-09-08 00:00:00  Earnings     CHSB   1.00026116
2021-09-09 00:00:00  Earnings     CHSB   1.00026116
2021-09-10 00:00:00  Earnings     CHSB   1.00026116
2021-09-11 00:00:00  Earnings     CHSB   1.00026116
2021-09-12 00:00:00  Earnings     CHSB   1.00026116
2021-09-13 00:00:00  Earnings     CHSB   1.00026116
2021-09-14 00:00:00  Earnings     CHSB   1.00026116
2021-09-15 00:00:00  Earnings     CHSB   1.00026116
2021-09-16 00:00:00  Earnings     CHSB   1.00026116
2021-09-17 00:00:00  Earnings     CHSB   1.00026116
2021-09-18 00:00:00  Earnings     CHSB   1.00026116
2021-09-19 00:00:00  Earnings     CHSB   1.00026116
2021-09-20 00:00:00  Earnings     CHSB   1.00026116
2021-09-21 00:00:00  Earnings     CHSB   1.00026116
2021-09-22 00:00:00  Earnings     CHSB   1.00026116
2021-09-23 00:00:00  Earnings     CHSB   1.00026116
2021-09-24 00:00:00  Earnings     CHSB   1.00026116
2021-09-25 00:00:00  Earnings     CHSB   1.00026116
2021-09-26 00:00:00  Earnings     CHSB   1.00026116
2021-09-27 00:00:00  Earnings     CHSB   1.00026116
2021-09-28 00:00:00  Earnings     CHSB   1.00026116
2021-09-29 00:00:00  Earnings     CHSB   1.00026116
2021-09-30 00:00:00  Earnings     CHSB   1.00026116
2021-10-01 00:00:00  Earnings     CHSB   1.00026116
2021-10-02 00:00:00  Earnings     CHSB   1.00026116
2021-10-03 00:00:00  Earnings     CHSB   1.00026116
2021-10-04 00:00:00  Earnings     CHSB   1.00026116
2021-10-05 00:00:00  Earnings     CHSB   1.00026116
2021-10-06 00:00:00  Earnings     CHSB   1.00026116
2021-10-07 00:00:00  Earnings     CHSB   1.00026116
2021-10-08 00:00:00  Earnings     CHSB   1.00026116
2021-10-09 00:00:00  Earnings     CHSB   1.00026116
2021-10-10 00:00:00  Earnings     CHSB   1.00026116
2021-10-11 00:00:00  Earnings     CHSB   1.00026116
2021-10-12 00:00:00  Earnings     CHSB   1.00026116
2021-10-13 00:00:00  Earnings     CHSB   1.00026116
2021-10-14 00:00:00  Earnings     CHSB   1.00026116
2021-10-15 00:00:00  Earnings     CHSB   1.00026116
2021-10-16 00:00:00  Earnings     CHSB   1.00026116
2021-10-17 00:00:00  Earnings     CHSB   1.00026116
2021-10-18 00:00:00  Earnings     CHSB   1.00026116
2021-10-19 00:00:00  Earnings     CHSB   1.00026116
2021-10-20 00:00:00  Earnings     CHSB   1.00026116
2021-10-21 00:00:00  Earnings     CHSB   1.00026116
2021-10-22 00:00:00  Earnings     CHSB   1.00026116
2021-10-23 00:00:00  Earnings     CHSB   1.00026116
2021-10-24 00:00:00  Earnings     CHSB   1.00026116
2021-10-25 00:00:00  Earnings     CHSB   1.00026116
2021-10-26 00:00:00  Earnings     CHSB   1.00026116
2021-10-27 00:00:00  Earnings     CHSB   1.00026116
2021-10-28 00:00:00  Earnings     CHSB   1.00026116
2021-10-29 00:00:00  Earnings     CHSB   1.00026116
2021-10-30 00:00:00  Earnings     CHSB   1.00026116
2021-10-31 00:00:00  Earnings     CHSB   1.00026116
2021-11-01 00:00:00  Earnings     CHSB   1.00026116
2021-11-02 00:00:00  Earnings     CHSB   1.00026116
2021-11-03 00:00:00  Earnings     CHSB   1.00026116
2021-11-04 00:00:00  Earnings     CHSB   1.00026116
2021-11-05 00:00:00  Earnings     CHSB   1.00026116
2021-11-06 00:00:00  Earnings     CHSB   1.00026116
2021-11-07 00:00:00  Earnings     CHSB   1.00026116
2021-11-08 00:00:00  Earnings     CHSB   1.00026116
2021-11-09 00:00:00  Earnings     CHSB   1.00026116
2021-11-10 00:00:00  Earnings     CHSB   1.00026116
2021-11-11 00:00:00  Earnings     CHSB   1.00026116
2021-11-12 00:00:00  Earnings     CHSB   1.00026116
2021-11-13 00:00:00  Earnings     CHSB   1.00026116
2021-11-14 00:00:00  Earnings     CHSB   1.00026116
2021-11-15 00:00:00  Earnings     CHSB   1.00026116
2021-11-16 00:00:00  Earnings     CHSB   1.00026116
2021-11-17 00:00:00  Earnings     CHSB   1.00026116
2021-11-18 00:00:00  Earnings     CHSB   1.00026116
2021-11-19 00:00:00  Earnings     CHSB   1.00026116
2021-11-20 00:00:00  Earnings     CHSB   1.00026116
2021-11-21 00:00:00  Earnings     CHSB   1.00026116
2021-11-22 00:00:00  Earnings     CHSB   1.00026116
2021-11-23 00:00:00  Earnings     CHSB   1.00026116
2021-11-24 00:00:00  Earnings     CHSB   1.00026116
2021-11-25 00:00:00  Earnings     CHSB   1.00026116
2021-11-26 00:00:00  Earnings     CHSB   1.00026116
2021-11-27 00:00:00  Earnings     CHSB   1.00026116
2021-11-28 00:00:00  Earnings     CHSB   1.00026116
2021-11-29 00:00:00  Earnings     CHSB   1.00026116
2021-11-30 00:00:00  Earnings     CHSB   1.00026116
2021-12-01 00:00:00  Earnings     CHSB   1.00026116
2021-12-02 00:00:00  Earnings     CHSB   1.00026116
2021-12-03 00:00:00  Earnings     CHSB   1.00026116
2021-12-04 00:00:00  Earnings     CHSB   1.00026116
2021-12-05 00:00:00  Earnings     CHSB   1.00026116
2021-12-06 00:00:00  Earnings     CHSB   1.00026116
2021-12-07 00:00:00  Earnings     CHSB   1.00026116
2021-12-08 00:00:00  Earnings     CHSB   1.00026116
2021-12-09 00:00:00  Earnings     CHSB   1.00026116
2021-12-10 00:00:00  Earnings     CHSB   1.00026116
2021-12-11 00:00:00  Earnings     CHSB   1.00026116
2021-12-12 00:00:00  Earnings     CHSB   1.00026116
2021-12-13 00:00:00  Earnings     CHSB   1.00026116
2021-12-14 00:00:00  Earnings     CHSB   1.00026116
2021-12-15 00:00:00  Earnings     CHSB   1.00026116
2021-12-16 00:00:00  Earnings     CHSB   1.00026116
2021-12-17 00:00:00  Earnings     CHSB   1.00026116
2021-12-18 00:00:00  Earnings     CHSB   1.00026116
2021-12-19 00:00:00  Earnings     CHSB   1.00026116
2021-12-20 00:00:00  Earnings     CHSB   1.00026116
2021-12-21 00:00:00  Earnings     CHSB   1.00026116
2021-12-22 00:00:00  Earnings     CHSB   1.00026116
2021-12-23 00:00:00  Earnings     CHSB   1.00026116
2021-12-24 00:00:00  Earnings     CHSB   1.00026116
2021-12-25 00:00:00  Earnings     CHSB   1.00026116
2021-12-26 00:00:00  Earnings     CHSB   1.00026116
2021-12-27 00:00:00  Earnings     CHSB   1.00026116
2021-12-28 00:00:00  Earnings     CHSB   1.00026116
2021-12-29 00:00:00  Earnings     CHSB   1.00026116
2021-12-30 00:00:00  Earnings     CHSB   1.00026116
2021-12-31 00:00:00  Earnings     CHSB   1.00026116
TOTAL                                  365.09532262'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                   DEP/WITHDR                                                                          \n' + \
'                  CHSB                                    CHF            CAPITAL                    DATE              YIELD            \n' + \
'        Tot incl yield  DF RATE  CUR RATE CAP GAIN CAP GAIN %     CHSB       CHF        FROM          TO DAYS   CHSB    CHF  Y % YR Y %\n' + \
'OWNER                                                                                                                                  ' + \
'''
JPS           9,000.00 4,500.00 13,500.00 9,000.00     200.00 9,000.00 13,500.00  2021-01-01  2021-12-31  365 328.59 492.88 3.65   3.65
TOTAL         9,328.59 4,500.00 13,992.88 9,000.00     200.00                                                 328.59 492.88            ''' + \
'''
Papa          1,000.00   500.00  1,500.00 1,000.00     200.00 1,000.00  1,500.00  2021-01-01  2021-12-31  365  36.51  54.76 3.65   3.65
TOTAL         1,036.51   500.00  1,554.76 1,000.00     200.00                                                  36.51  54.76            ''' + \
'''
G TOTAL      10,365.10          15,547.64                                                                     365.10 547.64            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_1_fiat_simple_values_1_owner_withdrawal_gain(self):
		"""
		CHSB crypto, 1 owner with 1 withdrawal, fixed yield rate,
		CHSB/CHF final rateof 1.5. Withdrawal of 500 CHSB for 2000 CHF,
		so a gain of 1250 CHF since current withdrawal CHF value is
		750 CHF.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_withdrawal_gain.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency     Net amount\n' + \
'Local time                                           ' + \
'''
2021-01-01 00:00:00  Earnings     CHSB     2.61157876
2021-01-02 00:00:00  Earnings     CHSB     2.61226080
2021-01-03 00:00:00  Earnings     CHSB     2.61294301
2021-01-04 00:00:00  Earnings     CHSB     2.61362540
2021-01-05 00:00:00  Earnings     CHSB     2.61430797
2021-01-06 00:00:00  Earnings     CHSB     2.87614859
2021-01-07 00:00:00  Earnings     CHSB     2.87689972
2021-01-08 00:00:00  Earnings     CHSB     2.87765104
2021-01-09 00:00:00  Earnings     CHSB     2.87840257
2021-01-10 00:00:00  Earnings     CHSB     2.74857534
2021-01-11 00:00:00  Earnings     CHSB     2.75001116
2021-01-12 00:00:00  Earnings     CHSB     2.75072934
2021-01-13 00:00:00  Earnings     CHSB     2.75144772
2021-01-14 00:00:00  Earnings     CHSB     2.75216628
2021-01-15 00:00:00  Earnings     CHSB     2.75288503
2021-01-16 00:00:00  Earnings     CHSB     2.75360397
2021-01-17 00:00:00  Earnings     CHSB     2.75432309
2021-01-18 00:00:00  Earnings     CHSB     2.75504241
2021-01-19 00:00:00  Earnings     CHSB     2.75576191
2021-01-20 00:00:00  Earnings     CHSB     2.75648160
2021-01-21 00:00:00  Earnings     CHSB     2.75720147
2021-01-22 00:00:00  Earnings     CHSB     2.75792154
2021-01-23 00:00:00  Earnings     CHSB     2.75864179
2021-01-24 00:00:00  Earnings     CHSB     2.75936223
2021-01-25 00:00:00  Earnings     CHSB     2.76008286
2021-01-26 00:00:00  Earnings     CHSB     2.76080368
2021-01-27 00:00:00  Earnings     CHSB     2.76152468
2021-01-28 00:00:00  Earnings     CHSB     2.76224588
2021-01-29 00:00:00  Earnings     CHSB     2.76296726
2021-01-30 00:00:00  Earnings     CHSB     2.76368883
2021-01-31 00:00:00  Earnings     CHSB     2.76441059
2021-02-01 00:00:00  Earnings     CHSB     2.76513254
2021-02-02 00:00:00  Earnings     CHSB     2.76585467
2021-02-03 00:00:00  Earnings     CHSB     2.76657700
2021-02-04 00:00:00  Earnings     CHSB     2.76729951
2021-02-05 00:00:00  Earnings     CHSB     2.76802221
2021-02-06 00:00:00  Earnings     CHSB     2.76874510
2021-02-07 00:00:00  Earnings     CHSB     2.76946818
2021-02-08 00:00:00  Earnings     CHSB     2.77019145
2021-02-09 00:00:00  Earnings     CHSB     2.77091491
2021-02-10 00:00:00  Earnings     CHSB     2.77163856
2021-02-11 00:00:00  Earnings     CHSB     2.77236239
2021-02-12 00:00:00  Earnings     CHSB     2.77308642
2021-02-13 00:00:00  Earnings     CHSB     2.77381063
2021-02-14 00:00:00  Earnings     CHSB     2.77453503
2021-02-15 00:00:00  Earnings     CHSB     2.77525962
2021-02-16 00:00:00  Earnings     CHSB     2.77598440
2021-02-17 00:00:00  Earnings     CHSB     2.77670937
2021-02-18 00:00:00  Earnings     CHSB     2.77743453
2021-02-19 00:00:00  Earnings     CHSB     2.77815988
2021-02-20 00:00:00  Earnings     CHSB     2.77888542
2021-02-21 00:00:00  Earnings     CHSB     2.77961115
2021-02-22 00:00:00  Earnings     CHSB     2.78033707
2021-02-23 00:00:00  Earnings     CHSB     2.78106317
2021-02-24 00:00:00  Earnings     CHSB     2.78178947
2021-02-25 00:00:00  Earnings     CHSB     2.78251596
2021-02-26 00:00:00  Earnings     CHSB     2.78324263
2021-02-27 00:00:00  Earnings     CHSB     2.78396950
2021-02-28 00:00:00  Earnings     CHSB     2.78469655
2021-03-01 00:00:00  Earnings     CHSB     2.78542380
2021-03-02 00:00:00  Earnings     CHSB     2.78615123
2021-03-03 00:00:00  Earnings     CHSB     2.78687886
2021-03-04 00:00:00  Earnings     CHSB     2.78760668
2021-03-05 00:00:00  Earnings     CHSB     2.78833468
2021-03-06 00:00:00  Earnings     CHSB     2.78906288
2021-03-07 00:00:00  Earnings     CHSB     2.78979126
2021-03-08 00:00:00  Earnings     CHSB     2.79051984
2021-03-09 00:00:00  Earnings     CHSB     2.79124860
2021-03-10 00:00:00  Earnings     CHSB     2.79197756
2021-03-11 00:00:00  Earnings     CHSB     2.79270671
2021-03-12 00:00:00  Earnings     CHSB     2.79343604
2021-03-13 00:00:00  Earnings     CHSB     2.79416557
2021-03-14 00:00:00  Earnings     CHSB     2.79489529
2021-03-15 00:00:00  Earnings     CHSB     2.79562520
2021-03-16 00:00:00  Earnings     CHSB     2.79635530
2021-03-17 00:00:00  Earnings     CHSB     2.79708559
2021-03-18 00:00:00  Earnings     CHSB     2.79781607
2021-03-19 00:00:00  Earnings     CHSB     2.79854674
2021-03-20 00:00:00  Earnings     CHSB     2.79927760
2021-03-21 00:00:00  Earnings     CHSB     2.80000866
2021-03-22 00:00:00  Earnings     CHSB     2.80073990
2021-03-23 00:00:00  Earnings     CHSB     2.80147134
2021-03-24 00:00:00  Earnings     CHSB     2.80220296
2021-03-25 00:00:00  Earnings     CHSB     2.80293478
2021-03-26 00:00:00  Earnings     CHSB     2.80366679
2021-03-27 00:00:00  Earnings     CHSB     2.80439899
2021-03-28 00:00:00  Earnings     CHSB     2.80513138
2021-03-29 00:00:00  Earnings     CHSB     2.80586396
2021-03-30 00:00:00  Earnings     CHSB     2.80659674
2021-03-31 00:00:00  Earnings     CHSB     2.80732970
2021-04-01 00:00:00  Earnings     CHSB     2.80806286
2021-04-02 00:00:00  Earnings     CHSB     2.80879621
2021-04-03 00:00:00  Earnings     CHSB     2.80952974
2021-04-04 00:00:00  Earnings     CHSB     2.81026348
2021-04-05 00:00:00  Earnings     CHSB     2.81099740
2021-04-06 00:00:00  Earnings     CHSB     2.81173151
2021-04-07 00:00:00  Earnings     CHSB     2.81246582
2021-04-08 00:00:00  Earnings     CHSB     2.81320032
2021-04-09 00:00:00  Earnings     CHSB     2.81393500
2021-04-10 00:00:00  Earnings     CHSB     2.81466989
2021-04-11 00:00:00  Earnings     CHSB     2.81540496
2021-04-12 00:00:00  Earnings     CHSB     2.81614022
2021-04-13 00:00:00  Earnings     CHSB     2.81687568
2021-04-14 00:00:00  Earnings     CHSB     2.81761133
2021-04-15 00:00:00  Earnings     CHSB     2.81834717
2021-04-16 00:00:00  Earnings     CHSB     2.81908321
2021-04-17 00:00:00  Earnings     CHSB     2.81981943
2021-04-18 00:00:00  Earnings     CHSB     2.82055585
2021-04-19 00:00:00  Earnings     CHSB     2.82129246
2021-04-20 00:00:00  Earnings     CHSB     2.82202926
2021-04-21 00:00:00  Earnings     CHSB     2.82276626
2021-04-22 00:00:00  Earnings     CHSB     2.82350345
2021-04-23 00:00:00  Earnings     CHSB     2.82424083
2021-04-24 00:00:00  Earnings     CHSB     2.82497840
2021-04-25 00:00:00  Earnings     CHSB     2.82571616
2021-04-26 00:00:00  Earnings     CHSB     2.82645412
2021-04-27 00:00:00  Earnings     CHSB     2.82719227
2021-04-28 00:00:00  Earnings     CHSB     2.82793062
2021-04-29 00:00:00  Earnings     CHSB     2.82866915
2021-04-30 00:00:00  Earnings     CHSB     2.82940788
2021-05-01 00:00:00  Earnings     CHSB     2.83014680
2021-05-02 00:00:00  Earnings     CHSB     2.83088592
2021-05-03 00:00:00  Earnings     CHSB     2.83162523
2021-05-04 00:00:00  Earnings     CHSB     2.83236473
2021-05-05 00:00:00  Earnings     CHSB     2.83310442
2021-05-06 00:00:00  Earnings     CHSB     2.83384431
2021-05-07 00:00:00  Earnings     CHSB     2.83458439
2021-05-08 00:00:00  Earnings     CHSB     2.83532466
2021-05-09 00:00:00  Earnings     CHSB     2.83606513
2021-05-10 00:00:00  Earnings     CHSB     2.83680579
2021-05-11 00:00:00  Earnings     CHSB     2.83754665
2021-05-12 00:00:00  Earnings     CHSB     2.83828769
2021-05-13 00:00:00  Earnings     CHSB     2.83902894
2021-05-14 00:00:00  Earnings     CHSB     2.83977037
2021-05-15 00:00:00  Earnings     CHSB     2.84051200
2021-05-16 00:00:00  Earnings     CHSB     2.84125382
2021-05-17 00:00:00  Earnings     CHSB     2.84199584
2021-05-18 00:00:00  Earnings     CHSB     2.84273805
2021-05-19 00:00:00  Earnings     CHSB     2.84348045
2021-05-20 00:00:00  Earnings     CHSB     2.84422305
2021-05-21 00:00:00  Earnings     CHSB     2.84496584
2021-05-22 00:00:00  Earnings     CHSB     2.84570882
2021-05-23 00:00:00  Earnings     CHSB     2.84645200
2021-05-24 00:00:00  Earnings     CHSB     2.84719538
2021-05-25 00:00:00  Earnings     CHSB     2.84793894
2021-05-26 00:00:00  Earnings     CHSB     2.84868271
2021-05-27 00:00:00  Earnings     CHSB     2.84942666
2021-05-28 00:00:00  Earnings     CHSB     2.85017081
2021-05-29 00:00:00  Earnings     CHSB     2.85091516
2021-05-30 00:00:00  Earnings     CHSB     2.85165970
2021-05-31 00:00:00  Earnings     CHSB     2.85240443
2021-06-01 00:00:00  Earnings     CHSB     2.85314936
2021-06-02 00:00:00  Earnings     CHSB     2.85389448
2021-06-03 00:00:00  Earnings     CHSB     2.85463980
2021-06-04 00:00:00  Earnings     CHSB     2.85538531
2021-06-05 00:00:00  Earnings     CHSB     2.85613101
2021-06-06 00:00:00  Earnings     CHSB     2.85687692
2021-06-07 00:00:00  Earnings     CHSB     2.85762301
2021-06-08 00:00:00  Earnings     CHSB     2.85836930
2021-06-09 00:00:00  Earnings     CHSB     2.85911579
2021-06-10 00:00:00  Earnings     CHSB     2.85986247
2021-06-11 00:00:00  Earnings     CHSB     2.86060934
2021-06-12 00:00:00  Earnings     CHSB     2.86135641
2021-06-13 00:00:00  Earnings     CHSB     2.86210368
2021-06-14 00:00:00  Earnings     CHSB     2.86285114
2021-06-15 00:00:00  Earnings     CHSB     2.86359880
2021-06-16 00:00:00  Earnings     CHSB     2.86434665
2021-06-17 00:00:00  Earnings     CHSB     2.86509470
2021-06-18 00:00:00  Earnings     CHSB     2.86584294
2021-06-19 00:00:00  Earnings     CHSB     2.86659137
2021-06-20 00:00:00  Earnings     CHSB     2.86734001
2021-06-21 00:00:00  Earnings     CHSB     2.86808884
2021-06-22 00:00:00  Earnings     CHSB     2.86883786
2021-06-23 00:00:00  Earnings     CHSB     2.86958708
2021-06-24 00:00:00  Earnings     CHSB     2.87033649
2021-06-25 00:00:00  Earnings     CHSB     2.87108611
2021-06-26 00:00:00  Earnings     CHSB     2.87183591
2021-06-27 00:00:00  Earnings     CHSB     2.87258592
2021-06-28 00:00:00  Earnings     CHSB     2.87333611
2021-06-29 00:00:00  Earnings     CHSB     2.87408651
2021-06-30 00:00:00  Earnings     CHSB     2.87483710
2021-07-01 00:00:00  Earnings     CHSB     2.87558788
2021-07-02 00:00:00  Earnings     CHSB     2.87633887
2021-07-03 00:00:00  Earnings     CHSB     2.87709005
2021-07-04 00:00:00  Earnings     CHSB     2.87784142
2021-07-05 00:00:00  Earnings     CHSB     2.87859299
2021-07-06 00:00:00  Earnings     CHSB     2.87934476
2021-07-07 00:00:00  Earnings     CHSB     2.88009672
2021-07-08 00:00:00  Earnings     CHSB     2.88084888
2021-07-09 00:00:00  Earnings     CHSB     2.88160124
2021-07-10 00:00:00  Earnings     CHSB     2.88235379
2021-07-11 00:00:00  Earnings     CHSB     2.88310654
2021-07-12 00:00:00  Earnings     CHSB     2.88385949
2021-07-13 00:00:00  Earnings     CHSB     2.88461263
2021-07-14 00:00:00  Earnings     CHSB     2.88536597
2021-07-15 00:00:00  Earnings     CHSB     2.88611950
2021-07-16 00:00:00  Earnings     CHSB     2.88687324
2021-07-17 00:00:00  Earnings     CHSB     2.88762717
2021-07-18 00:00:00  Earnings     CHSB     2.88838129
2021-07-19 00:00:00  Earnings     CHSB     2.88913562
2021-07-20 00:00:00  Earnings     CHSB     2.88989014
2021-07-21 00:00:00  Earnings     CHSB     2.89064486
2021-07-22 00:00:00  Earnings     CHSB     2.89139977
2021-07-23 00:00:00  Earnings     CHSB     2.89215488
2021-07-24 00:00:00  Earnings     CHSB     2.89291019
2021-07-25 00:00:00  Earnings     CHSB     2.89366570
2021-07-26 00:00:00  Earnings     CHSB     2.89442140
2021-07-27 00:00:00  Earnings     CHSB     2.89517730
2021-07-28 00:00:00  Earnings     CHSB     2.89593340
2021-07-29 00:00:00  Earnings     CHSB     2.89668970
2021-07-30 00:00:00  Earnings     CHSB     2.89744619
2021-07-31 00:00:00  Earnings     CHSB     2.89820288
2021-08-01 00:00:00  Earnings     CHSB     2.89895977
2021-08-02 00:00:00  Earnings     CHSB     2.89971685
2021-08-03 00:00:00  Earnings     CHSB     2.90047414
2021-08-04 00:00:00  Earnings     CHSB     2.90123162
2021-08-05 00:00:00  Earnings     CHSB     2.90198930
2021-08-06 00:00:00  Earnings     CHSB     2.90274718
2021-08-07 00:00:00  Earnings     CHSB     2.90350525
2021-08-08 00:00:00  Earnings     CHSB     2.90426353
2021-08-09 00:00:00  Earnings     CHSB     2.90502200
2021-08-10 00:00:00  Earnings     CHSB     2.90578067
2021-08-11 00:00:00  Earnings     CHSB     2.90653953
2021-08-12 00:00:00  Earnings     CHSB     2.90729860
2021-08-13 00:00:00  Earnings     CHSB     2.90805786
2021-08-14 00:00:00  Earnings     CHSB     2.90881733
2021-08-15 00:00:00  Earnings     CHSB     2.90957699
2021-08-16 00:00:00  Earnings     CHSB     2.91033685
2021-08-17 00:00:00  Earnings     CHSB     2.91109690
2021-08-18 00:00:00  Earnings     CHSB     2.91185716
2021-08-19 00:00:00  Earnings     CHSB     2.91261761
2021-08-20 00:00:00  Earnings     CHSB     2.91337827
2021-08-21 00:00:00  Earnings     CHSB     2.91413912
2021-08-22 00:00:00  Earnings     CHSB     2.91490017
2021-08-23 00:00:00  Earnings     CHSB     2.91566142
2021-08-24 00:00:00  Earnings     CHSB     2.91642287
2021-08-25 00:00:00  Earnings     CHSB     2.91718451
2021-08-26 00:00:00  Earnings     CHSB     2.91794636
2021-08-27 00:00:00  Earnings     CHSB     2.91870840
2021-08-28 00:00:00  Earnings     CHSB     2.91947065
2021-08-29 00:00:00  Earnings     CHSB     2.92023309
2021-08-30 00:00:00  Earnings     CHSB     2.92099573
2021-08-31 00:00:00  Earnings     CHSB     2.92175857
2021-09-01 00:00:00  Earnings     CHSB     2.92252161
2021-09-02 00:00:00  Earnings     CHSB     2.92328485
2021-09-03 00:00:00  Earnings     CHSB     2.92404829
2021-09-04 00:00:00  Earnings     CHSB     2.92481193
2021-09-05 00:00:00  Earnings     CHSB     2.92557577
2021-09-06 00:00:00  Earnings     CHSB     2.92633980
2021-09-07 00:00:00  Earnings     CHSB     2.92710404
2021-09-08 00:00:00  Earnings     CHSB     2.92786848
2021-09-09 00:00:00  Earnings     CHSB     2.92863311
2021-09-10 00:00:00  Earnings     CHSB     2.92939795
2021-09-11 00:00:00  Earnings     CHSB     2.93016298
2021-09-12 00:00:00  Earnings     CHSB     2.93092822
2021-09-13 00:00:00  Earnings     CHSB     2.93169365
2021-09-14 00:00:00  Earnings     CHSB     2.93245929
2021-09-15 00:00:00  Earnings     CHSB     2.93322512
2021-09-16 00:00:00  Earnings     CHSB     2.93399116
2021-09-17 00:00:00  Earnings     CHSB     2.93475739
2021-09-18 00:00:00  Earnings     CHSB     2.93552383
2021-09-19 00:00:00  Earnings     CHSB     2.93629046
2021-09-20 00:00:00  Earnings     CHSB     2.93705730
2021-09-21 00:00:00  Earnings     CHSB     2.93782433
2021-09-22 00:00:00  Earnings     CHSB     2.93859157
2021-09-23 00:00:00  Earnings     CHSB     2.93935901
2021-09-24 00:00:00  Earnings     CHSB     2.94012664
2021-09-25 00:00:00  Earnings     CHSB     2.94089448
2021-09-26 00:00:00  Earnings     CHSB     2.94166252
2021-09-27 00:00:00  Earnings     CHSB     2.94243076
2021-09-28 00:00:00  Earnings     CHSB     2.94319920
2021-09-29 00:00:00  Earnings     CHSB     2.94396784
2021-09-30 00:00:00  Earnings     CHSB     2.94473668
2021-10-01 00:00:00  Earnings     CHSB     2.94550572
2021-10-02 00:00:00  Earnings     CHSB     2.94627496
2021-10-03 00:00:00  Earnings     CHSB     2.94704440
2021-10-04 00:00:00  Earnings     CHSB     2.94781405
2021-10-05 00:00:00  Earnings     CHSB     2.94858389
2021-10-06 00:00:00  Earnings     CHSB     2.94935394
2021-10-07 00:00:00  Earnings     CHSB     2.95012418
2021-10-08 00:00:00  Earnings     CHSB     2.95089463
2021-10-09 00:00:00  Earnings     CHSB     2.95166528
2021-10-10 00:00:00  Earnings     CHSB     2.95243613
2021-10-11 00:00:00  Earnings     CHSB     2.95320718
2021-10-12 00:00:00  Earnings     CHSB     2.95397844
2021-10-13 00:00:00  Earnings     CHSB     2.95474989
2021-10-14 00:00:00  Earnings     CHSB     2.95552155
2021-10-15 00:00:00  Earnings     CHSB     2.95629341
2021-10-16 00:00:00  Earnings     CHSB     2.95706546
2021-10-17 00:00:00  Earnings     CHSB     2.95783773
2021-10-18 00:00:00  Earnings     CHSB     2.95861019
2021-10-19 00:00:00  Earnings     CHSB     2.95938285
2021-10-20 00:00:00  Earnings     CHSB     2.96015572
2021-10-21 00:00:00  Earnings     CHSB     2.96092879
2021-10-22 00:00:00  Earnings     CHSB     2.96170206
2021-10-23 00:00:00  Earnings     CHSB     2.96247553
2021-10-24 00:00:00  Earnings     CHSB     2.96324920
2021-10-25 00:00:00  Earnings     CHSB     2.96402308
2021-10-26 00:00:00  Earnings     CHSB     2.96479716
2021-10-27 00:00:00  Earnings     CHSB     2.96557144
2021-10-28 00:00:00  Earnings     CHSB     2.96634592
2021-10-29 00:00:00  Earnings     CHSB     2.96712060
2021-10-30 00:00:00  Earnings     CHSB     2.96789549
2021-10-31 00:00:00  Earnings     CHSB     2.96867058
2021-11-01 00:00:00  Earnings     CHSB     2.96944587
2021-11-02 00:00:00  Earnings     CHSB     2.97022137
2021-11-03 00:00:00  Earnings     CHSB     2.97099706
2021-11-04 00:00:00  Earnings     CHSB     2.97177296
2021-11-05 00:00:00  Earnings     CHSB     2.97254906
2021-11-06 00:00:00  Earnings     CHSB     2.97332537
2021-11-07 00:00:00  Earnings     CHSB     2.97410187
2021-11-08 00:00:00  Earnings     CHSB     2.97487859
2021-11-09 00:00:00  Earnings     CHSB     2.97565550
2021-11-10 00:00:00  Earnings     CHSB     2.97643261
2021-11-11 00:00:00  Earnings     CHSB     2.97720993
2021-11-12 00:00:00  Earnings     CHSB     2.97798745
2021-11-13 00:00:00  Earnings     CHSB     2.97876518
2021-11-14 00:00:00  Earnings     CHSB     2.97954311
2021-11-15 00:00:00  Earnings     CHSB     2.98032124
2021-11-16 00:00:00  Earnings     CHSB     2.98109957
2021-11-17 00:00:00  Earnings     CHSB     2.98187811
2021-11-18 00:00:00  Earnings     CHSB     2.98265685
2021-11-19 00:00:00  Earnings     CHSB     2.98343580
2021-11-20 00:00:00  Earnings     CHSB     2.98421494
2021-11-21 00:00:00  Earnings     CHSB     2.98499429
2021-11-22 00:00:00  Earnings     CHSB     2.98577385
2021-11-23 00:00:00  Earnings     CHSB     2.98655361
2021-11-24 00:00:00  Earnings     CHSB     2.98733357
2021-11-25 00:00:00  Earnings     CHSB     2.98811374
2021-11-26 00:00:00  Earnings     CHSB     2.98889411
2021-11-27 00:00:00  Earnings     CHSB     2.98967468
2021-11-28 00:00:00  Earnings     CHSB     2.99045546
2021-11-29 00:00:00  Earnings     CHSB     2.99123644
2021-11-30 00:00:00  Earnings     CHSB     2.99201762
2021-12-01 00:00:00  Earnings     CHSB     2.99279901
2021-12-02 00:00:00  Earnings     CHSB     2.99358060
2021-12-03 00:00:00  Earnings     CHSB     2.99436240
2021-12-04 00:00:00  Earnings     CHSB     2.99514440
2021-12-05 00:00:00  Earnings     CHSB     2.99592661
2021-12-06 00:00:00  Earnings     CHSB     2.99670902
2021-12-07 00:00:00  Earnings     CHSB     2.99749163
2021-12-08 00:00:00  Earnings     CHSB     2.99827445
2021-12-09 00:00:00  Earnings     CHSB     2.99905747
2021-12-10 00:00:00  Earnings     CHSB     2.99984070
2021-12-11 00:00:00  Earnings     CHSB     3.00062413
2021-12-12 00:00:00  Earnings     CHSB     3.00140777
2021-12-13 00:00:00  Earnings     CHSB     3.00219161
2021-12-14 00:00:00  Earnings     CHSB     3.00297566
2021-12-15 00:00:00  Earnings     CHSB     3.00375991
2021-12-16 00:00:00  Earnings     CHSB     3.00454436
2021-12-17 00:00:00  Earnings     CHSB     3.00532902
2021-12-18 00:00:00  Earnings     CHSB     3.00611389
2021-12-19 00:00:00  Earnings     CHSB     3.00689896
2021-12-20 00:00:00  Earnings     CHSB     3.00768423
2021-12-21 00:00:00  Earnings     CHSB     3.00846971
2021-12-22 00:00:00  Earnings     CHSB     3.00925540
2021-12-23 00:00:00  Earnings     CHSB     3.01004129
2021-12-24 00:00:00  Earnings     CHSB     3.01082739
2021-12-25 00:00:00  Earnings     CHSB     3.01161369
2021-12-26 00:00:00  Earnings     CHSB     3.01240019
2021-12-27 00:00:00  Earnings     CHSB     3.01318691
2021-12-28 00:00:00  Earnings     CHSB     3.01397382
2021-12-29 00:00:00  Earnings     CHSB     3.01476095
2021-12-30 00:00:00  Earnings     CHSB     3.01554828
2021-12-31 00:00:00  Earnings     CHSB     3.01633581
TOTAL                                  1,050.12284407'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.maxDiff=None
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                     DEP/WITHDR                                                                               \n' + \
'                  CHSB                                      CHF             CAPITAL                    DATE                  YIELD            \n' + \
'        Tot incl yield   DF RATE  CUR RATE  CAP GAIN CAP GAIN %      CHSB       CHF        FROM          TO DAYS     CHSB      CHF  Y % YR Y %\n' + \
'OWNER                                                                                                                                         ' + \
'''
JPS          10,000.00  5,000.00 15,000.00 10,000.00     200.00 10,000.00 15,000.00  2021-01-01  2021-01-05    5    13.06    19.60 0.13  10.00
JPS           1,000.00  1,000.00  1,500.00    500.00      50.00 11,013.06 16,519.60  2021-01-06  2021-01-09    4    11.51    17.26 0.10  10.00
JPS            -500.00 -2,000.00   -750.00  1,250.00      62.50 10,524.57 15,786.86  2021-01-10  2021-12-31  356 1,025.55 1,538.32 9.74  10.00
TOTAL        11,550.12  4,000.00 17,325.18 11,750.00     293.75                                                  1,050.12 1,575.18            ''' + \
'''
G TOTAL      11,550.12           17,325.18                                                                       1,050.12 1,575.18            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_1_fiat_simple_values_1_owner_1_deposit_gain(self):
		"""
		CHSB crypto, 1 owner with 1 deposit, fixed yield rate,
		CHSB/CHF final rateof 1.5..
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner_1_deposit.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_1_deposit_gain.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto = self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2021-01-01 00:00:00  Earnings     CHSB   1.00026116
2021-01-02 00:00:00  Earnings     CHSB   1.00026116
2021-01-03 00:00:00  Earnings     CHSB   1.00026116
2021-01-04 00:00:00  Earnings     CHSB   1.00026116
2021-01-05 00:00:00  Earnings     CHSB   1.00026116
2021-01-06 00:00:00  Earnings     CHSB   1.00026116
2021-01-07 00:00:00  Earnings     CHSB   1.00026116
2021-01-08 00:00:00  Earnings     CHSB   1.00026116
2021-01-09 00:00:00  Earnings     CHSB   1.00026116
2021-01-10 00:00:00  Earnings     CHSB   1.00026116
2021-01-11 00:00:00  Earnings     CHSB   1.00026116
2021-01-12 00:00:00  Earnings     CHSB   1.00026116
2021-01-13 00:00:00  Earnings     CHSB   1.00026116
2021-01-14 00:00:00  Earnings     CHSB   1.00026116
2021-01-15 00:00:00  Earnings     CHSB   1.00026116
2021-01-16 00:00:00  Earnings     CHSB   1.00026116
2021-01-17 00:00:00  Earnings     CHSB   1.00026116
2021-01-18 00:00:00  Earnings     CHSB   1.00026116
2021-01-19 00:00:00  Earnings     CHSB   1.00026116
2021-01-20 00:00:00  Earnings     CHSB   1.00026116
2021-01-21 00:00:00  Earnings     CHSB   1.00026116
2021-01-22 00:00:00  Earnings     CHSB   1.00026116
2021-01-23 00:00:00  Earnings     CHSB   1.00026116
2021-01-24 00:00:00  Earnings     CHSB   1.00026116
2021-01-25 00:00:00  Earnings     CHSB   1.00026116
2021-01-26 00:00:00  Earnings     CHSB   1.00026116
2021-01-27 00:00:00  Earnings     CHSB   1.00026116
2021-01-28 00:00:00  Earnings     CHSB   1.00026116
2021-01-29 00:00:00  Earnings     CHSB   1.00026116
2021-01-30 00:00:00  Earnings     CHSB   1.00026116
2021-01-31 00:00:00  Earnings     CHSB   1.00026116
2021-02-01 00:00:00  Earnings     CHSB   1.00026116
2021-02-02 00:00:00  Earnings     CHSB   1.00026116
2021-02-03 00:00:00  Earnings     CHSB   1.00026116
2021-02-04 00:00:00  Earnings     CHSB   1.00026116
2021-02-05 00:00:00  Earnings     CHSB   1.00026116
2021-02-06 00:00:00  Earnings     CHSB   1.00026116
2021-02-07 00:00:00  Earnings     CHSB   1.00026116
2021-02-08 00:00:00  Earnings     CHSB   1.00026116
2021-02-09 00:00:00  Earnings     CHSB   1.00026116
2021-02-10 00:00:00  Earnings     CHSB   1.00026116
2021-02-11 00:00:00  Earnings     CHSB   1.00026116
2021-02-12 00:00:00  Earnings     CHSB   1.00026116
2021-02-13 00:00:00  Earnings     CHSB   1.00026116
2021-02-14 00:00:00  Earnings     CHSB   1.00026116
2021-02-15 00:00:00  Earnings     CHSB   1.00026116
2021-02-16 00:00:00  Earnings     CHSB   1.00026116
2021-02-17 00:00:00  Earnings     CHSB   1.00026116
2021-02-18 00:00:00  Earnings     CHSB   1.00026116
2021-02-19 00:00:00  Earnings     CHSB   1.00026116
2021-02-20 00:00:00  Earnings     CHSB   1.00026116
2021-02-21 00:00:00  Earnings     CHSB   1.00026116
2021-02-22 00:00:00  Earnings     CHSB   1.00026116
2021-02-23 00:00:00  Earnings     CHSB   1.00026116
2021-02-24 00:00:00  Earnings     CHSB   1.00026116
2021-02-25 00:00:00  Earnings     CHSB   1.00026116
2021-02-26 00:00:00  Earnings     CHSB   1.00026116
2021-02-27 00:00:00  Earnings     CHSB   1.00026116
2021-02-28 00:00:00  Earnings     CHSB   1.00026116
2021-03-01 00:00:00  Earnings     CHSB   1.00026116
2021-03-02 00:00:00  Earnings     CHSB   1.00026116
2021-03-03 00:00:00  Earnings     CHSB   1.00026116
2021-03-04 00:00:00  Earnings     CHSB   1.00026116
2021-03-05 00:00:00  Earnings     CHSB   1.00026116
2021-03-06 00:00:00  Earnings     CHSB   1.00026116
2021-03-07 00:00:00  Earnings     CHSB   1.00026116
2021-03-08 00:00:00  Earnings     CHSB   1.00026116
2021-03-09 00:00:00  Earnings     CHSB   1.00026116
2021-03-10 00:00:00  Earnings     CHSB   1.00026116
2021-03-11 00:00:00  Earnings     CHSB   1.00026116
2021-03-12 00:00:00  Earnings     CHSB   1.00026116
2021-03-13 00:00:00  Earnings     CHSB   1.00026116
2021-03-14 00:00:00  Earnings     CHSB   1.00026116
2021-03-15 00:00:00  Earnings     CHSB   1.00026116
2021-03-16 00:00:00  Earnings     CHSB   1.00026116
2021-03-17 00:00:00  Earnings     CHSB   1.00026116
2021-03-18 00:00:00  Earnings     CHSB   1.00026116
2021-03-19 00:00:00  Earnings     CHSB   1.00026116
2021-03-20 00:00:00  Earnings     CHSB   1.00026116
2021-03-21 00:00:00  Earnings     CHSB   1.00026116
2021-03-22 00:00:00  Earnings     CHSB   1.00026116
2021-03-23 00:00:00  Earnings     CHSB   1.00026116
2021-03-24 00:00:00  Earnings     CHSB   1.00026116
2021-03-25 00:00:00  Earnings     CHSB   1.00026116
2021-03-26 00:00:00  Earnings     CHSB   1.00026116
2021-03-27 00:00:00  Earnings     CHSB   1.00026116
2021-03-28 00:00:00  Earnings     CHSB   1.00026116
2021-03-29 00:00:00  Earnings     CHSB   1.00026116
2021-03-30 00:00:00  Earnings     CHSB   1.00026116
2021-03-31 00:00:00  Earnings     CHSB   1.00026116
2021-04-01 00:00:00  Earnings     CHSB   1.00026116
2021-04-02 00:00:00  Earnings     CHSB   1.00026116
2021-04-03 00:00:00  Earnings     CHSB   1.00026116
2021-04-04 00:00:00  Earnings     CHSB   1.00026116
2021-04-05 00:00:00  Earnings     CHSB   1.00026116
2021-04-06 00:00:00  Earnings     CHSB   1.00026116
2021-04-07 00:00:00  Earnings     CHSB   1.00026116
2021-04-08 00:00:00  Earnings     CHSB   1.00026116
2021-04-09 00:00:00  Earnings     CHSB   1.00026116
2021-04-10 00:00:00  Earnings     CHSB   1.00026116
2021-04-11 00:00:00  Earnings     CHSB   1.00026116
2021-04-12 00:00:00  Earnings     CHSB   1.00026116
2021-04-13 00:00:00  Earnings     CHSB   1.00026116
2021-04-14 00:00:00  Earnings     CHSB   1.00026116
2021-04-15 00:00:00  Earnings     CHSB   1.00026116
2021-04-16 00:00:00  Earnings     CHSB   1.00026116
2021-04-17 00:00:00  Earnings     CHSB   1.00026116
2021-04-18 00:00:00  Earnings     CHSB   1.00026116
2021-04-19 00:00:00  Earnings     CHSB   1.00026116
2021-04-20 00:00:00  Earnings     CHSB   1.00026116
2021-04-21 00:00:00  Earnings     CHSB   1.00026116
2021-04-22 00:00:00  Earnings     CHSB   1.00026116
2021-04-23 00:00:00  Earnings     CHSB   1.00026116
2021-04-24 00:00:00  Earnings     CHSB   1.00026116
2021-04-25 00:00:00  Earnings     CHSB   1.00026116
2021-04-26 00:00:00  Earnings     CHSB   1.00026116
2021-04-27 00:00:00  Earnings     CHSB   1.00026116
2021-04-28 00:00:00  Earnings     CHSB   1.00026116
2021-04-29 00:00:00  Earnings     CHSB   1.00026116
2021-04-30 00:00:00  Earnings     CHSB   1.00026116
2021-05-01 00:00:00  Earnings     CHSB   1.00026116
2021-05-02 00:00:00  Earnings     CHSB   1.00026116
2021-05-03 00:00:00  Earnings     CHSB   1.00026116
2021-05-04 00:00:00  Earnings     CHSB   1.00026116
2021-05-05 00:00:00  Earnings     CHSB   1.00026116
2021-05-06 00:00:00  Earnings     CHSB   1.00026116
2021-05-07 00:00:00  Earnings     CHSB   1.00026116
2021-05-08 00:00:00  Earnings     CHSB   1.00026116
2021-05-09 00:00:00  Earnings     CHSB   1.00026116
2021-05-10 00:00:00  Earnings     CHSB   1.00026116
2021-05-11 00:00:00  Earnings     CHSB   1.00026116
2021-05-12 00:00:00  Earnings     CHSB   1.00026116
2021-05-13 00:00:00  Earnings     CHSB   1.00026116
2021-05-14 00:00:00  Earnings     CHSB   1.00026116
2021-05-15 00:00:00  Earnings     CHSB   1.00026116
2021-05-16 00:00:00  Earnings     CHSB   1.00026116
2021-05-17 00:00:00  Earnings     CHSB   1.00026116
2021-05-18 00:00:00  Earnings     CHSB   1.00026116
2021-05-19 00:00:00  Earnings     CHSB   1.00026116
2021-05-20 00:00:00  Earnings     CHSB   1.00026116
2021-05-21 00:00:00  Earnings     CHSB   1.00026116
2021-05-22 00:00:00  Earnings     CHSB   1.00026116
2021-05-23 00:00:00  Earnings     CHSB   1.00026116
2021-05-24 00:00:00  Earnings     CHSB   1.00026116
2021-05-25 00:00:00  Earnings     CHSB   1.00026116
2021-05-26 00:00:00  Earnings     CHSB   1.00026116
2021-05-27 00:00:00  Earnings     CHSB   1.00026116
2021-05-28 00:00:00  Earnings     CHSB   1.00026116
2021-05-29 00:00:00  Earnings     CHSB   1.00026116
2021-05-30 00:00:00  Earnings     CHSB   1.00026116
2021-05-31 00:00:00  Earnings     CHSB   1.00026116
2021-06-01 00:00:00  Earnings     CHSB   1.00026116
2021-06-02 00:00:00  Earnings     CHSB   1.00026116
2021-06-03 00:00:00  Earnings     CHSB   1.00026116
2021-06-04 00:00:00  Earnings     CHSB   1.00026116
2021-06-05 00:00:00  Earnings     CHSB   1.00026116
2021-06-06 00:00:00  Earnings     CHSB   1.00026116
2021-06-07 00:00:00  Earnings     CHSB   1.00026116
2021-06-08 00:00:00  Earnings     CHSB   1.00026116
2021-06-09 00:00:00  Earnings     CHSB   1.00026116
2021-06-10 00:00:00  Earnings     CHSB   1.00026116
2021-06-11 00:00:00  Earnings     CHSB   1.00026116
2021-06-12 00:00:00  Earnings     CHSB   1.00026116
2021-06-13 00:00:00  Earnings     CHSB   1.00026116
2021-06-14 00:00:00  Earnings     CHSB   1.00026116
2021-06-15 00:00:00  Earnings     CHSB   1.00026116
2021-06-16 00:00:00  Earnings     CHSB   1.00026116
2021-06-17 00:00:00  Earnings     CHSB   1.00026116
2021-06-18 00:00:00  Earnings     CHSB   1.00026116
2021-06-19 00:00:00  Earnings     CHSB   1.00026116
2021-06-20 00:00:00  Earnings     CHSB   1.00026116
2021-06-21 00:00:00  Earnings     CHSB   1.00026116
2021-06-22 00:00:00  Earnings     CHSB   1.00026116
2021-06-23 00:00:00  Earnings     CHSB   1.00026116
2021-06-24 00:00:00  Earnings     CHSB   1.00026116
2021-06-25 00:00:00  Earnings     CHSB   1.00026116
2021-06-26 00:00:00  Earnings     CHSB   1.00026116
2021-06-27 00:00:00  Earnings     CHSB   1.00026116
2021-06-28 00:00:00  Earnings     CHSB   1.00026116
2021-06-29 00:00:00  Earnings     CHSB   1.00026116
2021-06-30 00:00:00  Earnings     CHSB   1.00026116
2021-07-01 00:00:00  Earnings     CHSB   1.00026116
2021-07-02 00:00:00  Earnings     CHSB   1.00026116
2021-07-03 00:00:00  Earnings     CHSB   1.00026116
2021-07-04 00:00:00  Earnings     CHSB   1.00026116
2021-07-05 00:00:00  Earnings     CHSB   1.00026116
2021-07-06 00:00:00  Earnings     CHSB   1.00026116
2021-07-07 00:00:00  Earnings     CHSB   1.00026116
2021-07-08 00:00:00  Earnings     CHSB   1.00026116
2021-07-09 00:00:00  Earnings     CHSB   1.00026116
2021-07-10 00:00:00  Earnings     CHSB   1.00026116
2021-07-11 00:00:00  Earnings     CHSB   1.00026116
2021-07-12 00:00:00  Earnings     CHSB   1.00026116
2021-07-13 00:00:00  Earnings     CHSB   1.00026116
2021-07-14 00:00:00  Earnings     CHSB   1.00026116
2021-07-15 00:00:00  Earnings     CHSB   1.00026116
2021-07-16 00:00:00  Earnings     CHSB   1.00026116
2021-07-17 00:00:00  Earnings     CHSB   1.00026116
2021-07-18 00:00:00  Earnings     CHSB   1.00026116
2021-07-19 00:00:00  Earnings     CHSB   1.00026116
2021-07-20 00:00:00  Earnings     CHSB   1.00026116
2021-07-21 00:00:00  Earnings     CHSB   1.00026116
2021-07-22 00:00:00  Earnings     CHSB   1.00026116
2021-07-23 00:00:00  Earnings     CHSB   1.00026116
2021-07-24 00:00:00  Earnings     CHSB   1.00026116
2021-07-25 00:00:00  Earnings     CHSB   1.00026116
2021-07-26 00:00:00  Earnings     CHSB   1.00026116
2021-07-27 00:00:00  Earnings     CHSB   1.00026116
2021-07-28 00:00:00  Earnings     CHSB   1.00026116
2021-07-29 00:00:00  Earnings     CHSB   1.00026116
2021-07-30 00:00:00  Earnings     CHSB   1.00026116
2021-07-31 00:00:00  Earnings     CHSB   1.00026116
2021-08-01 00:00:00  Earnings     CHSB   1.00026116
2021-08-02 00:00:00  Earnings     CHSB   1.00026116
2021-08-03 00:00:00  Earnings     CHSB   1.00026116
2021-08-04 00:00:00  Earnings     CHSB   1.00026116
2021-08-05 00:00:00  Earnings     CHSB   1.00026116
2021-08-06 00:00:00  Earnings     CHSB   1.00026116
2021-08-07 00:00:00  Earnings     CHSB   1.00026116
2021-08-08 00:00:00  Earnings     CHSB   1.00026116
2021-08-09 00:00:00  Earnings     CHSB   1.00026116
2021-08-10 00:00:00  Earnings     CHSB   1.00026116
2021-08-11 00:00:00  Earnings     CHSB   1.00026116
2021-08-12 00:00:00  Earnings     CHSB   1.00026116
2021-08-13 00:00:00  Earnings     CHSB   1.00026116
2021-08-14 00:00:00  Earnings     CHSB   1.00026116
2021-08-15 00:00:00  Earnings     CHSB   1.00026116
2021-08-16 00:00:00  Earnings     CHSB   1.00026116
2021-08-17 00:00:00  Earnings     CHSB   1.00026116
2021-08-18 00:00:00  Earnings     CHSB   1.00026116
2021-08-19 00:00:00  Earnings     CHSB   1.00026116
2021-08-20 00:00:00  Earnings     CHSB   1.00026116
2021-08-21 00:00:00  Earnings     CHSB   1.00026116
2021-08-22 00:00:00  Earnings     CHSB   1.00026116
2021-08-23 00:00:00  Earnings     CHSB   1.00026116
2021-08-24 00:00:00  Earnings     CHSB   1.00026116
2021-08-25 00:00:00  Earnings     CHSB   1.00026116
2021-08-26 00:00:00  Earnings     CHSB   1.00026116
2021-08-27 00:00:00  Earnings     CHSB   1.00026116
2021-08-28 00:00:00  Earnings     CHSB   1.00026116
2021-08-29 00:00:00  Earnings     CHSB   1.00026116
2021-08-30 00:00:00  Earnings     CHSB   1.00026116
2021-08-31 00:00:00  Earnings     CHSB   1.00026116
2021-09-01 00:00:00  Earnings     CHSB   1.00026116
2021-09-02 00:00:00  Earnings     CHSB   1.00026116
2021-09-03 00:00:00  Earnings     CHSB   1.00026116
2021-09-04 00:00:00  Earnings     CHSB   1.00026116
2021-09-05 00:00:00  Earnings     CHSB   1.00026116
2021-09-06 00:00:00  Earnings     CHSB   1.00026116
2021-09-07 00:00:00  Earnings     CHSB   1.00026116
2021-09-08 00:00:00  Earnings     CHSB   1.00026116
2021-09-09 00:00:00  Earnings     CHSB   1.00026116
2021-09-10 00:00:00  Earnings     CHSB   1.00026116
2021-09-11 00:00:00  Earnings     CHSB   1.00026116
2021-09-12 00:00:00  Earnings     CHSB   1.00026116
2021-09-13 00:00:00  Earnings     CHSB   1.00026116
2021-09-14 00:00:00  Earnings     CHSB   1.00026116
2021-09-15 00:00:00  Earnings     CHSB   1.00026116
2021-09-16 00:00:00  Earnings     CHSB   1.00026116
2021-09-17 00:00:00  Earnings     CHSB   1.00026116
2021-09-18 00:00:00  Earnings     CHSB   1.00026116
2021-09-19 00:00:00  Earnings     CHSB   1.00026116
2021-09-20 00:00:00  Earnings     CHSB   1.00026116
2021-09-21 00:00:00  Earnings     CHSB   1.00026116
2021-09-22 00:00:00  Earnings     CHSB   1.00026116
2021-09-23 00:00:00  Earnings     CHSB   1.00026116
2021-09-24 00:00:00  Earnings     CHSB   1.00026116
2021-09-25 00:00:00  Earnings     CHSB   1.00026116
2021-09-26 00:00:00  Earnings     CHSB   1.00026116
2021-09-27 00:00:00  Earnings     CHSB   1.00026116
2021-09-28 00:00:00  Earnings     CHSB   1.00026116
2021-09-29 00:00:00  Earnings     CHSB   1.00026116
2021-09-30 00:00:00  Earnings     CHSB   1.00026116
2021-10-01 00:00:00  Earnings     CHSB   1.00026116
2021-10-02 00:00:00  Earnings     CHSB   1.00026116
2021-10-03 00:00:00  Earnings     CHSB   1.00026116
2021-10-04 00:00:00  Earnings     CHSB   1.00026116
2021-10-05 00:00:00  Earnings     CHSB   1.00026116
2021-10-06 00:00:00  Earnings     CHSB   1.00026116
2021-10-07 00:00:00  Earnings     CHSB   1.00026116
2021-10-08 00:00:00  Earnings     CHSB   1.00026116
2021-10-09 00:00:00  Earnings     CHSB   1.00026116
2021-10-10 00:00:00  Earnings     CHSB   1.00026116
2021-10-11 00:00:00  Earnings     CHSB   1.00026116
2021-10-12 00:00:00  Earnings     CHSB   1.00026116
2021-10-13 00:00:00  Earnings     CHSB   1.00026116
2021-10-14 00:00:00  Earnings     CHSB   1.00026116
2021-10-15 00:00:00  Earnings     CHSB   1.00026116
2021-10-16 00:00:00  Earnings     CHSB   1.00026116
2021-10-17 00:00:00  Earnings     CHSB   1.00026116
2021-10-18 00:00:00  Earnings     CHSB   1.00026116
2021-10-19 00:00:00  Earnings     CHSB   1.00026116
2021-10-20 00:00:00  Earnings     CHSB   1.00026116
2021-10-21 00:00:00  Earnings     CHSB   1.00026116
2021-10-22 00:00:00  Earnings     CHSB   1.00026116
2021-10-23 00:00:00  Earnings     CHSB   1.00026116
2021-10-24 00:00:00  Earnings     CHSB   1.00026116
2021-10-25 00:00:00  Earnings     CHSB   1.00026116
2021-10-26 00:00:00  Earnings     CHSB   1.00026116
2021-10-27 00:00:00  Earnings     CHSB   1.00026116
2021-10-28 00:00:00  Earnings     CHSB   1.00026116
2021-10-29 00:00:00  Earnings     CHSB   1.00026116
2021-10-30 00:00:00  Earnings     CHSB   1.00026116
2021-10-31 00:00:00  Earnings     CHSB   1.00026116
2021-11-01 00:00:00  Earnings     CHSB   1.00026116
2021-11-02 00:00:00  Earnings     CHSB   1.00026116
2021-11-03 00:00:00  Earnings     CHSB   1.00026116
2021-11-04 00:00:00  Earnings     CHSB   1.00026116
2021-11-05 00:00:00  Earnings     CHSB   1.00026116
2021-11-06 00:00:00  Earnings     CHSB   1.00026116
2021-11-07 00:00:00  Earnings     CHSB   1.00026116
2021-11-08 00:00:00  Earnings     CHSB   1.00026116
2021-11-09 00:00:00  Earnings     CHSB   1.00026116
2021-11-10 00:00:00  Earnings     CHSB   1.00026116
2021-11-11 00:00:00  Earnings     CHSB   1.00026116
2021-11-12 00:00:00  Earnings     CHSB   1.00026116
2021-11-13 00:00:00  Earnings     CHSB   1.00026116
2021-11-14 00:00:00  Earnings     CHSB   1.00026116
2021-11-15 00:00:00  Earnings     CHSB   1.00026116
2021-11-16 00:00:00  Earnings     CHSB   1.00026116
2021-11-17 00:00:00  Earnings     CHSB   1.00026116
2021-11-18 00:00:00  Earnings     CHSB   1.00026116
2021-11-19 00:00:00  Earnings     CHSB   1.00026116
2021-11-20 00:00:00  Earnings     CHSB   1.00026116
2021-11-21 00:00:00  Earnings     CHSB   1.00026116
2021-11-22 00:00:00  Earnings     CHSB   1.00026116
2021-11-23 00:00:00  Earnings     CHSB   1.00026116
2021-11-24 00:00:00  Earnings     CHSB   1.00026116
2021-11-25 00:00:00  Earnings     CHSB   1.00026116
2021-11-26 00:00:00  Earnings     CHSB   1.00026116
2021-11-27 00:00:00  Earnings     CHSB   1.00026116
2021-11-28 00:00:00  Earnings     CHSB   1.00026116
2021-11-29 00:00:00  Earnings     CHSB   1.00026116
2021-11-30 00:00:00  Earnings     CHSB   1.00026116
2021-12-01 00:00:00  Earnings     CHSB   1.00026116
2021-12-02 00:00:00  Earnings     CHSB   1.00026116
2021-12-03 00:00:00  Earnings     CHSB   1.00026116
2021-12-04 00:00:00  Earnings     CHSB   1.00026116
2021-12-05 00:00:00  Earnings     CHSB   1.00026116
2021-12-06 00:00:00  Earnings     CHSB   1.00026116
2021-12-07 00:00:00  Earnings     CHSB   1.00026116
2021-12-08 00:00:00  Earnings     CHSB   1.00026116
2021-12-09 00:00:00  Earnings     CHSB   1.00026116
2021-12-10 00:00:00  Earnings     CHSB   1.00026116
2021-12-11 00:00:00  Earnings     CHSB   1.00026116
2021-12-12 00:00:00  Earnings     CHSB   1.00026116
2021-12-13 00:00:00  Earnings     CHSB   1.00026116
2021-12-14 00:00:00  Earnings     CHSB   1.00026116
2021-12-15 00:00:00  Earnings     CHSB   1.00026116
2021-12-16 00:00:00  Earnings     CHSB   1.00026116
2021-12-17 00:00:00  Earnings     CHSB   1.00026116
2021-12-18 00:00:00  Earnings     CHSB   1.00026116
2021-12-19 00:00:00  Earnings     CHSB   1.00026116
2021-12-20 00:00:00  Earnings     CHSB   1.00026116
2021-12-21 00:00:00  Earnings     CHSB   1.00026116
2021-12-22 00:00:00  Earnings     CHSB   1.00026116
2021-12-23 00:00:00  Earnings     CHSB   1.00026116
2021-12-24 00:00:00  Earnings     CHSB   1.00026116
2021-12-25 00:00:00  Earnings     CHSB   1.00026116
2021-12-26 00:00:00  Earnings     CHSB   1.00026116
2021-12-27 00:00:00  Earnings     CHSB   1.00026116
2021-12-28 00:00:00  Earnings     CHSB   1.00026116
2021-12-29 00:00:00  Earnings     CHSB   1.00026116
2021-12-30 00:00:00  Earnings     CHSB   1.00026116
2021-12-31 00:00:00  Earnings     CHSB   1.00026116
TOTAL                                  365.09532262'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.maxDiff = None
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                    DEP/WITHDR                                                                           \n' + \
'                  CHSB                                     CHF             CAPITAL                    DATE              YIELD            \n' + \
'        Tot incl yield  DF RATE  CUR RATE  CAP GAIN CAP GAIN %      CHSB       CHF        FROM          TO DAYS   CHSB    CHF  Y % YR Y %\n' + \
'OWNER                                                                                                                                    ' + \
'''
JPS          10,000.00 5,000.00 15,000.00 10,000.00     200.00 10,000.00 15,000.00  2021-01-01  2021-12-31  365 365.10 547.64 3.65   3.65
TOTAL        10,365.10 5,000.00 15,547.64 10,000.00     200.00                                                  365.10 547.64            ''' + \
'''
G TOTAL      10,365.10          15,547.64                                                                       365.10 547.64            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_1_fiat_simple_values_1_owner_withdrawal_loss(self):
		"""
		CHSB crypto, 2 owners, 1 with 1 withdrawal, fixed yield rate,
		CHSB/CHF final rateof 1.5. Withdrawal of 500 CHSB for 600 CHF,
		so a loss of 150 CHF since current withdrawal CHF value is
		750 CHF.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_withdrawal_loss.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency     Net amount\n' + \
'Local time                                           ' + \
'''
2021-01-01 00:00:00  Earnings     CHSB     2.61157876
2021-01-02 00:00:00  Earnings     CHSB     2.61226080
2021-01-03 00:00:00  Earnings     CHSB     2.61294301
2021-01-04 00:00:00  Earnings     CHSB     2.61362540
2021-01-05 00:00:00  Earnings     CHSB     2.61430797
2021-01-06 00:00:00  Earnings     CHSB     2.87614859
2021-01-07 00:00:00  Earnings     CHSB     2.87689972
2021-01-08 00:00:00  Earnings     CHSB     2.87765104
2021-01-09 00:00:00  Earnings     CHSB     2.87840257
2021-01-10 00:00:00  Earnings     CHSB     2.74857534
2021-01-11 00:00:00  Earnings     CHSB     2.75001116
2021-01-12 00:00:00  Earnings     CHSB     2.75072934
2021-01-13 00:00:00  Earnings     CHSB     2.75144772
2021-01-14 00:00:00  Earnings     CHSB     2.75216628
2021-01-15 00:00:00  Earnings     CHSB     2.75288503
2021-01-16 00:00:00  Earnings     CHSB     2.75360397
2021-01-17 00:00:00  Earnings     CHSB     2.75432309
2021-01-18 00:00:00  Earnings     CHSB     2.75504241
2021-01-19 00:00:00  Earnings     CHSB     2.75576191
2021-01-20 00:00:00  Earnings     CHSB     2.75648160
2021-01-21 00:00:00  Earnings     CHSB     2.75720147
2021-01-22 00:00:00  Earnings     CHSB     2.75792154
2021-01-23 00:00:00  Earnings     CHSB     2.75864179
2021-01-24 00:00:00  Earnings     CHSB     2.75936223
2021-01-25 00:00:00  Earnings     CHSB     2.76008286
2021-01-26 00:00:00  Earnings     CHSB     2.76080368
2021-01-27 00:00:00  Earnings     CHSB     2.76152468
2021-01-28 00:00:00  Earnings     CHSB     2.76224588
2021-01-29 00:00:00  Earnings     CHSB     2.76296726
2021-01-30 00:00:00  Earnings     CHSB     2.76368883
2021-01-31 00:00:00  Earnings     CHSB     2.76441059
2021-02-01 00:00:00  Earnings     CHSB     2.76513254
2021-02-02 00:00:00  Earnings     CHSB     2.76585467
2021-02-03 00:00:00  Earnings     CHSB     2.76657700
2021-02-04 00:00:00  Earnings     CHSB     2.76729951
2021-02-05 00:00:00  Earnings     CHSB     2.76802221
2021-02-06 00:00:00  Earnings     CHSB     2.76874510
2021-02-07 00:00:00  Earnings     CHSB     2.76946818
2021-02-08 00:00:00  Earnings     CHSB     2.77019145
2021-02-09 00:00:00  Earnings     CHSB     2.77091491
2021-02-10 00:00:00  Earnings     CHSB     2.77163856
2021-02-11 00:00:00  Earnings     CHSB     2.77236239
2021-02-12 00:00:00  Earnings     CHSB     2.77308642
2021-02-13 00:00:00  Earnings     CHSB     2.77381063
2021-02-14 00:00:00  Earnings     CHSB     2.77453503
2021-02-15 00:00:00  Earnings     CHSB     2.77525962
2021-02-16 00:00:00  Earnings     CHSB     2.77598440
2021-02-17 00:00:00  Earnings     CHSB     2.77670937
2021-02-18 00:00:00  Earnings     CHSB     2.77743453
2021-02-19 00:00:00  Earnings     CHSB     2.77815988
2021-02-20 00:00:00  Earnings     CHSB     2.77888542
2021-02-21 00:00:00  Earnings     CHSB     2.77961115
2021-02-22 00:00:00  Earnings     CHSB     2.78033707
2021-02-23 00:00:00  Earnings     CHSB     2.78106317
2021-02-24 00:00:00  Earnings     CHSB     2.78178947
2021-02-25 00:00:00  Earnings     CHSB     2.78251596
2021-02-26 00:00:00  Earnings     CHSB     2.78324263
2021-02-27 00:00:00  Earnings     CHSB     2.78396950
2021-02-28 00:00:00  Earnings     CHSB     2.78469655
2021-03-01 00:00:00  Earnings     CHSB     2.78542380
2021-03-02 00:00:00  Earnings     CHSB     2.78615123
2021-03-03 00:00:00  Earnings     CHSB     2.78687886
2021-03-04 00:00:00  Earnings     CHSB     2.78760668
2021-03-05 00:00:00  Earnings     CHSB     2.78833468
2021-03-06 00:00:00  Earnings     CHSB     2.78906288
2021-03-07 00:00:00  Earnings     CHSB     2.78979126
2021-03-08 00:00:00  Earnings     CHSB     2.79051984
2021-03-09 00:00:00  Earnings     CHSB     2.79124860
2021-03-10 00:00:00  Earnings     CHSB     2.79197756
2021-03-11 00:00:00  Earnings     CHSB     2.79270671
2021-03-12 00:00:00  Earnings     CHSB     2.79343604
2021-03-13 00:00:00  Earnings     CHSB     2.79416557
2021-03-14 00:00:00  Earnings     CHSB     2.79489529
2021-03-15 00:00:00  Earnings     CHSB     2.79562520
2021-03-16 00:00:00  Earnings     CHSB     2.79635530
2021-03-17 00:00:00  Earnings     CHSB     2.79708559
2021-03-18 00:00:00  Earnings     CHSB     2.79781607
2021-03-19 00:00:00  Earnings     CHSB     2.79854674
2021-03-20 00:00:00  Earnings     CHSB     2.79927760
2021-03-21 00:00:00  Earnings     CHSB     2.80000866
2021-03-22 00:00:00  Earnings     CHSB     2.80073990
2021-03-23 00:00:00  Earnings     CHSB     2.80147134
2021-03-24 00:00:00  Earnings     CHSB     2.80220296
2021-03-25 00:00:00  Earnings     CHSB     2.80293478
2021-03-26 00:00:00  Earnings     CHSB     2.80366679
2021-03-27 00:00:00  Earnings     CHSB     2.80439899
2021-03-28 00:00:00  Earnings     CHSB     2.80513138
2021-03-29 00:00:00  Earnings     CHSB     2.80586396
2021-03-30 00:00:00  Earnings     CHSB     2.80659674
2021-03-31 00:00:00  Earnings     CHSB     2.80732970
2021-04-01 00:00:00  Earnings     CHSB     2.80806286
2021-04-02 00:00:00  Earnings     CHSB     2.80879621
2021-04-03 00:00:00  Earnings     CHSB     2.80952974
2021-04-04 00:00:00  Earnings     CHSB     2.81026348
2021-04-05 00:00:00  Earnings     CHSB     2.81099740
2021-04-06 00:00:00  Earnings     CHSB     2.81173151
2021-04-07 00:00:00  Earnings     CHSB     2.81246582
2021-04-08 00:00:00  Earnings     CHSB     2.81320032
2021-04-09 00:00:00  Earnings     CHSB     2.81393500
2021-04-10 00:00:00  Earnings     CHSB     2.81466989
2021-04-11 00:00:00  Earnings     CHSB     2.81540496
2021-04-12 00:00:00  Earnings     CHSB     2.81614022
2021-04-13 00:00:00  Earnings     CHSB     2.81687568
2021-04-14 00:00:00  Earnings     CHSB     2.81761133
2021-04-15 00:00:00  Earnings     CHSB     2.81834717
2021-04-16 00:00:00  Earnings     CHSB     2.81908321
2021-04-17 00:00:00  Earnings     CHSB     2.81981943
2021-04-18 00:00:00  Earnings     CHSB     2.82055585
2021-04-19 00:00:00  Earnings     CHSB     2.82129246
2021-04-20 00:00:00  Earnings     CHSB     2.82202926
2021-04-21 00:00:00  Earnings     CHSB     2.82276626
2021-04-22 00:00:00  Earnings     CHSB     2.82350345
2021-04-23 00:00:00  Earnings     CHSB     2.82424083
2021-04-24 00:00:00  Earnings     CHSB     2.82497840
2021-04-25 00:00:00  Earnings     CHSB     2.82571616
2021-04-26 00:00:00  Earnings     CHSB     2.82645412
2021-04-27 00:00:00  Earnings     CHSB     2.82719227
2021-04-28 00:00:00  Earnings     CHSB     2.82793062
2021-04-29 00:00:00  Earnings     CHSB     2.82866915
2021-04-30 00:00:00  Earnings     CHSB     2.82940788
2021-05-01 00:00:00  Earnings     CHSB     2.83014680
2021-05-02 00:00:00  Earnings     CHSB     2.83088592
2021-05-03 00:00:00  Earnings     CHSB     2.83162523
2021-05-04 00:00:00  Earnings     CHSB     2.83236473
2021-05-05 00:00:00  Earnings     CHSB     2.83310442
2021-05-06 00:00:00  Earnings     CHSB     2.83384431
2021-05-07 00:00:00  Earnings     CHSB     2.83458439
2021-05-08 00:00:00  Earnings     CHSB     2.83532466
2021-05-09 00:00:00  Earnings     CHSB     2.83606513
2021-05-10 00:00:00  Earnings     CHSB     2.83680579
2021-05-11 00:00:00  Earnings     CHSB     2.83754665
2021-05-12 00:00:00  Earnings     CHSB     2.83828769
2021-05-13 00:00:00  Earnings     CHSB     2.83902894
2021-05-14 00:00:00  Earnings     CHSB     2.83977037
2021-05-15 00:00:00  Earnings     CHSB     2.84051200
2021-05-16 00:00:00  Earnings     CHSB     2.84125382
2021-05-17 00:00:00  Earnings     CHSB     2.84199584
2021-05-18 00:00:00  Earnings     CHSB     2.84273805
2021-05-19 00:00:00  Earnings     CHSB     2.84348045
2021-05-20 00:00:00  Earnings     CHSB     2.84422305
2021-05-21 00:00:00  Earnings     CHSB     2.84496584
2021-05-22 00:00:00  Earnings     CHSB     2.84570882
2021-05-23 00:00:00  Earnings     CHSB     2.84645200
2021-05-24 00:00:00  Earnings     CHSB     2.84719538
2021-05-25 00:00:00  Earnings     CHSB     2.84793894
2021-05-26 00:00:00  Earnings     CHSB     2.84868271
2021-05-27 00:00:00  Earnings     CHSB     2.84942666
2021-05-28 00:00:00  Earnings     CHSB     2.85017081
2021-05-29 00:00:00  Earnings     CHSB     2.85091516
2021-05-30 00:00:00  Earnings     CHSB     2.85165970
2021-05-31 00:00:00  Earnings     CHSB     2.85240443
2021-06-01 00:00:00  Earnings     CHSB     2.85314936
2021-06-02 00:00:00  Earnings     CHSB     2.85389448
2021-06-03 00:00:00  Earnings     CHSB     2.85463980
2021-06-04 00:00:00  Earnings     CHSB     2.85538531
2021-06-05 00:00:00  Earnings     CHSB     2.85613101
2021-06-06 00:00:00  Earnings     CHSB     2.85687692
2021-06-07 00:00:00  Earnings     CHSB     2.85762301
2021-06-08 00:00:00  Earnings     CHSB     2.85836930
2021-06-09 00:00:00  Earnings     CHSB     2.85911579
2021-06-10 00:00:00  Earnings     CHSB     2.85986247
2021-06-11 00:00:00  Earnings     CHSB     2.86060934
2021-06-12 00:00:00  Earnings     CHSB     2.86135641
2021-06-13 00:00:00  Earnings     CHSB     2.86210368
2021-06-14 00:00:00  Earnings     CHSB     2.86285114
2021-06-15 00:00:00  Earnings     CHSB     2.86359880
2021-06-16 00:00:00  Earnings     CHSB     2.86434665
2021-06-17 00:00:00  Earnings     CHSB     2.86509470
2021-06-18 00:00:00  Earnings     CHSB     2.86584294
2021-06-19 00:00:00  Earnings     CHSB     2.86659137
2021-06-20 00:00:00  Earnings     CHSB     2.86734001
2021-06-21 00:00:00  Earnings     CHSB     2.86808884
2021-06-22 00:00:00  Earnings     CHSB     2.86883786
2021-06-23 00:00:00  Earnings     CHSB     2.86958708
2021-06-24 00:00:00  Earnings     CHSB     2.87033649
2021-06-25 00:00:00  Earnings     CHSB     2.87108611
2021-06-26 00:00:00  Earnings     CHSB     2.87183591
2021-06-27 00:00:00  Earnings     CHSB     2.87258592
2021-06-28 00:00:00  Earnings     CHSB     2.87333611
2021-06-29 00:00:00  Earnings     CHSB     2.87408651
2021-06-30 00:00:00  Earnings     CHSB     2.87483710
2021-07-01 00:00:00  Earnings     CHSB     2.87558788
2021-07-02 00:00:00  Earnings     CHSB     2.87633887
2021-07-03 00:00:00  Earnings     CHSB     2.87709005
2021-07-04 00:00:00  Earnings     CHSB     2.87784142
2021-07-05 00:00:00  Earnings     CHSB     2.87859299
2021-07-06 00:00:00  Earnings     CHSB     2.87934476
2021-07-07 00:00:00  Earnings     CHSB     2.88009672
2021-07-08 00:00:00  Earnings     CHSB     2.88084888
2021-07-09 00:00:00  Earnings     CHSB     2.88160124
2021-07-10 00:00:00  Earnings     CHSB     2.88235379
2021-07-11 00:00:00  Earnings     CHSB     2.88310654
2021-07-12 00:00:00  Earnings     CHSB     2.88385949
2021-07-13 00:00:00  Earnings     CHSB     2.88461263
2021-07-14 00:00:00  Earnings     CHSB     2.88536597
2021-07-15 00:00:00  Earnings     CHSB     2.88611950
2021-07-16 00:00:00  Earnings     CHSB     2.88687324
2021-07-17 00:00:00  Earnings     CHSB     2.88762717
2021-07-18 00:00:00  Earnings     CHSB     2.88838129
2021-07-19 00:00:00  Earnings     CHSB     2.88913562
2021-07-20 00:00:00  Earnings     CHSB     2.88989014
2021-07-21 00:00:00  Earnings     CHSB     2.89064486
2021-07-22 00:00:00  Earnings     CHSB     2.89139977
2021-07-23 00:00:00  Earnings     CHSB     2.89215488
2021-07-24 00:00:00  Earnings     CHSB     2.89291019
2021-07-25 00:00:00  Earnings     CHSB     2.89366570
2021-07-26 00:00:00  Earnings     CHSB     2.89442140
2021-07-27 00:00:00  Earnings     CHSB     2.89517730
2021-07-28 00:00:00  Earnings     CHSB     2.89593340
2021-07-29 00:00:00  Earnings     CHSB     2.89668970
2021-07-30 00:00:00  Earnings     CHSB     2.89744619
2021-07-31 00:00:00  Earnings     CHSB     2.89820288
2021-08-01 00:00:00  Earnings     CHSB     2.89895977
2021-08-02 00:00:00  Earnings     CHSB     2.89971685
2021-08-03 00:00:00  Earnings     CHSB     2.90047414
2021-08-04 00:00:00  Earnings     CHSB     2.90123162
2021-08-05 00:00:00  Earnings     CHSB     2.90198930
2021-08-06 00:00:00  Earnings     CHSB     2.90274718
2021-08-07 00:00:00  Earnings     CHSB     2.90350525
2021-08-08 00:00:00  Earnings     CHSB     2.90426353
2021-08-09 00:00:00  Earnings     CHSB     2.90502200
2021-08-10 00:00:00  Earnings     CHSB     2.90578067
2021-08-11 00:00:00  Earnings     CHSB     2.90653953
2021-08-12 00:00:00  Earnings     CHSB     2.90729860
2021-08-13 00:00:00  Earnings     CHSB     2.90805786
2021-08-14 00:00:00  Earnings     CHSB     2.90881733
2021-08-15 00:00:00  Earnings     CHSB     2.90957699
2021-08-16 00:00:00  Earnings     CHSB     2.91033685
2021-08-17 00:00:00  Earnings     CHSB     2.91109690
2021-08-18 00:00:00  Earnings     CHSB     2.91185716
2021-08-19 00:00:00  Earnings     CHSB     2.91261761
2021-08-20 00:00:00  Earnings     CHSB     2.91337827
2021-08-21 00:00:00  Earnings     CHSB     2.91413912
2021-08-22 00:00:00  Earnings     CHSB     2.91490017
2021-08-23 00:00:00  Earnings     CHSB     2.91566142
2021-08-24 00:00:00  Earnings     CHSB     2.91642287
2021-08-25 00:00:00  Earnings     CHSB     2.91718451
2021-08-26 00:00:00  Earnings     CHSB     2.91794636
2021-08-27 00:00:00  Earnings     CHSB     2.91870840
2021-08-28 00:00:00  Earnings     CHSB     2.91947065
2021-08-29 00:00:00  Earnings     CHSB     2.92023309
2021-08-30 00:00:00  Earnings     CHSB     2.92099573
2021-08-31 00:00:00  Earnings     CHSB     2.92175857
2021-09-01 00:00:00  Earnings     CHSB     2.92252161
2021-09-02 00:00:00  Earnings     CHSB     2.92328485
2021-09-03 00:00:00  Earnings     CHSB     2.92404829
2021-09-04 00:00:00  Earnings     CHSB     2.92481193
2021-09-05 00:00:00  Earnings     CHSB     2.92557577
2021-09-06 00:00:00  Earnings     CHSB     2.92633980
2021-09-07 00:00:00  Earnings     CHSB     2.92710404
2021-09-08 00:00:00  Earnings     CHSB     2.92786848
2021-09-09 00:00:00  Earnings     CHSB     2.92863311
2021-09-10 00:00:00  Earnings     CHSB     2.92939795
2021-09-11 00:00:00  Earnings     CHSB     2.93016298
2021-09-12 00:00:00  Earnings     CHSB     2.93092822
2021-09-13 00:00:00  Earnings     CHSB     2.93169365
2021-09-14 00:00:00  Earnings     CHSB     2.93245929
2021-09-15 00:00:00  Earnings     CHSB     2.93322512
2021-09-16 00:00:00  Earnings     CHSB     2.93399116
2021-09-17 00:00:00  Earnings     CHSB     2.93475739
2021-09-18 00:00:00  Earnings     CHSB     2.93552383
2021-09-19 00:00:00  Earnings     CHSB     2.93629046
2021-09-20 00:00:00  Earnings     CHSB     2.93705730
2021-09-21 00:00:00  Earnings     CHSB     2.93782433
2021-09-22 00:00:00  Earnings     CHSB     2.93859157
2021-09-23 00:00:00  Earnings     CHSB     2.93935901
2021-09-24 00:00:00  Earnings     CHSB     2.94012664
2021-09-25 00:00:00  Earnings     CHSB     2.94089448
2021-09-26 00:00:00  Earnings     CHSB     2.94166252
2021-09-27 00:00:00  Earnings     CHSB     2.94243076
2021-09-28 00:00:00  Earnings     CHSB     2.94319920
2021-09-29 00:00:00  Earnings     CHSB     2.94396784
2021-09-30 00:00:00  Earnings     CHSB     2.94473668
2021-10-01 00:00:00  Earnings     CHSB     2.94550572
2021-10-02 00:00:00  Earnings     CHSB     2.94627496
2021-10-03 00:00:00  Earnings     CHSB     2.94704440
2021-10-04 00:00:00  Earnings     CHSB     2.94781405
2021-10-05 00:00:00  Earnings     CHSB     2.94858389
2021-10-06 00:00:00  Earnings     CHSB     2.94935394
2021-10-07 00:00:00  Earnings     CHSB     2.95012418
2021-10-08 00:00:00  Earnings     CHSB     2.95089463
2021-10-09 00:00:00  Earnings     CHSB     2.95166528
2021-10-10 00:00:00  Earnings     CHSB     2.95243613
2021-10-11 00:00:00  Earnings     CHSB     2.95320718
2021-10-12 00:00:00  Earnings     CHSB     2.95397844
2021-10-13 00:00:00  Earnings     CHSB     2.95474989
2021-10-14 00:00:00  Earnings     CHSB     2.95552155
2021-10-15 00:00:00  Earnings     CHSB     2.95629341
2021-10-16 00:00:00  Earnings     CHSB     2.95706546
2021-10-17 00:00:00  Earnings     CHSB     2.95783773
2021-10-18 00:00:00  Earnings     CHSB     2.95861019
2021-10-19 00:00:00  Earnings     CHSB     2.95938285
2021-10-20 00:00:00  Earnings     CHSB     2.96015572
2021-10-21 00:00:00  Earnings     CHSB     2.96092879
2021-10-22 00:00:00  Earnings     CHSB     2.96170206
2021-10-23 00:00:00  Earnings     CHSB     2.96247553
2021-10-24 00:00:00  Earnings     CHSB     2.96324920
2021-10-25 00:00:00  Earnings     CHSB     2.96402308
2021-10-26 00:00:00  Earnings     CHSB     2.96479716
2021-10-27 00:00:00  Earnings     CHSB     2.96557144
2021-10-28 00:00:00  Earnings     CHSB     2.96634592
2021-10-29 00:00:00  Earnings     CHSB     2.96712060
2021-10-30 00:00:00  Earnings     CHSB     2.96789549
2021-10-31 00:00:00  Earnings     CHSB     2.96867058
2021-11-01 00:00:00  Earnings     CHSB     2.96944587
2021-11-02 00:00:00  Earnings     CHSB     2.97022137
2021-11-03 00:00:00  Earnings     CHSB     2.97099706
2021-11-04 00:00:00  Earnings     CHSB     2.97177296
2021-11-05 00:00:00  Earnings     CHSB     2.97254906
2021-11-06 00:00:00  Earnings     CHSB     2.97332537
2021-11-07 00:00:00  Earnings     CHSB     2.97410187
2021-11-08 00:00:00  Earnings     CHSB     2.97487859
2021-11-09 00:00:00  Earnings     CHSB     2.97565550
2021-11-10 00:00:00  Earnings     CHSB     2.97643261
2021-11-11 00:00:00  Earnings     CHSB     2.97720993
2021-11-12 00:00:00  Earnings     CHSB     2.97798745
2021-11-13 00:00:00  Earnings     CHSB     2.97876518
2021-11-14 00:00:00  Earnings     CHSB     2.97954311
2021-11-15 00:00:00  Earnings     CHSB     2.98032124
2021-11-16 00:00:00  Earnings     CHSB     2.98109957
2021-11-17 00:00:00  Earnings     CHSB     2.98187811
2021-11-18 00:00:00  Earnings     CHSB     2.98265685
2021-11-19 00:00:00  Earnings     CHSB     2.98343580
2021-11-20 00:00:00  Earnings     CHSB     2.98421494
2021-11-21 00:00:00  Earnings     CHSB     2.98499429
2021-11-22 00:00:00  Earnings     CHSB     2.98577385
2021-11-23 00:00:00  Earnings     CHSB     2.98655361
2021-11-24 00:00:00  Earnings     CHSB     2.98733357
2021-11-25 00:00:00  Earnings     CHSB     2.98811374
2021-11-26 00:00:00  Earnings     CHSB     2.98889411
2021-11-27 00:00:00  Earnings     CHSB     2.98967468
2021-11-28 00:00:00  Earnings     CHSB     2.99045546
2021-11-29 00:00:00  Earnings     CHSB     2.99123644
2021-11-30 00:00:00  Earnings     CHSB     2.99201762
2021-12-01 00:00:00  Earnings     CHSB     2.99279901
2021-12-02 00:00:00  Earnings     CHSB     2.99358060
2021-12-03 00:00:00  Earnings     CHSB     2.99436240
2021-12-04 00:00:00  Earnings     CHSB     2.99514440
2021-12-05 00:00:00  Earnings     CHSB     2.99592661
2021-12-06 00:00:00  Earnings     CHSB     2.99670902
2021-12-07 00:00:00  Earnings     CHSB     2.99749163
2021-12-08 00:00:00  Earnings     CHSB     2.99827445
2021-12-09 00:00:00  Earnings     CHSB     2.99905747
2021-12-10 00:00:00  Earnings     CHSB     2.99984070
2021-12-11 00:00:00  Earnings     CHSB     3.00062413
2021-12-12 00:00:00  Earnings     CHSB     3.00140777
2021-12-13 00:00:00  Earnings     CHSB     3.00219161
2021-12-14 00:00:00  Earnings     CHSB     3.00297566
2021-12-15 00:00:00  Earnings     CHSB     3.00375991
2021-12-16 00:00:00  Earnings     CHSB     3.00454436
2021-12-17 00:00:00  Earnings     CHSB     3.00532902
2021-12-18 00:00:00  Earnings     CHSB     3.00611389
2021-12-19 00:00:00  Earnings     CHSB     3.00689896
2021-12-20 00:00:00  Earnings     CHSB     3.00768423
2021-12-21 00:00:00  Earnings     CHSB     3.00846971
2021-12-22 00:00:00  Earnings     CHSB     3.00925540
2021-12-23 00:00:00  Earnings     CHSB     3.01004129
2021-12-24 00:00:00  Earnings     CHSB     3.01082739
2021-12-25 00:00:00  Earnings     CHSB     3.01161369
2021-12-26 00:00:00  Earnings     CHSB     3.01240019
2021-12-27 00:00:00  Earnings     CHSB     3.01318691
2021-12-28 00:00:00  Earnings     CHSB     3.01397382
2021-12-29 00:00:00  Earnings     CHSB     3.01476095
2021-12-30 00:00:00  Earnings     CHSB     3.01554828
2021-12-31 00:00:00  Earnings     CHSB     3.01633581
TOTAL                                  1,050.12284407'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.maxDiff=None
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                    DEP/WITHDR                                                                               \n' + \
'                  CHSB                                     CHF             CAPITAL                    DATE                  YIELD            \n' + \
'        Tot incl yield  DF RATE  CUR RATE  CAP GAIN CAP GAIN %      CHSB       CHF        FROM          TO DAYS     CHSB      CHF  Y % YR Y %\n' + \
'OWNER                                                                                                                                        ' + \
'''
JPS          10,000.00 5,000.00 15,000.00 10,000.00     200.00 10,000.00 15,000.00  2021-01-01  2021-01-05    5    13.06    19.60 0.13  10.00
JPS           1,000.00 1,000.00  1,500.00    500.00      50.00 11,013.06 16,519.60  2021-01-06  2021-01-09    4    11.51    17.26 0.10  10.00
JPS            -500.00  -600.00   -750.00   -150.00     -25.00 10,524.57 15,786.86  2021-01-10  2021-12-31  356 1,025.55 1,538.32 9.74  10.00
TOTAL        11,550.12 5,400.00 17,325.18 10,350.00     191.67                                                  1,050.12 1,575.18            ''' + \
'''
G TOTAL      11,550.12          17,325.18                                                                       1,050.12 1,575.18            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_1_fiat_simple_values_1_owner_withdrawal_loss_big(self):
		"""
		CHSB crypto, 2 owners, 1 with 1 withdrawal, fixed yield rate,
		CHSB/CHF final rateof 1.5. Withdrawal of 500 CHSB for 600 CHF,
		so a loss of 150 CHF since current withdrawal CHF value is
		750 CHF.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_withdrawal_loss_big.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency     Net amount\n' + \
'Local time                                           ' + \
'''
2021-01-01 00:00:00  Earnings     CHSB     2.61157876
2021-01-02 00:00:00  Earnings     CHSB     2.61226080
2021-01-03 00:00:00  Earnings     CHSB     2.61294301
2021-01-04 00:00:00  Earnings     CHSB     2.61362540
2021-01-05 00:00:00  Earnings     CHSB     2.61430797
2021-01-06 00:00:00  Earnings     CHSB     2.87614859
2021-01-07 00:00:00  Earnings     CHSB     2.87689972
2021-01-08 00:00:00  Earnings     CHSB     2.87765104
2021-01-09 00:00:00  Earnings     CHSB     2.87840257
2021-01-10 00:00:00  Earnings     CHSB     2.74857534
2021-01-11 00:00:00  Earnings     CHSB     2.75001116
2021-01-12 00:00:00  Earnings     CHSB     2.75072934
2021-01-13 00:00:00  Earnings     CHSB     2.75144772
2021-01-14 00:00:00  Earnings     CHSB     2.75216628
2021-01-15 00:00:00  Earnings     CHSB     2.75288503
2021-01-16 00:00:00  Earnings     CHSB     2.75360397
2021-01-17 00:00:00  Earnings     CHSB     2.75432309
2021-01-18 00:00:00  Earnings     CHSB     2.75504241
2021-01-19 00:00:00  Earnings     CHSB     2.75576191
2021-01-20 00:00:00  Earnings     CHSB     2.75648160
2021-01-21 00:00:00  Earnings     CHSB     2.75720147
2021-01-22 00:00:00  Earnings     CHSB     2.75792154
2021-01-23 00:00:00  Earnings     CHSB     2.75864179
2021-01-24 00:00:00  Earnings     CHSB     2.75936223
2021-01-25 00:00:00  Earnings     CHSB     2.76008286
2021-01-26 00:00:00  Earnings     CHSB     2.76080368
2021-01-27 00:00:00  Earnings     CHSB     2.76152468
2021-01-28 00:00:00  Earnings     CHSB     2.76224588
2021-01-29 00:00:00  Earnings     CHSB     2.76296726
2021-01-30 00:00:00  Earnings     CHSB     2.76368883
2021-01-31 00:00:00  Earnings     CHSB     2.76441059
2021-02-01 00:00:00  Earnings     CHSB     2.76513254
2021-02-02 00:00:00  Earnings     CHSB     2.76585467
2021-02-03 00:00:00  Earnings     CHSB     2.76657700
2021-02-04 00:00:00  Earnings     CHSB     2.76729951
2021-02-05 00:00:00  Earnings     CHSB     2.76802221
2021-02-06 00:00:00  Earnings     CHSB     2.76874510
2021-02-07 00:00:00  Earnings     CHSB     2.76946818
2021-02-08 00:00:00  Earnings     CHSB     2.77019145
2021-02-09 00:00:00  Earnings     CHSB     2.77091491
2021-02-10 00:00:00  Earnings     CHSB     2.77163856
2021-02-11 00:00:00  Earnings     CHSB     2.77236239
2021-02-12 00:00:00  Earnings     CHSB     2.77308642
2021-02-13 00:00:00  Earnings     CHSB     2.77381063
2021-02-14 00:00:00  Earnings     CHSB     2.77453503
2021-02-15 00:00:00  Earnings     CHSB     2.77525962
2021-02-16 00:00:00  Earnings     CHSB     2.77598440
2021-02-17 00:00:00  Earnings     CHSB     2.77670937
2021-02-18 00:00:00  Earnings     CHSB     2.77743453
2021-02-19 00:00:00  Earnings     CHSB     2.77815988
2021-02-20 00:00:00  Earnings     CHSB     2.77888542
2021-02-21 00:00:00  Earnings     CHSB     2.77961115
2021-02-22 00:00:00  Earnings     CHSB     2.78033707
2021-02-23 00:00:00  Earnings     CHSB     2.78106317
2021-02-24 00:00:00  Earnings     CHSB     2.78178947
2021-02-25 00:00:00  Earnings     CHSB     2.78251596
2021-02-26 00:00:00  Earnings     CHSB     2.78324263
2021-02-27 00:00:00  Earnings     CHSB     2.78396950
2021-02-28 00:00:00  Earnings     CHSB     2.78469655
2021-03-01 00:00:00  Earnings     CHSB     2.78542380
2021-03-02 00:00:00  Earnings     CHSB     2.78615123
2021-03-03 00:00:00  Earnings     CHSB     2.78687886
2021-03-04 00:00:00  Earnings     CHSB     2.78760668
2021-03-05 00:00:00  Earnings     CHSB     2.78833468
2021-03-06 00:00:00  Earnings     CHSB     2.78906288
2021-03-07 00:00:00  Earnings     CHSB     2.78979126
2021-03-08 00:00:00  Earnings     CHSB     2.79051984
2021-03-09 00:00:00  Earnings     CHSB     2.79124860
2021-03-10 00:00:00  Earnings     CHSB     2.79197756
2021-03-11 00:00:00  Earnings     CHSB     2.79270671
2021-03-12 00:00:00  Earnings     CHSB     2.79343604
2021-03-13 00:00:00  Earnings     CHSB     2.79416557
2021-03-14 00:00:00  Earnings     CHSB     2.79489529
2021-03-15 00:00:00  Earnings     CHSB     2.79562520
2021-03-16 00:00:00  Earnings     CHSB     2.79635530
2021-03-17 00:00:00  Earnings     CHSB     2.79708559
2021-03-18 00:00:00  Earnings     CHSB     2.79781607
2021-03-19 00:00:00  Earnings     CHSB     2.79854674
2021-03-20 00:00:00  Earnings     CHSB     2.79927760
2021-03-21 00:00:00  Earnings     CHSB     2.80000866
2021-03-22 00:00:00  Earnings     CHSB     2.80073990
2021-03-23 00:00:00  Earnings     CHSB     2.80147134
2021-03-24 00:00:00  Earnings     CHSB     2.80220296
2021-03-25 00:00:00  Earnings     CHSB     2.80293478
2021-03-26 00:00:00  Earnings     CHSB     2.80366679
2021-03-27 00:00:00  Earnings     CHSB     2.80439899
2021-03-28 00:00:00  Earnings     CHSB     2.80513138
2021-03-29 00:00:00  Earnings     CHSB     2.80586396
2021-03-30 00:00:00  Earnings     CHSB     2.80659674
2021-03-31 00:00:00  Earnings     CHSB     2.80732970
2021-04-01 00:00:00  Earnings     CHSB     2.80806286
2021-04-02 00:00:00  Earnings     CHSB     2.80879621
2021-04-03 00:00:00  Earnings     CHSB     2.80952974
2021-04-04 00:00:00  Earnings     CHSB     2.81026348
2021-04-05 00:00:00  Earnings     CHSB     2.81099740
2021-04-06 00:00:00  Earnings     CHSB     2.81173151
2021-04-07 00:00:00  Earnings     CHSB     2.81246582
2021-04-08 00:00:00  Earnings     CHSB     2.81320032
2021-04-09 00:00:00  Earnings     CHSB     2.81393500
2021-04-10 00:00:00  Earnings     CHSB     2.81466989
2021-04-11 00:00:00  Earnings     CHSB     2.81540496
2021-04-12 00:00:00  Earnings     CHSB     2.81614022
2021-04-13 00:00:00  Earnings     CHSB     2.81687568
2021-04-14 00:00:00  Earnings     CHSB     2.81761133
2021-04-15 00:00:00  Earnings     CHSB     2.81834717
2021-04-16 00:00:00  Earnings     CHSB     2.81908321
2021-04-17 00:00:00  Earnings     CHSB     2.81981943
2021-04-18 00:00:00  Earnings     CHSB     2.82055585
2021-04-19 00:00:00  Earnings     CHSB     2.82129246
2021-04-20 00:00:00  Earnings     CHSB     2.82202926
2021-04-21 00:00:00  Earnings     CHSB     2.82276626
2021-04-22 00:00:00  Earnings     CHSB     2.82350345
2021-04-23 00:00:00  Earnings     CHSB     2.82424083
2021-04-24 00:00:00  Earnings     CHSB     2.82497840
2021-04-25 00:00:00  Earnings     CHSB     2.82571616
2021-04-26 00:00:00  Earnings     CHSB     2.82645412
2021-04-27 00:00:00  Earnings     CHSB     2.82719227
2021-04-28 00:00:00  Earnings     CHSB     2.82793062
2021-04-29 00:00:00  Earnings     CHSB     2.82866915
2021-04-30 00:00:00  Earnings     CHSB     2.82940788
2021-05-01 00:00:00  Earnings     CHSB     2.83014680
2021-05-02 00:00:00  Earnings     CHSB     2.83088592
2021-05-03 00:00:00  Earnings     CHSB     2.83162523
2021-05-04 00:00:00  Earnings     CHSB     2.83236473
2021-05-05 00:00:00  Earnings     CHSB     2.83310442
2021-05-06 00:00:00  Earnings     CHSB     2.83384431
2021-05-07 00:00:00  Earnings     CHSB     2.83458439
2021-05-08 00:00:00  Earnings     CHSB     2.83532466
2021-05-09 00:00:00  Earnings     CHSB     2.83606513
2021-05-10 00:00:00  Earnings     CHSB     2.83680579
2021-05-11 00:00:00  Earnings     CHSB     2.83754665
2021-05-12 00:00:00  Earnings     CHSB     2.83828769
2021-05-13 00:00:00  Earnings     CHSB     2.83902894
2021-05-14 00:00:00  Earnings     CHSB     2.83977037
2021-05-15 00:00:00  Earnings     CHSB     2.84051200
2021-05-16 00:00:00  Earnings     CHSB     2.84125382
2021-05-17 00:00:00  Earnings     CHSB     2.84199584
2021-05-18 00:00:00  Earnings     CHSB     2.84273805
2021-05-19 00:00:00  Earnings     CHSB     2.84348045
2021-05-20 00:00:00  Earnings     CHSB     2.84422305
2021-05-21 00:00:00  Earnings     CHSB     2.84496584
2021-05-22 00:00:00  Earnings     CHSB     2.84570882
2021-05-23 00:00:00  Earnings     CHSB     2.84645200
2021-05-24 00:00:00  Earnings     CHSB     2.84719538
2021-05-25 00:00:00  Earnings     CHSB     2.84793894
2021-05-26 00:00:00  Earnings     CHSB     2.84868271
2021-05-27 00:00:00  Earnings     CHSB     2.84942666
2021-05-28 00:00:00  Earnings     CHSB     2.85017081
2021-05-29 00:00:00  Earnings     CHSB     2.85091516
2021-05-30 00:00:00  Earnings     CHSB     2.85165970
2021-05-31 00:00:00  Earnings     CHSB     2.85240443
2021-06-01 00:00:00  Earnings     CHSB     2.85314936
2021-06-02 00:00:00  Earnings     CHSB     2.85389448
2021-06-03 00:00:00  Earnings     CHSB     2.85463980
2021-06-04 00:00:00  Earnings     CHSB     2.85538531
2021-06-05 00:00:00  Earnings     CHSB     2.85613101
2021-06-06 00:00:00  Earnings     CHSB     2.85687692
2021-06-07 00:00:00  Earnings     CHSB     2.85762301
2021-06-08 00:00:00  Earnings     CHSB     2.85836930
2021-06-09 00:00:00  Earnings     CHSB     2.85911579
2021-06-10 00:00:00  Earnings     CHSB     2.85986247
2021-06-11 00:00:00  Earnings     CHSB     2.86060934
2021-06-12 00:00:00  Earnings     CHSB     2.86135641
2021-06-13 00:00:00  Earnings     CHSB     2.86210368
2021-06-14 00:00:00  Earnings     CHSB     2.86285114
2021-06-15 00:00:00  Earnings     CHSB     2.86359880
2021-06-16 00:00:00  Earnings     CHSB     2.86434665
2021-06-17 00:00:00  Earnings     CHSB     2.86509470
2021-06-18 00:00:00  Earnings     CHSB     2.86584294
2021-06-19 00:00:00  Earnings     CHSB     2.86659137
2021-06-20 00:00:00  Earnings     CHSB     2.86734001
2021-06-21 00:00:00  Earnings     CHSB     2.86808884
2021-06-22 00:00:00  Earnings     CHSB     2.86883786
2021-06-23 00:00:00  Earnings     CHSB     2.86958708
2021-06-24 00:00:00  Earnings     CHSB     2.87033649
2021-06-25 00:00:00  Earnings     CHSB     2.87108611
2021-06-26 00:00:00  Earnings     CHSB     2.87183591
2021-06-27 00:00:00  Earnings     CHSB     2.87258592
2021-06-28 00:00:00  Earnings     CHSB     2.87333611
2021-06-29 00:00:00  Earnings     CHSB     2.87408651
2021-06-30 00:00:00  Earnings     CHSB     2.87483710
2021-07-01 00:00:00  Earnings     CHSB     2.87558788
2021-07-02 00:00:00  Earnings     CHSB     2.87633887
2021-07-03 00:00:00  Earnings     CHSB     2.87709005
2021-07-04 00:00:00  Earnings     CHSB     2.87784142
2021-07-05 00:00:00  Earnings     CHSB     2.87859299
2021-07-06 00:00:00  Earnings     CHSB     2.87934476
2021-07-07 00:00:00  Earnings     CHSB     2.88009672
2021-07-08 00:00:00  Earnings     CHSB     2.88084888
2021-07-09 00:00:00  Earnings     CHSB     2.88160124
2021-07-10 00:00:00  Earnings     CHSB     2.88235379
2021-07-11 00:00:00  Earnings     CHSB     2.88310654
2021-07-12 00:00:00  Earnings     CHSB     2.88385949
2021-07-13 00:00:00  Earnings     CHSB     2.88461263
2021-07-14 00:00:00  Earnings     CHSB     2.88536597
2021-07-15 00:00:00  Earnings     CHSB     2.88611950
2021-07-16 00:00:00  Earnings     CHSB     2.88687324
2021-07-17 00:00:00  Earnings     CHSB     2.88762717
2021-07-18 00:00:00  Earnings     CHSB     2.88838129
2021-07-19 00:00:00  Earnings     CHSB     2.88913562
2021-07-20 00:00:00  Earnings     CHSB     2.88989014
2021-07-21 00:00:00  Earnings     CHSB     2.89064486
2021-07-22 00:00:00  Earnings     CHSB     2.89139977
2021-07-23 00:00:00  Earnings     CHSB     2.89215488
2021-07-24 00:00:00  Earnings     CHSB     2.89291019
2021-07-25 00:00:00  Earnings     CHSB     2.89366570
2021-07-26 00:00:00  Earnings     CHSB     2.89442140
2021-07-27 00:00:00  Earnings     CHSB     2.89517730
2021-07-28 00:00:00  Earnings     CHSB     2.89593340
2021-07-29 00:00:00  Earnings     CHSB     2.89668970
2021-07-30 00:00:00  Earnings     CHSB     2.89744619
2021-07-31 00:00:00  Earnings     CHSB     2.89820288
2021-08-01 00:00:00  Earnings     CHSB     2.89895977
2021-08-02 00:00:00  Earnings     CHSB     2.89971685
2021-08-03 00:00:00  Earnings     CHSB     2.90047414
2021-08-04 00:00:00  Earnings     CHSB     2.90123162
2021-08-05 00:00:00  Earnings     CHSB     2.90198930
2021-08-06 00:00:00  Earnings     CHSB     2.90274718
2021-08-07 00:00:00  Earnings     CHSB     2.90350525
2021-08-08 00:00:00  Earnings     CHSB     2.90426353
2021-08-09 00:00:00  Earnings     CHSB     2.90502200
2021-08-10 00:00:00  Earnings     CHSB     2.90578067
2021-08-11 00:00:00  Earnings     CHSB     2.90653953
2021-08-12 00:00:00  Earnings     CHSB     2.90729860
2021-08-13 00:00:00  Earnings     CHSB     2.90805786
2021-08-14 00:00:00  Earnings     CHSB     2.90881733
2021-08-15 00:00:00  Earnings     CHSB     2.90957699
2021-08-16 00:00:00  Earnings     CHSB     2.91033685
2021-08-17 00:00:00  Earnings     CHSB     2.91109690
2021-08-18 00:00:00  Earnings     CHSB     2.91185716
2021-08-19 00:00:00  Earnings     CHSB     2.91261761
2021-08-20 00:00:00  Earnings     CHSB     2.91337827
2021-08-21 00:00:00  Earnings     CHSB     2.91413912
2021-08-22 00:00:00  Earnings     CHSB     2.91490017
2021-08-23 00:00:00  Earnings     CHSB     2.91566142
2021-08-24 00:00:00  Earnings     CHSB     2.91642287
2021-08-25 00:00:00  Earnings     CHSB     2.91718451
2021-08-26 00:00:00  Earnings     CHSB     2.91794636
2021-08-27 00:00:00  Earnings     CHSB     2.91870840
2021-08-28 00:00:00  Earnings     CHSB     2.91947065
2021-08-29 00:00:00  Earnings     CHSB     2.92023309
2021-08-30 00:00:00  Earnings     CHSB     2.92099573
2021-08-31 00:00:00  Earnings     CHSB     2.92175857
2021-09-01 00:00:00  Earnings     CHSB     2.92252161
2021-09-02 00:00:00  Earnings     CHSB     2.92328485
2021-09-03 00:00:00  Earnings     CHSB     2.92404829
2021-09-04 00:00:00  Earnings     CHSB     2.92481193
2021-09-05 00:00:00  Earnings     CHSB     2.92557577
2021-09-06 00:00:00  Earnings     CHSB     2.92633980
2021-09-07 00:00:00  Earnings     CHSB     2.92710404
2021-09-08 00:00:00  Earnings     CHSB     2.92786848
2021-09-09 00:00:00  Earnings     CHSB     2.92863311
2021-09-10 00:00:00  Earnings     CHSB     2.92939795
2021-09-11 00:00:00  Earnings     CHSB     2.93016298
2021-09-12 00:00:00  Earnings     CHSB     2.93092822
2021-09-13 00:00:00  Earnings     CHSB     2.93169365
2021-09-14 00:00:00  Earnings     CHSB     2.93245929
2021-09-15 00:00:00  Earnings     CHSB     2.93322512
2021-09-16 00:00:00  Earnings     CHSB     2.93399116
2021-09-17 00:00:00  Earnings     CHSB     2.93475739
2021-09-18 00:00:00  Earnings     CHSB     2.93552383
2021-09-19 00:00:00  Earnings     CHSB     2.93629046
2021-09-20 00:00:00  Earnings     CHSB     2.93705730
2021-09-21 00:00:00  Earnings     CHSB     2.93782433
2021-09-22 00:00:00  Earnings     CHSB     2.93859157
2021-09-23 00:00:00  Earnings     CHSB     2.93935901
2021-09-24 00:00:00  Earnings     CHSB     2.94012664
2021-09-25 00:00:00  Earnings     CHSB     2.94089448
2021-09-26 00:00:00  Earnings     CHSB     2.94166252
2021-09-27 00:00:00  Earnings     CHSB     2.94243076
2021-09-28 00:00:00  Earnings     CHSB     2.94319920
2021-09-29 00:00:00  Earnings     CHSB     2.94396784
2021-09-30 00:00:00  Earnings     CHSB     2.94473668
2021-10-01 00:00:00  Earnings     CHSB     2.94550572
2021-10-02 00:00:00  Earnings     CHSB     2.94627496
2021-10-03 00:00:00  Earnings     CHSB     2.94704440
2021-10-04 00:00:00  Earnings     CHSB     2.94781405
2021-10-05 00:00:00  Earnings     CHSB     2.94858389
2021-10-06 00:00:00  Earnings     CHSB     2.94935394
2021-10-07 00:00:00  Earnings     CHSB     2.95012418
2021-10-08 00:00:00  Earnings     CHSB     2.95089463
2021-10-09 00:00:00  Earnings     CHSB     2.95166528
2021-10-10 00:00:00  Earnings     CHSB     2.95243613
2021-10-11 00:00:00  Earnings     CHSB     2.95320718
2021-10-12 00:00:00  Earnings     CHSB     2.95397844
2021-10-13 00:00:00  Earnings     CHSB     2.95474989
2021-10-14 00:00:00  Earnings     CHSB     2.95552155
2021-10-15 00:00:00  Earnings     CHSB     2.95629341
2021-10-16 00:00:00  Earnings     CHSB     2.95706546
2021-10-17 00:00:00  Earnings     CHSB     2.95783773
2021-10-18 00:00:00  Earnings     CHSB     2.95861019
2021-10-19 00:00:00  Earnings     CHSB     2.95938285
2021-10-20 00:00:00  Earnings     CHSB     2.96015572
2021-10-21 00:00:00  Earnings     CHSB     2.96092879
2021-10-22 00:00:00  Earnings     CHSB     2.96170206
2021-10-23 00:00:00  Earnings     CHSB     2.96247553
2021-10-24 00:00:00  Earnings     CHSB     2.96324920
2021-10-25 00:00:00  Earnings     CHSB     2.96402308
2021-10-26 00:00:00  Earnings     CHSB     2.96479716
2021-10-27 00:00:00  Earnings     CHSB     2.96557144
2021-10-28 00:00:00  Earnings     CHSB     2.96634592
2021-10-29 00:00:00  Earnings     CHSB     2.96712060
2021-10-30 00:00:00  Earnings     CHSB     2.96789549
2021-10-31 00:00:00  Earnings     CHSB     2.96867058
2021-11-01 00:00:00  Earnings     CHSB     2.96944587
2021-11-02 00:00:00  Earnings     CHSB     2.97022137
2021-11-03 00:00:00  Earnings     CHSB     2.97099706
2021-11-04 00:00:00  Earnings     CHSB     2.97177296
2021-11-05 00:00:00  Earnings     CHSB     2.97254906
2021-11-06 00:00:00  Earnings     CHSB     2.97332537
2021-11-07 00:00:00  Earnings     CHSB     2.97410187
2021-11-08 00:00:00  Earnings     CHSB     2.97487859
2021-11-09 00:00:00  Earnings     CHSB     2.97565550
2021-11-10 00:00:00  Earnings     CHSB     2.97643261
2021-11-11 00:00:00  Earnings     CHSB     2.97720993
2021-11-12 00:00:00  Earnings     CHSB     2.97798745
2021-11-13 00:00:00  Earnings     CHSB     2.97876518
2021-11-14 00:00:00  Earnings     CHSB     2.97954311
2021-11-15 00:00:00  Earnings     CHSB     2.98032124
2021-11-16 00:00:00  Earnings     CHSB     2.98109957
2021-11-17 00:00:00  Earnings     CHSB     2.98187811
2021-11-18 00:00:00  Earnings     CHSB     2.98265685
2021-11-19 00:00:00  Earnings     CHSB     2.98343580
2021-11-20 00:00:00  Earnings     CHSB     2.98421494
2021-11-21 00:00:00  Earnings     CHSB     2.98499429
2021-11-22 00:00:00  Earnings     CHSB     2.98577385
2021-11-23 00:00:00  Earnings     CHSB     2.98655361
2021-11-24 00:00:00  Earnings     CHSB     2.98733357
2021-11-25 00:00:00  Earnings     CHSB     2.98811374
2021-11-26 00:00:00  Earnings     CHSB     2.98889411
2021-11-27 00:00:00  Earnings     CHSB     2.98967468
2021-11-28 00:00:00  Earnings     CHSB     2.99045546
2021-11-29 00:00:00  Earnings     CHSB     2.99123644
2021-11-30 00:00:00  Earnings     CHSB     2.99201762
2021-12-01 00:00:00  Earnings     CHSB     2.99279901
2021-12-02 00:00:00  Earnings     CHSB     2.99358060
2021-12-03 00:00:00  Earnings     CHSB     2.99436240
2021-12-04 00:00:00  Earnings     CHSB     2.99514440
2021-12-05 00:00:00  Earnings     CHSB     2.99592661
2021-12-06 00:00:00  Earnings     CHSB     2.99670902
2021-12-07 00:00:00  Earnings     CHSB     2.99749163
2021-12-08 00:00:00  Earnings     CHSB     2.99827445
2021-12-09 00:00:00  Earnings     CHSB     2.99905747
2021-12-10 00:00:00  Earnings     CHSB     2.99984070
2021-12-11 00:00:00  Earnings     CHSB     3.00062413
2021-12-12 00:00:00  Earnings     CHSB     3.00140777
2021-12-13 00:00:00  Earnings     CHSB     3.00219161
2021-12-14 00:00:00  Earnings     CHSB     3.00297566
2021-12-15 00:00:00  Earnings     CHSB     3.00375991
2021-12-16 00:00:00  Earnings     CHSB     3.00454436
2021-12-17 00:00:00  Earnings     CHSB     3.00532902
2021-12-18 00:00:00  Earnings     CHSB     3.00611389
2021-12-19 00:00:00  Earnings     CHSB     3.00689896
2021-12-20 00:00:00  Earnings     CHSB     3.00768423
2021-12-21 00:00:00  Earnings     CHSB     3.00846971
2021-12-22 00:00:00  Earnings     CHSB     3.00925540
2021-12-23 00:00:00  Earnings     CHSB     3.01004129
2021-12-24 00:00:00  Earnings     CHSB     3.01082739
2021-12-25 00:00:00  Earnings     CHSB     3.01161369
2021-12-26 00:00:00  Earnings     CHSB     3.01240019
2021-12-27 00:00:00  Earnings     CHSB     3.01318691
2021-12-28 00:00:00  Earnings     CHSB     3.01397382
2021-12-29 00:00:00  Earnings     CHSB     3.01476095
2021-12-30 00:00:00  Earnings     CHSB     3.01554828
2021-12-31 00:00:00  Earnings     CHSB     3.01633581
TOTAL                                  1,050.12284407'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.maxDiff=None
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                    DEP/WITHDR                                                                               \n' + \
'                  CHSB                                     CHF             CAPITAL                    DATE                  YIELD            \n' + \
'        Tot incl yield  DF RATE  CUR RATE  CAP GAIN CAP GAIN %      CHSB       CHF        FROM          TO DAYS     CHSB      CHF  Y % YR Y %\n' + \
'OWNER                                                                                                                                        ' + \
'''
JPS          10,000.00 5,000.00 15,000.00 10,000.00     200.00 10,000.00 15,000.00  2021-01-01  2021-01-05    5    13.06    19.60 0.13  10.00
JPS           1,000.00 1,000.00  1,500.00    500.00      50.00 11,013.06 16,519.60  2021-01-06  2021-01-09    4    11.51    17.26 0.10  10.00
JPS            -500.00  -250.00   -750.00   -500.00    -200.00 10,524.57 15,786.86  2021-01-10  2021-12-31  356 1,025.55 1,538.32 9.74  10.00
TOTAL        11,550.12 5,750.00 17,325.18 10,000.00     173.91                                                  1,050.12 1,575.18            ''' + \
'''
G TOTAL      11,550.12          17,325.18                                                                       1,050.12 1,575.18            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_1_fiat_simple_values_1_owner_no_withdrawal(self):
		"""
		CHSB crypto, 2 owners, 1 with 1 withdrawal, fixed yield rate,
		CHSB/CHF final rateof 1.5. No wWithdrawal.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner_no_withdrawal.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_no_withdrawal.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency     Net amount\n' + \
'Local time                                           ' + \
'''
2021-01-01 00:00:00  Earnings     CHSB     2.61157876
2021-01-02 00:00:00  Earnings     CHSB     2.61226080
2021-01-03 00:00:00  Earnings     CHSB     2.61294301
2021-01-04 00:00:00  Earnings     CHSB     2.61362540
2021-01-05 00:00:00  Earnings     CHSB     2.61430797
2021-01-06 00:00:00  Earnings     CHSB     2.87614859
2021-01-07 00:00:00  Earnings     CHSB     2.87689972
2021-01-08 00:00:00  Earnings     CHSB     2.87765104
2021-01-09 00:00:00  Earnings     CHSB     2.87840257
2021-01-10 00:00:00  Earnings     CHSB     2.87915428
2021-01-11 00:00:00  Earnings     CHSB     2.87990620
2021-01-12 00:00:00  Earnings     CHSB     2.88065831
2021-01-13 00:00:00  Earnings     CHSB     2.88141061
2021-01-14 00:00:00  Earnings     CHSB     2.88216312
2021-01-15 00:00:00  Earnings     CHSB     2.88291582
2021-01-16 00:00:00  Earnings     CHSB     2.88366871
2021-01-17 00:00:00  Earnings     CHSB     2.88442181
2021-01-18 00:00:00  Earnings     CHSB     2.88517509
2021-01-19 00:00:00  Earnings     CHSB     2.88592858
2021-01-20 00:00:00  Earnings     CHSB     2.88668226
2021-01-21 00:00:00  Earnings     CHSB     2.88743614
2021-01-22 00:00:00  Earnings     CHSB     2.88819022
2021-01-23 00:00:00  Earnings     CHSB     2.88894449
2021-01-24 00:00:00  Earnings     CHSB     2.88969896
2021-01-25 00:00:00  Earnings     CHSB     2.89045363
2021-01-26 00:00:00  Earnings     CHSB     2.89120850
2021-01-27 00:00:00  Earnings     CHSB     2.89196356
2021-01-28 00:00:00  Earnings     CHSB     2.89271882
2021-01-29 00:00:00  Earnings     CHSB     2.89347427
2021-01-30 00:00:00  Earnings     CHSB     2.89422993
2021-01-31 00:00:00  Earnings     CHSB     2.89498578
2021-02-01 00:00:00  Earnings     CHSB     2.89574183
2021-02-02 00:00:00  Earnings     CHSB     2.89649807
2021-02-03 00:00:00  Earnings     CHSB     2.89725452
2021-02-04 00:00:00  Earnings     CHSB     2.89801116
2021-02-05 00:00:00  Earnings     CHSB     2.89876800
2021-02-06 00:00:00  Earnings     CHSB     2.89952503
2021-02-07 00:00:00  Earnings     CHSB     2.90028227
2021-02-08 00:00:00  Earnings     CHSB     2.90103970
2021-02-09 00:00:00  Earnings     CHSB     2.90179733
2021-02-10 00:00:00  Earnings     CHSB     2.90255515
2021-02-11 00:00:00  Earnings     CHSB     2.90331318
2021-02-12 00:00:00  Earnings     CHSB     2.90407140
2021-02-13 00:00:00  Earnings     CHSB     2.90482982
2021-02-14 00:00:00  Earnings     CHSB     2.90558844
2021-02-15 00:00:00  Earnings     CHSB     2.90634726
2021-02-16 00:00:00  Earnings     CHSB     2.90710627
2021-02-17 00:00:00  Earnings     CHSB     2.90786549
2021-02-18 00:00:00  Earnings     CHSB     2.90862490
2021-02-19 00:00:00  Earnings     CHSB     2.90938451
2021-02-20 00:00:00  Earnings     CHSB     2.91014432
2021-02-21 00:00:00  Earnings     CHSB     2.91090433
2021-02-22 00:00:00  Earnings     CHSB     2.91166453
2021-02-23 00:00:00  Earnings     CHSB     2.91242494
2021-02-24 00:00:00  Earnings     CHSB     2.91318554
2021-02-25 00:00:00  Earnings     CHSB     2.91394634
2021-02-26 00:00:00  Earnings     CHSB     2.91470734
2021-02-27 00:00:00  Earnings     CHSB     2.91546854
2021-02-28 00:00:00  Earnings     CHSB     2.91622994
2021-03-01 00:00:00  Earnings     CHSB     2.91699153
2021-03-02 00:00:00  Earnings     CHSB     2.91775333
2021-03-03 00:00:00  Earnings     CHSB     2.91851532
2021-03-04 00:00:00  Earnings     CHSB     2.91927752
2021-03-05 00:00:00  Earnings     CHSB     2.92003991
2021-03-06 00:00:00  Earnings     CHSB     2.92080250
2021-03-07 00:00:00  Earnings     CHSB     2.92156529
2021-03-08 00:00:00  Earnings     CHSB     2.92232828
2021-03-09 00:00:00  Earnings     CHSB     2.92309147
2021-03-10 00:00:00  Earnings     CHSB     2.92385486
2021-03-11 00:00:00  Earnings     CHSB     2.92461845
2021-03-12 00:00:00  Earnings     CHSB     2.92538223
2021-03-13 00:00:00  Earnings     CHSB     2.92614622
2021-03-14 00:00:00  Earnings     CHSB     2.92691040
2021-03-15 00:00:00  Earnings     CHSB     2.92767479
2021-03-16 00:00:00  Earnings     CHSB     2.92843938
2021-03-17 00:00:00  Earnings     CHSB     2.92920416
2021-03-18 00:00:00  Earnings     CHSB     2.92996915
2021-03-19 00:00:00  Earnings     CHSB     2.93073433
2021-03-20 00:00:00  Earnings     CHSB     2.93149971
2021-03-21 00:00:00  Earnings     CHSB     2.93226530
2021-03-22 00:00:00  Earnings     CHSB     2.93303108
2021-03-23 00:00:00  Earnings     CHSB     2.93379707
2021-03-24 00:00:00  Earnings     CHSB     2.93456325
2021-03-25 00:00:00  Earnings     CHSB     2.93532964
2021-03-26 00:00:00  Earnings     CHSB     2.93609622
2021-03-27 00:00:00  Earnings     CHSB     2.93686300
2021-03-28 00:00:00  Earnings     CHSB     2.93762999
2021-03-29 00:00:00  Earnings     CHSB     2.93839717
2021-03-30 00:00:00  Earnings     CHSB     2.93916456
2021-03-31 00:00:00  Earnings     CHSB     2.93993215
2021-04-01 00:00:00  Earnings     CHSB     2.94069993
2021-04-02 00:00:00  Earnings     CHSB     2.94146792
2021-04-03 00:00:00  Earnings     CHSB     2.94223611
2021-04-04 00:00:00  Earnings     CHSB     2.94300450
2021-04-05 00:00:00  Earnings     CHSB     2.94377308
2021-04-06 00:00:00  Earnings     CHSB     2.94454187
2021-04-07 00:00:00  Earnings     CHSB     2.94531086
2021-04-08 00:00:00  Earnings     CHSB     2.94608006
2021-04-09 00:00:00  Earnings     CHSB     2.94684945
2021-04-10 00:00:00  Earnings     CHSB     2.94761904
2021-04-11 00:00:00  Earnings     CHSB     2.94838883
2021-04-12 00:00:00  Earnings     CHSB     2.94915883
2021-04-13 00:00:00  Earnings     CHSB     2.94992903
2021-04-14 00:00:00  Earnings     CHSB     2.95069942
2021-04-15 00:00:00  Earnings     CHSB     2.95147002
2021-04-16 00:00:00  Earnings     CHSB     2.95224082
2021-04-17 00:00:00  Earnings     CHSB     2.95301182
2021-04-18 00:00:00  Earnings     CHSB     2.95378302
2021-04-19 00:00:00  Earnings     CHSB     2.95455443
2021-04-20 00:00:00  Earnings     CHSB     2.95532603
2021-04-21 00:00:00  Earnings     CHSB     2.95609784
2021-04-22 00:00:00  Earnings     CHSB     2.95686985
2021-04-23 00:00:00  Earnings     CHSB     2.95764206
2021-04-24 00:00:00  Earnings     CHSB     2.95841447
2021-04-25 00:00:00  Earnings     CHSB     2.95918708
2021-04-26 00:00:00  Earnings     CHSB     2.95995990
2021-04-27 00:00:00  Earnings     CHSB     2.96073291
2021-04-28 00:00:00  Earnings     CHSB     2.96150613
2021-04-29 00:00:00  Earnings     CHSB     2.96227955
2021-04-30 00:00:00  Earnings     CHSB     2.96305318
2021-05-01 00:00:00  Earnings     CHSB     2.96382700
2021-05-02 00:00:00  Earnings     CHSB     2.96460103
2021-05-03 00:00:00  Earnings     CHSB     2.96537526
2021-05-04 00:00:00  Earnings     CHSB     2.96614969
2021-05-05 00:00:00  Earnings     CHSB     2.96692432
2021-05-06 00:00:00  Earnings     CHSB     2.96769916
2021-05-07 00:00:00  Earnings     CHSB     2.96847419
2021-05-08 00:00:00  Earnings     CHSB     2.96924943
2021-05-09 00:00:00  Earnings     CHSB     2.97002488
2021-05-10 00:00:00  Earnings     CHSB     2.97080052
2021-05-11 00:00:00  Earnings     CHSB     2.97157637
2021-05-12 00:00:00  Earnings     CHSB     2.97235242
2021-05-13 00:00:00  Earnings     CHSB     2.97312867
2021-05-14 00:00:00  Earnings     CHSB     2.97390513
2021-05-15 00:00:00  Earnings     CHSB     2.97468179
2021-05-16 00:00:00  Earnings     CHSB     2.97545865
2021-05-17 00:00:00  Earnings     CHSB     2.97623572
2021-05-18 00:00:00  Earnings     CHSB     2.97701298
2021-05-19 00:00:00  Earnings     CHSB     2.97779045
2021-05-20 00:00:00  Earnings     CHSB     2.97856813
2021-05-21 00:00:00  Earnings     CHSB     2.97934600
2021-05-22 00:00:00  Earnings     CHSB     2.98012408
2021-05-23 00:00:00  Earnings     CHSB     2.98090237
2021-05-24 00:00:00  Earnings     CHSB     2.98168085
2021-05-25 00:00:00  Earnings     CHSB     2.98245954
2021-05-26 00:00:00  Earnings     CHSB     2.98323843
2021-05-27 00:00:00  Earnings     CHSB     2.98401753
2021-05-28 00:00:00  Earnings     CHSB     2.98479683
2021-05-29 00:00:00  Earnings     CHSB     2.98557633
2021-05-30 00:00:00  Earnings     CHSB     2.98635604
2021-05-31 00:00:00  Earnings     CHSB     2.98713595
2021-06-01 00:00:00  Earnings     CHSB     2.98791606
2021-06-02 00:00:00  Earnings     CHSB     2.98869638
2021-06-03 00:00:00  Earnings     CHSB     2.98947690
2021-06-04 00:00:00  Earnings     CHSB     2.99025763
2021-06-05 00:00:00  Earnings     CHSB     2.99103856
2021-06-06 00:00:00  Earnings     CHSB     2.99181969
2021-06-07 00:00:00  Earnings     CHSB     2.99260103
2021-06-08 00:00:00  Earnings     CHSB     2.99338257
2021-06-09 00:00:00  Earnings     CHSB     2.99416432
2021-06-10 00:00:00  Earnings     CHSB     2.99494627
2021-06-11 00:00:00  Earnings     CHSB     2.99572842
2021-06-12 00:00:00  Earnings     CHSB     2.99651078
2021-06-13 00:00:00  Earnings     CHSB     2.99729334
2021-06-14 00:00:00  Earnings     CHSB     2.99807611
2021-06-15 00:00:00  Earnings     CHSB     2.99885908
2021-06-16 00:00:00  Earnings     CHSB     2.99964225
2021-06-17 00:00:00  Earnings     CHSB     3.00042563
2021-06-18 00:00:00  Earnings     CHSB     3.00120922
2021-06-19 00:00:00  Earnings     CHSB     3.00199301
2021-06-20 00:00:00  Earnings     CHSB     3.00277700
2021-06-21 00:00:00  Earnings     CHSB     3.00356120
2021-06-22 00:00:00  Earnings     CHSB     3.00434560
2021-06-23 00:00:00  Earnings     CHSB     3.00513021
2021-06-24 00:00:00  Earnings     CHSB     3.00591503
2021-06-25 00:00:00  Earnings     CHSB     3.00670004
2021-06-26 00:00:00  Earnings     CHSB     3.00748527
2021-06-27 00:00:00  Earnings     CHSB     3.00827070
2021-06-28 00:00:00  Earnings     CHSB     3.00905633
2021-06-29 00:00:00  Earnings     CHSB     3.00984217
2021-06-30 00:00:00  Earnings     CHSB     3.01062821
2021-07-01 00:00:00  Earnings     CHSB     3.01141446
2021-07-02 00:00:00  Earnings     CHSB     3.01220092
2021-07-03 00:00:00  Earnings     CHSB     3.01298758
2021-07-04 00:00:00  Earnings     CHSB     3.01377444
2021-07-05 00:00:00  Earnings     CHSB     3.01456151
2021-07-06 00:00:00  Earnings     CHSB     3.01534879
2021-07-07 00:00:00  Earnings     CHSB     3.01613627
2021-07-08 00:00:00  Earnings     CHSB     3.01692396
2021-07-09 00:00:00  Earnings     CHSB     3.01771185
2021-07-10 00:00:00  Earnings     CHSB     3.01849995
2021-07-11 00:00:00  Earnings     CHSB     3.01928826
2021-07-12 00:00:00  Earnings     CHSB     3.02007677
2021-07-13 00:00:00  Earnings     CHSB     3.02086549
2021-07-14 00:00:00  Earnings     CHSB     3.02165441
2021-07-15 00:00:00  Earnings     CHSB     3.02244354
2021-07-16 00:00:00  Earnings     CHSB     3.02323287
2021-07-17 00:00:00  Earnings     CHSB     3.02402241
2021-07-18 00:00:00  Earnings     CHSB     3.02481216
2021-07-19 00:00:00  Earnings     CHSB     3.02560211
2021-07-20 00:00:00  Earnings     CHSB     3.02639227
2021-07-21 00:00:00  Earnings     CHSB     3.02718264
2021-07-22 00:00:00  Earnings     CHSB     3.02797321
2021-07-23 00:00:00  Earnings     CHSB     3.02876399
2021-07-24 00:00:00  Earnings     CHSB     3.02955498
2021-07-25 00:00:00  Earnings     CHSB     3.03034617
2021-07-26 00:00:00  Earnings     CHSB     3.03113757
2021-07-27 00:00:00  Earnings     CHSB     3.03192917
2021-07-28 00:00:00  Earnings     CHSB     3.03272099
2021-07-29 00:00:00  Earnings     CHSB     3.03351300
2021-07-30 00:00:00  Earnings     CHSB     3.03430523
2021-07-31 00:00:00  Earnings     CHSB     3.03509766
2021-08-01 00:00:00  Earnings     CHSB     3.03589030
2021-08-02 00:00:00  Earnings     CHSB     3.03668315
2021-08-03 00:00:00  Earnings     CHSB     3.03747620
2021-08-04 00:00:00  Earnings     CHSB     3.03826946
2021-08-05 00:00:00  Earnings     CHSB     3.03906293
2021-08-06 00:00:00  Earnings     CHSB     3.03985661
2021-08-07 00:00:00  Earnings     CHSB     3.04065049
2021-08-08 00:00:00  Earnings     CHSB     3.04144458
2021-08-09 00:00:00  Earnings     CHSB     3.04223888
2021-08-10 00:00:00  Earnings     CHSB     3.04303338
2021-08-11 00:00:00  Earnings     CHSB     3.04382809
2021-08-12 00:00:00  Earnings     CHSB     3.04462301
2021-08-13 00:00:00  Earnings     CHSB     3.04541814
2021-08-14 00:00:00  Earnings     CHSB     3.04621348
2021-08-15 00:00:00  Earnings     CHSB     3.04700902
2021-08-16 00:00:00  Earnings     CHSB     3.04780477
2021-08-17 00:00:00  Earnings     CHSB     3.04860073
2021-08-18 00:00:00  Earnings     CHSB     3.04939689
2021-08-19 00:00:00  Earnings     CHSB     3.05019327
2021-08-20 00:00:00  Earnings     CHSB     3.05098985
2021-08-21 00:00:00  Earnings     CHSB     3.05178664
2021-08-22 00:00:00  Earnings     CHSB     3.05258364
2021-08-23 00:00:00  Earnings     CHSB     3.05338084
2021-08-24 00:00:00  Earnings     CHSB     3.05417826
2021-08-25 00:00:00  Earnings     CHSB     3.05497588
2021-08-26 00:00:00  Earnings     CHSB     3.05577371
2021-08-27 00:00:00  Earnings     CHSB     3.05657175
2021-08-28 00:00:00  Earnings     CHSB     3.05737000
2021-08-29 00:00:00  Earnings     CHSB     3.05816845
2021-08-30 00:00:00  Earnings     CHSB     3.05896712
2021-08-31 00:00:00  Earnings     CHSB     3.05976599
2021-09-01 00:00:00  Earnings     CHSB     3.06056507
2021-09-02 00:00:00  Earnings     CHSB     3.06136437
2021-09-03 00:00:00  Earnings     CHSB     3.06216386
2021-09-04 00:00:00  Earnings     CHSB     3.06296357
2021-09-05 00:00:00  Earnings     CHSB     3.06376349
2021-09-06 00:00:00  Earnings     CHSB     3.06456362
2021-09-07 00:00:00  Earnings     CHSB     3.06536395
2021-09-08 00:00:00  Earnings     CHSB     3.06616449
2021-09-09 00:00:00  Earnings     CHSB     3.06696525
2021-09-10 00:00:00  Earnings     CHSB     3.06776621
2021-09-11 00:00:00  Earnings     CHSB     3.06856738
2021-09-12 00:00:00  Earnings     CHSB     3.06936876
2021-09-13 00:00:00  Earnings     CHSB     3.07017035
2021-09-14 00:00:00  Earnings     CHSB     3.07097215
2021-09-15 00:00:00  Earnings     CHSB     3.07177416
2021-09-16 00:00:00  Earnings     CHSB     3.07257638
2021-09-17 00:00:00  Earnings     CHSB     3.07337880
2021-09-18 00:00:00  Earnings     CHSB     3.07418144
2021-09-19 00:00:00  Earnings     CHSB     3.07498429
2021-09-20 00:00:00  Earnings     CHSB     3.07578734
2021-09-21 00:00:00  Earnings     CHSB     3.07659061
2021-09-22 00:00:00  Earnings     CHSB     3.07739409
2021-09-23 00:00:00  Earnings     CHSB     3.07819777
2021-09-24 00:00:00  Earnings     CHSB     3.07900167
2021-09-25 00:00:00  Earnings     CHSB     3.07980577
2021-09-26 00:00:00  Earnings     CHSB     3.08061009
2021-09-27 00:00:00  Earnings     CHSB     3.08141461
2021-09-28 00:00:00  Earnings     CHSB     3.08221935
2021-09-29 00:00:00  Earnings     CHSB     3.08302430
2021-09-30 00:00:00  Earnings     CHSB     3.08382945
2021-10-01 00:00:00  Earnings     CHSB     3.08463482
2021-10-02 00:00:00  Earnings     CHSB     3.08544040
2021-10-03 00:00:00  Earnings     CHSB     3.08624618
2021-10-04 00:00:00  Earnings     CHSB     3.08705218
2021-10-05 00:00:00  Earnings     CHSB     3.08785839
2021-10-06 00:00:00  Earnings     CHSB     3.08866481
2021-10-07 00:00:00  Earnings     CHSB     3.08947144
2021-10-08 00:00:00  Earnings     CHSB     3.09027828
2021-10-09 00:00:00  Earnings     CHSB     3.09108533
2021-10-10 00:00:00  Earnings     CHSB     3.09189259
2021-10-11 00:00:00  Earnings     CHSB     3.09270006
2021-10-12 00:00:00  Earnings     CHSB     3.09350774
2021-10-13 00:00:00  Earnings     CHSB     3.09431564
2021-10-14 00:00:00  Earnings     CHSB     3.09512374
2021-10-15 00:00:00  Earnings     CHSB     3.09593206
2021-10-16 00:00:00  Earnings     CHSB     3.09674058
2021-10-17 00:00:00  Earnings     CHSB     3.09754932
2021-10-18 00:00:00  Earnings     CHSB     3.09835827
2021-10-19 00:00:00  Earnings     CHSB     3.09916743
2021-10-20 00:00:00  Earnings     CHSB     3.09997680
2021-10-21 00:00:00  Earnings     CHSB     3.10078639
2021-10-22 00:00:00  Earnings     CHSB     3.10159618
2021-10-23 00:00:00  Earnings     CHSB     3.10240619
2021-10-24 00:00:00  Earnings     CHSB     3.10321641
2021-10-25 00:00:00  Earnings     CHSB     3.10402684
2021-10-26 00:00:00  Earnings     CHSB     3.10483748
2021-10-27 00:00:00  Earnings     CHSB     3.10564833
2021-10-28 00:00:00  Earnings     CHSB     3.10645939
2021-10-29 00:00:00  Earnings     CHSB     3.10727067
2021-10-30 00:00:00  Earnings     CHSB     3.10808216
2021-10-31 00:00:00  Earnings     CHSB     3.10889386
2021-11-01 00:00:00  Earnings     CHSB     3.10970577
2021-11-02 00:00:00  Earnings     CHSB     3.11051790
2021-11-03 00:00:00  Earnings     CHSB     3.11133023
2021-11-04 00:00:00  Earnings     CHSB     3.11214278
2021-11-05 00:00:00  Earnings     CHSB     3.11295554
2021-11-06 00:00:00  Earnings     CHSB     3.11376851
2021-11-07 00:00:00  Earnings     CHSB     3.11458170
2021-11-08 00:00:00  Earnings     CHSB     3.11539510
2021-11-09 00:00:00  Earnings     CHSB     3.11620871
2021-11-10 00:00:00  Earnings     CHSB     3.11702253
2021-11-11 00:00:00  Earnings     CHSB     3.11783656
2021-11-12 00:00:00  Earnings     CHSB     3.11865081
2021-11-13 00:00:00  Earnings     CHSB     3.11946527
2021-11-14 00:00:00  Earnings     CHSB     3.12027994
2021-11-15 00:00:00  Earnings     CHSB     3.12109483
2021-11-16 00:00:00  Earnings     CHSB     3.12190993
2021-11-17 00:00:00  Earnings     CHSB     3.12272524
2021-11-18 00:00:00  Earnings     CHSB     3.12354076
2021-11-19 00:00:00  Earnings     CHSB     3.12435650
2021-11-20 00:00:00  Earnings     CHSB     3.12517245
2021-11-21 00:00:00  Earnings     CHSB     3.12598862
2021-11-22 00:00:00  Earnings     CHSB     3.12680499
2021-11-23 00:00:00  Earnings     CHSB     3.12762158
2021-11-24 00:00:00  Earnings     CHSB     3.12843838
2021-11-25 00:00:00  Earnings     CHSB     3.12925540
2021-11-26 00:00:00  Earnings     CHSB     3.13007263
2021-11-27 00:00:00  Earnings     CHSB     3.13089007
2021-11-28 00:00:00  Earnings     CHSB     3.13170773
2021-11-29 00:00:00  Earnings     CHSB     3.13252560
2021-11-30 00:00:00  Earnings     CHSB     3.13334368
2021-12-01 00:00:00  Earnings     CHSB     3.13416198
2021-12-02 00:00:00  Earnings     CHSB     3.13498049
2021-12-03 00:00:00  Earnings     CHSB     3.13579922
2021-12-04 00:00:00  Earnings     CHSB     3.13661816
2021-12-05 00:00:00  Earnings     CHSB     3.13743731
2021-12-06 00:00:00  Earnings     CHSB     3.13825668
2021-12-07 00:00:00  Earnings     CHSB     3.13907626
2021-12-08 00:00:00  Earnings     CHSB     3.13989605
2021-12-09 00:00:00  Earnings     CHSB     3.14071606
2021-12-10 00:00:00  Earnings     CHSB     3.14153628
2021-12-11 00:00:00  Earnings     CHSB     3.14235672
2021-12-12 00:00:00  Earnings     CHSB     3.14317737
2021-12-13 00:00:00  Earnings     CHSB     3.14399824
2021-12-14 00:00:00  Earnings     CHSB     3.14481931
2021-12-15 00:00:00  Earnings     CHSB     3.14564061
2021-12-16 00:00:00  Earnings     CHSB     3.14646212
2021-12-17 00:00:00  Earnings     CHSB     3.14728384
2021-12-18 00:00:00  Earnings     CHSB     3.14810578
2021-12-19 00:00:00  Earnings     CHSB     3.14892793
2021-12-20 00:00:00  Earnings     CHSB     3.14975030
2021-12-21 00:00:00  Earnings     CHSB     3.15057288
2021-12-22 00:00:00  Earnings     CHSB     3.15139568
2021-12-23 00:00:00  Earnings     CHSB     3.15221869
2021-12-24 00:00:00  Earnings     CHSB     3.15304192
2021-12-25 00:00:00  Earnings     CHSB     3.15386536
2021-12-26 00:00:00  Earnings     CHSB     3.15468902
2021-12-27 00:00:00  Earnings     CHSB     3.15551289
2021-12-28 00:00:00  Earnings     CHSB     3.15633697
2021-12-29 00:00:00  Earnings     CHSB     3.15716128
2021-12-30 00:00:00  Earnings     CHSB     3.15798579
2021-12-31 00:00:00  Earnings     CHSB     3.15881053
TOTAL                                  1,098.56475635'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.maxDiff=None
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                    DEP/WITHDR                                                                               \n' + \
'                  CHSB                                     CHF             CAPITAL                    DATE                  YIELD            \n' + \
'        Tot incl yield  DF RATE  CUR RATE  CAP GAIN CAP GAIN %      CHSB       CHF        FROM          TO DAYS     CHSB      CHF  Y % YR Y %\n' + \
'OWNER                                                                                                                                        ' + \
'''
JPS          10,000.00 5,000.00 15,000.00 10,000.00     200.00 10,000.00 15,000.00  2021-01-01  2021-01-05    5    13.06    19.60 0.13  10.00
JPS           1,000.00 1,000.00  1,500.00    500.00      50.00 11,013.06 16,519.60  2021-01-06  2021-12-31  360 1,085.50 1,628.25 9.86  10.00
TOTAL        12,098.56 6,000.00 18,147.85 10,500.00     175.00                                                  1,098.56 1,647.85            ''' + \
'''
G TOTAL      12,098.56          18,147.85                                                                       1,098.56 1,647.85            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_1_fiat_simple_values_1_owner_2_fiats_no_withdrawal(self):
		"""
		CHSB crypto, 2 owners, 1 with 1 withdrawal, fixed yield rate,
		CHSB/CHF final rateof 1.5. No wWithdrawal.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner_no_withdrawal.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_2_fiats_no_withdrawal.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency     Net amount\n' + \
'Local time                                           ' + \
'''
2021-01-01 00:00:00  Earnings     CHSB     2.61157876
2021-01-02 00:00:00  Earnings     CHSB     2.61226080
2021-01-03 00:00:00  Earnings     CHSB     2.61294301
2021-01-04 00:00:00  Earnings     CHSB     2.61362540
2021-01-05 00:00:00  Earnings     CHSB     2.61430797
2021-01-06 00:00:00  Earnings     CHSB     2.87614859
2021-01-07 00:00:00  Earnings     CHSB     2.87689972
2021-01-08 00:00:00  Earnings     CHSB     2.87765104
2021-01-09 00:00:00  Earnings     CHSB     2.87840257
2021-01-10 00:00:00  Earnings     CHSB     2.87915428
2021-01-11 00:00:00  Earnings     CHSB     2.87990620
2021-01-12 00:00:00  Earnings     CHSB     2.88065831
2021-01-13 00:00:00  Earnings     CHSB     2.88141061
2021-01-14 00:00:00  Earnings     CHSB     2.88216312
2021-01-15 00:00:00  Earnings     CHSB     2.88291582
2021-01-16 00:00:00  Earnings     CHSB     2.88366871
2021-01-17 00:00:00  Earnings     CHSB     2.88442181
2021-01-18 00:00:00  Earnings     CHSB     2.88517509
2021-01-19 00:00:00  Earnings     CHSB     2.88592858
2021-01-20 00:00:00  Earnings     CHSB     2.88668226
2021-01-21 00:00:00  Earnings     CHSB     2.88743614
2021-01-22 00:00:00  Earnings     CHSB     2.88819022
2021-01-23 00:00:00  Earnings     CHSB     2.88894449
2021-01-24 00:00:00  Earnings     CHSB     2.88969896
2021-01-25 00:00:00  Earnings     CHSB     2.89045363
2021-01-26 00:00:00  Earnings     CHSB     2.89120850
2021-01-27 00:00:00  Earnings     CHSB     2.89196356
2021-01-28 00:00:00  Earnings     CHSB     2.89271882
2021-01-29 00:00:00  Earnings     CHSB     2.89347427
2021-01-30 00:00:00  Earnings     CHSB     2.89422993
2021-01-31 00:00:00  Earnings     CHSB     2.89498578
2021-02-01 00:00:00  Earnings     CHSB     2.89574183
2021-02-02 00:00:00  Earnings     CHSB     2.89649807
2021-02-03 00:00:00  Earnings     CHSB     2.89725452
2021-02-04 00:00:00  Earnings     CHSB     2.89801116
2021-02-05 00:00:00  Earnings     CHSB     2.89876800
2021-02-06 00:00:00  Earnings     CHSB     2.89952503
2021-02-07 00:00:00  Earnings     CHSB     2.90028227
2021-02-08 00:00:00  Earnings     CHSB     2.90103970
2021-02-09 00:00:00  Earnings     CHSB     2.90179733
2021-02-10 00:00:00  Earnings     CHSB     2.90255515
2021-02-11 00:00:00  Earnings     CHSB     2.90331318
2021-02-12 00:00:00  Earnings     CHSB     2.90407140
2021-02-13 00:00:00  Earnings     CHSB     2.90482982
2021-02-14 00:00:00  Earnings     CHSB     2.90558844
2021-02-15 00:00:00  Earnings     CHSB     2.90634726
2021-02-16 00:00:00  Earnings     CHSB     2.90710627
2021-02-17 00:00:00  Earnings     CHSB     2.90786549
2021-02-18 00:00:00  Earnings     CHSB     2.90862490
2021-02-19 00:00:00  Earnings     CHSB     2.90938451
2021-02-20 00:00:00  Earnings     CHSB     2.91014432
2021-02-21 00:00:00  Earnings     CHSB     2.91090433
2021-02-22 00:00:00  Earnings     CHSB     2.91166453
2021-02-23 00:00:00  Earnings     CHSB     2.91242494
2021-02-24 00:00:00  Earnings     CHSB     2.91318554
2021-02-25 00:00:00  Earnings     CHSB     2.91394634
2021-02-26 00:00:00  Earnings     CHSB     2.91470734
2021-02-27 00:00:00  Earnings     CHSB     2.91546854
2021-02-28 00:00:00  Earnings     CHSB     2.91622994
2021-03-01 00:00:00  Earnings     CHSB     2.91699153
2021-03-02 00:00:00  Earnings     CHSB     2.91775333
2021-03-03 00:00:00  Earnings     CHSB     2.91851532
2021-03-04 00:00:00  Earnings     CHSB     2.91927752
2021-03-05 00:00:00  Earnings     CHSB     2.92003991
2021-03-06 00:00:00  Earnings     CHSB     2.92080250
2021-03-07 00:00:00  Earnings     CHSB     2.92156529
2021-03-08 00:00:00  Earnings     CHSB     2.92232828
2021-03-09 00:00:00  Earnings     CHSB     2.92309147
2021-03-10 00:00:00  Earnings     CHSB     2.92385486
2021-03-11 00:00:00  Earnings     CHSB     2.92461845
2021-03-12 00:00:00  Earnings     CHSB     2.92538223
2021-03-13 00:00:00  Earnings     CHSB     2.92614622
2021-03-14 00:00:00  Earnings     CHSB     2.92691040
2021-03-15 00:00:00  Earnings     CHSB     2.92767479
2021-03-16 00:00:00  Earnings     CHSB     2.92843938
2021-03-17 00:00:00  Earnings     CHSB     2.92920416
2021-03-18 00:00:00  Earnings     CHSB     2.92996915
2021-03-19 00:00:00  Earnings     CHSB     2.93073433
2021-03-20 00:00:00  Earnings     CHSB     2.93149971
2021-03-21 00:00:00  Earnings     CHSB     2.93226530
2021-03-22 00:00:00  Earnings     CHSB     2.93303108
2021-03-23 00:00:00  Earnings     CHSB     2.93379707
2021-03-24 00:00:00  Earnings     CHSB     2.93456325
2021-03-25 00:00:00  Earnings     CHSB     2.93532964
2021-03-26 00:00:00  Earnings     CHSB     2.93609622
2021-03-27 00:00:00  Earnings     CHSB     2.93686300
2021-03-28 00:00:00  Earnings     CHSB     2.93762999
2021-03-29 00:00:00  Earnings     CHSB     2.93839717
2021-03-30 00:00:00  Earnings     CHSB     2.93916456
2021-03-31 00:00:00  Earnings     CHSB     2.93993215
2021-04-01 00:00:00  Earnings     CHSB     2.94069993
2021-04-02 00:00:00  Earnings     CHSB     2.94146792
2021-04-03 00:00:00  Earnings     CHSB     2.94223611
2021-04-04 00:00:00  Earnings     CHSB     2.94300450
2021-04-05 00:00:00  Earnings     CHSB     2.94377308
2021-04-06 00:00:00  Earnings     CHSB     2.94454187
2021-04-07 00:00:00  Earnings     CHSB     2.94531086
2021-04-08 00:00:00  Earnings     CHSB     2.94608006
2021-04-09 00:00:00  Earnings     CHSB     2.94684945
2021-04-10 00:00:00  Earnings     CHSB     2.94761904
2021-04-11 00:00:00  Earnings     CHSB     2.94838883
2021-04-12 00:00:00  Earnings     CHSB     2.94915883
2021-04-13 00:00:00  Earnings     CHSB     2.94992903
2021-04-14 00:00:00  Earnings     CHSB     2.95069942
2021-04-15 00:00:00  Earnings     CHSB     2.95147002
2021-04-16 00:00:00  Earnings     CHSB     2.95224082
2021-04-17 00:00:00  Earnings     CHSB     2.95301182
2021-04-18 00:00:00  Earnings     CHSB     2.95378302
2021-04-19 00:00:00  Earnings     CHSB     2.95455443
2021-04-20 00:00:00  Earnings     CHSB     2.95532603
2021-04-21 00:00:00  Earnings     CHSB     2.95609784
2021-04-22 00:00:00  Earnings     CHSB     2.95686985
2021-04-23 00:00:00  Earnings     CHSB     2.95764206
2021-04-24 00:00:00  Earnings     CHSB     2.95841447
2021-04-25 00:00:00  Earnings     CHSB     2.95918708
2021-04-26 00:00:00  Earnings     CHSB     2.95995990
2021-04-27 00:00:00  Earnings     CHSB     2.96073291
2021-04-28 00:00:00  Earnings     CHSB     2.96150613
2021-04-29 00:00:00  Earnings     CHSB     2.96227955
2021-04-30 00:00:00  Earnings     CHSB     2.96305318
2021-05-01 00:00:00  Earnings     CHSB     2.96382700
2021-05-02 00:00:00  Earnings     CHSB     2.96460103
2021-05-03 00:00:00  Earnings     CHSB     2.96537526
2021-05-04 00:00:00  Earnings     CHSB     2.96614969
2021-05-05 00:00:00  Earnings     CHSB     2.96692432
2021-05-06 00:00:00  Earnings     CHSB     2.96769916
2021-05-07 00:00:00  Earnings     CHSB     2.96847419
2021-05-08 00:00:00  Earnings     CHSB     2.96924943
2021-05-09 00:00:00  Earnings     CHSB     2.97002488
2021-05-10 00:00:00  Earnings     CHSB     2.97080052
2021-05-11 00:00:00  Earnings     CHSB     2.97157637
2021-05-12 00:00:00  Earnings     CHSB     2.97235242
2021-05-13 00:00:00  Earnings     CHSB     2.97312867
2021-05-14 00:00:00  Earnings     CHSB     2.97390513
2021-05-15 00:00:00  Earnings     CHSB     2.97468179
2021-05-16 00:00:00  Earnings     CHSB     2.97545865
2021-05-17 00:00:00  Earnings     CHSB     2.97623572
2021-05-18 00:00:00  Earnings     CHSB     2.97701298
2021-05-19 00:00:00  Earnings     CHSB     2.97779045
2021-05-20 00:00:00  Earnings     CHSB     2.97856813
2021-05-21 00:00:00  Earnings     CHSB     2.97934600
2021-05-22 00:00:00  Earnings     CHSB     2.98012408
2021-05-23 00:00:00  Earnings     CHSB     2.98090237
2021-05-24 00:00:00  Earnings     CHSB     2.98168085
2021-05-25 00:00:00  Earnings     CHSB     2.98245954
2021-05-26 00:00:00  Earnings     CHSB     2.98323843
2021-05-27 00:00:00  Earnings     CHSB     2.98401753
2021-05-28 00:00:00  Earnings     CHSB     2.98479683
2021-05-29 00:00:00  Earnings     CHSB     2.98557633
2021-05-30 00:00:00  Earnings     CHSB     2.98635604
2021-05-31 00:00:00  Earnings     CHSB     2.98713595
2021-06-01 00:00:00  Earnings     CHSB     2.98791606
2021-06-02 00:00:00  Earnings     CHSB     2.98869638
2021-06-03 00:00:00  Earnings     CHSB     2.98947690
2021-06-04 00:00:00  Earnings     CHSB     2.99025763
2021-06-05 00:00:00  Earnings     CHSB     2.99103856
2021-06-06 00:00:00  Earnings     CHSB     2.99181969
2021-06-07 00:00:00  Earnings     CHSB     2.99260103
2021-06-08 00:00:00  Earnings     CHSB     2.99338257
2021-06-09 00:00:00  Earnings     CHSB     2.99416432
2021-06-10 00:00:00  Earnings     CHSB     2.99494627
2021-06-11 00:00:00  Earnings     CHSB     2.99572842
2021-06-12 00:00:00  Earnings     CHSB     2.99651078
2021-06-13 00:00:00  Earnings     CHSB     2.99729334
2021-06-14 00:00:00  Earnings     CHSB     2.99807611
2021-06-15 00:00:00  Earnings     CHSB     2.99885908
2021-06-16 00:00:00  Earnings     CHSB     2.99964225
2021-06-17 00:00:00  Earnings     CHSB     3.00042563
2021-06-18 00:00:00  Earnings     CHSB     3.00120922
2021-06-19 00:00:00  Earnings     CHSB     3.00199301
2021-06-20 00:00:00  Earnings     CHSB     3.00277700
2021-06-21 00:00:00  Earnings     CHSB     3.00356120
2021-06-22 00:00:00  Earnings     CHSB     3.00434560
2021-06-23 00:00:00  Earnings     CHSB     3.00513021
2021-06-24 00:00:00  Earnings     CHSB     3.00591503
2021-06-25 00:00:00  Earnings     CHSB     3.00670004
2021-06-26 00:00:00  Earnings     CHSB     3.00748527
2021-06-27 00:00:00  Earnings     CHSB     3.00827070
2021-06-28 00:00:00  Earnings     CHSB     3.00905633
2021-06-29 00:00:00  Earnings     CHSB     3.00984217
2021-06-30 00:00:00  Earnings     CHSB     3.01062821
2021-07-01 00:00:00  Earnings     CHSB     3.01141446
2021-07-02 00:00:00  Earnings     CHSB     3.01220092
2021-07-03 00:00:00  Earnings     CHSB     3.01298758
2021-07-04 00:00:00  Earnings     CHSB     3.01377444
2021-07-05 00:00:00  Earnings     CHSB     3.01456151
2021-07-06 00:00:00  Earnings     CHSB     3.01534879
2021-07-07 00:00:00  Earnings     CHSB     3.01613627
2021-07-08 00:00:00  Earnings     CHSB     3.01692396
2021-07-09 00:00:00  Earnings     CHSB     3.01771185
2021-07-10 00:00:00  Earnings     CHSB     3.01849995
2021-07-11 00:00:00  Earnings     CHSB     3.01928826
2021-07-12 00:00:00  Earnings     CHSB     3.02007677
2021-07-13 00:00:00  Earnings     CHSB     3.02086549
2021-07-14 00:00:00  Earnings     CHSB     3.02165441
2021-07-15 00:00:00  Earnings     CHSB     3.02244354
2021-07-16 00:00:00  Earnings     CHSB     3.02323287
2021-07-17 00:00:00  Earnings     CHSB     3.02402241
2021-07-18 00:00:00  Earnings     CHSB     3.02481216
2021-07-19 00:00:00  Earnings     CHSB     3.02560211
2021-07-20 00:00:00  Earnings     CHSB     3.02639227
2021-07-21 00:00:00  Earnings     CHSB     3.02718264
2021-07-22 00:00:00  Earnings     CHSB     3.02797321
2021-07-23 00:00:00  Earnings     CHSB     3.02876399
2021-07-24 00:00:00  Earnings     CHSB     3.02955498
2021-07-25 00:00:00  Earnings     CHSB     3.03034617
2021-07-26 00:00:00  Earnings     CHSB     3.03113757
2021-07-27 00:00:00  Earnings     CHSB     3.03192917
2021-07-28 00:00:00  Earnings     CHSB     3.03272099
2021-07-29 00:00:00  Earnings     CHSB     3.03351300
2021-07-30 00:00:00  Earnings     CHSB     3.03430523
2021-07-31 00:00:00  Earnings     CHSB     3.03509766
2021-08-01 00:00:00  Earnings     CHSB     3.03589030
2021-08-02 00:00:00  Earnings     CHSB     3.03668315
2021-08-03 00:00:00  Earnings     CHSB     3.03747620
2021-08-04 00:00:00  Earnings     CHSB     3.03826946
2021-08-05 00:00:00  Earnings     CHSB     3.03906293
2021-08-06 00:00:00  Earnings     CHSB     3.03985661
2021-08-07 00:00:00  Earnings     CHSB     3.04065049
2021-08-08 00:00:00  Earnings     CHSB     3.04144458
2021-08-09 00:00:00  Earnings     CHSB     3.04223888
2021-08-10 00:00:00  Earnings     CHSB     3.04303338
2021-08-11 00:00:00  Earnings     CHSB     3.04382809
2021-08-12 00:00:00  Earnings     CHSB     3.04462301
2021-08-13 00:00:00  Earnings     CHSB     3.04541814
2021-08-14 00:00:00  Earnings     CHSB     3.04621348
2021-08-15 00:00:00  Earnings     CHSB     3.04700902
2021-08-16 00:00:00  Earnings     CHSB     3.04780477
2021-08-17 00:00:00  Earnings     CHSB     3.04860073
2021-08-18 00:00:00  Earnings     CHSB     3.04939689
2021-08-19 00:00:00  Earnings     CHSB     3.05019327
2021-08-20 00:00:00  Earnings     CHSB     3.05098985
2021-08-21 00:00:00  Earnings     CHSB     3.05178664
2021-08-22 00:00:00  Earnings     CHSB     3.05258364
2021-08-23 00:00:00  Earnings     CHSB     3.05338084
2021-08-24 00:00:00  Earnings     CHSB     3.05417826
2021-08-25 00:00:00  Earnings     CHSB     3.05497588
2021-08-26 00:00:00  Earnings     CHSB     3.05577371
2021-08-27 00:00:00  Earnings     CHSB     3.05657175
2021-08-28 00:00:00  Earnings     CHSB     3.05737000
2021-08-29 00:00:00  Earnings     CHSB     3.05816845
2021-08-30 00:00:00  Earnings     CHSB     3.05896712
2021-08-31 00:00:00  Earnings     CHSB     3.05976599
2021-09-01 00:00:00  Earnings     CHSB     3.06056507
2021-09-02 00:00:00  Earnings     CHSB     3.06136437
2021-09-03 00:00:00  Earnings     CHSB     3.06216386
2021-09-04 00:00:00  Earnings     CHSB     3.06296357
2021-09-05 00:00:00  Earnings     CHSB     3.06376349
2021-09-06 00:00:00  Earnings     CHSB     3.06456362
2021-09-07 00:00:00  Earnings     CHSB     3.06536395
2021-09-08 00:00:00  Earnings     CHSB     3.06616449
2021-09-09 00:00:00  Earnings     CHSB     3.06696525
2021-09-10 00:00:00  Earnings     CHSB     3.06776621
2021-09-11 00:00:00  Earnings     CHSB     3.06856738
2021-09-12 00:00:00  Earnings     CHSB     3.06936876
2021-09-13 00:00:00  Earnings     CHSB     3.07017035
2021-09-14 00:00:00  Earnings     CHSB     3.07097215
2021-09-15 00:00:00  Earnings     CHSB     3.07177416
2021-09-16 00:00:00  Earnings     CHSB     3.07257638
2021-09-17 00:00:00  Earnings     CHSB     3.07337880
2021-09-18 00:00:00  Earnings     CHSB     3.07418144
2021-09-19 00:00:00  Earnings     CHSB     3.07498429
2021-09-20 00:00:00  Earnings     CHSB     3.07578734
2021-09-21 00:00:00  Earnings     CHSB     3.07659061
2021-09-22 00:00:00  Earnings     CHSB     3.07739409
2021-09-23 00:00:00  Earnings     CHSB     3.07819777
2021-09-24 00:00:00  Earnings     CHSB     3.07900167
2021-09-25 00:00:00  Earnings     CHSB     3.07980577
2021-09-26 00:00:00  Earnings     CHSB     3.08061009
2021-09-27 00:00:00  Earnings     CHSB     3.08141461
2021-09-28 00:00:00  Earnings     CHSB     3.08221935
2021-09-29 00:00:00  Earnings     CHSB     3.08302430
2021-09-30 00:00:00  Earnings     CHSB     3.08382945
2021-10-01 00:00:00  Earnings     CHSB     3.08463482
2021-10-02 00:00:00  Earnings     CHSB     3.08544040
2021-10-03 00:00:00  Earnings     CHSB     3.08624618
2021-10-04 00:00:00  Earnings     CHSB     3.08705218
2021-10-05 00:00:00  Earnings     CHSB     3.08785839
2021-10-06 00:00:00  Earnings     CHSB     3.08866481
2021-10-07 00:00:00  Earnings     CHSB     3.08947144
2021-10-08 00:00:00  Earnings     CHSB     3.09027828
2021-10-09 00:00:00  Earnings     CHSB     3.09108533
2021-10-10 00:00:00  Earnings     CHSB     3.09189259
2021-10-11 00:00:00  Earnings     CHSB     3.09270006
2021-10-12 00:00:00  Earnings     CHSB     3.09350774
2021-10-13 00:00:00  Earnings     CHSB     3.09431564
2021-10-14 00:00:00  Earnings     CHSB     3.09512374
2021-10-15 00:00:00  Earnings     CHSB     3.09593206
2021-10-16 00:00:00  Earnings     CHSB     3.09674058
2021-10-17 00:00:00  Earnings     CHSB     3.09754932
2021-10-18 00:00:00  Earnings     CHSB     3.09835827
2021-10-19 00:00:00  Earnings     CHSB     3.09916743
2021-10-20 00:00:00  Earnings     CHSB     3.09997680
2021-10-21 00:00:00  Earnings     CHSB     3.10078639
2021-10-22 00:00:00  Earnings     CHSB     3.10159618
2021-10-23 00:00:00  Earnings     CHSB     3.10240619
2021-10-24 00:00:00  Earnings     CHSB     3.10321641
2021-10-25 00:00:00  Earnings     CHSB     3.10402684
2021-10-26 00:00:00  Earnings     CHSB     3.10483748
2021-10-27 00:00:00  Earnings     CHSB     3.10564833
2021-10-28 00:00:00  Earnings     CHSB     3.10645939
2021-10-29 00:00:00  Earnings     CHSB     3.10727067
2021-10-30 00:00:00  Earnings     CHSB     3.10808216
2021-10-31 00:00:00  Earnings     CHSB     3.10889386
2021-11-01 00:00:00  Earnings     CHSB     3.10970577
2021-11-02 00:00:00  Earnings     CHSB     3.11051790
2021-11-03 00:00:00  Earnings     CHSB     3.11133023
2021-11-04 00:00:00  Earnings     CHSB     3.11214278
2021-11-05 00:00:00  Earnings     CHSB     3.11295554
2021-11-06 00:00:00  Earnings     CHSB     3.11376851
2021-11-07 00:00:00  Earnings     CHSB     3.11458170
2021-11-08 00:00:00  Earnings     CHSB     3.11539510
2021-11-09 00:00:00  Earnings     CHSB     3.11620871
2021-11-10 00:00:00  Earnings     CHSB     3.11702253
2021-11-11 00:00:00  Earnings     CHSB     3.11783656
2021-11-12 00:00:00  Earnings     CHSB     3.11865081
2021-11-13 00:00:00  Earnings     CHSB     3.11946527
2021-11-14 00:00:00  Earnings     CHSB     3.12027994
2021-11-15 00:00:00  Earnings     CHSB     3.12109483
2021-11-16 00:00:00  Earnings     CHSB     3.12190993
2021-11-17 00:00:00  Earnings     CHSB     3.12272524
2021-11-18 00:00:00  Earnings     CHSB     3.12354076
2021-11-19 00:00:00  Earnings     CHSB     3.12435650
2021-11-20 00:00:00  Earnings     CHSB     3.12517245
2021-11-21 00:00:00  Earnings     CHSB     3.12598862
2021-11-22 00:00:00  Earnings     CHSB     3.12680499
2021-11-23 00:00:00  Earnings     CHSB     3.12762158
2021-11-24 00:00:00  Earnings     CHSB     3.12843838
2021-11-25 00:00:00  Earnings     CHSB     3.12925540
2021-11-26 00:00:00  Earnings     CHSB     3.13007263
2021-11-27 00:00:00  Earnings     CHSB     3.13089007
2021-11-28 00:00:00  Earnings     CHSB     3.13170773
2021-11-29 00:00:00  Earnings     CHSB     3.13252560
2021-11-30 00:00:00  Earnings     CHSB     3.13334368
2021-12-01 00:00:00  Earnings     CHSB     3.13416198
2021-12-02 00:00:00  Earnings     CHSB     3.13498049
2021-12-03 00:00:00  Earnings     CHSB     3.13579922
2021-12-04 00:00:00  Earnings     CHSB     3.13661816
2021-12-05 00:00:00  Earnings     CHSB     3.13743731
2021-12-06 00:00:00  Earnings     CHSB     3.13825668
2021-12-07 00:00:00  Earnings     CHSB     3.13907626
2021-12-08 00:00:00  Earnings     CHSB     3.13989605
2021-12-09 00:00:00  Earnings     CHSB     3.14071606
2021-12-10 00:00:00  Earnings     CHSB     3.14153628
2021-12-11 00:00:00  Earnings     CHSB     3.14235672
2021-12-12 00:00:00  Earnings     CHSB     3.14317737
2021-12-13 00:00:00  Earnings     CHSB     3.14399824
2021-12-14 00:00:00  Earnings     CHSB     3.14481931
2021-12-15 00:00:00  Earnings     CHSB     3.14564061
2021-12-16 00:00:00  Earnings     CHSB     3.14646212
2021-12-17 00:00:00  Earnings     CHSB     3.14728384
2021-12-18 00:00:00  Earnings     CHSB     3.14810578
2021-12-19 00:00:00  Earnings     CHSB     3.14892793
2021-12-20 00:00:00  Earnings     CHSB     3.14975030
2021-12-21 00:00:00  Earnings     CHSB     3.15057288
2021-12-22 00:00:00  Earnings     CHSB     3.15139568
2021-12-23 00:00:00  Earnings     CHSB     3.15221869
2021-12-24 00:00:00  Earnings     CHSB     3.15304192
2021-12-25 00:00:00  Earnings     CHSB     3.15386536
2021-12-26 00:00:00  Earnings     CHSB     3.15468902
2021-12-27 00:00:00  Earnings     CHSB     3.15551289
2021-12-28 00:00:00  Earnings     CHSB     3.15633697
2021-12-29 00:00:00  Earnings     CHSB     3.15716128
2021-12-30 00:00:00  Earnings     CHSB     3.15798579
2021-12-31 00:00:00  Earnings     CHSB     3.15881053
TOTAL                                  1,098.56475635'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.maxDiff=None
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                                                             DEP/WITHDR                                                                                                  \n' + \
'                  CHSB                                     CHF                                      USD                       CAPITAL                    DATE                           YIELD            \n' + \
'        Tot incl yield  DF RATE  CUR RATE  CAP GAIN CAP GAIN %  DF RATE  CUR RATE  CAP GAIN  CAP GAIN %      CHSB       CHF       USD        FROM          TO DAYS     CHSB      CHF      USD  Y % YR Y %\n' + \
'OWNER                                                                                                                                                                                                    ' + \
'''
JPS          10,000.00 5,000.00 15,000.00 10,000.00     200.00 4,800.00 17,000.00 12,200.00      254.17 10,000.00 15,000.00 17,000.00  2021-01-01  2021-01-05    5    13.06    19.60    22.21 0.13  10.00
JPS           1,000.00 1,000.00  1,500.00    500.00      50.00   980.00  1,700.00    720.00       73.47 11,013.06 16,519.60 18,722.21  2021-01-06  2021-12-31  360 1,085.50 1,628.25 1,845.35 9.86  10.00
TOTAL        12,098.56 6,000.00 18,147.85 10,500.00     175.00 5,780.00 20,567.56 12,920.00      223.53                                                            1,098.56 1,647.85 1,867.56            ''' + \
'''
G TOTAL      12,098.56          18,147.85                               20,567.56                                                                                  1,098.56 1,647.85 1,867.56            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_USDC_1_fiat_simple_values_2_owners_bug(self):
		"""
		USDC crypto, 2 owners with 1 deposit, fixed yield rate,
		USDC/CHF final rate of 1.5.

		Corresponding OwnerDepositYieldComputer tesz:
		TestOwnerDepositYieldComputer.testComputeDepositsYields_2_owners_bug
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSBEarningUsdc_simple_values_bug.xlsx'
		depositSheetFileName = 'depositUsdc_fiat_chf_simple_values_bug.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(),
								   self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2021-02-20 00:00:00  Earnings     USDC   1.04463150
2021-02-21 00:00:00  Earnings     USDC   1.04490432
2021-02-22 00:00:00  Earnings     USDC   1.04517720
2021-02-23 00:00:00  Earnings     USDC   1.04545016
2021-02-24 00:00:00  Earnings     USDC   1.04572319
2021-02-25 00:00:00  Earnings     USDC   1.04599629
2021-02-26 00:00:00  Earnings     USDC   1.04626946
2021-02-27 00:00:00  Earnings     USDC   1.04654270
2021-02-28 00:00:00  Earnings     USDC   1.04681601
2021-03-01 00:00:00  Earnings     USDC   1.04708939
2021-03-02 00:00:00  Earnings     USDC   1.04736285
2021-03-03 00:00:00  Earnings     USDC   1.04763638
2021-03-04 00:00:00  Earnings     USDC   1.04790998
2021-03-05 00:00:00  Earnings     USDC   1.04818365
2021-03-06 00:00:00  Earnings     USDC   1.04845739
2021-03-07 00:00:00  Earnings     USDC   1.04873120
2021-03-08 00:00:00  Earnings     USDC   1.04900508
2021-03-09 00:00:00  Earnings     USDC   1.04927904
2021-03-10 00:00:00  Earnings     USDC   1.04955307
2021-03-11 00:00:00  Earnings     USDC   1.04982717
2021-03-12 00:00:00  Earnings     USDC   1.05010134
2021-03-13 00:00:00  Earnings     USDC   1.05037558
2021-03-14 00:00:00  Earnings     USDC   1.05064989
2021-03-15 00:00:00  Earnings     USDC   1.05092428
2021-03-16 00:00:00  Earnings     USDC   1.05119874
2021-03-17 00:00:00  Earnings     USDC   1.05147326
2021-03-18 00:00:00  Earnings     USDC   1.05174787
2021-03-19 00:00:00  Earnings     USDC   1.05202254
2021-03-20 00:00:00  Earnings     USDC   1.05229728
2021-03-21 00:00:00  Earnings     USDC   1.05257210
2021-03-22 00:00:00  Earnings     USDC   2.35863637
2021-03-23 00:00:00  Earnings     USDC   2.35925234
2021-03-24 00:00:00  Earnings     USDC   2.35986848
2021-03-25 00:00:00  Earnings     USDC   2.36048478
2021-03-26 00:00:00  Earnings     USDC   2.36110124
2021-03-27 00:00:00  Earnings     USDC   2.36171786
2021-03-28 00:00:00  Earnings     USDC   2.36233464
2021-03-29 00:00:00  Earnings     USDC   2.36295158
2021-03-30 00:00:00  Earnings     USDC   2.36356868
2021-03-31 00:00:00  Earnings     USDC   2.36418595
2021-04-01 00:00:00  Earnings     USDC   2.36480337
2021-04-02 00:00:00  Earnings     USDC   2.36542096
2021-04-03 00:00:00  Earnings     USDC   2.36603871
2021-04-04 00:00:00  Earnings     USDC   2.36665662
2021-04-05 00:00:00  Earnings     USDC   2.36727469
2021-04-06 00:00:00  Earnings     USDC   2.36789292
2021-04-07 00:00:00  Earnings     USDC   2.36851132
2021-04-08 00:00:00  Earnings     USDC   2.36912987
2021-04-09 00:00:00  Earnings     USDC   2.36974859
2021-04-10 00:00:00  Earnings     USDC   2.37036747
2021-04-11 00:00:00  Earnings     USDC   2.37098651
2021-04-12 00:00:00  Earnings     USDC   2.37160571
2021-04-13 00:00:00  Earnings     USDC   2.37222507
2021-04-14 00:00:00  Earnings     USDC   2.37284460
2021-04-15 00:00:00  Earnings     USDC   2.37346428
2021-04-16 00:00:00  Earnings     USDC   2.37408413
2021-04-17 00:00:00  Earnings     USDC   2.37470414
2021-04-18 00:00:00  Earnings     USDC   2.37532432
2021-04-19 00:00:00  Earnings     USDC   2.37594465
2021-04-20 00:00:00  Earnings     USDC   2.37656515
2021-04-21 00:00:00  Earnings     USDC   2.37718581
2021-04-22 00:00:00  Earnings     USDC   2.37780663
2021-04-23 00:00:00  Earnings     USDC   2.37842761
2021-04-24 00:00:00  Earnings     USDC   2.37904876
2021-04-25 00:00:00  Earnings     USDC   2.37967006
2021-04-26 00:00:00  Earnings     USDC   2.38029153
2021-04-27 00:00:00  Earnings     USDC   2.38091316
2021-04-28 00:00:00  Earnings     USDC   2.38153496
2021-04-29 00:00:00  Earnings     USDC   2.38215692
2021-04-30 00:00:00  Earnings     USDC   2.38277903
2021-05-01 00:00:00  Earnings     USDC   2.38340132
2021-05-02 00:00:00  Earnings     USDC   2.38402376
2021-05-03 00:00:00  Earnings     USDC   2.38464637
2021-05-04 00:00:00  Earnings     USDC   2.38526914
2021-05-05 00:00:00  Earnings     USDC   2.38589207
2021-05-06 00:00:00  Earnings     USDC   2.38651516
2021-05-07 00:00:00  Earnings     USDC   2.38713842
2021-05-08 00:00:00  Earnings     USDC   2.38776184
2021-05-09 00:00:00  Earnings     USDC   2.38838542
2021-05-10 00:00:00  Earnings     USDC   2.38900917
2021-05-11 00:00:00  Earnings     USDC   2.38963308
2021-05-12 00:00:00  Earnings     USDC   2.39025715
2021-05-13 00:00:00  Earnings     USDC   2.39088138
2021-05-14 00:00:00  Earnings     USDC   2.39150578
2021-05-15 00:00:00  Earnings     USDC   2.39213034
2021-05-16 00:00:00  Earnings     USDC   2.39275506
2021-05-17 00:00:00  Earnings     USDC   2.39337995
2021-05-18 00:00:00  Earnings     USDC   2.39400500
2021-05-19 00:00:00  Earnings     USDC   2.39463021
2021-05-20 00:00:00  Earnings     USDC   2.39525559
2021-05-21 00:00:00  Earnings     USDC   2.39588113
2021-05-22 00:00:00  Earnings     USDC   2.39650683
2021-05-23 00:00:00  Earnings     USDC   2.39713270
2021-05-24 00:00:00  Earnings     USDC   2.39775873
2021-05-25 00:00:00  Earnings     USDC   2.39838492
2021-05-26 00:00:00  Earnings     USDC   2.39901128
2021-05-27 00:00:00  Earnings     USDC   2.39963780
2021-05-28 00:00:00  Earnings     USDC   2.40026449
2021-05-29 00:00:00  Earnings     USDC   2.40089133
2021-05-30 00:00:00  Earnings     USDC   2.40151835
2021-05-31 00:00:00  Earnings     USDC   2.40214552
2021-06-01 00:00:00  Earnings     USDC   2.40277286
2021-06-02 00:00:00  Earnings     USDC   2.40340036
2021-06-03 00:00:00  Earnings     USDC   2.40402803
2021-06-04 00:00:00  Earnings     USDC   2.40465586
2021-06-05 00:00:00  Earnings     USDC   2.40528386
2021-06-06 00:00:00  Earnings     USDC   2.40591202
2021-06-07 00:00:00  Earnings     USDC   2.40654034
2021-06-08 00:00:00  Earnings     USDC   2.40716883
2021-06-09 00:00:00  Earnings     USDC   2.40779748
2021-06-10 00:00:00  Earnings     USDC   2.40842629
2021-06-11 00:00:00  Earnings     USDC   2.40905527
2021-06-12 00:00:00  Earnings     USDC   2.40968441
2021-06-13 00:00:00  Earnings     USDC   2.41031372
2021-06-14 00:00:00  Earnings     USDC   2.41094320
2021-06-15 00:00:00  Earnings     USDC   2.41157283
2021-06-16 00:00:00  Earnings     USDC   2.41220263
2021-06-17 00:00:00  Earnings     USDC   2.41283260
2021-06-18 00:00:00  Earnings     USDC   2.41346273
2021-06-19 00:00:00  Earnings     USDC   2.41409302
2021-06-20 00:00:00  Earnings     USDC   2.41472348
2021-06-21 00:00:00  Earnings     USDC   2.41535411
2021-06-22 00:00:00  Earnings     USDC   2.41598490
2021-06-23 00:00:00  Earnings     USDC   2.41661585
2021-06-24 00:00:00  Earnings     USDC   2.41724697
2021-06-25 00:00:00  Earnings     USDC   2.41787825
2021-06-26 00:00:00  Earnings     USDC   2.41850970
2021-06-27 00:00:00  Earnings     USDC   2.41914131
2021-06-28 00:00:00  Earnings     USDC   2.41977309
2021-06-29 00:00:00  Earnings     USDC   2.42040503
2021-06-30 00:00:00  Earnings     USDC   2.42103714
2021-07-01 00:00:00  Earnings     USDC   2.42166941
2021-07-02 00:00:00  Earnings     USDC   2.42230185
2021-07-03 00:00:00  Earnings     USDC   2.42293445
2021-07-04 00:00:00  Earnings     USDC   2.42356722
2021-07-05 00:00:00  Earnings     USDC   2.42420016
2021-07-06 00:00:00  Earnings     USDC   2.42483326
2021-07-07 00:00:00  Earnings     USDC   2.42546652
2021-07-08 00:00:00  Earnings     USDC   2.42609995
2021-07-09 00:00:00  Earnings     USDC   2.42673354
2021-07-10 00:00:00  Earnings     USDC   2.42736731
2021-07-11 00:00:00  Earnings     USDC   2.42800123
2021-07-12 00:00:00  Earnings     USDC   2.42863532
2021-07-13 00:00:00  Earnings     USDC   2.42926958
2021-07-14 00:00:00  Earnings     USDC   2.42990400
2021-07-15 00:00:00  Earnings     USDC   2.43053859
2021-07-16 00:00:00  Earnings     USDC   2.43117335
2021-07-17 00:00:00  Earnings     USDC   2.43180827
2021-07-18 00:00:00  Earnings     USDC   2.43244335
2021-07-19 00:00:00  Earnings     USDC   2.43307860
2021-07-20 00:00:00  Earnings     USDC   2.43371402
2021-07-21 00:00:00  Earnings     USDC   2.43434960
2021-07-22 00:00:00  Earnings     USDC   2.43498535
2021-07-23 00:00:00  Earnings     USDC   2.43562127
2021-07-24 00:00:00  Earnings     USDC   2.43625735
2021-07-25 00:00:00  Earnings     USDC   2.43689360
2021-07-26 00:00:00  Earnings     USDC   2.43753001
2021-07-27 00:00:00  Earnings     USDC   2.43816659
2021-07-28 00:00:00  Earnings     USDC   2.43880334
2021-07-29 00:00:00  Earnings     USDC   2.43944025
2021-07-30 00:00:00  Earnings     USDC   2.44007733
2021-07-31 00:00:00  Earnings     USDC   2.44071458
2021-08-01 00:00:00  Earnings     USDC   2.44135199
2021-08-02 00:00:00  Earnings     USDC   2.44198957
2021-08-03 00:00:00  Earnings     USDC   2.44262731
2021-08-04 00:00:00  Earnings     USDC   2.44326522
2021-08-05 00:00:00  Earnings     USDC   2.44390330
2021-08-06 00:00:00  Earnings     USDC   2.44454155
2021-08-07 00:00:00  Earnings     USDC   2.44517996
2021-08-08 00:00:00  Earnings     USDC   2.44581854
2021-08-09 00:00:00  Earnings     USDC   2.44645728
2021-08-10 00:00:00  Earnings     USDC   2.44709619
2021-08-11 00:00:00  Earnings     USDC   2.44773527
2021-08-12 00:00:00  Earnings     USDC   2.44837452
2021-08-13 00:00:00  Earnings     USDC   2.44901393
2021-08-14 00:00:00  Earnings     USDC   2.44965351
2021-08-15 00:00:00  Earnings     USDC   2.45029325
2021-08-16 00:00:00  Earnings     USDC   2.45093317
2021-08-17 00:00:00  Earnings     USDC   2.45157325
2021-08-18 00:00:00  Earnings     USDC   2.45221349
2021-08-19 00:00:00  Earnings     USDC   2.45285391
2021-08-20 00:00:00  Earnings     USDC   2.45349449
2021-08-21 00:00:00  Earnings     USDC   2.45413524
2021-08-22 00:00:00  Earnings     USDC   2.45477616
2021-08-23 00:00:00  Earnings     USDC   2.45541724
2021-08-24 00:00:00  Earnings     USDC   2.45605849
2021-08-25 00:00:00  Earnings     USDC   2.45669991
2021-08-26 00:00:00  Earnings     USDC   2.45734150
2021-08-27 00:00:00  Earnings     USDC   2.45798325
2021-08-28 00:00:00  Earnings     USDC   2.45862518
2021-08-29 00:00:00  Earnings     USDC   2.45926726
2021-08-30 00:00:00  Earnings     USDC   2.45990952
2021-08-31 00:00:00  Earnings     USDC   2.46055195
2021-09-01 00:00:00  Earnings     USDC   2.46119454
2021-09-02 00:00:00  Earnings     USDC   2.46183730
2021-09-03 00:00:00  Earnings     USDC   2.46248023
2021-09-04 00:00:00  Earnings     USDC   2.46312332
2021-09-05 00:00:00  Earnings     USDC   2.46376659
2021-09-06 00:00:00  Earnings     USDC   2.46441002
2021-09-07 00:00:00  Earnings     USDC   2.46505362
2021-09-08 00:00:00  Earnings     USDC   2.46569739
2021-09-09 00:00:00  Earnings     USDC   2.46634132
2021-09-10 00:00:00  Earnings     USDC   2.46698543
2021-09-11 00:00:00  Earnings     USDC   2.46762970
2021-09-12 00:00:00  Earnings     USDC   2.46827414
2021-09-13 00:00:00  Earnings     USDC   2.46891875
2021-09-14 00:00:00  Earnings     USDC   2.46956353
2021-09-15 00:00:00  Earnings     USDC   2.47020847
2021-09-16 00:00:00  Earnings     USDC   2.47085359
2021-09-17 00:00:00  Earnings     USDC   2.47149887
2021-09-18 00:00:00  Earnings     USDC   2.47214432
2021-09-19 00:00:00  Earnings     USDC   2.47278994
2021-09-20 00:00:00  Earnings     USDC   2.47343573
2021-09-21 00:00:00  Earnings     USDC   2.47408169
2021-09-22 00:00:00  Earnings     USDC   2.47472782
2021-09-23 00:00:00  Earnings     USDC   2.47537411
2021-09-24 00:00:00  Earnings     USDC   2.47602057
2021-09-25 00:00:00  Earnings     USDC   2.47666721
2021-09-26 00:00:00  Earnings     USDC   2.47731401
2021-09-27 00:00:00  Earnings     USDC   2.47796098
2021-09-28 00:00:00  Earnings     USDC   2.47860812
2021-09-29 00:00:00  Earnings     USDC   2.47925542
2021-09-30 00:00:00  Earnings     USDC   2.47990290
2021-10-01 00:00:00  Earnings     USDC   2.48055055
2021-10-02 00:00:00  Earnings     USDC   2.48119836
2021-10-03 00:00:00  Earnings     USDC   2.48184635
2021-10-04 00:00:00  Earnings     USDC   2.48249450
2021-10-05 00:00:00  Earnings     USDC   2.48314282
2021-10-06 00:00:00  Earnings     USDC   2.48379132
2021-10-07 00:00:00  Earnings     USDC   2.48443998
2021-10-08 00:00:00  Earnings     USDC   2.48508881
2021-10-09 00:00:00  Earnings     USDC   2.48573781
2021-10-10 00:00:00  Earnings     USDC   2.48638698
2021-10-11 00:00:00  Earnings     USDC   2.48703632
2021-10-12 00:00:00  Earnings     USDC   2.48768583
2021-10-13 00:00:00  Earnings     USDC   2.48833551
2021-10-14 00:00:00  Earnings     USDC   2.48898535
2021-10-15 00:00:00  Earnings     USDC   2.48963537
2021-10-16 00:00:00  Earnings     USDC   2.49028556
2021-10-17 00:00:00  Earnings     USDC   2.49093592
2021-10-18 00:00:00  Earnings     USDC   2.49158645
2021-10-19 00:00:00  Earnings     USDC   2.49223714
2021-10-20 00:00:00  Earnings     USDC   2.49288801
2021-10-21 00:00:00  Earnings     USDC   2.49353905
2021-10-22 00:00:00  Earnings     USDC   2.49419026
2021-10-23 00:00:00  Earnings     USDC   2.49484163
2021-10-24 00:00:00  Earnings     USDC   2.49549318
2021-10-25 00:00:00  Earnings     USDC   2.49614490
2021-10-26 00:00:00  Earnings     USDC   2.49679679
2021-10-27 00:00:00  Earnings     USDC   2.49744884
2021-10-28 00:00:00  Earnings     USDC   2.49810107
2021-10-29 00:00:00  Earnings     USDC   2.49875347
2021-10-30 00:00:00  Earnings     USDC   2.49940604
2021-10-31 00:00:00  Earnings     USDC   2.50005878
2021-11-01 00:00:00  Earnings     USDC   2.50071169
2021-11-02 00:00:00  Earnings     USDC   2.50136477
2021-11-03 00:00:00  Earnings     USDC   2.50201802
2021-11-04 00:00:00  Earnings     USDC   2.50267144
2021-11-05 00:00:00  Earnings     USDC   2.50332504
2021-11-06 00:00:00  Earnings     USDC   2.50397880
2021-11-07 00:00:00  Earnings     USDC   2.50463273
2021-11-08 00:00:00  Earnings     USDC   2.50528684
2021-11-09 00:00:00  Earnings     USDC   2.50594111
2021-11-10 00:00:00  Earnings     USDC   2.50659556
2021-11-11 00:00:00  Earnings     USDC   2.50725018
2021-11-12 00:00:00  Earnings     USDC   2.50790496
2021-11-13 00:00:00  Earnings     USDC   2.50855992
2021-11-14 00:00:00  Earnings     USDC   2.50921505
2021-11-15 00:00:00  Earnings     USDC   2.50987036
2021-11-16 00:00:00  Earnings     USDC   2.51052583
2021-11-17 00:00:00  Earnings     USDC   2.51118147
2021-11-18 00:00:00  Earnings     USDC   2.51183729
2021-11-19 00:00:00  Earnings     USDC   2.51249327
2021-11-20 00:00:00  Earnings     USDC   2.51314943
2021-11-21 00:00:00  Earnings     USDC   2.51380576
2021-11-22 00:00:00  Earnings     USDC   2.51446226
2021-11-23 00:00:00  Earnings     USDC   2.51511893
2021-11-24 00:00:00  Earnings     USDC   2.51577577
2021-11-25 00:00:00  Earnings     USDC   2.51643279
2021-11-26 00:00:00  Earnings     USDC   2.51708997
2021-11-27 00:00:00  Earnings     USDC   2.51774733
2021-11-28 00:00:00  Earnings     USDC   2.51840486
2021-11-29 00:00:00  Earnings     USDC   2.51906256
2021-11-30 00:00:00  Earnings     USDC   2.51972044
2021-12-01 00:00:00  Earnings     USDC   2.52037848
2021-12-02 00:00:00  Earnings     USDC   2.52103670
2021-12-03 00:00:00  Earnings     USDC   2.52169509
2021-12-04 00:00:00  Earnings     USDC   2.52235365
2021-12-05 00:00:00  Earnings     USDC   2.52301238
2021-12-06 00:00:00  Earnings     USDC   2.52367128
2021-12-07 00:00:00  Earnings     USDC   2.52433036
2021-12-08 00:00:00  Earnings     USDC   2.52498961
2021-12-09 00:00:00  Earnings     USDC   2.52564903
2021-12-10 00:00:00  Earnings     USDC   2.52630862
2021-12-11 00:00:00  Earnings     USDC   2.52696839
2021-12-12 00:00:00  Earnings     USDC   2.52762833
2021-12-13 00:00:00  Earnings     USDC   2.52828844
2021-12-14 00:00:00  Earnings     USDC   2.52894872
2021-12-15 00:00:00  Earnings     USDC   2.52960917
2021-12-16 00:00:00  Earnings     USDC   2.53026980
2021-12-17 00:00:00  Earnings     USDC   2.53093060
2021-12-18 00:00:00  Earnings     USDC   2.53159157
2021-12-19 00:00:00  Earnings     USDC   2.53225272
2021-12-20 00:00:00  Earnings     USDC   2.53291404
2021-12-21 00:00:00  Earnings     USDC   2.53357553
2021-12-22 00:00:00  Earnings     USDC   2.53423719
2021-12-23 00:00:00  Earnings     USDC   2.53489903
2021-12-24 00:00:00  Earnings     USDC   2.53556103
2021-12-25 00:00:00  Earnings     USDC   2.53622322
2021-12-26 00:00:00  Earnings     USDC   2.53688557
2021-12-27 00:00:00  Earnings     USDC   2.53754810
2021-12-28 00:00:00  Earnings     USDC   2.53821080
2021-12-29 00:00:00  Earnings     USDC   2.53887367
2021-12-30 00:00:00  Earnings     USDC   2.53953672
2021-12-31 00:00:00  Earnings     USDC   2.54019994
TOTAL                                  729.22345326'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                  DEP/WITHDR                                                                         \n' + \
'                  USDC                                   CHF           CAPITAL                    DATE              YIELD            \n' + \
'        Tot incl yield  DF RATE CUR RATE CAP GAIN CAP GAIN %     USDC      CHF        FROM          TO DAYS   USDC    CHF  Y % YR Y %\n' + \
'OWNER                                                                                                                                ' + \
'''
Béa           4,000.00 4,000.00 3,642.00  -358.00      -8.95 4,000.00 3,642.00  2021-02-20  2021-12-31  315 342.93 312.23 8.57  10.00
TOTAL         4,342.93 4,000.00 3,954.23  -358.00      -8.95                                                342.93 312.23            ''' + \
'''
JPS           5,000.00 5,000.00 4,552.50  -447.50      -8.95 5,000.00 4,552.50  2021-03-22  2021-12-31  285 386.30 351.72 7.73  10.00
TOTAL         5,386.30 5,000.00 4,904.22  -447.50      -8.95                                                386.30 351.72            ''' + \
'''
G TOTAL       9,729.22          8,858.46                                                                    729.22 663.96            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_USDC_1_fiat_simple_values_2_owners_bug_french_language(self):
		"""
		USDC crypto, 2 owners with 1 deposit, fixed yield rate,
		USDC/CHF final rate of 1.5.

		Corresponding OwnerDepositYieldComputer tesz:
		TestOwnerDepositYieldComputer.testComputeDepositsYields_2_owners_bug
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSBEarningUsdc_simple_values_bug.xlsx'
		depositSheetFileName = 'depositUsdc_fiat_chf_simple_values_bug.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(),
								   self.cryptoFiatCsvFilePathName),
								   language=FR)

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2021-02-20 00:00:00  Earnings     USDC   1.04463150
2021-02-21 00:00:00  Earnings     USDC   1.04490432
2021-02-22 00:00:00  Earnings     USDC   1.04517720
2021-02-23 00:00:00  Earnings     USDC   1.04545016
2021-02-24 00:00:00  Earnings     USDC   1.04572319
2021-02-25 00:00:00  Earnings     USDC   1.04599629
2021-02-26 00:00:00  Earnings     USDC   1.04626946
2021-02-27 00:00:00  Earnings     USDC   1.04654270
2021-02-28 00:00:00  Earnings     USDC   1.04681601
2021-03-01 00:00:00  Earnings     USDC   1.04708939
2021-03-02 00:00:00  Earnings     USDC   1.04736285
2021-03-03 00:00:00  Earnings     USDC   1.04763638
2021-03-04 00:00:00  Earnings     USDC   1.04790998
2021-03-05 00:00:00  Earnings     USDC   1.04818365
2021-03-06 00:00:00  Earnings     USDC   1.04845739
2021-03-07 00:00:00  Earnings     USDC   1.04873120
2021-03-08 00:00:00  Earnings     USDC   1.04900508
2021-03-09 00:00:00  Earnings     USDC   1.04927904
2021-03-10 00:00:00  Earnings     USDC   1.04955307
2021-03-11 00:00:00  Earnings     USDC   1.04982717
2021-03-12 00:00:00  Earnings     USDC   1.05010134
2021-03-13 00:00:00  Earnings     USDC   1.05037558
2021-03-14 00:00:00  Earnings     USDC   1.05064989
2021-03-15 00:00:00  Earnings     USDC   1.05092428
2021-03-16 00:00:00  Earnings     USDC   1.05119874
2021-03-17 00:00:00  Earnings     USDC   1.05147326
2021-03-18 00:00:00  Earnings     USDC   1.05174787
2021-03-19 00:00:00  Earnings     USDC   1.05202254
2021-03-20 00:00:00  Earnings     USDC   1.05229728
2021-03-21 00:00:00  Earnings     USDC   1.05257210
2021-03-22 00:00:00  Earnings     USDC   2.35863637
2021-03-23 00:00:00  Earnings     USDC   2.35925234
2021-03-24 00:00:00  Earnings     USDC   2.35986848
2021-03-25 00:00:00  Earnings     USDC   2.36048478
2021-03-26 00:00:00  Earnings     USDC   2.36110124
2021-03-27 00:00:00  Earnings     USDC   2.36171786
2021-03-28 00:00:00  Earnings     USDC   2.36233464
2021-03-29 00:00:00  Earnings     USDC   2.36295158
2021-03-30 00:00:00  Earnings     USDC   2.36356868
2021-03-31 00:00:00  Earnings     USDC   2.36418595
2021-04-01 00:00:00  Earnings     USDC   2.36480337
2021-04-02 00:00:00  Earnings     USDC   2.36542096
2021-04-03 00:00:00  Earnings     USDC   2.36603871
2021-04-04 00:00:00  Earnings     USDC   2.36665662
2021-04-05 00:00:00  Earnings     USDC   2.36727469
2021-04-06 00:00:00  Earnings     USDC   2.36789292
2021-04-07 00:00:00  Earnings     USDC   2.36851132
2021-04-08 00:00:00  Earnings     USDC   2.36912987
2021-04-09 00:00:00  Earnings     USDC   2.36974859
2021-04-10 00:00:00  Earnings     USDC   2.37036747
2021-04-11 00:00:00  Earnings     USDC   2.37098651
2021-04-12 00:00:00  Earnings     USDC   2.37160571
2021-04-13 00:00:00  Earnings     USDC   2.37222507
2021-04-14 00:00:00  Earnings     USDC   2.37284460
2021-04-15 00:00:00  Earnings     USDC   2.37346428
2021-04-16 00:00:00  Earnings     USDC   2.37408413
2021-04-17 00:00:00  Earnings     USDC   2.37470414
2021-04-18 00:00:00  Earnings     USDC   2.37532432
2021-04-19 00:00:00  Earnings     USDC   2.37594465
2021-04-20 00:00:00  Earnings     USDC   2.37656515
2021-04-21 00:00:00  Earnings     USDC   2.37718581
2021-04-22 00:00:00  Earnings     USDC   2.37780663
2021-04-23 00:00:00  Earnings     USDC   2.37842761
2021-04-24 00:00:00  Earnings     USDC   2.37904876
2021-04-25 00:00:00  Earnings     USDC   2.37967006
2021-04-26 00:00:00  Earnings     USDC   2.38029153
2021-04-27 00:00:00  Earnings     USDC   2.38091316
2021-04-28 00:00:00  Earnings     USDC   2.38153496
2021-04-29 00:00:00  Earnings     USDC   2.38215692
2021-04-30 00:00:00  Earnings     USDC   2.38277903
2021-05-01 00:00:00  Earnings     USDC   2.38340132
2021-05-02 00:00:00  Earnings     USDC   2.38402376
2021-05-03 00:00:00  Earnings     USDC   2.38464637
2021-05-04 00:00:00  Earnings     USDC   2.38526914
2021-05-05 00:00:00  Earnings     USDC   2.38589207
2021-05-06 00:00:00  Earnings     USDC   2.38651516
2021-05-07 00:00:00  Earnings     USDC   2.38713842
2021-05-08 00:00:00  Earnings     USDC   2.38776184
2021-05-09 00:00:00  Earnings     USDC   2.38838542
2021-05-10 00:00:00  Earnings     USDC   2.38900917
2021-05-11 00:00:00  Earnings     USDC   2.38963308
2021-05-12 00:00:00  Earnings     USDC   2.39025715
2021-05-13 00:00:00  Earnings     USDC   2.39088138
2021-05-14 00:00:00  Earnings     USDC   2.39150578
2021-05-15 00:00:00  Earnings     USDC   2.39213034
2021-05-16 00:00:00  Earnings     USDC   2.39275506
2021-05-17 00:00:00  Earnings     USDC   2.39337995
2021-05-18 00:00:00  Earnings     USDC   2.39400500
2021-05-19 00:00:00  Earnings     USDC   2.39463021
2021-05-20 00:00:00  Earnings     USDC   2.39525559
2021-05-21 00:00:00  Earnings     USDC   2.39588113
2021-05-22 00:00:00  Earnings     USDC   2.39650683
2021-05-23 00:00:00  Earnings     USDC   2.39713270
2021-05-24 00:00:00  Earnings     USDC   2.39775873
2021-05-25 00:00:00  Earnings     USDC   2.39838492
2021-05-26 00:00:00  Earnings     USDC   2.39901128
2021-05-27 00:00:00  Earnings     USDC   2.39963780
2021-05-28 00:00:00  Earnings     USDC   2.40026449
2021-05-29 00:00:00  Earnings     USDC   2.40089133
2021-05-30 00:00:00  Earnings     USDC   2.40151835
2021-05-31 00:00:00  Earnings     USDC   2.40214552
2021-06-01 00:00:00  Earnings     USDC   2.40277286
2021-06-02 00:00:00  Earnings     USDC   2.40340036
2021-06-03 00:00:00  Earnings     USDC   2.40402803
2021-06-04 00:00:00  Earnings     USDC   2.40465586
2021-06-05 00:00:00  Earnings     USDC   2.40528386
2021-06-06 00:00:00  Earnings     USDC   2.40591202
2021-06-07 00:00:00  Earnings     USDC   2.40654034
2021-06-08 00:00:00  Earnings     USDC   2.40716883
2021-06-09 00:00:00  Earnings     USDC   2.40779748
2021-06-10 00:00:00  Earnings     USDC   2.40842629
2021-06-11 00:00:00  Earnings     USDC   2.40905527
2021-06-12 00:00:00  Earnings     USDC   2.40968441
2021-06-13 00:00:00  Earnings     USDC   2.41031372
2021-06-14 00:00:00  Earnings     USDC   2.41094320
2021-06-15 00:00:00  Earnings     USDC   2.41157283
2021-06-16 00:00:00  Earnings     USDC   2.41220263
2021-06-17 00:00:00  Earnings     USDC   2.41283260
2021-06-18 00:00:00  Earnings     USDC   2.41346273
2021-06-19 00:00:00  Earnings     USDC   2.41409302
2021-06-20 00:00:00  Earnings     USDC   2.41472348
2021-06-21 00:00:00  Earnings     USDC   2.41535411
2021-06-22 00:00:00  Earnings     USDC   2.41598490
2021-06-23 00:00:00  Earnings     USDC   2.41661585
2021-06-24 00:00:00  Earnings     USDC   2.41724697
2021-06-25 00:00:00  Earnings     USDC   2.41787825
2021-06-26 00:00:00  Earnings     USDC   2.41850970
2021-06-27 00:00:00  Earnings     USDC   2.41914131
2021-06-28 00:00:00  Earnings     USDC   2.41977309
2021-06-29 00:00:00  Earnings     USDC   2.42040503
2021-06-30 00:00:00  Earnings     USDC   2.42103714
2021-07-01 00:00:00  Earnings     USDC   2.42166941
2021-07-02 00:00:00  Earnings     USDC   2.42230185
2021-07-03 00:00:00  Earnings     USDC   2.42293445
2021-07-04 00:00:00  Earnings     USDC   2.42356722
2021-07-05 00:00:00  Earnings     USDC   2.42420016
2021-07-06 00:00:00  Earnings     USDC   2.42483326
2021-07-07 00:00:00  Earnings     USDC   2.42546652
2021-07-08 00:00:00  Earnings     USDC   2.42609995
2021-07-09 00:00:00  Earnings     USDC   2.42673354
2021-07-10 00:00:00  Earnings     USDC   2.42736731
2021-07-11 00:00:00  Earnings     USDC   2.42800123
2021-07-12 00:00:00  Earnings     USDC   2.42863532
2021-07-13 00:00:00  Earnings     USDC   2.42926958
2021-07-14 00:00:00  Earnings     USDC   2.42990400
2021-07-15 00:00:00  Earnings     USDC   2.43053859
2021-07-16 00:00:00  Earnings     USDC   2.43117335
2021-07-17 00:00:00  Earnings     USDC   2.43180827
2021-07-18 00:00:00  Earnings     USDC   2.43244335
2021-07-19 00:00:00  Earnings     USDC   2.43307860
2021-07-20 00:00:00  Earnings     USDC   2.43371402
2021-07-21 00:00:00  Earnings     USDC   2.43434960
2021-07-22 00:00:00  Earnings     USDC   2.43498535
2021-07-23 00:00:00  Earnings     USDC   2.43562127
2021-07-24 00:00:00  Earnings     USDC   2.43625735
2021-07-25 00:00:00  Earnings     USDC   2.43689360
2021-07-26 00:00:00  Earnings     USDC   2.43753001
2021-07-27 00:00:00  Earnings     USDC   2.43816659
2021-07-28 00:00:00  Earnings     USDC   2.43880334
2021-07-29 00:00:00  Earnings     USDC   2.43944025
2021-07-30 00:00:00  Earnings     USDC   2.44007733
2021-07-31 00:00:00  Earnings     USDC   2.44071458
2021-08-01 00:00:00  Earnings     USDC   2.44135199
2021-08-02 00:00:00  Earnings     USDC   2.44198957
2021-08-03 00:00:00  Earnings     USDC   2.44262731
2021-08-04 00:00:00  Earnings     USDC   2.44326522
2021-08-05 00:00:00  Earnings     USDC   2.44390330
2021-08-06 00:00:00  Earnings     USDC   2.44454155
2021-08-07 00:00:00  Earnings     USDC   2.44517996
2021-08-08 00:00:00  Earnings     USDC   2.44581854
2021-08-09 00:00:00  Earnings     USDC   2.44645728
2021-08-10 00:00:00  Earnings     USDC   2.44709619
2021-08-11 00:00:00  Earnings     USDC   2.44773527
2021-08-12 00:00:00  Earnings     USDC   2.44837452
2021-08-13 00:00:00  Earnings     USDC   2.44901393
2021-08-14 00:00:00  Earnings     USDC   2.44965351
2021-08-15 00:00:00  Earnings     USDC   2.45029325
2021-08-16 00:00:00  Earnings     USDC   2.45093317
2021-08-17 00:00:00  Earnings     USDC   2.45157325
2021-08-18 00:00:00  Earnings     USDC   2.45221349
2021-08-19 00:00:00  Earnings     USDC   2.45285391
2021-08-20 00:00:00  Earnings     USDC   2.45349449
2021-08-21 00:00:00  Earnings     USDC   2.45413524
2021-08-22 00:00:00  Earnings     USDC   2.45477616
2021-08-23 00:00:00  Earnings     USDC   2.45541724
2021-08-24 00:00:00  Earnings     USDC   2.45605849
2021-08-25 00:00:00  Earnings     USDC   2.45669991
2021-08-26 00:00:00  Earnings     USDC   2.45734150
2021-08-27 00:00:00  Earnings     USDC   2.45798325
2021-08-28 00:00:00  Earnings     USDC   2.45862518
2021-08-29 00:00:00  Earnings     USDC   2.45926726
2021-08-30 00:00:00  Earnings     USDC   2.45990952
2021-08-31 00:00:00  Earnings     USDC   2.46055195
2021-09-01 00:00:00  Earnings     USDC   2.46119454
2021-09-02 00:00:00  Earnings     USDC   2.46183730
2021-09-03 00:00:00  Earnings     USDC   2.46248023
2021-09-04 00:00:00  Earnings     USDC   2.46312332
2021-09-05 00:00:00  Earnings     USDC   2.46376659
2021-09-06 00:00:00  Earnings     USDC   2.46441002
2021-09-07 00:00:00  Earnings     USDC   2.46505362
2021-09-08 00:00:00  Earnings     USDC   2.46569739
2021-09-09 00:00:00  Earnings     USDC   2.46634132
2021-09-10 00:00:00  Earnings     USDC   2.46698543
2021-09-11 00:00:00  Earnings     USDC   2.46762970
2021-09-12 00:00:00  Earnings     USDC   2.46827414
2021-09-13 00:00:00  Earnings     USDC   2.46891875
2021-09-14 00:00:00  Earnings     USDC   2.46956353
2021-09-15 00:00:00  Earnings     USDC   2.47020847
2021-09-16 00:00:00  Earnings     USDC   2.47085359
2021-09-17 00:00:00  Earnings     USDC   2.47149887
2021-09-18 00:00:00  Earnings     USDC   2.47214432
2021-09-19 00:00:00  Earnings     USDC   2.47278994
2021-09-20 00:00:00  Earnings     USDC   2.47343573
2021-09-21 00:00:00  Earnings     USDC   2.47408169
2021-09-22 00:00:00  Earnings     USDC   2.47472782
2021-09-23 00:00:00  Earnings     USDC   2.47537411
2021-09-24 00:00:00  Earnings     USDC   2.47602057
2021-09-25 00:00:00  Earnings     USDC   2.47666721
2021-09-26 00:00:00  Earnings     USDC   2.47731401
2021-09-27 00:00:00  Earnings     USDC   2.47796098
2021-09-28 00:00:00  Earnings     USDC   2.47860812
2021-09-29 00:00:00  Earnings     USDC   2.47925542
2021-09-30 00:00:00  Earnings     USDC   2.47990290
2021-10-01 00:00:00  Earnings     USDC   2.48055055
2021-10-02 00:00:00  Earnings     USDC   2.48119836
2021-10-03 00:00:00  Earnings     USDC   2.48184635
2021-10-04 00:00:00  Earnings     USDC   2.48249450
2021-10-05 00:00:00  Earnings     USDC   2.48314282
2021-10-06 00:00:00  Earnings     USDC   2.48379132
2021-10-07 00:00:00  Earnings     USDC   2.48443998
2021-10-08 00:00:00  Earnings     USDC   2.48508881
2021-10-09 00:00:00  Earnings     USDC   2.48573781
2021-10-10 00:00:00  Earnings     USDC   2.48638698
2021-10-11 00:00:00  Earnings     USDC   2.48703632
2021-10-12 00:00:00  Earnings     USDC   2.48768583
2021-10-13 00:00:00  Earnings     USDC   2.48833551
2021-10-14 00:00:00  Earnings     USDC   2.48898535
2021-10-15 00:00:00  Earnings     USDC   2.48963537
2021-10-16 00:00:00  Earnings     USDC   2.49028556
2021-10-17 00:00:00  Earnings     USDC   2.49093592
2021-10-18 00:00:00  Earnings     USDC   2.49158645
2021-10-19 00:00:00  Earnings     USDC   2.49223714
2021-10-20 00:00:00  Earnings     USDC   2.49288801
2021-10-21 00:00:00  Earnings     USDC   2.49353905
2021-10-22 00:00:00  Earnings     USDC   2.49419026
2021-10-23 00:00:00  Earnings     USDC   2.49484163
2021-10-24 00:00:00  Earnings     USDC   2.49549318
2021-10-25 00:00:00  Earnings     USDC   2.49614490
2021-10-26 00:00:00  Earnings     USDC   2.49679679
2021-10-27 00:00:00  Earnings     USDC   2.49744884
2021-10-28 00:00:00  Earnings     USDC   2.49810107
2021-10-29 00:00:00  Earnings     USDC   2.49875347
2021-10-30 00:00:00  Earnings     USDC   2.49940604
2021-10-31 00:00:00  Earnings     USDC   2.50005878
2021-11-01 00:00:00  Earnings     USDC   2.50071169
2021-11-02 00:00:00  Earnings     USDC   2.50136477
2021-11-03 00:00:00  Earnings     USDC   2.50201802
2021-11-04 00:00:00  Earnings     USDC   2.50267144
2021-11-05 00:00:00  Earnings     USDC   2.50332504
2021-11-06 00:00:00  Earnings     USDC   2.50397880
2021-11-07 00:00:00  Earnings     USDC   2.50463273
2021-11-08 00:00:00  Earnings     USDC   2.50528684
2021-11-09 00:00:00  Earnings     USDC   2.50594111
2021-11-10 00:00:00  Earnings     USDC   2.50659556
2021-11-11 00:00:00  Earnings     USDC   2.50725018
2021-11-12 00:00:00  Earnings     USDC   2.50790496
2021-11-13 00:00:00  Earnings     USDC   2.50855992
2021-11-14 00:00:00  Earnings     USDC   2.50921505
2021-11-15 00:00:00  Earnings     USDC   2.50987036
2021-11-16 00:00:00  Earnings     USDC   2.51052583
2021-11-17 00:00:00  Earnings     USDC   2.51118147
2021-11-18 00:00:00  Earnings     USDC   2.51183729
2021-11-19 00:00:00  Earnings     USDC   2.51249327
2021-11-20 00:00:00  Earnings     USDC   2.51314943
2021-11-21 00:00:00  Earnings     USDC   2.51380576
2021-11-22 00:00:00  Earnings     USDC   2.51446226
2021-11-23 00:00:00  Earnings     USDC   2.51511893
2021-11-24 00:00:00  Earnings     USDC   2.51577577
2021-11-25 00:00:00  Earnings     USDC   2.51643279
2021-11-26 00:00:00  Earnings     USDC   2.51708997
2021-11-27 00:00:00  Earnings     USDC   2.51774733
2021-11-28 00:00:00  Earnings     USDC   2.51840486
2021-11-29 00:00:00  Earnings     USDC   2.51906256
2021-11-30 00:00:00  Earnings     USDC   2.51972044
2021-12-01 00:00:00  Earnings     USDC   2.52037848
2021-12-02 00:00:00  Earnings     USDC   2.52103670
2021-12-03 00:00:00  Earnings     USDC   2.52169509
2021-12-04 00:00:00  Earnings     USDC   2.52235365
2021-12-05 00:00:00  Earnings     USDC   2.52301238
2021-12-06 00:00:00  Earnings     USDC   2.52367128
2021-12-07 00:00:00  Earnings     USDC   2.52433036
2021-12-08 00:00:00  Earnings     USDC   2.52498961
2021-12-09 00:00:00  Earnings     USDC   2.52564903
2021-12-10 00:00:00  Earnings     USDC   2.52630862
2021-12-11 00:00:00  Earnings     USDC   2.52696839
2021-12-12 00:00:00  Earnings     USDC   2.52762833
2021-12-13 00:00:00  Earnings     USDC   2.52828844
2021-12-14 00:00:00  Earnings     USDC   2.52894872
2021-12-15 00:00:00  Earnings     USDC   2.52960917
2021-12-16 00:00:00  Earnings     USDC   2.53026980
2021-12-17 00:00:00  Earnings     USDC   2.53093060
2021-12-18 00:00:00  Earnings     USDC   2.53159157
2021-12-19 00:00:00  Earnings     USDC   2.53225272
2021-12-20 00:00:00  Earnings     USDC   2.53291404
2021-12-21 00:00:00  Earnings     USDC   2.53357553
2021-12-22 00:00:00  Earnings     USDC   2.53423719
2021-12-23 00:00:00  Earnings     USDC   2.53489903
2021-12-24 00:00:00  Earnings     USDC   2.53556103
2021-12-25 00:00:00  Earnings     USDC   2.53622322
2021-12-26 00:00:00  Earnings     USDC   2.53688557
2021-12-27 00:00:00  Earnings     USDC   2.53754810
2021-12-28 00:00:00  Earnings     USDC   2.53821080
2021-12-29 00:00:00  Earnings     USDC   2.53887367
2021-12-30 00:00:00  Earnings     USDC   2.53953672
2021-12-31 00:00:00  Earnings     USDC   2.54019994
TOTAL                                  729.22345326'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                           DEPOTS/RETRAITS                                                                                 \n' + \
'                     USDC                                              CHF           CAPITAL                    DATE               INTERETS                \n' + \
'        Tot incl intérêts TX DAT DEP   TX ACT PLUS-VAL CAP       P-V CAP %     USDC      CHF          DE           A  JOURS   USDC      CHF INT % INT ANN %\n' + \
'PROPR                                                                                                                                                      ' + \
'''
Béa              4,000.00   4,000.00 3,642.00      -358.00           -8.95 4,000.00 3,642.00  2021-02-20  2021-12-31    315 342.93   312.23  8.57     10.00
TOTAL            4,342.93   4,000.00 3,954.23      -358.00           -8.95                                                  342.93   312.23                ''' + \
'''
JPS              5,000.00   5,000.00 4,552.50      -447.50           -8.95 5,000.00 4,552.50  2021-03-22  2021-12-31    285 386.30   351.72  7.73     10.00
TOTAL            5,386.30   5,000.00 4,904.22      -447.50           -8.95                                                  386.30   351.72                ''' + \
'''
G TOTAL          9,729.22            8,858.46                                                                               729.22   663.96                '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_USDC_1_fiat_simple_values_2_owners_2_deposits_bug_french_language(self):
		"""
		USDC crypto, 2 owners with 2 deposit and 1 withdrawal, fixed yield rate,
		USDC/CHF final rate of 1.5.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSBEarningUsdc_simple_values_multi_depwithdr_bug.xlsx'
		depositSheetFileName = 'depositUsdc_fiat_chf_simple_values_depwithdr_bug.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(),
								   self.cryptoFiatCsvFilePathName),
								   language=FR)

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2021-02-20 00:00:00  Earnings     USDC   1.04463150
2021-02-21 00:00:00  Earnings     USDC   1.04490432
2021-02-22 00:00:00  Earnings     USDC   1.04517720
2021-02-23 00:00:00  Earnings     USDC   1.04545016
2021-02-24 00:00:00  Earnings     USDC   1.04572319
2021-02-25 00:00:00  Earnings     USDC   1.04599629
2021-02-26 00:00:00  Earnings     USDC   1.04626946
2021-02-27 00:00:00  Earnings     USDC   1.04654270
2021-02-28 00:00:00  Earnings     USDC   1.04681601
2021-03-01 00:00:00  Earnings     USDC   1.04708939
2021-03-02 00:00:00  Earnings     USDC   1.04736285
2021-03-03 00:00:00  Earnings     USDC   1.04763638
2021-03-04 00:00:00  Earnings     USDC   1.04790998
2021-03-05 00:00:00  Earnings     USDC   1.04818365
2021-03-06 00:00:00  Earnings     USDC   1.04845739
2021-03-07 00:00:00  Earnings     USDC   1.04873120
2021-03-08 00:00:00  Earnings     USDC   1.04900508
2021-03-09 00:00:00  Earnings     USDC   1.04927904
2021-03-10 00:00:00  Earnings     USDC   1.04955307
2021-03-11 00:00:00  Earnings     USDC   1.04982717
2021-03-12 00:00:00  Earnings     USDC   1.05010134
2021-03-13 00:00:00  Earnings     USDC   1.05037558
2021-03-14 00:00:00  Earnings     USDC   1.05064989
2021-03-15 00:00:00  Earnings     USDC   1.05092428
2021-03-16 00:00:00  Earnings     USDC   1.05119874
2021-03-17 00:00:00  Earnings     USDC   1.05147326
2021-03-18 00:00:00  Earnings     USDC   1.05174787
2021-03-19 00:00:00  Earnings     USDC   1.05202254
2021-03-20 00:00:00  Earnings     USDC   1.05229728
2021-03-21 00:00:00  Earnings     USDC   1.05257210
2021-03-22 00:00:00  Earnings     USDC   2.35863637
2021-03-23 00:00:00  Earnings     USDC   2.35925234
2021-03-24 00:00:00  Earnings     USDC   2.35986848
2021-03-25 00:00:00  Earnings     USDC   2.36048478
2021-03-26 00:00:00  Earnings     USDC   2.36110124
2021-03-27 00:00:00  Earnings     USDC   2.36171786
2021-03-28 00:00:00  Earnings     USDC   2.36233464
2021-03-29 00:00:00  Earnings     USDC   2.36295158
2021-03-30 00:00:00  Earnings     USDC   2.36356868
2021-03-31 00:00:00  Earnings     USDC   2.36418595
2021-04-01 00:00:00  Earnings     USDC   2.36480337
2021-04-02 00:00:00  Earnings     USDC   2.36542096
2021-04-03 00:00:00  Earnings     USDC   2.36603871
2021-04-04 00:00:00  Earnings     USDC   2.36665662
2021-04-05 00:00:00  Earnings     USDC   2.36727469
2021-04-06 00:00:00  Earnings     USDC   2.36789292
2021-04-07 00:00:00  Earnings     USDC   2.36851132
2021-04-08 00:00:00  Earnings     USDC   2.36912987
2021-04-09 00:00:00  Earnings     USDC   2.36974859
2021-04-10 00:00:00  Earnings     USDC   2.37036747
2021-04-11 00:00:00  Earnings     USDC   2.37098651
2021-04-12 00:00:00  Earnings     USDC   2.37160571
2021-04-13 00:00:00  Earnings     USDC   2.37222507
2021-04-14 00:00:00  Earnings     USDC   2.37284460
2021-04-15 00:00:00  Earnings     USDC   2.37346428
2021-04-16 00:00:00  Earnings     USDC   2.37408413
2021-04-17 00:00:00  Earnings     USDC   2.37470414
2021-04-18 00:00:00  Earnings     USDC   2.37532432
2021-04-19 00:00:00  Earnings     USDC   2.37594465
2021-04-20 00:00:00  Earnings     USDC   2.37656515
2021-04-21 00:00:00  Earnings     USDC   2.37718581
2021-04-22 00:00:00  Earnings     USDC   2.11664875
2021-04-23 00:00:00  Earnings     USDC   2.11775446
2021-04-24 00:00:00  Earnings     USDC   2.11830752
2021-04-25 00:00:00  Earnings     USDC   2.11886074
2021-04-26 00:00:00  Earnings     USDC   2.11941409
2021-04-27 00:00:00  Earnings     USDC   2.11996760
2021-04-28 00:00:00  Earnings     USDC   2.12052124
2021-04-29 00:00:00  Earnings     USDC   2.12107503
2021-04-30 00:00:00  Earnings     USDC   2.12162897
2021-05-01 00:00:00  Earnings     USDC   2.12218305
2021-05-02 00:00:00  Earnings     USDC   2.12273727
2021-05-03 00:00:00  Earnings     USDC   2.12329164
2021-05-04 00:00:00  Earnings     USDC   2.12384616
2021-05-05 00:00:00  Earnings     USDC   2.12440082
2021-05-06 00:00:00  Earnings     USDC   2.12495562
2021-05-07 00:00:00  Earnings     USDC   2.12551057
2021-05-08 00:00:00  Earnings     USDC   2.12606566
2021-05-09 00:00:00  Earnings     USDC   2.12662090
2021-05-10 00:00:00  Earnings     USDC   2.12717628
2021-05-11 00:00:00  Earnings     USDC   2.12773181
2021-05-12 00:00:00  Earnings     USDC   2.12828749
2021-05-13 00:00:00  Earnings     USDC   2.12884331
2021-05-14 00:00:00  Earnings     USDC   2.12939927
2021-05-15 00:00:00  Earnings     USDC   2.12995538
2021-05-16 00:00:00  Earnings     USDC   2.13051163
2021-05-17 00:00:00  Earnings     USDC   2.13106803
2021-05-18 00:00:00  Earnings     USDC   2.13162458
2021-05-19 00:00:00  Earnings     USDC   2.13218127
2021-05-20 00:00:00  Earnings     USDC   2.13273811
2021-05-21 00:00:00  Earnings     USDC   2.13329509
2021-05-22 00:00:00  Earnings     USDC   2.13385221
2021-05-23 00:00:00  Earnings     USDC   2.13440949
2021-05-24 00:00:00  Earnings     USDC   2.13496690
2021-05-25 00:00:00  Earnings     USDC   2.13552447
2021-05-26 00:00:00  Earnings     USDC   2.13608218
2021-05-27 00:00:00  Earnings     USDC   2.13664003
2021-05-28 00:00:00  Earnings     USDC   2.13719803
2021-05-29 00:00:00  Earnings     USDC   2.13775618
2021-05-30 00:00:00  Earnings     USDC   2.13831447
2021-05-31 00:00:00  Earnings     USDC   2.13887291
2021-06-01 00:00:00  Earnings     USDC   2.13943149
2021-06-02 00:00:00  Earnings     USDC   2.13999022
2021-06-03 00:00:00  Earnings     USDC   2.14054910
2021-06-04 00:00:00  Earnings     USDC   2.14110812
2021-06-05 00:00:00  Earnings     USDC   2.14166728
2021-06-06 00:00:00  Earnings     USDC   2.14222660
2021-06-07 00:00:00  Earnings     USDC   2.14278606
2021-06-08 00:00:00  Earnings     USDC   2.14334566
2021-06-09 00:00:00  Earnings     USDC   2.14390541
2021-06-10 00:00:00  Earnings     USDC   2.14446531
2021-06-11 00:00:00  Earnings     USDC   2.14502536
2021-06-12 00:00:00  Earnings     USDC   2.14558555
2021-06-13 00:00:00  Earnings     USDC   2.14614588
2021-06-14 00:00:00  Earnings     USDC   2.14670637
2021-06-15 00:00:00  Earnings     USDC   2.14726700
2021-06-16 00:00:00  Earnings     USDC   2.14782777
2021-06-17 00:00:00  Earnings     USDC   2.14838869
2021-06-18 00:00:00  Earnings     USDC   2.14894976
2021-06-19 00:00:00  Earnings     USDC   2.14951098
2021-06-20 00:00:00  Earnings     USDC   2.15007234
2021-06-21 00:00:00  Earnings     USDC   2.15063385
2021-06-22 00:00:00  Earnings     USDC   2.15119550
2021-06-23 00:00:00  Earnings     USDC   2.15175730
2021-06-24 00:00:00  Earnings     USDC   2.15231925
2021-06-25 00:00:00  Earnings     USDC   2.15288135
2021-06-26 00:00:00  Earnings     USDC   2.15344359
2021-06-27 00:00:00  Earnings     USDC   2.15400598
2021-06-28 00:00:00  Earnings     USDC   2.15456851
2021-06-29 00:00:00  Earnings     USDC   2.15513120
2021-06-30 00:00:00  Earnings     USDC   2.15569403
2021-07-01 00:00:00  Earnings     USDC   2.15625700
2021-07-02 00:00:00  Earnings     USDC   2.15682013
2021-07-03 00:00:00  Earnings     USDC   2.15738340
2021-07-04 00:00:00  Earnings     USDC   2.15794681
2021-07-05 00:00:00  Earnings     USDC   2.15851038
2021-07-06 00:00:00  Earnings     USDC   2.15907409
2021-07-07 00:00:00  Earnings     USDC   2.15963795
2021-07-08 00:00:00  Earnings     USDC   2.16020196
2021-07-09 00:00:00  Earnings     USDC   2.16076611
2021-07-10 00:00:00  Earnings     USDC   2.16133041
2021-07-11 00:00:00  Earnings     USDC   2.16189486
2021-07-12 00:00:00  Earnings     USDC   2.16245946
2021-07-13 00:00:00  Earnings     USDC   2.16302420
2021-07-14 00:00:00  Earnings     USDC   2.16358909
2021-07-15 00:00:00  Earnings     USDC   2.16415413
2021-07-16 00:00:00  Earnings     USDC   2.16471931
2021-07-17 00:00:00  Earnings     USDC   2.16528465
2021-07-18 00:00:00  Earnings     USDC   2.16585013
2021-07-19 00:00:00  Earnings     USDC   2.16641576
2021-07-20 00:00:00  Earnings     USDC   2.16698153
2021-07-21 00:00:00  Earnings     USDC   2.16754746
2021-07-22 00:00:00  Earnings     USDC   2.16811353
2021-07-23 00:00:00  Earnings     USDC   2.16867975
2021-07-24 00:00:00  Earnings     USDC   2.16924612
2021-07-25 00:00:00  Earnings     USDC   2.16981263
2021-07-26 00:00:00  Earnings     USDC   2.17037930
2021-07-27 00:00:00  Earnings     USDC   2.17094611
2021-07-28 00:00:00  Earnings     USDC   2.17151307
2021-07-29 00:00:00  Earnings     USDC   2.17208018
2021-07-30 00:00:00  Earnings     USDC   2.17264743
2021-07-31 00:00:00  Earnings     USDC   2.17321484
2021-08-01 00:00:00  Earnings     USDC   2.17378239
2021-08-02 00:00:00  Earnings     USDC   2.17435009
2021-08-03 00:00:00  Earnings     USDC   2.17491794
2021-08-04 00:00:00  Earnings     USDC   2.17548593
2021-08-05 00:00:00  Earnings     USDC   2.17605408
2021-08-06 00:00:00  Earnings     USDC   2.17662237
2021-08-07 00:00:00  Earnings     USDC   2.17719081
2021-08-08 00:00:00  Earnings     USDC   2.17775941
2021-08-09 00:00:00  Earnings     USDC   2.17832814
2021-08-10 00:00:00  Earnings     USDC   2.17889703
2021-08-11 00:00:00  Earnings     USDC   2.17946607
2021-08-12 00:00:00  Earnings     USDC   2.18003525
2021-08-13 00:00:00  Earnings     USDC   2.18060459
2021-08-14 00:00:00  Earnings     USDC   2.18117407
2021-08-15 00:00:00  Earnings     USDC   2.18174370
2021-08-16 00:00:00  Earnings     USDC   2.18231348
2021-08-17 00:00:00  Earnings     USDC   2.18288341
2021-08-18 00:00:00  Earnings     USDC   2.18345348
2021-08-19 00:00:00  Earnings     USDC   2.18402371
2021-08-20 00:00:00  Earnings     USDC   2.18459409
2021-08-21 00:00:00  Earnings     USDC   2.18516461
2021-08-22 00:00:00  Earnings     USDC   2.18573528
2021-08-23 00:00:00  Earnings     USDC   2.18630610
2021-08-24 00:00:00  Earnings     USDC   2.18687708
2021-08-25 00:00:00  Earnings     USDC   2.18744820
2021-08-26 00:00:00  Earnings     USDC   2.18801946
2021-08-27 00:00:00  Earnings     USDC   2.18859088
2021-08-28 00:00:00  Earnings     USDC   2.18916245
2021-08-29 00:00:00  Earnings     USDC   2.18973417
2021-08-30 00:00:00  Earnings     USDC   2.19030603
2021-08-31 00:00:00  Earnings     USDC   2.19087805
2021-09-01 00:00:00  Earnings     USDC   2.19145022
2021-09-02 00:00:00  Earnings     USDC   2.19202253
2021-09-03 00:00:00  Earnings     USDC   2.19259499
2021-09-04 00:00:00  Earnings     USDC   2.19316761
2021-09-05 00:00:00  Earnings     USDC   2.19374037
2021-09-06 00:00:00  Earnings     USDC   2.19431328
2021-09-07 00:00:00  Earnings     USDC   2.19488634
2021-09-08 00:00:00  Earnings     USDC   2.19545956
2021-09-09 00:00:00  Earnings     USDC   2.19603292
2021-09-10 00:00:00  Earnings     USDC   2.19660643
2021-09-11 00:00:00  Earnings     USDC   2.19718009
2021-09-12 00:00:00  Earnings     USDC   2.19775390
2021-09-13 00:00:00  Earnings     USDC   2.19832786
2021-09-14 00:00:00  Earnings     USDC   2.19890197
2021-09-15 00:00:00  Earnings     USDC   2.19947623
2021-09-16 00:00:00  Earnings     USDC   2.20005064
2021-09-17 00:00:00  Earnings     USDC   2.20062520
2021-09-18 00:00:00  Earnings     USDC   2.20119992
2021-09-19 00:00:00  Earnings     USDC   2.20177478
2021-09-20 00:00:00  Earnings     USDC   2.20234979
2021-09-21 00:00:00  Earnings     USDC   2.20292495
2021-09-22 00:00:00  Earnings     USDC   2.20350026
2021-09-23 00:00:00  Earnings     USDC   2.20407572
2021-09-24 00:00:00  Earnings     USDC   2.20465133
2021-09-25 00:00:00  Earnings     USDC   2.20522709
2021-09-26 00:00:00  Earnings     USDC   2.20580301
2021-09-27 00:00:00  Earnings     USDC   2.20637907
2021-09-28 00:00:00  Earnings     USDC   2.20695528
2021-09-29 00:00:00  Earnings     USDC   2.20753165
2021-09-30 00:00:00  Earnings     USDC   2.20810816
2021-10-01 00:00:00  Earnings     USDC   2.20868483
2021-10-02 00:00:00  Earnings     USDC   2.20926164
2021-10-03 00:00:00  Earnings     USDC   2.20983861
2021-10-04 00:00:00  Earnings     USDC   2.21041572
2021-10-05 00:00:00  Earnings     USDC   2.21099299
2021-10-06 00:00:00  Earnings     USDC   2.21157041
2021-10-07 00:00:00  Earnings     USDC   2.21214798
2021-10-08 00:00:00  Earnings     USDC   2.21272570
2021-10-09 00:00:00  Earnings     USDC   2.21330357
2021-10-10 00:00:00  Earnings     USDC   2.21388159
2021-10-11 00:00:00  Earnings     USDC   2.21445976
2021-10-12 00:00:00  Earnings     USDC   2.21503809
2021-10-13 00:00:00  Earnings     USDC   2.21561656
2021-10-14 00:00:00  Earnings     USDC   2.21619519
2021-10-15 00:00:00  Earnings     USDC   2.21677396
2021-10-16 00:00:00  Earnings     USDC   2.21735289
2021-10-17 00:00:00  Earnings     USDC   2.21793197
2021-10-18 00:00:00  Earnings     USDC   2.21851120
2021-10-19 00:00:00  Earnings     USDC   2.21909058
2021-10-20 00:00:00  Earnings     USDC   2.21967012
2021-10-21 00:00:00  Earnings     USDC   2.22024980
2021-10-22 00:00:00  Earnings     USDC   2.22082964
2021-10-23 00:00:00  Earnings     USDC   2.22140962
2021-10-24 00:00:00  Earnings     USDC   2.22198976
2021-10-25 00:00:00  Earnings     USDC   2.22257005
2021-10-26 00:00:00  Earnings     USDC   2.22315049
2021-10-27 00:00:00  Earnings     USDC   2.22373109
2021-10-28 00:00:00  Earnings     USDC   2.22431183
2021-10-29 00:00:00  Earnings     USDC   2.22489273
2021-10-30 00:00:00  Earnings     USDC   2.22547378
2021-10-31 00:00:00  Earnings     USDC   2.22605498
2021-11-01 00:00:00  Earnings     USDC   2.22663633
2021-11-02 00:00:00  Earnings     USDC   2.22721783
2021-11-03 00:00:00  Earnings     USDC   2.22779949
2021-11-04 00:00:00  Earnings     USDC   2.22838130
2021-11-05 00:00:00  Earnings     USDC   2.22896325
2021-11-06 00:00:00  Earnings     USDC   2.22954537
2021-11-07 00:00:00  Earnings     USDC   2.23012763
2021-11-08 00:00:00  Earnings     USDC   2.23071004
2021-11-09 00:00:00  Earnings     USDC   2.23129261
2021-11-10 00:00:00  Earnings     USDC   2.23187533
2021-11-11 00:00:00  Earnings     USDC   2.23245820
2021-11-12 00:00:00  Earnings     USDC   2.23304123
2021-11-13 00:00:00  Earnings     USDC   2.23362440
2021-11-14 00:00:00  Earnings     USDC   2.23420773
2021-11-15 00:00:00  Earnings     USDC   2.23479121
2021-11-16 00:00:00  Earnings     USDC   2.23537485
2021-11-17 00:00:00  Earnings     USDC   2.23595863
2021-11-18 00:00:00  Earnings     USDC   2.23654257
2021-11-19 00:00:00  Earnings     USDC   2.23712666
2021-11-20 00:00:00  Earnings     USDC   2.23771090
2021-11-21 00:00:00  Earnings     USDC   2.23829530
2021-11-22 00:00:00  Earnings     USDC   2.23887985
2021-11-23 00:00:00  Earnings     USDC   2.23946455
2021-11-24 00:00:00  Earnings     USDC   2.24004940
2021-11-25 00:00:00  Earnings     USDC   2.24063441
2021-11-26 00:00:00  Earnings     USDC   2.24121957
2021-11-27 00:00:00  Earnings     USDC   2.24180488
2021-11-28 00:00:00  Earnings     USDC   2.24239035
2021-11-29 00:00:00  Earnings     USDC   2.24297596
2021-11-30 00:00:00  Earnings     USDC   2.24356174
2021-12-01 00:00:00  Earnings     USDC   2.24414766
2021-12-02 00:00:00  Earnings     USDC   2.24473374
2021-12-03 00:00:00  Earnings     USDC   2.24531997
2021-12-04 00:00:00  Earnings     USDC   2.24590635
2021-12-05 00:00:00  Earnings     USDC   2.24649289
2021-12-06 00:00:00  Earnings     USDC   2.24707957
2021-12-07 00:00:00  Earnings     USDC   2.24766642
2021-12-08 00:00:00  Earnings     USDC   2.24825341
2021-12-09 00:00:00  Earnings     USDC   2.24884056
2021-12-10 00:00:00  Earnings     USDC   2.24942786
2021-12-11 00:00:00  Earnings     USDC   2.25001532
2021-12-12 00:00:00  Earnings     USDC   2.25060293
2021-12-13 00:00:00  Earnings     USDC   2.25119069
2021-12-14 00:00:00  Earnings     USDC   2.25177861
2021-12-15 00:00:00  Earnings     USDC   2.25236668
2021-12-16 00:00:00  Earnings     USDC   2.25295490
2021-12-17 00:00:00  Earnings     USDC   2.25354328
2021-12-18 00:00:00  Earnings     USDC   2.25413181
2021-12-19 00:00:00  Earnings     USDC   2.25472049
2021-12-20 00:00:00  Earnings     USDC   2.25530933
2021-12-21 00:00:00  Earnings     USDC   2.25589832
2021-12-22 00:00:00  Earnings     USDC   2.25648747
2021-12-23 00:00:00  Earnings     USDC   2.25707677
2021-12-24 00:00:00  Earnings     USDC   2.25766622
2021-12-25 00:00:00  Earnings     USDC   2.25825583
2021-12-26 00:00:00  Earnings     USDC   2.25884559
2021-12-27 00:00:00  Earnings     USDC   2.25943551
2021-12-28 00:00:00  Earnings     USDC   2.26002557
2021-12-29 00:00:00  Earnings     USDC   2.26061580
2021-12-30 00:00:00  Earnings     USDC   2.26120618
2021-12-31 00:00:00  Earnings     USDC   2.26179671
TOTAL                                  660.79363079'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                           DEPOTS/RETRAITS                                                                                 \n' + \
'                     USDC                                              CHF           CAPITAL                    DATE               INTERETS                \n' + \
'        Tot incl intérêts TX DAT DEP   TX ACT PLUS-VAL CAP       P-V CAP %     USDC      CHF          DE           A  JOURS   USDC      CHF INT % INT ANN %\n' + \
'PROPR                                                                                                                                                      ' + \
'''
Béa              4,000.00   4,000.00 3,642.00      -358.00           -8.95 4,000.00 3,642.00  2021-02-20  2021-12-31    315 343.00   312.30  8.57     10.00
TOTAL            4,343.00   4,000.00 3,954.30      -358.00           -8.95                                                  343.00   312.30                ''' + \
'''
JPS              5,000.00   5,000.00 4,552.50      -447.50           -8.95 5,000.00 4,552.50  2021-03-22  2021-04-21     31  40.64    37.00  0.81     10.00
JPS             -1,000.00  -1,200.00  -910.50       289.50           24.12 4,040.64 3,679.00  2021-04-22  2021-12-31    254 277.16   252.35  6.86     10.00
TOTAL            4,317.79   3,800.00 3,931.35      -158.00           -4.16                                                  317.79   289.35                ''' + \
'''
G TOTAL          8,660.79            7,885.65                                                                               660.79   601.65                '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_USDC_2_fiats_simple_values_2_owners_2_deposits_bug_french_language(self):
		"""
		USDC crypto, 2 owners with 2 deposit and 1 withdrawal, fixed yield rate,
		USDC/CHF final rate of 1.5 and USDC/EUR final rate of 1.4
		"""
		PRINT = False

		sbAccountSheetFileName = 'testSBEarningUsdc_simple_values_multi_depwithdr_bug.xlsx'
		depositSheetFileName = 'depositUsdc_fiat_chf_eur_simple_values_depwithdr_bug.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(),
								   self.cryptoFiatCsvFilePathName),
								   language=FR)

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency   Net amount\n' + \
'Local time                                         ' + \
'''
2021-02-20 00:00:00  Earnings     USDC   1.04463150
2021-02-21 00:00:00  Earnings     USDC   1.04490432
2021-02-22 00:00:00  Earnings     USDC   1.04517720
2021-02-23 00:00:00  Earnings     USDC   1.04545016
2021-02-24 00:00:00  Earnings     USDC   1.04572319
2021-02-25 00:00:00  Earnings     USDC   1.04599629
2021-02-26 00:00:00  Earnings     USDC   1.04626946
2021-02-27 00:00:00  Earnings     USDC   1.04654270
2021-02-28 00:00:00  Earnings     USDC   1.04681601
2021-03-01 00:00:00  Earnings     USDC   1.04708939
2021-03-02 00:00:00  Earnings     USDC   1.04736285
2021-03-03 00:00:00  Earnings     USDC   1.04763638
2021-03-04 00:00:00  Earnings     USDC   1.04790998
2021-03-05 00:00:00  Earnings     USDC   1.04818365
2021-03-06 00:00:00  Earnings     USDC   1.04845739
2021-03-07 00:00:00  Earnings     USDC   1.04873120
2021-03-08 00:00:00  Earnings     USDC   1.04900508
2021-03-09 00:00:00  Earnings     USDC   1.04927904
2021-03-10 00:00:00  Earnings     USDC   1.04955307
2021-03-11 00:00:00  Earnings     USDC   1.04982717
2021-03-12 00:00:00  Earnings     USDC   1.05010134
2021-03-13 00:00:00  Earnings     USDC   1.05037558
2021-03-14 00:00:00  Earnings     USDC   1.05064989
2021-03-15 00:00:00  Earnings     USDC   1.05092428
2021-03-16 00:00:00  Earnings     USDC   1.05119874
2021-03-17 00:00:00  Earnings     USDC   1.05147326
2021-03-18 00:00:00  Earnings     USDC   1.05174787
2021-03-19 00:00:00  Earnings     USDC   1.05202254
2021-03-20 00:00:00  Earnings     USDC   1.05229728
2021-03-21 00:00:00  Earnings     USDC   1.05257210
2021-03-22 00:00:00  Earnings     USDC   2.35863637
2021-03-23 00:00:00  Earnings     USDC   2.35925234
2021-03-24 00:00:00  Earnings     USDC   2.35986848
2021-03-25 00:00:00  Earnings     USDC   2.36048478
2021-03-26 00:00:00  Earnings     USDC   2.36110124
2021-03-27 00:00:00  Earnings     USDC   2.36171786
2021-03-28 00:00:00  Earnings     USDC   2.36233464
2021-03-29 00:00:00  Earnings     USDC   2.36295158
2021-03-30 00:00:00  Earnings     USDC   2.36356868
2021-03-31 00:00:00  Earnings     USDC   2.36418595
2021-04-01 00:00:00  Earnings     USDC   2.36480337
2021-04-02 00:00:00  Earnings     USDC   2.36542096
2021-04-03 00:00:00  Earnings     USDC   2.36603871
2021-04-04 00:00:00  Earnings     USDC   2.36665662
2021-04-05 00:00:00  Earnings     USDC   2.36727469
2021-04-06 00:00:00  Earnings     USDC   2.36789292
2021-04-07 00:00:00  Earnings     USDC   2.36851132
2021-04-08 00:00:00  Earnings     USDC   2.36912987
2021-04-09 00:00:00  Earnings     USDC   2.36974859
2021-04-10 00:00:00  Earnings     USDC   2.37036747
2021-04-11 00:00:00  Earnings     USDC   2.37098651
2021-04-12 00:00:00  Earnings     USDC   2.37160571
2021-04-13 00:00:00  Earnings     USDC   2.37222507
2021-04-14 00:00:00  Earnings     USDC   2.37284460
2021-04-15 00:00:00  Earnings     USDC   2.37346428
2021-04-16 00:00:00  Earnings     USDC   2.37408413
2021-04-17 00:00:00  Earnings     USDC   2.37470414
2021-04-18 00:00:00  Earnings     USDC   2.37532432
2021-04-19 00:00:00  Earnings     USDC   2.37594465
2021-04-20 00:00:00  Earnings     USDC   2.37656515
2021-04-21 00:00:00  Earnings     USDC   2.37718581
2021-04-22 00:00:00  Earnings     USDC   2.11664875
2021-04-23 00:00:00  Earnings     USDC   2.11775446
2021-04-24 00:00:00  Earnings     USDC   2.11830752
2021-04-25 00:00:00  Earnings     USDC   2.11886074
2021-04-26 00:00:00  Earnings     USDC   2.11941409
2021-04-27 00:00:00  Earnings     USDC   2.11996760
2021-04-28 00:00:00  Earnings     USDC   2.12052124
2021-04-29 00:00:00  Earnings     USDC   2.12107503
2021-04-30 00:00:00  Earnings     USDC   2.12162897
2021-05-01 00:00:00  Earnings     USDC   2.12218305
2021-05-02 00:00:00  Earnings     USDC   2.12273727
2021-05-03 00:00:00  Earnings     USDC   2.12329164
2021-05-04 00:00:00  Earnings     USDC   2.12384616
2021-05-05 00:00:00  Earnings     USDC   2.12440082
2021-05-06 00:00:00  Earnings     USDC   2.12495562
2021-05-07 00:00:00  Earnings     USDC   2.12551057
2021-05-08 00:00:00  Earnings     USDC   2.12606566
2021-05-09 00:00:00  Earnings     USDC   2.12662090
2021-05-10 00:00:00  Earnings     USDC   2.12717628
2021-05-11 00:00:00  Earnings     USDC   2.12773181
2021-05-12 00:00:00  Earnings     USDC   2.12828749
2021-05-13 00:00:00  Earnings     USDC   2.12884331
2021-05-14 00:00:00  Earnings     USDC   2.12939927
2021-05-15 00:00:00  Earnings     USDC   2.12995538
2021-05-16 00:00:00  Earnings     USDC   2.13051163
2021-05-17 00:00:00  Earnings     USDC   2.13106803
2021-05-18 00:00:00  Earnings     USDC   2.13162458
2021-05-19 00:00:00  Earnings     USDC   2.13218127
2021-05-20 00:00:00  Earnings     USDC   2.13273811
2021-05-21 00:00:00  Earnings     USDC   2.13329509
2021-05-22 00:00:00  Earnings     USDC   2.13385221
2021-05-23 00:00:00  Earnings     USDC   2.13440949
2021-05-24 00:00:00  Earnings     USDC   2.13496690
2021-05-25 00:00:00  Earnings     USDC   2.13552447
2021-05-26 00:00:00  Earnings     USDC   2.13608218
2021-05-27 00:00:00  Earnings     USDC   2.13664003
2021-05-28 00:00:00  Earnings     USDC   2.13719803
2021-05-29 00:00:00  Earnings     USDC   2.13775618
2021-05-30 00:00:00  Earnings     USDC   2.13831447
2021-05-31 00:00:00  Earnings     USDC   2.13887291
2021-06-01 00:00:00  Earnings     USDC   2.13943149
2021-06-02 00:00:00  Earnings     USDC   2.13999022
2021-06-03 00:00:00  Earnings     USDC   2.14054910
2021-06-04 00:00:00  Earnings     USDC   2.14110812
2021-06-05 00:00:00  Earnings     USDC   2.14166728
2021-06-06 00:00:00  Earnings     USDC   2.14222660
2021-06-07 00:00:00  Earnings     USDC   2.14278606
2021-06-08 00:00:00  Earnings     USDC   2.14334566
2021-06-09 00:00:00  Earnings     USDC   2.14390541
2021-06-10 00:00:00  Earnings     USDC   2.14446531
2021-06-11 00:00:00  Earnings     USDC   2.14502536
2021-06-12 00:00:00  Earnings     USDC   2.14558555
2021-06-13 00:00:00  Earnings     USDC   2.14614588
2021-06-14 00:00:00  Earnings     USDC   2.14670637
2021-06-15 00:00:00  Earnings     USDC   2.14726700
2021-06-16 00:00:00  Earnings     USDC   2.14782777
2021-06-17 00:00:00  Earnings     USDC   2.14838869
2021-06-18 00:00:00  Earnings     USDC   2.14894976
2021-06-19 00:00:00  Earnings     USDC   2.14951098
2021-06-20 00:00:00  Earnings     USDC   2.15007234
2021-06-21 00:00:00  Earnings     USDC   2.15063385
2021-06-22 00:00:00  Earnings     USDC   2.15119550
2021-06-23 00:00:00  Earnings     USDC   2.15175730
2021-06-24 00:00:00  Earnings     USDC   2.15231925
2021-06-25 00:00:00  Earnings     USDC   2.15288135
2021-06-26 00:00:00  Earnings     USDC   2.15344359
2021-06-27 00:00:00  Earnings     USDC   2.15400598
2021-06-28 00:00:00  Earnings     USDC   2.15456851
2021-06-29 00:00:00  Earnings     USDC   2.15513120
2021-06-30 00:00:00  Earnings     USDC   2.15569403
2021-07-01 00:00:00  Earnings     USDC   2.15625700
2021-07-02 00:00:00  Earnings     USDC   2.15682013
2021-07-03 00:00:00  Earnings     USDC   2.15738340
2021-07-04 00:00:00  Earnings     USDC   2.15794681
2021-07-05 00:00:00  Earnings     USDC   2.15851038
2021-07-06 00:00:00  Earnings     USDC   2.15907409
2021-07-07 00:00:00  Earnings     USDC   2.15963795
2021-07-08 00:00:00  Earnings     USDC   2.16020196
2021-07-09 00:00:00  Earnings     USDC   2.16076611
2021-07-10 00:00:00  Earnings     USDC   2.16133041
2021-07-11 00:00:00  Earnings     USDC   2.16189486
2021-07-12 00:00:00  Earnings     USDC   2.16245946
2021-07-13 00:00:00  Earnings     USDC   2.16302420
2021-07-14 00:00:00  Earnings     USDC   2.16358909
2021-07-15 00:00:00  Earnings     USDC   2.16415413
2021-07-16 00:00:00  Earnings     USDC   2.16471931
2021-07-17 00:00:00  Earnings     USDC   2.16528465
2021-07-18 00:00:00  Earnings     USDC   2.16585013
2021-07-19 00:00:00  Earnings     USDC   2.16641576
2021-07-20 00:00:00  Earnings     USDC   2.16698153
2021-07-21 00:00:00  Earnings     USDC   2.16754746
2021-07-22 00:00:00  Earnings     USDC   2.16811353
2021-07-23 00:00:00  Earnings     USDC   2.16867975
2021-07-24 00:00:00  Earnings     USDC   2.16924612
2021-07-25 00:00:00  Earnings     USDC   2.16981263
2021-07-26 00:00:00  Earnings     USDC   2.17037930
2021-07-27 00:00:00  Earnings     USDC   2.17094611
2021-07-28 00:00:00  Earnings     USDC   2.17151307
2021-07-29 00:00:00  Earnings     USDC   2.17208018
2021-07-30 00:00:00  Earnings     USDC   2.17264743
2021-07-31 00:00:00  Earnings     USDC   2.17321484
2021-08-01 00:00:00  Earnings     USDC   2.17378239
2021-08-02 00:00:00  Earnings     USDC   2.17435009
2021-08-03 00:00:00  Earnings     USDC   2.17491794
2021-08-04 00:00:00  Earnings     USDC   2.17548593
2021-08-05 00:00:00  Earnings     USDC   2.17605408
2021-08-06 00:00:00  Earnings     USDC   2.17662237
2021-08-07 00:00:00  Earnings     USDC   2.17719081
2021-08-08 00:00:00  Earnings     USDC   2.17775941
2021-08-09 00:00:00  Earnings     USDC   2.17832814
2021-08-10 00:00:00  Earnings     USDC   2.17889703
2021-08-11 00:00:00  Earnings     USDC   2.17946607
2021-08-12 00:00:00  Earnings     USDC   2.18003525
2021-08-13 00:00:00  Earnings     USDC   2.18060459
2021-08-14 00:00:00  Earnings     USDC   2.18117407
2021-08-15 00:00:00  Earnings     USDC   2.18174370
2021-08-16 00:00:00  Earnings     USDC   2.18231348
2021-08-17 00:00:00  Earnings     USDC   2.18288341
2021-08-18 00:00:00  Earnings     USDC   2.18345348
2021-08-19 00:00:00  Earnings     USDC   2.18402371
2021-08-20 00:00:00  Earnings     USDC   2.18459409
2021-08-21 00:00:00  Earnings     USDC   2.18516461
2021-08-22 00:00:00  Earnings     USDC   2.18573528
2021-08-23 00:00:00  Earnings     USDC   2.18630610
2021-08-24 00:00:00  Earnings     USDC   2.18687708
2021-08-25 00:00:00  Earnings     USDC   2.18744820
2021-08-26 00:00:00  Earnings     USDC   2.18801946
2021-08-27 00:00:00  Earnings     USDC   2.18859088
2021-08-28 00:00:00  Earnings     USDC   2.18916245
2021-08-29 00:00:00  Earnings     USDC   2.18973417
2021-08-30 00:00:00  Earnings     USDC   2.19030603
2021-08-31 00:00:00  Earnings     USDC   2.19087805
2021-09-01 00:00:00  Earnings     USDC   2.19145022
2021-09-02 00:00:00  Earnings     USDC   2.19202253
2021-09-03 00:00:00  Earnings     USDC   2.19259499
2021-09-04 00:00:00  Earnings     USDC   2.19316761
2021-09-05 00:00:00  Earnings     USDC   2.19374037
2021-09-06 00:00:00  Earnings     USDC   2.19431328
2021-09-07 00:00:00  Earnings     USDC   2.19488634
2021-09-08 00:00:00  Earnings     USDC   2.19545956
2021-09-09 00:00:00  Earnings     USDC   2.19603292
2021-09-10 00:00:00  Earnings     USDC   2.19660643
2021-09-11 00:00:00  Earnings     USDC   2.19718009
2021-09-12 00:00:00  Earnings     USDC   2.19775390
2021-09-13 00:00:00  Earnings     USDC   2.19832786
2021-09-14 00:00:00  Earnings     USDC   2.19890197
2021-09-15 00:00:00  Earnings     USDC   2.19947623
2021-09-16 00:00:00  Earnings     USDC   2.20005064
2021-09-17 00:00:00  Earnings     USDC   2.20062520
2021-09-18 00:00:00  Earnings     USDC   2.20119992
2021-09-19 00:00:00  Earnings     USDC   2.20177478
2021-09-20 00:00:00  Earnings     USDC   2.20234979
2021-09-21 00:00:00  Earnings     USDC   2.20292495
2021-09-22 00:00:00  Earnings     USDC   2.20350026
2021-09-23 00:00:00  Earnings     USDC   2.20407572
2021-09-24 00:00:00  Earnings     USDC   2.20465133
2021-09-25 00:00:00  Earnings     USDC   2.20522709
2021-09-26 00:00:00  Earnings     USDC   2.20580301
2021-09-27 00:00:00  Earnings     USDC   2.20637907
2021-09-28 00:00:00  Earnings     USDC   2.20695528
2021-09-29 00:00:00  Earnings     USDC   2.20753165
2021-09-30 00:00:00  Earnings     USDC   2.20810816
2021-10-01 00:00:00  Earnings     USDC   2.20868483
2021-10-02 00:00:00  Earnings     USDC   2.20926164
2021-10-03 00:00:00  Earnings     USDC   2.20983861
2021-10-04 00:00:00  Earnings     USDC   2.21041572
2021-10-05 00:00:00  Earnings     USDC   2.21099299
2021-10-06 00:00:00  Earnings     USDC   2.21157041
2021-10-07 00:00:00  Earnings     USDC   2.21214798
2021-10-08 00:00:00  Earnings     USDC   2.21272570
2021-10-09 00:00:00  Earnings     USDC   2.21330357
2021-10-10 00:00:00  Earnings     USDC   2.21388159
2021-10-11 00:00:00  Earnings     USDC   2.21445976
2021-10-12 00:00:00  Earnings     USDC   2.21503809
2021-10-13 00:00:00  Earnings     USDC   2.21561656
2021-10-14 00:00:00  Earnings     USDC   2.21619519
2021-10-15 00:00:00  Earnings     USDC   2.21677396
2021-10-16 00:00:00  Earnings     USDC   2.21735289
2021-10-17 00:00:00  Earnings     USDC   2.21793197
2021-10-18 00:00:00  Earnings     USDC   2.21851120
2021-10-19 00:00:00  Earnings     USDC   2.21909058
2021-10-20 00:00:00  Earnings     USDC   2.21967012
2021-10-21 00:00:00  Earnings     USDC   2.22024980
2021-10-22 00:00:00  Earnings     USDC   2.22082964
2021-10-23 00:00:00  Earnings     USDC   2.22140962
2021-10-24 00:00:00  Earnings     USDC   2.22198976
2021-10-25 00:00:00  Earnings     USDC   2.22257005
2021-10-26 00:00:00  Earnings     USDC   2.22315049
2021-10-27 00:00:00  Earnings     USDC   2.22373109
2021-10-28 00:00:00  Earnings     USDC   2.22431183
2021-10-29 00:00:00  Earnings     USDC   2.22489273
2021-10-30 00:00:00  Earnings     USDC   2.22547378
2021-10-31 00:00:00  Earnings     USDC   2.22605498
2021-11-01 00:00:00  Earnings     USDC   2.22663633
2021-11-02 00:00:00  Earnings     USDC   2.22721783
2021-11-03 00:00:00  Earnings     USDC   2.22779949
2021-11-04 00:00:00  Earnings     USDC   2.22838130
2021-11-05 00:00:00  Earnings     USDC   2.22896325
2021-11-06 00:00:00  Earnings     USDC   2.22954537
2021-11-07 00:00:00  Earnings     USDC   2.23012763
2021-11-08 00:00:00  Earnings     USDC   2.23071004
2021-11-09 00:00:00  Earnings     USDC   2.23129261
2021-11-10 00:00:00  Earnings     USDC   2.23187533
2021-11-11 00:00:00  Earnings     USDC   2.23245820
2021-11-12 00:00:00  Earnings     USDC   2.23304123
2021-11-13 00:00:00  Earnings     USDC   2.23362440
2021-11-14 00:00:00  Earnings     USDC   2.23420773
2021-11-15 00:00:00  Earnings     USDC   2.23479121
2021-11-16 00:00:00  Earnings     USDC   2.23537485
2021-11-17 00:00:00  Earnings     USDC   2.23595863
2021-11-18 00:00:00  Earnings     USDC   2.23654257
2021-11-19 00:00:00  Earnings     USDC   2.23712666
2021-11-20 00:00:00  Earnings     USDC   2.23771090
2021-11-21 00:00:00  Earnings     USDC   2.23829530
2021-11-22 00:00:00  Earnings     USDC   2.23887985
2021-11-23 00:00:00  Earnings     USDC   2.23946455
2021-11-24 00:00:00  Earnings     USDC   2.24004940
2021-11-25 00:00:00  Earnings     USDC   2.24063441
2021-11-26 00:00:00  Earnings     USDC   2.24121957
2021-11-27 00:00:00  Earnings     USDC   2.24180488
2021-11-28 00:00:00  Earnings     USDC   2.24239035
2021-11-29 00:00:00  Earnings     USDC   2.24297596
2021-11-30 00:00:00  Earnings     USDC   2.24356174
2021-12-01 00:00:00  Earnings     USDC   2.24414766
2021-12-02 00:00:00  Earnings     USDC   2.24473374
2021-12-03 00:00:00  Earnings     USDC   2.24531997
2021-12-04 00:00:00  Earnings     USDC   2.24590635
2021-12-05 00:00:00  Earnings     USDC   2.24649289
2021-12-06 00:00:00  Earnings     USDC   2.24707957
2021-12-07 00:00:00  Earnings     USDC   2.24766642
2021-12-08 00:00:00  Earnings     USDC   2.24825341
2021-12-09 00:00:00  Earnings     USDC   2.24884056
2021-12-10 00:00:00  Earnings     USDC   2.24942786
2021-12-11 00:00:00  Earnings     USDC   2.25001532
2021-12-12 00:00:00  Earnings     USDC   2.25060293
2021-12-13 00:00:00  Earnings     USDC   2.25119069
2021-12-14 00:00:00  Earnings     USDC   2.25177861
2021-12-15 00:00:00  Earnings     USDC   2.25236668
2021-12-16 00:00:00  Earnings     USDC   2.25295490
2021-12-17 00:00:00  Earnings     USDC   2.25354328
2021-12-18 00:00:00  Earnings     USDC   2.25413181
2021-12-19 00:00:00  Earnings     USDC   2.25472049
2021-12-20 00:00:00  Earnings     USDC   2.25530933
2021-12-21 00:00:00  Earnings     USDC   2.25589832
2021-12-22 00:00:00  Earnings     USDC   2.25648747
2021-12-23 00:00:00  Earnings     USDC   2.25707677
2021-12-24 00:00:00  Earnings     USDC   2.25766622
2021-12-25 00:00:00  Earnings     USDC   2.25825583
2021-12-26 00:00:00  Earnings     USDC   2.25884559
2021-12-27 00:00:00  Earnings     USDC   2.25943551
2021-12-28 00:00:00  Earnings     USDC   2.26002557
2021-12-29 00:00:00  Earnings     USDC   2.26061580
2021-12-30 00:00:00  Earnings     USDC   2.26120618
2021-12-31 00:00:00  Earnings     USDC   2.26179671
TOTAL                                  660.79363079'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                                                                         DEPOTS/RETRAITS                                                                                                 \n' + \
'                     USDC                                        CHF                                                 EUR                    CAPITAL                    DATE                      INTERETS                \n' + \
'        Tot incl intérêts TX DAT DEP   TX ACT PLUS-VAL CAP P-V CAP %  TX DAT DEP    TX ACT  PLUS-VAL CAP       P-V CAP %     USDC      CHF      EUR          DE           A  JOURS   USDC    CHF      EUR INT % INT ANN %\n' + \
'PROPR                                                                                                                                                                                                                    ' + \
'''
Béa              4,000.00   4,000.00 3,642.00      -358.00     -8.95    2,800.00  5,600.00      2,800.00          100.00 4,000.00 3,642.00 5,600.00  2021-02-20  2021-12-31    315 343.00 312.30   480.20  8.57     10.00
TOTAL            4,343.00   4,000.00 3,954.30      -358.00     -8.95    2,800.00  6,080.20      2,800.00          100.00                                                           343.00 312.30   480.20                ''' + \
'''
JPS              5,000.00   5,000.00 4,552.50      -447.50     -8.95    4,000.00  7,000.00      3,000.00           75.00 5,000.00 4,552.50 7,000.00  2021-03-22  2021-04-21     31  40.64  37.00    56.89  0.81     10.00
JPS             -1,000.00  -1,200.00  -910.50       289.50     24.12   -1,100.00 -1,400.00       -300.00          -27.27 4,040.64 3,679.00 5,656.89  2021-04-22  2021-12-31    254 277.16 252.35   388.02  6.86     10.00
TOTAL            4,317.79   3,800.00 3,931.35      -158.00     -4.16    2,900.00  6,044.91      2,700.00           93.10                                                           317.79 289.35   444.91                ''' + \
'''
G TOTAL          8,660.79            7,885.65                                    12,125.11                                                                                         660.79 601.65   925.11                '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testAddFiatConversionInfo_1_fiat_simple_values_1_owner_max_withdrawal_bug(self):
		"""
		CHSB crypto, 1 owner with 1 withdrawal whic withdraw the maximum
		available amount, fixed yield rate,	CHSB/CHF final rateof 1.5.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner_max_withdrawal.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_max_withdrawal.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency  Net amount\n' + \
'Local time                                        ' + \
'''
2021-01-01 00:00:00  Earnings     CHSB  2.61157876
2021-01-02 00:00:00  Earnings     CHSB  2.61226080
2021-01-03 00:00:00  Earnings     CHSB  2.61294301
2021-01-04 00:00:00  Earnings     CHSB  2.61362540
2021-01-05 00:00:00  Earnings     CHSB  2.61430797
2021-01-06 00:00:00  Earnings     CHSB  2.87614859
2021-01-07 00:00:00  Earnings     CHSB  2.87689972
2021-01-08 00:00:00  Earnings     CHSB  2.87765104
2021-01-09 00:00:00  Earnings     CHSB  2.87840257
2021-01-10 00:00:00  Earnings     CHSB  0.00000100
2021-01-11 00:00:00  Earnings     CHSB  0.00000100
2021-01-12 00:00:00  Earnings     CHSB  0.00000100
2021-01-13 00:00:00  Earnings     CHSB  0.00000100
2021-01-14 00:00:00  Earnings     CHSB  0.00000100
2021-01-15 00:00:00  Earnings     CHSB  0.00000100
2021-01-16 00:00:00  Earnings     CHSB  0.00000100
2021-01-17 00:00:00  Earnings     CHSB  0.00000100
2021-01-18 00:00:00  Earnings     CHSB  0.00000100
2021-01-19 00:00:00  Earnings     CHSB  0.00000100
2021-01-20 00:00:00  Earnings     CHSB  0.00000100
2021-01-21 00:00:00  Earnings     CHSB  0.00000100
2021-01-22 00:00:00  Earnings     CHSB  0.00000100
2021-01-23 00:00:00  Earnings     CHSB  0.00000100
2021-01-24 00:00:00  Earnings     CHSB  0.00000100
2021-01-25 00:00:00  Earnings     CHSB  0.00000100
2021-01-26 00:00:00  Earnings     CHSB  0.00000100
2021-01-27 00:00:00  Earnings     CHSB  0.00000100
2021-01-28 00:00:00  Earnings     CHSB  0.00000100
2021-01-29 00:00:00  Earnings     CHSB  0.00000100
2021-01-30 00:00:00  Earnings     CHSB  0.00000100
2021-01-31 00:00:00  Earnings     CHSB  0.00000100
2021-02-01 00:00:00  Earnings     CHSB  0.00000100
2021-02-02 00:00:00  Earnings     CHSB  0.00000100
2021-02-03 00:00:00  Earnings     CHSB  0.00000100
2021-02-04 00:00:00  Earnings     CHSB  0.00000100
2021-02-05 00:00:00  Earnings     CHSB  0.00000100
2021-02-06 00:00:00  Earnings     CHSB  0.00000100
2021-02-07 00:00:00  Earnings     CHSB  0.00000100
2021-02-08 00:00:00  Earnings     CHSB  0.00000100
2021-02-09 00:00:00  Earnings     CHSB  0.00000101
2021-02-10 00:00:00  Earnings     CHSB  0.00000101
2021-02-11 00:00:00  Earnings     CHSB  0.00000101
2021-02-12 00:00:00  Earnings     CHSB  0.00000101
2021-02-13 00:00:00  Earnings     CHSB  0.00000101
2021-02-14 00:00:00  Earnings     CHSB  0.00000101
2021-02-15 00:00:00  Earnings     CHSB  0.00000101
2021-02-16 00:00:00  Earnings     CHSB  0.00000101
2021-02-17 00:00:00  Earnings     CHSB  0.00000101
2021-02-18 00:00:00  Earnings     CHSB  0.00000101
2021-02-19 00:00:00  Earnings     CHSB  0.00000101
2021-02-20 00:00:00  Earnings     CHSB  0.00000101
2021-02-21 00:00:00  Earnings     CHSB  0.00000101
2021-02-22 00:00:00  Earnings     CHSB  0.00000101
2021-02-23 00:00:00  Earnings     CHSB  0.00000101
2021-02-24 00:00:00  Earnings     CHSB  0.00000101
2021-02-25 00:00:00  Earnings     CHSB  0.00000101
2021-02-26 00:00:00  Earnings     CHSB  0.00000101
2021-02-27 00:00:00  Earnings     CHSB  0.00000101
2021-02-28 00:00:00  Earnings     CHSB  0.00000101
2021-03-01 00:00:00  Earnings     CHSB  0.00000101
2021-03-02 00:00:00  Earnings     CHSB  0.00000101
2021-03-03 00:00:00  Earnings     CHSB  0.00000101
2021-03-04 00:00:00  Earnings     CHSB  0.00000101
2021-03-05 00:00:00  Earnings     CHSB  0.00000101
2021-03-06 00:00:00  Earnings     CHSB  0.00000101
2021-03-07 00:00:00  Earnings     CHSB  0.00000101
2021-03-08 00:00:00  Earnings     CHSB  0.00000101
2021-03-09 00:00:00  Earnings     CHSB  0.00000101
2021-03-10 00:00:00  Earnings     CHSB  0.00000101
2021-03-11 00:00:00  Earnings     CHSB  0.00000101
2021-03-12 00:00:00  Earnings     CHSB  0.00000101
2021-03-13 00:00:00  Earnings     CHSB  0.00000101
2021-03-14 00:00:00  Earnings     CHSB  0.00000101
2021-03-15 00:00:00  Earnings     CHSB  0.00000101
2021-03-16 00:00:00  Earnings     CHSB  0.00000101
2021-03-17 00:00:00  Earnings     CHSB  0.00000101
2021-03-18 00:00:00  Earnings     CHSB  0.00000101
2021-03-19 00:00:00  Earnings     CHSB  0.00000102
2021-03-20 00:00:00  Earnings     CHSB  0.00000102
2021-03-21 00:00:00  Earnings     CHSB  0.00000102
2021-03-22 00:00:00  Earnings     CHSB  0.00000102
2021-03-23 00:00:00  Earnings     CHSB  0.00000102
2021-03-24 00:00:00  Earnings     CHSB  0.00000102
2021-03-25 00:00:00  Earnings     CHSB  0.00000102
2021-03-26 00:00:00  Earnings     CHSB  0.00000102
2021-03-27 00:00:00  Earnings     CHSB  0.00000102
2021-03-28 00:00:00  Earnings     CHSB  0.00000102
2021-03-29 00:00:00  Earnings     CHSB  0.00000102
2021-03-30 00:00:00  Earnings     CHSB  0.00000102
2021-03-31 00:00:00  Earnings     CHSB  0.00000102
2021-04-01 00:00:00  Earnings     CHSB  0.00000102
2021-04-02 00:00:00  Earnings     CHSB  0.00000102
2021-04-03 00:00:00  Earnings     CHSB  0.00000102
2021-04-04 00:00:00  Earnings     CHSB  0.00000102
2021-04-05 00:00:00  Earnings     CHSB  0.00000102
2021-04-06 00:00:00  Earnings     CHSB  0.00000102
2021-04-07 00:00:00  Earnings     CHSB  0.00000102
2021-04-08 00:00:00  Earnings     CHSB  0.00000102
2021-04-09 00:00:00  Earnings     CHSB  0.00000102
2021-04-10 00:00:00  Earnings     CHSB  0.00000102
2021-04-11 00:00:00  Earnings     CHSB  0.00000102
2021-04-12 00:00:00  Earnings     CHSB  0.00000102
2021-04-13 00:00:00  Earnings     CHSB  0.00000102
2021-04-14 00:00:00  Earnings     CHSB  0.00000102
2021-04-15 00:00:00  Earnings     CHSB  0.00000102
2021-04-16 00:00:00  Earnings     CHSB  0.00000102
2021-04-17 00:00:00  Earnings     CHSB  0.00000102
2021-04-18 00:00:00  Earnings     CHSB  0.00000102
2021-04-19 00:00:00  Earnings     CHSB  0.00000102
2021-04-20 00:00:00  Earnings     CHSB  0.00000102
2021-04-21 00:00:00  Earnings     CHSB  0.00000102
2021-04-22 00:00:00  Earnings     CHSB  0.00000102
2021-04-23 00:00:00  Earnings     CHSB  0.00000102
2021-04-24 00:00:00  Earnings     CHSB  0.00000102
2021-04-25 00:00:00  Earnings     CHSB  0.00000103
2021-04-26 00:00:00  Earnings     CHSB  0.00000103
2021-04-27 00:00:00  Earnings     CHSB  0.00000103
2021-04-28 00:00:00  Earnings     CHSB  0.00000103
2021-04-29 00:00:00  Earnings     CHSB  0.00000103
2021-04-30 00:00:00  Earnings     CHSB  0.00000103
2021-05-01 00:00:00  Earnings     CHSB  0.00000103
2021-05-02 00:00:00  Earnings     CHSB  0.00000103
2021-05-03 00:00:00  Earnings     CHSB  0.00000103
2021-05-04 00:00:00  Earnings     CHSB  0.00000103
2021-05-05 00:00:00  Earnings     CHSB  0.00000103
2021-05-06 00:00:00  Earnings     CHSB  0.00000103
2021-05-07 00:00:00  Earnings     CHSB  0.00000103
2021-05-08 00:00:00  Earnings     CHSB  0.00000103
2021-05-09 00:00:00  Earnings     CHSB  0.00000103
2021-05-10 00:00:00  Earnings     CHSB  0.00000103
2021-05-11 00:00:00  Earnings     CHSB  0.00000103
2021-05-12 00:00:00  Earnings     CHSB  0.00000103
2021-05-13 00:00:00  Earnings     CHSB  0.00000103
2021-05-14 00:00:00  Earnings     CHSB  0.00000103
2021-05-15 00:00:00  Earnings     CHSB  0.00000103
2021-05-16 00:00:00  Earnings     CHSB  0.00000103
2021-05-17 00:00:00  Earnings     CHSB  0.00000103
2021-05-18 00:00:00  Earnings     CHSB  0.00000103
2021-05-19 00:00:00  Earnings     CHSB  0.00000103
2021-05-20 00:00:00  Earnings     CHSB  0.00000103
2021-05-21 00:00:00  Earnings     CHSB  0.00000103
2021-05-22 00:00:00  Earnings     CHSB  0.00000103
2021-05-23 00:00:00  Earnings     CHSB  0.00000103
2021-05-24 00:00:00  Earnings     CHSB  0.00000103
2021-05-25 00:00:00  Earnings     CHSB  0.00000103
2021-05-26 00:00:00  Earnings     CHSB  0.00000103
2021-05-27 00:00:00  Earnings     CHSB  0.00000103
2021-05-28 00:00:00  Earnings     CHSB  0.00000103
2021-05-29 00:00:00  Earnings     CHSB  0.00000103
2021-05-30 00:00:00  Earnings     CHSB  0.00000103
2021-05-31 00:00:00  Earnings     CHSB  0.00000103
2021-06-01 00:00:00  Earnings     CHSB  0.00000103
2021-06-02 00:00:00  Earnings     CHSB  0.00000104
2021-06-03 00:00:00  Earnings     CHSB  0.00000104
2021-06-04 00:00:00  Earnings     CHSB  0.00000104
2021-06-05 00:00:00  Earnings     CHSB  0.00000104
2021-06-06 00:00:00  Earnings     CHSB  0.00000104
2021-06-07 00:00:00  Earnings     CHSB  0.00000104
2021-06-08 00:00:00  Earnings     CHSB  0.00000104
2021-06-09 00:00:00  Earnings     CHSB  0.00000104
2021-06-10 00:00:00  Earnings     CHSB  0.00000104
2021-06-11 00:00:00  Earnings     CHSB  0.00000104
2021-06-12 00:00:00  Earnings     CHSB  0.00000104
2021-06-13 00:00:00  Earnings     CHSB  0.00000104
2021-06-14 00:00:00  Earnings     CHSB  0.00000104
2021-06-15 00:00:00  Earnings     CHSB  0.00000104
2021-06-16 00:00:00  Earnings     CHSB  0.00000104
2021-06-17 00:00:00  Earnings     CHSB  0.00000104
2021-06-18 00:00:00  Earnings     CHSB  0.00000104
2021-06-19 00:00:00  Earnings     CHSB  0.00000104
2021-06-20 00:00:00  Earnings     CHSB  0.00000104
2021-06-21 00:00:00  Earnings     CHSB  0.00000104
2021-06-22 00:00:00  Earnings     CHSB  0.00000104
2021-06-23 00:00:00  Earnings     CHSB  0.00000104
2021-06-24 00:00:00  Earnings     CHSB  0.00000104
2021-06-25 00:00:00  Earnings     CHSB  0.00000104
2021-06-26 00:00:00  Earnings     CHSB  0.00000104
2021-06-27 00:00:00  Earnings     CHSB  0.00000104
2021-06-28 00:00:00  Earnings     CHSB  0.00000104
2021-06-29 00:00:00  Earnings     CHSB  0.00000104
2021-06-30 00:00:00  Earnings     CHSB  0.00000104
2021-07-01 00:00:00  Earnings     CHSB  0.00000104
2021-07-02 00:00:00  Earnings     CHSB  0.00000104
2021-07-03 00:00:00  Earnings     CHSB  0.00000104
2021-07-04 00:00:00  Earnings     CHSB  0.00000104
2021-07-05 00:00:00  Earnings     CHSB  0.00000104
2021-07-06 00:00:00  Earnings     CHSB  0.00000104
2021-07-07 00:00:00  Earnings     CHSB  0.00000104
2021-07-08 00:00:00  Earnings     CHSB  0.00000105
2021-07-09 00:00:00  Earnings     CHSB  0.00000105
2021-07-10 00:00:00  Earnings     CHSB  0.00000105
2021-07-11 00:00:00  Earnings     CHSB  0.00000105
2021-07-12 00:00:00  Earnings     CHSB  0.00000105
2021-07-13 00:00:00  Earnings     CHSB  0.00000105
2021-07-14 00:00:00  Earnings     CHSB  0.00000105
2021-07-15 00:00:00  Earnings     CHSB  0.00000105
2021-07-16 00:00:00  Earnings     CHSB  0.00000105
2021-07-17 00:00:00  Earnings     CHSB  0.00000105
2021-07-18 00:00:00  Earnings     CHSB  0.00000105
2021-07-19 00:00:00  Earnings     CHSB  0.00000105
2021-07-20 00:00:00  Earnings     CHSB  0.00000105
2021-07-21 00:00:00  Earnings     CHSB  0.00000105
2021-07-22 00:00:00  Earnings     CHSB  0.00000105
2021-07-23 00:00:00  Earnings     CHSB  0.00000105
2021-07-24 00:00:00  Earnings     CHSB  0.00000105
2021-07-25 00:00:00  Earnings     CHSB  0.00000105
2021-07-26 00:00:00  Earnings     CHSB  0.00000105
2021-07-27 00:00:00  Earnings     CHSB  0.00000105
2021-07-28 00:00:00  Earnings     CHSB  0.00000105
2021-07-29 00:00:00  Earnings     CHSB  0.00000105
2021-07-30 00:00:00  Earnings     CHSB  0.00000105
2021-07-31 00:00:00  Earnings     CHSB  0.00000105
2021-08-01 00:00:00  Earnings     CHSB  0.00000105
2021-08-02 00:00:00  Earnings     CHSB  0.00000105
2021-08-03 00:00:00  Earnings     CHSB  0.00000105
2021-08-04 00:00:00  Earnings     CHSB  0.00000105
2021-08-05 00:00:00  Earnings     CHSB  0.00000105
2021-08-06 00:00:00  Earnings     CHSB  0.00000105
2021-08-07 00:00:00  Earnings     CHSB  0.00000105
2021-08-08 00:00:00  Earnings     CHSB  0.00000105
2021-08-09 00:00:00  Earnings     CHSB  0.00000105
2021-08-10 00:00:00  Earnings     CHSB  0.00000105
2021-08-11 00:00:00  Earnings     CHSB  0.00000105
2021-08-12 00:00:00  Earnings     CHSB  0.00000105
2021-08-13 00:00:00  Earnings     CHSB  0.00000105
2021-08-14 00:00:00  Earnings     CHSB  0.00000106
2021-08-15 00:00:00  Earnings     CHSB  0.00000106
2021-08-16 00:00:00  Earnings     CHSB  0.00000106
2021-08-17 00:00:00  Earnings     CHSB  0.00000106
2021-08-18 00:00:00  Earnings     CHSB  0.00000106
2021-08-19 00:00:00  Earnings     CHSB  0.00000106
2021-08-20 00:00:00  Earnings     CHSB  0.00000106
2021-08-21 00:00:00  Earnings     CHSB  0.00000106
2021-08-22 00:00:00  Earnings     CHSB  0.00000106
2021-08-23 00:00:00  Earnings     CHSB  0.00000106
2021-08-24 00:00:00  Earnings     CHSB  0.00000106
2021-08-25 00:00:00  Earnings     CHSB  0.00000106
2021-08-26 00:00:00  Earnings     CHSB  0.00000106
2021-08-27 00:00:00  Earnings     CHSB  0.00000106
2021-08-28 00:00:00  Earnings     CHSB  0.00000106
2021-08-29 00:00:00  Earnings     CHSB  0.00000106
2021-08-30 00:00:00  Earnings     CHSB  0.00000106
2021-08-31 00:00:00  Earnings     CHSB  0.00000106
2021-09-01 00:00:00  Earnings     CHSB  0.00000106
2021-09-02 00:00:00  Earnings     CHSB  0.00000106
2021-09-03 00:00:00  Earnings     CHSB  0.00000106
2021-09-04 00:00:00  Earnings     CHSB  0.00000106
2021-09-05 00:00:00  Earnings     CHSB  0.00000106
2021-09-06 00:00:00  Earnings     CHSB  0.00000106
2021-09-07 00:00:00  Earnings     CHSB  0.00000106
2021-09-08 00:00:00  Earnings     CHSB  0.00000106
2021-09-09 00:00:00  Earnings     CHSB  0.00000106
2021-09-10 00:00:00  Earnings     CHSB  0.00000106
2021-09-11 00:00:00  Earnings     CHSB  0.00000106
2021-09-12 00:00:00  Earnings     CHSB  0.00000106
2021-09-13 00:00:00  Earnings     CHSB  0.00000106
2021-09-14 00:00:00  Earnings     CHSB  0.00000106
2021-09-15 00:00:00  Earnings     CHSB  0.00000106
2021-09-16 00:00:00  Earnings     CHSB  0.00000106
2021-09-17 00:00:00  Earnings     CHSB  0.00000106
2021-09-18 00:00:00  Earnings     CHSB  0.00000106
2021-09-19 00:00:00  Earnings     CHSB  0.00000107
2021-09-20 00:00:00  Earnings     CHSB  0.00000107
2021-09-21 00:00:00  Earnings     CHSB  0.00000107
2021-09-22 00:00:00  Earnings     CHSB  0.00000107
2021-09-23 00:00:00  Earnings     CHSB  0.00000107
2021-09-24 00:00:00  Earnings     CHSB  0.00000107
2021-09-25 00:00:00  Earnings     CHSB  0.00000107
2021-09-26 00:00:00  Earnings     CHSB  0.00000107
2021-09-27 00:00:00  Earnings     CHSB  0.00000107
2021-09-28 00:00:00  Earnings     CHSB  0.00000107
2021-09-29 00:00:00  Earnings     CHSB  0.00000107
2021-09-30 00:00:00  Earnings     CHSB  0.00000107
2021-10-01 00:00:00  Earnings     CHSB  0.00000107
2021-10-02 00:00:00  Earnings     CHSB  0.00000107
2021-10-03 00:00:00  Earnings     CHSB  0.00000107
2021-10-04 00:00:00  Earnings     CHSB  0.00000107
2021-10-05 00:00:00  Earnings     CHSB  0.00000107
2021-10-06 00:00:00  Earnings     CHSB  0.00000107
2021-10-07 00:00:00  Earnings     CHSB  0.00000107
2021-10-08 00:00:00  Earnings     CHSB  0.00000107
2021-10-09 00:00:00  Earnings     CHSB  0.00000107
2021-10-10 00:00:00  Earnings     CHSB  0.00000107
2021-10-11 00:00:00  Earnings     CHSB  0.00000107
2021-10-12 00:00:00  Earnings     CHSB  0.00000107
2021-10-13 00:00:00  Earnings     CHSB  0.00000107
2021-10-14 00:00:00  Earnings     CHSB  0.00000107
2021-10-15 00:00:00  Earnings     CHSB  0.00000107
2021-10-16 00:00:00  Earnings     CHSB  0.00000107
2021-10-17 00:00:00  Earnings     CHSB  0.00000107
2021-10-18 00:00:00  Earnings     CHSB  0.00000107
2021-10-19 00:00:00  Earnings     CHSB  0.00000107
2021-10-20 00:00:00  Earnings     CHSB  0.00000107
2021-10-21 00:00:00  Earnings     CHSB  0.00000107
2021-10-22 00:00:00  Earnings     CHSB  0.00000107
2021-10-23 00:00:00  Earnings     CHSB  0.00000107
2021-10-24 00:00:00  Earnings     CHSB  0.00000107
2021-10-25 00:00:00  Earnings     CHSB  0.00000108
2021-10-26 00:00:00  Earnings     CHSB  0.00000108
2021-10-27 00:00:00  Earnings     CHSB  0.00000108
2021-10-28 00:00:00  Earnings     CHSB  0.00000108
2021-10-29 00:00:00  Earnings     CHSB  0.00000108
2021-10-30 00:00:00  Earnings     CHSB  0.00000108
2021-10-31 00:00:00  Earnings     CHSB  0.00000108
2021-11-01 00:00:00  Earnings     CHSB  0.00000108
2021-11-02 00:00:00  Earnings     CHSB  0.00000108
2021-11-03 00:00:00  Earnings     CHSB  0.00000108
2021-11-04 00:00:00  Earnings     CHSB  0.00000108
2021-11-05 00:00:00  Earnings     CHSB  0.00000108
2021-11-06 00:00:00  Earnings     CHSB  0.00000108
2021-11-07 00:00:00  Earnings     CHSB  0.00000108
2021-11-08 00:00:00  Earnings     CHSB  0.00000108
2021-11-09 00:00:00  Earnings     CHSB  0.00000108
2021-11-10 00:00:00  Earnings     CHSB  0.00000108
2021-11-11 00:00:00  Earnings     CHSB  0.00000108
2021-11-12 00:00:00  Earnings     CHSB  0.00000108
2021-11-13 00:00:00  Earnings     CHSB  0.00000108
2021-11-14 00:00:00  Earnings     CHSB  0.00000108
2021-11-15 00:00:00  Earnings     CHSB  0.00000108
2021-11-16 00:00:00  Earnings     CHSB  0.00000108
2021-11-17 00:00:00  Earnings     CHSB  0.00000108
2021-11-18 00:00:00  Earnings     CHSB  0.00000108
2021-11-19 00:00:00  Earnings     CHSB  0.00000108
2021-11-20 00:00:00  Earnings     CHSB  0.00000108
2021-11-21 00:00:00  Earnings     CHSB  0.00000108
2021-11-22 00:00:00  Earnings     CHSB  0.00000108
2021-11-23 00:00:00  Earnings     CHSB  0.00000108
2021-11-24 00:00:00  Earnings     CHSB  0.00000108
2021-11-25 00:00:00  Earnings     CHSB  0.00000108
2021-11-26 00:00:00  Earnings     CHSB  0.00000108
2021-11-27 00:00:00  Earnings     CHSB  0.00000108
2021-11-28 00:00:00  Earnings     CHSB  0.00000108
2021-11-29 00:00:00  Earnings     CHSB  0.00000109
2021-11-30 00:00:00  Earnings     CHSB  0.00000109
2021-12-01 00:00:00  Earnings     CHSB  0.00000109
2021-12-02 00:00:00  Earnings     CHSB  0.00000109
2021-12-03 00:00:00  Earnings     CHSB  0.00000109
2021-12-04 00:00:00  Earnings     CHSB  0.00000109
2021-12-05 00:00:00  Earnings     CHSB  0.00000109
2021-12-06 00:00:00  Earnings     CHSB  0.00000109
2021-12-07 00:00:00  Earnings     CHSB  0.00000109
2021-12-08 00:00:00  Earnings     CHSB  0.00000109
2021-12-09 00:00:00  Earnings     CHSB  0.00000109
2021-12-10 00:00:00  Earnings     CHSB  0.00000109
2021-12-11 00:00:00  Earnings     CHSB  0.00000109
2021-12-12 00:00:00  Earnings     CHSB  0.00000109
2021-12-13 00:00:00  Earnings     CHSB  0.00000109
2021-12-14 00:00:00  Earnings     CHSB  0.00000109
2021-12-15 00:00:00  Earnings     CHSB  0.00000109
2021-12-16 00:00:00  Earnings     CHSB  0.00000109
2021-12-17 00:00:00  Earnings     CHSB  0.00000109
2021-12-18 00:00:00  Earnings     CHSB  0.00000109
2021-12-19 00:00:00  Earnings     CHSB  0.00000109
2021-12-20 00:00:00  Earnings     CHSB  0.00000109
2021-12-21 00:00:00  Earnings     CHSB  0.00000109
2021-12-22 00:00:00  Earnings     CHSB  0.00000109
2021-12-23 00:00:00  Earnings     CHSB  0.00000109
2021-12-24 00:00:00  Earnings     CHSB  0.00000109
2021-12-25 00:00:00  Earnings     CHSB  0.00000109
2021-12-26 00:00:00  Earnings     CHSB  0.00000109
2021-12-27 00:00:00  Earnings     CHSB  0.00000109
2021-12-28 00:00:00  Earnings     CHSB  0.00000109
2021-12-29 00:00:00  Earnings     CHSB  0.00000109
2021-12-30 00:00:00  Earnings     CHSB  0.00000109
2021-12-31 00:00:00  Earnings     CHSB  0.00000109
TOTAL                                  24.57418987'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.maxDiff=None
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                       DEP/WITHDR                                                                         \n' + \
'                  CHSB                                        CHF             CAPITAL                    DATE            YIELD            \n' + \
'        Tot incl yield    DF RATE   CUR RATE  CAP GAIN CAP GAIN %      CHSB       CHF        FROM          TO DAYS  CHSB   CHF  Y % YR Y %\n' + \
'OWNER                                                                                                                                     ' + \
'''
JPS          10,000.00   5,000.00  15,000.00 10,000.00     200.00 10,000.00 15,000.00  2021-01-01  2021-01-05    5 13.06 19.60 0.13  10.00
JPS           1,000.00   1,000.00   1,500.00    500.00      50.00 11,013.06 16,519.60  2021-01-06  2021-01-09    4 11.51 17.26 0.10  10.00
JPS         -11,024.57 -22,036.85 -16,536.85  5,500.00      24.96      0.00      0.01  2021-01-10  2021-12-31  356  0.00  0.00 9.74  10.00
TOTAL             0.00 -16,036.85       0.01 16,000.00     -99.77                                                  24.57 36.86            ''' + \
'''
G TOTAL           0.00                  0.01                                                                       24.57 36.86            '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

	def testDepositChsb_fiat_chf_pandas_avg_rate_explore(self):
		"""
		CHSB crypto, 1 owner with 1 withdrawal whic withdraw the maximum
		available amount, fixed yield rate,	CHSB/CHF final rateof 1.5.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositChsb_fiat_chf_pandas_avg_rate_explore.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_pandas_avg_rate_explore.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(), self.cryptoFiatCsvFilePathName))

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
		sbEarningsTotalDfExpectedStr = \
'                         Type Currency     Net amount\n' + \
'Local time                                           ' + \
'''
2021-01-01 00:00:00  Earnings     CHSB     2.61157876
2021-01-02 00:00:00  Earnings     CHSB     2.61226080
2021-01-03 00:00:00  Earnings     CHSB     2.61294301
2021-01-04 00:00:00  Earnings     CHSB     2.61362540
2021-01-05 00:00:00  Earnings     CHSB     2.61430797
2021-01-06 00:00:00  Earnings     CHSB     2.61499071
2021-01-07 00:00:00  Earnings     CHSB     2.61567364
2021-01-08 00:00:00  Earnings     CHSB     2.61635674
2021-01-09 00:00:00  Earnings     CHSB     2.61704003
2021-01-10 00:00:00  Earnings     CHSB     2.61772349
2021-01-11 00:00:00  Earnings     CHSB     2.61840713
2021-01-12 00:00:00  Earnings     CHSB     2.61909094
2021-01-13 00:00:00  Earnings     CHSB     2.61977494
2021-01-14 00:00:00  Earnings     CHSB     2.62045911
2021-01-15 00:00:00  Earnings     CHSB     2.62114347
2021-01-16 00:00:00  Earnings     CHSB     2.62182800
2021-01-17 00:00:00  Earnings     CHSB     2.62251271
2021-01-18 00:00:00  Earnings     CHSB     2.62319760
2021-01-19 00:00:00  Earnings     CHSB     2.62388267
2021-01-20 00:00:00  Earnings     CHSB     2.62456792
2021-01-21 00:00:00  Earnings     CHSB     2.62525334
2021-01-22 00:00:00  Earnings     CHSB     2.62593895
2021-01-23 00:00:00  Earnings     CHSB     2.62662473
2021-01-24 00:00:00  Earnings     CHSB     2.62731070
2021-01-25 00:00:00  Earnings     CHSB     2.62799684
2021-01-26 00:00:00  Earnings     CHSB     2.62868316
2021-01-27 00:00:00  Earnings     CHSB     2.62936966
2021-01-28 00:00:00  Earnings     CHSB     2.63005634
2021-01-29 00:00:00  Earnings     CHSB     2.63074320
2021-01-30 00:00:00  Earnings     CHSB     2.63143024
2021-01-31 00:00:00  Earnings     CHSB     2.63211746
2021-02-01 00:00:00  Earnings     CHSB     2.63280486
2021-02-02 00:00:00  Earnings     CHSB     2.63349244
2021-02-03 00:00:00  Earnings     CHSB     2.63418020
2021-02-04 00:00:00  Earnings     CHSB     2.63486813
2021-02-05 00:00:00  Earnings     CHSB     2.63555625
2021-02-06 00:00:00  Earnings     CHSB     2.63624455
2021-02-07 00:00:00  Earnings     CHSB     2.63693302
2021-02-08 00:00:00  Earnings     CHSB     2.63762168
2021-02-09 00:00:00  Earnings     CHSB     2.63831051
2021-02-10 00:00:00  Earnings     CHSB     2.63899953
2021-02-11 00:00:00  Earnings     CHSB     2.63968872
2021-02-12 00:00:00  Earnings     CHSB     2.64037810
2021-02-13 00:00:00  Earnings     CHSB     2.64106765
2021-02-14 00:00:00  Earnings     CHSB     2.64175739
2021-02-15 00:00:00  Earnings     CHSB     2.64244731
2021-02-16 00:00:00  Earnings     CHSB     2.64313740
2021-02-17 00:00:00  Earnings     CHSB     2.64382768
2021-02-18 00:00:00  Earnings     CHSB     2.64451813
2021-02-19 00:00:00  Earnings     CHSB     2.64520877
2021-02-20 00:00:00  Earnings     CHSB     2.64589959
2021-02-21 00:00:00  Earnings     CHSB     2.64659059
2021-02-22 00:00:00  Earnings     CHSB     2.64728176
2021-02-23 00:00:00  Earnings     CHSB     2.64797312
2021-02-24 00:00:00  Earnings     CHSB     2.64866466
2021-02-25 00:00:00  Earnings     CHSB     2.64935638
2021-02-26 00:00:00  Earnings     CHSB     2.65004828
2021-02-27 00:00:00  Earnings     CHSB     2.65074036
2021-02-28 00:00:00  Earnings     CHSB     2.65143262
2021-03-01 00:00:00  Earnings     CHSB     5.26370383
2021-03-02 00:00:00  Earnings     CHSB     5.26507849
2021-03-03 00:00:00  Earnings     CHSB     5.26645350
2021-03-04 00:00:00  Earnings     CHSB     5.26782888
2021-03-05 00:00:00  Earnings     CHSB     5.26920461
2021-03-06 00:00:00  Earnings     CHSB     5.27058071
2021-03-07 00:00:00  Earnings     CHSB     5.27195716
2021-03-08 00:00:00  Earnings     CHSB     5.27333397
2021-03-09 00:00:00  Earnings     CHSB     5.27471115
2021-03-10 00:00:00  Earnings     CHSB     5.27608868
2021-03-11 00:00:00  Earnings     CHSB     5.27746657
2021-03-12 00:00:00  Earnings     CHSB     5.27884482
2021-03-13 00:00:00  Earnings     CHSB     5.28022343
2021-03-14 00:00:00  Earnings     CHSB     5.28160241
2021-03-15 00:00:00  Earnings     CHSB     5.28298174
2021-03-16 00:00:00  Earnings     CHSB     5.28436143
2021-03-17 00:00:00  Earnings     CHSB     5.28574148
2021-03-18 00:00:00  Earnings     CHSB     5.28712190
2021-03-19 00:00:00  Earnings     CHSB     5.28850267
2021-03-20 00:00:00  Earnings     CHSB     5.28988380
2021-03-21 00:00:00  Earnings     CHSB     5.29126530
2021-03-22 00:00:00  Earnings     CHSB     5.29264715
2021-03-23 00:00:00  Earnings     CHSB     5.29402937
2021-03-24 00:00:00  Earnings     CHSB     5.29541195
2021-03-25 00:00:00  Earnings     CHSB     5.29679489
2021-03-26 00:00:00  Earnings     CHSB     5.29817819
2021-03-27 00:00:00  Earnings     CHSB     5.29956185
2021-03-28 00:00:00  Earnings     CHSB     5.30094587
2021-03-29 00:00:00  Earnings     CHSB     5.30233025
2021-03-30 00:00:00  Earnings     CHSB     5.30371500
2021-03-31 00:00:00  Earnings     CHSB     5.30510011
2021-04-01 00:00:00  Earnings     CHSB     5.56764345
2021-04-02 00:00:00  Earnings     CHSB     5.56909749
2021-04-03 00:00:00  Earnings     CHSB     5.57055190
2021-04-04 00:00:00  Earnings     CHSB     5.57200669
2021-04-05 00:00:00  Earnings     CHSB     5.57346187
2021-04-06 00:00:00  Earnings     CHSB     5.57491742
2021-04-07 00:00:00  Earnings     CHSB     5.57637335
2021-04-08 00:00:00  Earnings     CHSB     5.57782967
2021-04-09 00:00:00  Earnings     CHSB     5.57928636
2021-04-10 00:00:00  Earnings     CHSB     5.58074344
2021-04-11 00:00:00  Earnings     CHSB     5.58220089
2021-04-12 00:00:00  Earnings     CHSB     5.58365873
2021-04-13 00:00:00  Earnings     CHSB     5.58511694
2021-04-14 00:00:00  Earnings     CHSB     5.58657554
2021-04-15 00:00:00  Earnings     CHSB     5.58803452
2021-04-16 00:00:00  Earnings     CHSB     5.58949388
2021-04-17 00:00:00  Earnings     CHSB     5.59095362
2021-04-18 00:00:00  Earnings     CHSB     5.59241374
2021-04-19 00:00:00  Earnings     CHSB     5.59387424
2021-04-20 00:00:00  Earnings     CHSB     5.59533513
2021-04-21 00:00:00  Earnings     CHSB     5.59679639
2021-04-22 00:00:00  Earnings     CHSB     5.59825804
2021-04-23 00:00:00  Earnings     CHSB     5.59972007
2021-04-24 00:00:00  Earnings     CHSB     5.60118248
2021-04-25 00:00:00  Earnings     CHSB     5.60264527
2021-04-26 00:00:00  Earnings     CHSB     5.60410845
2021-04-27 00:00:00  Earnings     CHSB     5.60557200
2021-04-28 00:00:00  Earnings     CHSB     5.60703594
2021-04-29 00:00:00  Earnings     CHSB     5.60850027
2021-04-30 00:00:00  Earnings     CHSB     5.60996497
2021-05-01 00:00:00  Earnings     CHSB     5.48085112
2021-05-02 00:00:00  Earnings     CHSB     5.48371423
2021-05-03 00:00:00  Earnings     CHSB     5.48514634
2021-05-04 00:00:00  Earnings     CHSB     5.48657883
2021-05-05 00:00:00  Earnings     CHSB     5.48801169
2021-05-06 00:00:00  Earnings     CHSB     5.48944493
2021-05-07 00:00:00  Earnings     CHSB     5.49087854
2021-05-08 00:00:00  Earnings     CHSB     5.49231253
2021-05-09 00:00:00  Earnings     CHSB     5.49374689
2021-05-10 00:00:00  Earnings     CHSB     5.49518163
2021-05-11 00:00:00  Earnings     CHSB     5.49661674
2021-05-12 00:00:00  Earnings     CHSB     5.49805222
2021-05-13 00:00:00  Earnings     CHSB     5.49948808
2021-05-14 00:00:00  Earnings     CHSB     5.50092431
2021-05-15 00:00:00  Earnings     CHSB     5.50236092
2021-05-16 00:00:00  Earnings     CHSB     5.50379791
2021-05-17 00:00:00  Earnings     CHSB     5.50523527
2021-05-18 00:00:00  Earnings     CHSB     5.50667301
2021-05-19 00:00:00  Earnings     CHSB     5.50811112
2021-05-20 00:00:00  Earnings     CHSB     5.50954960
2021-05-21 00:00:00  Earnings     CHSB     5.51098847
2021-05-22 00:00:00  Earnings     CHSB     5.51242770
2021-05-23 00:00:00  Earnings     CHSB     5.51386732
2021-05-24 00:00:00  Earnings     CHSB     5.51530731
2021-05-25 00:00:00  Earnings     CHSB     5.51674767
2021-05-26 00:00:00  Earnings     CHSB     5.51818841
2021-05-27 00:00:00  Earnings     CHSB     5.51962953
2021-05-28 00:00:00  Earnings     CHSB     5.52107103
2021-05-29 00:00:00  Earnings     CHSB     5.52251290
2021-05-30 00:00:00  Earnings     CHSB     5.52395515
2021-05-31 00:00:00  Earnings     CHSB     5.52539777
2021-06-01 00:00:00  Earnings     CHSB     5.39626183
2021-06-02 00:00:00  Earnings     CHSB     5.39908076
2021-06-03 00:00:00  Earnings     CHSB     5.40049077
2021-06-04 00:00:00  Earnings     CHSB     5.40190115
2021-06-05 00:00:00  Earnings     CHSB     5.40331190
2021-06-06 00:00:00  Earnings     CHSB     5.40472301
2021-06-07 00:00:00  Earnings     CHSB     5.40613450
2021-06-08 00:00:00  Earnings     CHSB     5.40754636
2021-06-09 00:00:00  Earnings     CHSB     5.40895858
2021-06-10 00:00:00  Earnings     CHSB     5.41037117
2021-06-11 00:00:00  Earnings     CHSB     5.41178413
2021-06-12 00:00:00  Earnings     CHSB     5.41319746
2021-06-13 00:00:00  Earnings     CHSB     5.41461116
2021-06-14 00:00:00  Earnings     CHSB     5.41602523
2021-06-15 00:00:00  Earnings     CHSB     5.41743967
2021-06-16 00:00:00  Earnings     CHSB     5.41885447
2021-06-17 00:00:00  Earnings     CHSB     5.42026965
2021-06-18 00:00:00  Earnings     CHSB     5.42168520
2021-06-19 00:00:00  Earnings     CHSB     5.42310111
2021-06-20 00:00:00  Earnings     CHSB     5.42451740
2021-06-21 00:00:00  Earnings     CHSB     5.42593405
2021-06-22 00:00:00  Earnings     CHSB     5.42735108
2021-06-23 00:00:00  Earnings     CHSB     5.42876847
2021-06-24 00:00:00  Earnings     CHSB     5.43018624
2021-06-25 00:00:00  Earnings     CHSB     5.43160438
2021-06-26 00:00:00  Earnings     CHSB     5.43302288
2021-06-27 00:00:00  Earnings     CHSB     5.43444176
2021-06-28 00:00:00  Earnings     CHSB     5.43586101
2021-06-29 00:00:00  Earnings     CHSB     5.43728062
2021-06-30 00:00:00  Earnings     CHSB     5.43870061
2021-07-01 00:00:00  Earnings     CHSB     5.70127885
2021-07-02 00:00:00  Earnings     CHSB     5.70276778
2021-07-03 00:00:00  Earnings     CHSB     5.70425710
2021-07-04 00:00:00  Earnings     CHSB     5.70574682
2021-07-05 00:00:00  Earnings     CHSB     5.70723692
2021-07-06 00:00:00  Earnings     CHSB     5.70872741
2021-07-07 00:00:00  Earnings     CHSB     5.71021829
2021-07-08 00:00:00  Earnings     CHSB     5.71170955
2021-07-09 00:00:00  Earnings     CHSB     5.71320121
2021-07-10 00:00:00  Earnings     CHSB     5.71469326
2021-07-11 00:00:00  Earnings     CHSB     5.71618570
2021-07-12 00:00:00  Earnings     CHSB     5.71767852
2021-07-13 00:00:00  Earnings     CHSB     5.71917174
2021-07-14 00:00:00  Earnings     CHSB     5.72066535
2021-07-15 00:00:00  Earnings     CHSB     5.72215934
2021-07-16 00:00:00  Earnings     CHSB     5.72365373
2021-07-17 00:00:00  Earnings     CHSB     5.72514851
2021-07-18 00:00:00  Earnings     CHSB     5.72664368
2021-07-19 00:00:00  Earnings     CHSB     5.72813923
2021-07-20 00:00:00  Earnings     CHSB     5.72963518
2021-07-21 00:00:00  Earnings     CHSB     5.73113152
2021-07-22 00:00:00  Earnings     CHSB     5.73262825
2021-07-23 00:00:00  Earnings     CHSB     5.73412537
2021-07-24 00:00:00  Earnings     CHSB     5.73562289
2021-07-25 00:00:00  Earnings     CHSB     5.73712079
2021-07-26 00:00:00  Earnings     CHSB     5.73861908
2021-07-27 00:00:00  Earnings     CHSB     5.74011777
2021-07-28 00:00:00  Earnings     CHSB     5.74161685
2021-07-29 00:00:00  Earnings     CHSB     5.74311631
2021-07-30 00:00:00  Earnings     CHSB     5.74461617
2021-07-31 00:00:00  Earnings     CHSB     5.74611643
2021-08-01 00:00:00  Earnings     CHSB     5.74761707
2021-08-02 00:00:00  Earnings     CHSB     5.74911810
2021-08-03 00:00:00  Earnings     CHSB     5.75061953
2021-08-04 00:00:00  Earnings     CHSB     5.75212135
2021-08-05 00:00:00  Earnings     CHSB     5.75362356
2021-08-06 00:00:00  Earnings     CHSB     5.75512617
2021-08-07 00:00:00  Earnings     CHSB     5.75662916
2021-08-08 00:00:00  Earnings     CHSB     5.75813255
2021-08-09 00:00:00  Earnings     CHSB     5.75963634
2021-08-10 00:00:00  Earnings     CHSB     5.76114051
2021-08-11 00:00:00  Earnings     CHSB     5.76264508
2021-08-12 00:00:00  Earnings     CHSB     5.76415004
2021-08-13 00:00:00  Earnings     CHSB     5.76565539
2021-08-14 00:00:00  Earnings     CHSB     5.76716114
2021-08-15 00:00:00  Earnings     CHSB     5.76866728
2021-08-16 00:00:00  Earnings     CHSB     5.77017381
2021-08-17 00:00:00  Earnings     CHSB     5.77168074
2021-08-18 00:00:00  Earnings     CHSB     5.77318806
2021-08-19 00:00:00  Earnings     CHSB     5.77469577
2021-08-20 00:00:00  Earnings     CHSB     5.77620388
2021-08-21 00:00:00  Earnings     CHSB     5.77771238
2021-08-22 00:00:00  Earnings     CHSB     5.77922127
2021-08-23 00:00:00  Earnings     CHSB     5.78073056
2021-08-24 00:00:00  Earnings     CHSB     5.78224024
2021-08-25 00:00:00  Earnings     CHSB     5.78375032
2021-08-26 00:00:00  Earnings     CHSB     5.78526079
2021-08-27 00:00:00  Earnings     CHSB     5.78677166
2021-08-28 00:00:00  Earnings     CHSB     5.78828292
2021-08-29 00:00:00  Earnings     CHSB     5.78979458
2021-08-30 00:00:00  Earnings     CHSB     5.79130663
2021-08-31 00:00:00  Earnings     CHSB     5.79281907
2021-09-01 00:00:00  Earnings     CHSB     5.79433191
2021-09-02 00:00:00  Earnings     CHSB     5.79584515
2021-09-03 00:00:00  Earnings     CHSB     5.79735878
2021-09-04 00:00:00  Earnings     CHSB     5.79887281
2021-09-05 00:00:00  Earnings     CHSB     5.80038723
2021-09-06 00:00:00  Earnings     CHSB     5.80190204
2021-09-07 00:00:00  Earnings     CHSB     5.80341726
2021-09-08 00:00:00  Earnings     CHSB     5.80493286
2021-09-09 00:00:00  Earnings     CHSB     5.80644887
2021-09-10 00:00:00  Earnings     CHSB     5.80796527
2021-09-11 00:00:00  Earnings     CHSB     5.80948206
2021-09-12 00:00:00  Earnings     CHSB     5.81099926
2021-09-13 00:00:00  Earnings     CHSB     5.81251684
2021-09-14 00:00:00  Earnings     CHSB     5.81403483
2021-09-15 00:00:00  Earnings     CHSB     5.81555321
2021-09-16 00:00:00  Earnings     CHSB     5.81707199
2021-09-17 00:00:00  Earnings     CHSB     5.81859116
2021-09-18 00:00:00  Earnings     CHSB     5.82011073
2021-09-19 00:00:00  Earnings     CHSB     5.82163070
2021-09-20 00:00:00  Earnings     CHSB     5.82315106
2021-09-21 00:00:00  Earnings     CHSB     5.82467183
2021-09-22 00:00:00  Earnings     CHSB     5.82619299
2021-09-23 00:00:00  Earnings     CHSB     5.82771454
2021-09-24 00:00:00  Earnings     CHSB     5.82923649
2021-09-25 00:00:00  Earnings     CHSB     5.83075885
2021-09-26 00:00:00  Earnings     CHSB     5.83228159
2021-09-27 00:00:00  Earnings     CHSB     5.83380474
2021-09-28 00:00:00  Earnings     CHSB     5.83532828
2021-09-29 00:00:00  Earnings     CHSB     5.83685223
2021-09-30 00:00:00  Earnings     CHSB     5.83837657
2021-10-01 00:00:00  Earnings     CHSB     5.83990130
2021-10-02 00:00:00  Earnings     CHSB     5.84142644
2021-10-03 00:00:00  Earnings     CHSB     5.84295198
2021-10-04 00:00:00  Earnings     CHSB     5.84447791
2021-10-05 00:00:00  Earnings     CHSB     5.84600424
2021-10-06 00:00:00  Earnings     CHSB     5.84753097
2021-10-07 00:00:00  Earnings     CHSB     5.84905810
2021-10-08 00:00:00  Earnings     CHSB     5.85058563
2021-10-09 00:00:00  Earnings     CHSB     5.85211355
2021-10-10 00:00:00  Earnings     CHSB     5.85364188
2021-10-11 00:00:00  Earnings     CHSB     5.85517060
2021-10-12 00:00:00  Earnings     CHSB     5.85669973
2021-10-13 00:00:00  Earnings     CHSB     5.85822925
2021-10-14 00:00:00  Earnings     CHSB     5.85975917
2021-10-15 00:00:00  Earnings     CHSB     5.86128950
2021-10-16 00:00:00  Earnings     CHSB     5.86282022
2021-10-17 00:00:00  Earnings     CHSB     5.86435134
2021-10-18 00:00:00  Earnings     CHSB     5.86588286
2021-10-19 00:00:00  Earnings     CHSB     5.86741478
2021-10-20 00:00:00  Earnings     CHSB     5.86894710
2021-10-21 00:00:00  Earnings     CHSB     5.87047983
2021-10-22 00:00:00  Earnings     CHSB     5.87201295
2021-10-23 00:00:00  Earnings     CHSB     5.87354647
2021-10-24 00:00:00  Earnings     CHSB     5.87508039
2021-10-25 00:00:00  Earnings     CHSB     5.87661472
2021-10-26 00:00:00  Earnings     CHSB     5.87814944
2021-10-27 00:00:00  Earnings     CHSB     5.87968457
2021-10-28 00:00:00  Earnings     CHSB     5.88122009
2021-10-29 00:00:00  Earnings     CHSB     5.88275602
2021-10-30 00:00:00  Earnings     CHSB     5.88429235
2021-10-31 00:00:00  Earnings     CHSB     5.88582908
2021-11-01 00:00:00  Earnings     CHSB     0.00321810
2021-11-02 00:00:00  Earnings     CHSB     0.00321978
2021-11-03 00:00:00  Earnings     CHSB     0.00322062
2021-11-04 00:00:00  Earnings     CHSB     0.00322146
2021-11-05 00:00:00  Earnings     CHSB     0.00322230
2021-11-06 00:00:00  Earnings     CHSB     0.00322315
2021-11-07 00:00:00  Earnings     CHSB     0.00322399
2021-11-08 00:00:00  Earnings     CHSB     0.00322483
2021-11-09 00:00:00  Earnings     CHSB     0.00322567
2021-11-10 00:00:00  Earnings     CHSB     0.00322651
2021-11-11 00:00:00  Earnings     CHSB     0.00322736
2021-11-12 00:00:00  Earnings     CHSB     0.00322820
2021-11-13 00:00:00  Earnings     CHSB     0.00322904
2021-11-14 00:00:00  Earnings     CHSB     0.00322989
2021-11-15 00:00:00  Earnings     CHSB     0.00323073
2021-11-16 00:00:00  Earnings     CHSB     0.00323157
2021-11-17 00:00:00  Earnings     CHSB     0.00323242
2021-11-18 00:00:00  Earnings     CHSB     0.00323326
2021-11-19 00:00:00  Earnings     CHSB     0.00323411
2021-11-20 00:00:00  Earnings     CHSB     0.00323495
2021-11-21 00:00:00  Earnings     CHSB     0.00323580
2021-11-22 00:00:00  Earnings     CHSB     0.00323664
2021-11-23 00:00:00  Earnings     CHSB     0.00323749
2021-11-24 00:00:00  Earnings     CHSB     0.00323833
2021-11-25 00:00:00  Earnings     CHSB     0.00323918
2021-11-26 00:00:00  Earnings     CHSB     0.00324002
2021-11-27 00:00:00  Earnings     CHSB     0.00324087
2021-11-28 00:00:00  Earnings     CHSB     0.00324172
2021-11-29 00:00:00  Earnings     CHSB     0.00324256
2021-11-30 00:00:00  Earnings     CHSB     0.00324341
2021-12-01 00:00:00  Earnings     CHSB     0.00324426
2021-12-02 00:00:00  Earnings     CHSB     0.00324510
2021-12-03 00:00:00  Earnings     CHSB     0.00324595
2021-12-04 00:00:00  Earnings     CHSB     0.00324680
2021-12-05 00:00:00  Earnings     CHSB     0.00324765
2021-12-06 00:00:00  Earnings     CHSB     0.00324849
2021-12-07 00:00:00  Earnings     CHSB     0.00324934
2021-12-08 00:00:00  Earnings     CHSB     0.00325019
2021-12-09 00:00:00  Earnings     CHSB     0.00325104
2021-12-10 00:00:00  Earnings     CHSB     0.00325189
2021-12-11 00:00:00  Earnings     CHSB     0.00325274
2021-12-12 00:00:00  Earnings     CHSB     0.00325359
2021-12-13 00:00:00  Earnings     CHSB     0.00325444
2021-12-14 00:00:00  Earnings     CHSB     0.00325529
2021-12-15 00:00:00  Earnings     CHSB     0.00325614
2021-12-16 00:00:00  Earnings     CHSB     0.00325699
2021-12-17 00:00:00  Earnings     CHSB     0.00325784
2021-12-18 00:00:00  Earnings     CHSB     0.00325869
2021-12-19 00:00:00  Earnings     CHSB     0.00325954
2021-12-20 00:00:00  Earnings     CHSB     0.00326039
2021-12-21 00:00:00  Earnings     CHSB     0.00326124
2021-12-22 00:00:00  Earnings     CHSB     0.00326210
2021-12-23 00:00:00  Earnings     CHSB     0.00326295
2021-12-24 00:00:00  Earnings     CHSB     0.00326380
2021-12-25 00:00:00  Earnings     CHSB     0.00326465
2021-12-26 00:00:00  Earnings     CHSB     0.00326550
2021-12-27 00:00:00  Earnings     CHSB     0.00326636
2021-12-28 00:00:00  Earnings     CHSB     0.00326721
2021-12-29 00:00:00  Earnings     CHSB     0.00326806
2021-12-30 00:00:00  Earnings     CHSB     0.00326892
2021-12-31 00:00:00  Earnings     CHSB     0.00326977
TOTAL                                  1,532.64038002'''

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			self.maxDiff=None
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

		yieldOwnerWithTotalsDetailDfExpectedStr = \
'                                                       DEP/WITHDR                                                                                \n' + \
'                  CHSB                                        CHF             CAPITAL                    DATE                  YIELD             \n' + \
'        Tot incl yield    DF RATE   CUR RATE  CAP GAIN CAP GAIN %      CHSB       CHF        FROM          TO DAYS     CHSB      CHF   Y % YR Y %\n' + \
'OWNER                                                                                                                                            ' + \
'''
JPS          10,000.00   5,000.00  15,000.00 10,000.00     200.00 10,000.00 15,000.00  2021-01-01  2021-02-28   59   155.26   232.88  1.55  10.00
JPS          10,000.00  10,000.00  15,000.00  5,000.00      50.00 20,155.26 30,232.88  2021-03-01  2021-03-31   31   163.82   245.72  0.81  10.00
JPS           1,000.00   2,000.00   1,500.00   -500.00     -25.00 21,319.07 31,978.61  2021-04-01  2021-04-30   30   167.66   251.50  0.79  10.00
JPS            -500.00    -500.00    -750.00   -250.00     -50.00 20,986.73 31,480.10  2021-05-01  2021-05-31   31   170.62   255.93  0.81  10.00
JPS            -500.00  -1,000.00    -750.00    250.00      25.00 20,657.35 30,986.03  2021-06-01  2021-06-30   30   162.54   243.82  0.79  10.01
JPS           1,000.00     800.00   1,500.00    700.00      87.50 21,819.90 32,729.84  2021-07-01  2021-10-31  123   712.55 1,068.82  3.27  10.01
JPS         -22,531.55 -30,000.00 -33,797.32 -3,797.32     -12.66      0.89      1.34  2021-11-01  2021-12-31   61     0.20     0.30 22.17 231.48
TOTAL             1.09 -13,700.00       1.64 11,402.68     -83.23                                                  1,532.64 2,298.96             ''' + \
'''
G TOTAL           1.09                  1.64                                                                       1,532.64 2,298.96             '''

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, yieldOwnerWithTotalsDetailDfActualStr)

if __name__ == '__main__':
	if os.name == 'posix':
		unittest.main()
	else:
		tst = TestProcessor()
		# tst.testAddFiatConversionInfo_CHSB_2_fiats_2_owners()
		# tst.testAddFiatConversionInfo_CHSB_2_fiats_2_owners_french_language()
		tst.testAddFiatConversionInfo_USDC_1_fiat_4_owners()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_2_owners()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner_withdrawal_gain()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner_withdrawal_loss()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner_no_withdrawal()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner_2_fiats_no_withdrawal()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner_1_deposit_gain()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_2_owners_1_deposit()
		# tst.testAddFiatConversionInfo_USDC_1_fiat_simple_values_2_owners_bug()
		# tst.testAddFiatConversionInfo_USDC_1_fiat_simple_values_2_owners_2_deposits_bug_french_language()
		# tst.testAddFiatConversionInfo_USDC_2_fiats_simple_values_2_owners_2_deposits_bug_french_language()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner_max_withdrawal_bug()
		#tst.testDepositChsb_fiat_chf_pandas_avg_rate_explore()