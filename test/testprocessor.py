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
		PRINT = True

		sbAccountSheetFileName = 'testSwissborg_account_statement_20201218_20210408.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_usd_chf.csv'
		#depositSheetFileName = 'testDepositChsb_fiat_usd.csv'
		#depositSheetFileName = 'testDepositChsb_no_fiat.csv'
		#depositSheetFileName = 'testDepositChsb_fiat_chf.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName)

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)

		# resetting the pandas global float format so that the other unit test
		# are not impacted by the previous global float format setting
		pd.reset_option('display.float_format')

	def testAddFiatConversionInfo_1_fiat_simple_values_2_owners(self):
		"""
		CHSB crypto, 2 owners, 1 with 1 withdrawal, fixed yield rate,
		CHSB/CHF final rateof 1.5.
		"""
		PRINT = True

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
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

	def testAddFiatConversionInfo_1_fiat_simple_values_1_owner(self):
		"""
		CHSB crypto, 2 owners, 1 with 1 withdrawal, fixed yield rate,
		CHSB/CHF final rateof 1.5.
		"""
		PRINT = True

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner.csv'
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
			print('\nSwissborg earnings loaded from Swissborg account statement sheet ...')
			print(sbEarningsTotalDfActualStr)
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			self.maxDiff=None
			self.assertEqual(sbEarningsTotalDfExpectedStr, sbEarningsTotalDfActualStr)

if __name__ == '__main__':
	if os.name == 'posix':
		unittest.main()
	else:
		tst = TestProcessor()
		tst.testAddFiatConversionInfo_2_fiats_2_owners()
		tst.testAddFiatConversionInfo_1_fiat_simple_values_2_owners()
		tst.testAddFiatConversionInfo_1_fiat_simple_values_1_owner()
