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
	def initializeComputerClasses(self, sbAccountSheetFileName, depositSheetFileName, cryptoFiatCsvFileName):
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
		                                             depositSheetFilePathName)
		self.ownerDepositYieldComputer = OwnerDepositYieldComputer(self.yieldRateComputer)
		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequester(), self.cryptoFiatCsvFilePathName))

	def testAddFiatConversionInfo_2_fiats_2_owners(self):
		"""
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

		self.maxDiff=None

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDf, \
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
			print(yieldOwnerWithTotalsDetailDfActualStr)
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

	def testAddFiatConversionInfo_1_fiat_simple_values_2_owners(self):
		"""
		CHSB crypto, 2 owners, 1 with 1 withdrawal, fixed yield rate,
		CHSB/CHF final rateof 1.5.
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
		yieldOwnerWithTotalsDetailDf, \
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
			print(yieldOwnerWithTotalsDetailDfActualStr)
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

	def testAddFiatConversionInfo_1_fiat_simple_values_1_owner_withdrawal_gain(self):
		"""
		CHSB crypto, 2 owners, 1 with 1 withdrawal, fixed yield rate,
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
		yieldOwnerWithTotalsDetailDf, \
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
		yieldOwnerWithTotalsDetailDf, \
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
		yieldOwnerWithTotalsDetailDf, \
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
		yieldOwnerWithTotalsDetailDf, \
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
		yieldOwnerWithTotalsDetailDf, \
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

if __name__ == '__main__':
	if os.name == 'posix':
		unittest.main()
	else:
		tst = TestProcessor()
		tst.testAddFiatConversionInfo_2_fiats_2_owners()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_2_owners()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner_withdrawal_gain()
		# tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner_withdrawal_loss()
		tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner_no_withdrawal()
		tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner_2_fiats_no_withdrawal()