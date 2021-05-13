import unittest
import os,sys,inspect
from io import StringIO

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

class TestProcessorNewStructure(unittest.TestCase):
	def initializeComputerClasses(self,
								  sbAccountSheetFileName,
								  depositSheetFileName,
								  cryptoFiatCsvFileName,
								  sbAccountSheetFiat='USD',
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
		self.yieldRateComputer = SBYieldRateComputer(sbAccountSheetFilePathName=sbAccountSheetFilePathName,
													 sbAccountSheetFiat=sbAccountSheetFiat,
													 depositSheetFilePathName=depositSheetFilePathName,
													 language=self.language)
		self.ownerDepositYieldComputer = OwnerDepositYieldComputer(self.yieldRateComputer,
																   self.language)
		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequester(),
														  self.cryptoFiatCsvFilePathName),
								   self.language)
	def testAddFiatConversionInfo_ETH_1_fiat_2_owners_1_and_2_deposits_french_language(self):
		"""
		ETH crypto, 2 owners, 1 with 1 deposit and the other with 2 deposits
		"""
		PRINT = True

		sbAccountSheetFileName = 'test_ETH_SB_account_statement.xlsx'
		depositSheetFileName = 'test_Eth_2_owners_1_and_2_deposits.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_ETH

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName,
									   sbAccountSheetFiat='CHF')

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

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			sbEarningsTotalDfExpectedStr = \
'''                         Type Currency Net amount
Local time                                       
2021-03-20 09:00:00  Earnings      ETH 0.00220370
2021-03-21 09:00:00  Earnings      ETH 0.00203130
2021-03-22 09:00:00  Earnings      ETH 0.00193280
2021-03-23 09:00:00  Earnings      ETH 0.00226800
2021-03-24 09:00:00  Earnings      ETH 0.00189990
2021-03-25 09:00:00  Earnings      ETH 0.00191610
2021-03-26 09:00:00  Earnings      ETH 0.00180680
2021-03-27 09:00:00  Earnings      ETH 0.00176530
2021-03-28 10:00:00  Earnings      ETH 0.00192890
2021-03-29 10:00:00  Earnings      ETH 0.00175700
2021-03-30 10:00:00  Earnings      ETH 0.00178290
2021-03-31 10:00:00  Earnings      ETH 0.00180040
2021-04-01 10:00:00  Earnings      ETH 0.00170800
2021-04-02 10:00:00  Earnings      ETH 0.00162350
2021-04-03 10:00:00  Earnings      ETH 0.00155790
2021-04-04 10:00:00  Earnings      ETH 0.00170240
2021-04-05 10:00:00  Earnings      ETH 0.00151470
2021-04-06 10:00:00  Earnings      ETH 0.00157290
2021-04-07 10:00:00  Earnings      ETH 0.00147490
2021-04-08 10:00:00  Earnings      ETH 0.00157140
2021-04-09 10:00:00  Earnings      ETH 0.00156080
2021-04-10 10:00:00  Earnings      ETH 0.00156500
2021-04-11 10:00:00  Earnings      ETH 0.00145190
2021-04-12 10:00:00  Earnings      ETH 0.00144000
2021-04-13 10:00:00  Earnings      ETH 0.00158850
2021-04-14 10:00:00  Earnings      ETH 0.00153360
2021-04-15 10:00:00  Earnings      ETH 0.00149460
2021-04-16 10:00:00  Earnings      ETH 0.00144050
2021-04-17 10:00:00  Earnings      ETH 0.00145080
2021-04-18 10:00:00  Earnings      ETH 0.00142640
2021-04-19 10:00:00  Earnings      ETH 0.00134440
2021-04-20 10:00:00  Earnings      ETH 0.00131590
2021-04-21 10:00:00  Earnings      ETH 0.00133880
2021-04-22 10:00:00  Earnings      ETH 0.00120430
2021-04-23 10:00:00  Earnings      ETH 0.00119700
2021-04-24 10:00:00  Earnings      ETH 0.00109550
2021-04-25 10:00:00  Earnings      ETH 0.00107020
2021-04-26 10:00:00  Earnings      ETH 0.00107680
2021-04-27 10:00:00  Earnings      ETH 0.00119810
2021-04-28 10:00:00  Earnings      ETH 0.00107730
2021-04-29 10:00:00  Earnings      ETH 0.00107110
2021-04-30 10:00:00  Earnings      ETH 0.00107780
2021-05-01 10:00:00  Earnings      ETH 0.00107800
2021-05-02 10:00:00  Earnings      ETH 0.00106670
2021-05-03 10:00:00  Earnings      ETH 0.00096270
2021-05-04 10:00:00  Earnings      ETH 0.00112980
TOTAL                                  0.06907530
'''
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(sbEarningsTotalDfActualStr)

			sys.stdout = stdout

			self.assertEqual(sbEarningsTotalDfExpectedStr, capturedStdoutStr.getvalue())

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			yieldOwnerWithTotalsDetailDfExpectedStr = \
'''                                          DEPÔTS  /  RETRAITS                                                                          
                                MONTANT VAL DAT DEP   VAL ACT VAL ACT   VAL ACT PLUS-VAL CAP                                   INTÉRÊTS
                 DE           A     ETH         CHF       CHF INT CHF TOTAL CHF          CHF P-V CAP %  ETH  JOURS  ETH INT % INT ANN %
PROPR                                                                                                                                  
Béa      2021-03-20  2021-05-04    0.40      600.00  1,594.25   22.08  1,616.34       994.25    165.71 0.40     46 0.01  1.39     11.53
TOTAL                              0.40      600.00  1,616.34   22.08                 994.25    165.71             0.01                
Papa     2021-03-20  2021-05-04    4.59    7,583.15 18,351.66  254.22 18,605.88    10,768.51    142.01 4.59     46 0.06  1.39     11.53
TOTAL                              4.65    7,583.15 18,605.88  254.22              10,768.51    142.01             0.06                
G TOTAL                            5.06             20,222.22  276.30                                              0.07                
'''
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(yieldOwnerWithTotalsDetailDfActualStr)

			sys.stdout = stdout

			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, capturedStdoutStr.getvalue())

	def testAddFiatConversionInfo_ETH_1_fiat_2_owners_1_and_2_deposits_english_language(self):
		"""
		ETH crypto, 2 owners, 1 with 1 deposit and the other with 2 deposits
		"""
		PRINT = True

		sbAccountSheetFileName = 'test_ETH_SB_account_statement.xlsx'
		depositSheetFileName = 'test_Eth_2_owners_1_and_2_deposits.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_ETH

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName,
									   sbAccountSheetFiat='CHF')

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(),
														  self.cryptoFiatCsvFilePathName),
								   language=GB)

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDfActualStr, \
		depositCrypto =	self.processor.addFiatConversionInfo()

		sbEarningsTotalDf = self.yieldRateComputer.getSBEarningSheetTotalDf(expectedYieldCrypto)

		sbEarningsTotalDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			sbEarningsTotalDf,
			{
				SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			sbEarningsTotalDfExpectedStr = \
'''                         Type Currency Net amount
Local time                                       
2021-03-20 09:00:00  Earnings      ETH 0.00220370
2021-03-21 09:00:00  Earnings      ETH 0.00203130
2021-03-22 09:00:00  Earnings      ETH 0.00193280
2021-03-23 09:00:00  Earnings      ETH 0.00226800
2021-03-24 09:00:00  Earnings      ETH 0.00189990
2021-03-25 09:00:00  Earnings      ETH 0.00191610
2021-03-26 09:00:00  Earnings      ETH 0.00180680
2021-03-27 09:00:00  Earnings      ETH 0.00176530
2021-03-28 10:00:00  Earnings      ETH 0.00192890
2021-03-29 10:00:00  Earnings      ETH 0.00175700
2021-03-30 10:00:00  Earnings      ETH 0.00178290
2021-03-31 10:00:00  Earnings      ETH 0.00180040
2021-04-01 10:00:00  Earnings      ETH 0.00170800
2021-04-02 10:00:00  Earnings      ETH 0.00162350
2021-04-03 10:00:00  Earnings      ETH 0.00155790
2021-04-04 10:00:00  Earnings      ETH 0.00170240
2021-04-05 10:00:00  Earnings      ETH 0.00151470
2021-04-06 10:00:00  Earnings      ETH 0.00157290
2021-04-07 10:00:00  Earnings      ETH 0.00147490
2021-04-08 10:00:00  Earnings      ETH 0.00157140
2021-04-09 10:00:00  Earnings      ETH 0.00156080
2021-04-10 10:00:00  Earnings      ETH 0.00156500
2021-04-11 10:00:00  Earnings      ETH 0.00145190
2021-04-12 10:00:00  Earnings      ETH 0.00144000
2021-04-13 10:00:00  Earnings      ETH 0.00158850
2021-04-14 10:00:00  Earnings      ETH 0.00153360
2021-04-15 10:00:00  Earnings      ETH 0.00149460
2021-04-16 10:00:00  Earnings      ETH 0.00144050
2021-04-17 10:00:00  Earnings      ETH 0.00145080
2021-04-18 10:00:00  Earnings      ETH 0.00142640
2021-04-19 10:00:00  Earnings      ETH 0.00134440
2021-04-20 10:00:00  Earnings      ETH 0.00131590
2021-04-21 10:00:00  Earnings      ETH 0.00133880
2021-04-22 10:00:00  Earnings      ETH 0.00120430
2021-04-23 10:00:00  Earnings      ETH 0.00119700
2021-04-24 10:00:00  Earnings      ETH 0.00109550
2021-04-25 10:00:00  Earnings      ETH 0.00107020
2021-04-26 10:00:00  Earnings      ETH 0.00107680
2021-04-27 10:00:00  Earnings      ETH 0.00119810
2021-04-28 10:00:00  Earnings      ETH 0.00107730
2021-04-29 10:00:00  Earnings      ETH 0.00107110
2021-04-30 10:00:00  Earnings      ETH 0.00107780
2021-05-01 10:00:00  Earnings      ETH 0.00107800
2021-05-02 10:00:00  Earnings      ETH 0.00106670
2021-05-03 10:00:00  Earnings      ETH 0.00096270
2021-05-04 10:00:00  Earnings      ETH 0.00112980
TOTAL                                  0.06907530
'''
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(sbEarningsTotalDfActualStr)

			sys.stdout = stdout

			self.assertEqual(sbEarningsTotalDfExpectedStr, capturedStdoutStr.getvalue())

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			yieldOwnerWithTotalsDetailDfExpectedStr = \
'''                                       DEPOSITS   /   WITHDRAWALS                                                                   
                                AMOUNT     DEP RATE      CUR RATE CUR RATE  CUR RATE  CAP GAIN                                 YIELD
               FROM          TO    ETH          CHF           CHF  YLD CHF TOTAL CHF       CHF CAP GAIN %  ETH DAYS  ETH  Y % YR Y %
OWNER                                                                                                                               
Béa      2021-03-20  2021-05-04   0.40       600.00      1,594.25    22.08  1,616.34    994.25     165.71 0.40   46 0.01 1.39  11.53
TOTAL                             0.40       600.00      1,616.34    22.08              994.25     165.71           0.01            
Papa     2021-03-20  2021-05-04   4.59     7,583.15     18,351.66   254.22 18,605.88 10,768.51     142.01 4.59   46 0.06 1.39  11.53
TOTAL                             4.65     7,583.15     18,605.88   254.22           10,768.51     142.01           0.06            
G TOTAL                           5.06                  20,222.22   276.30                                          0.07            
'''
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(yieldOwnerWithTotalsDetailDfActualStr)

			sys.stdout = stdout

			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, capturedStdoutStr.getvalue())

	def testAddFiatConversionInfo_USDC_2_fiats_simple_values_2_owners_2_deposits_bug_french_language(self):
		"""
		USDC crypto, 2 owners with 2 deposit and 1 withdrawal, fixed yield rate,
		USDC/CHF final rate of 1.5 and USDC/EUR final rate of 1.4
		"""
		PRINT = True

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
'''                                            DEPÔTS  /  RETRAITS                                                                                                                                              
                                  MONTANT VAL DAT DEP   VAL ACT  VAL ACT   VAL ACT    VAL ACT     VAL ACT PLUS-VAL CAP                                                               INTÉRÊTS                
                 DE           A      USDC         CHF       CHF  INT CHF TOTAL CHF    INT EUR   TOTAL EUR          CHF P-V CAP %      EUR      EUR     EUR P-V CAP %     USDC  JOURS     USDC INT % INT ANN %
PROPR                                                                                                                                                                                                        
Béa      2021-02-20  2021-12-31  4,400.00    4,000.00  4,006.20   309.40  4,315.60     271.85    3,791.85         6.20      0.15 2,800.00 3,520.00  720.00     25.71 4,400.00    315   339.82  7.72      9.00
TOTAL                            4,739.82    4,000.00  4,315.60   309.40               271.85                     6.20      0.15 2,800.00 3,791.85  720.00     25.71                   339.82                
JPS      2021-03-22  2021-04-21  5,500.00    5,000.00  5,007.75    37.01  5,044.76      32.52    4,432.52         7.75      0.15 4,500.00 4,400.00 -100.00     -2.22 5,500.00     31    40.65  0.74      9.06
JPS      2021-04-22  2021-12-31 -1,000.00   -1,200.00   -910.50   255.24  4,389.50     224.26    3,856.78       289.50     24.12  -800.00  -800.00    0.00      0.00 4,540.65    254   280.32  6.17      8.99
TOTAL                            4,820.98    3,800.00  4,389.50   292.25               256.78                   297.25      7.82 3,700.00 3,856.78 -100.00     -2.70                   320.98                
G TOTAL                          9,560.79              8,705.10   601.65               528.63                                             7,648.63                                     660.79                
'''
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(yieldOwnerWithTotalsDetailDfActualStr)

			sys.stdout = stdout

			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, capturedStdoutStr.getvalue())

	def testAddFiatConversionInfo_USDC_2_fiats_simple_values_2_owners_2_deposits_bug_english_language(self):
		"""
		USDC crypto, 2 owners with 2 deposit and 1 withdrawal, fixed yield rate,
		USDC/CHF final rate of 1.5 and USDC/EUR final rate of 1.4
		"""
		PRINT = True

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
								   language=GB)

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
'''                                          DEPOSITS   /   WITHDRAWALS                                                                                                                                        
                                   AMOUNT     DEP RATE      CUR RATE  CUR RATE   CUR RATE    CUR RATE     CUR RATE CAP GAIN                                                                YIELD            
               FROM          TO      USDC          CHF           CHF   YLD CHF  TOTAL CHF     YLD EUR    TOTAL EUR      CHF CAP GAIN %      EUR      EUR     EUR CAP GAIN %     USDC DAYS   USDC  Y % YR Y %
OWNER                                                                                                                                                                                                       
Béa      2021-02-20  2021-12-31  4,400.00     4,000.00      4,006.20    309.40   4,315.60      271.85     3,791.85     6.20       0.15 2,800.00 3,520.00  720.00      25.71 4,400.00  315 339.82 7.72   9.00
TOTAL                            4,739.82     4,000.00      4,315.60    309.40                 271.85                  6.20       0.15 2,800.00 3,791.85  720.00      25.71               339.82            
JPS      2021-03-22  2021-04-21  5,500.00     5,000.00      5,007.75     37.01   5,044.76       32.52     4,432.52     7.75       0.15 4,500.00 4,400.00 -100.00      -2.22 5,500.00   31  40.65 0.74   9.06
JPS      2021-04-22  2021-12-31 -1,000.00    -1,200.00       -910.50    255.24   4,389.50      224.26     3,856.78   289.50      24.12  -800.00  -800.00    0.00       0.00 4,540.65  254 280.32 6.17   8.99
TOTAL                            4,820.98     3,800.00      4,389.50    292.25                 256.78                297.25       7.82 3,700.00 3,856.78 -100.00      -2.70               320.98            
G TOTAL                          9,560.79                   8,705.10    601.65                 528.63                                           7,648.63                                  660.79            
'''
		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents...')
			print(yieldOwnerWithTotalsDetailDfActualStr)
		else:
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(yieldOwnerWithTotalsDetailDfActualStr)

			sys.stdout = stdout

			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, capturedStdoutStr.getvalue())

if __name__ == '__main__':
	if os.name == 'posix':
		unittest.main()
	else:
		tst = TestProcessorNewStructure()
		tst.testAddFiatConversionInfo_USDC_2_fiats_simple_values_2_owners_2_deposits_bug_french_language()
		tst.testAddFiatConversionInfo_USDC_2_fiats_simple_values_2_owners_2_deposits_bug_english_language()
		tst.testAddFiatConversionInfo_ETH_1_fiat_2_owners_1_and_2_deposits_french_language()
		tst.testAddFiatConversionInfo_ETH_1_fiat_2_owners_1_and_2_deposits_english_language()