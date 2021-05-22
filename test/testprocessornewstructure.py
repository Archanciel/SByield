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
		PRINT = False

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
		yieldOwnerWithTotalsDetailDf, \
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
'''                                          DÉPÔTS  /  RETRAITS                                                                                      
                                MONTANT VAL DAT DÉP   VAL ACT VAL ACT  VAL ACT PLUS-VAL         JOURS  INT                 MONTANT INTÉRÊTS EN CHF 
                 DE           A     ETH         CHF       CHF INT CHF  TOT CHF  CAP CHF   EN %    INT  ETH EN %  % ANNUEL PAR JOUR PAR MOIS  PAR AN
PROPR                                                                                                                                              
Béa      2021-03-23  2021-05-04    0.40      600.00   1594.25   20.09  1614.34   994.25 165.71     43 0.01 1.26     11.21                          
TOTAL                              0.40      600.00   1594.25   20.09  1614.34   994.25 165.71        0.01          11.21     0.47    14.16  181.03
Papa     2021-03-20  2021-05-04    4.59     7583.15  18351.66  256.21 18607.88 10768.51 142.01     46 0.06 1.40     11.63                          
TOTAL                              4.59     7583.15  18351.66  256.21 18607.88 10768.51 142.01        0.06          11.21     5.42   163.27 2086.68
G TOTAL                            4.99              19945.92  276.30 20222.22                        0.07                                         
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
		PRINT = False

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
		yieldOwnerWithTotalsDetailDf, \
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
                                AMOUNT     DEP RATE      CUR RATE CUR RATE  CUR RATE CAP GAIN        DAYS  INT              AMOUNT INTERESTS IN CHF 
               FROM          TO    ETH          CHF           CHF  YLD CHF   TOT CHF ONLY CHF   IN %  INT  ETH IN % YRLY % PER DAY PER MONTH  PER YR
OWNER                                                                                                                                               
Béa      2021-03-23  2021-05-04   0.40       600.00       1594.25    20.09   1614.34   994.25 165.71   43 0.01 1.26  11.21                          
TOTAL                             0.40       600.00       1594.25    20.09   1614.34   994.25 165.71      0.01       11.21    0.47     14.16  181.03
Papa     2021-03-20  2021-05-04   4.59      7583.15      18351.66   256.21  18607.88 10768.51 142.01   46 0.06 1.40  11.63                          
TOTAL                             4.59      7583.15      18351.66   256.21  18607.88 10768.51 142.01      0.06       11.21    5.42    163.27 2086.68
G TOTAL                           4.99                   19945.92   276.30  20222.22                      0.07                                      
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
'''                                           DÉPÔTS  /  RETRAITS                                                                                                                                                   
                                 MONTANT VAL DAT DÉP   VAL ACT  VAL ACT   VAL ACT PLUS-VAL       VAL DAT DÉP VAL ACT    VAL ACT     VAL ACT PLUS-VAL        JOURS    INT                 MONTANT INTÉRÊTS EN CHF 
                 DE           A     USDC         CHF       CHF  INT CHF   TOT CHF  CAP CHF  EN %         EUR     EUR    INT EUR     TOT EUR  CAP EUR  EN %    INT   USDC EN %  % ANNUEL PAR JOUR PAR MOIS  PAR AN
PROPR                                                                                                                                                                                                            
Béa      2021-02-20  2021-12-31  4400.00     4000.00   4006.20   309.40   4315.60     6.20  0.15     2800.00 3520.00     271.85     3791.85   720.00 25.71    315 339.82 7.72      9.00                          
TOTAL                            4400.00     4000.00   4006.20   309.40   4315.60     6.20  0.15     2800.00 3520.00     271.85     3791.85   720.00 25.71        339.82           9.00     0.90    26.96  341.37
JPS      2021-03-22  2021-04-21  5500.00     5000.00   5007.75    37.01   5044.76     7.75  0.15     4500.00 4400.00      32.52     4432.52  -100.00 -2.22     31  40.65 0.74      9.06                          
JPS      2021-04-22  2021-12-31 -1000.00     -850.00   -910.50   255.24   4389.50   -60.50 -7.12     -800.00 -800.00     224.26     3856.78     0.00  0.00    254 280.32 6.17      8.99                          
TOTAL                            4500.00     4150.00   4097.25   292.25   4389.50   -52.75 -1.27     3700.00 3600.00     256.78     3856.78  -100.00 -2.70        320.98           9.00     0.91    27.41  347.00
G TOTAL                          8900.00               8103.45   601.65   8705.10                            7120.00     528.63     7648.63                       660.79                                         
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
								   language=GB)

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
'''                                         DEPOSITS   /   WITHDRAWALS                                                                                                                                                
                                  AMOUNT     DEP RATE      CUR RATE  CUR RATE   CUR RATE CAP GAIN       DEP RATE CUR RATE    CUR RATE     CUR RATE CAP GAIN       DAYS    INT              AMOUNT INTERESTS IN CHF 
               FROM          TO     USDC          CHF           CHF   YLD CHF    TOT CHF ONLY CHF  IN %      EUR      EUR     YLD EUR      TOT EUR ONLY EUR  IN %  INT   USDC IN % YRLY % PER DAY PER MONTH  PER YR
OWNER                                                                                                                                                                                                              
Béa      2021-02-20  2021-12-31  4400.00      4000.00       4006.20    309.40    4315.60     6.20  0.15  2800.00  3520.00      271.85      3791.85   720.00 25.71  315 339.82 7.72   9.00                          
TOTAL                            4400.00      4000.00       4006.20    309.40    4315.60     6.20  0.15  2800.00  3520.00      271.85      3791.85   720.00 25.71      339.82        9.00    0.90     26.96  341.37
JPS      2021-03-22  2021-04-21  5500.00      5000.00       5007.75     37.01    5044.76     7.75  0.15  4500.00  4400.00       32.52      4432.52  -100.00 -2.22   31  40.65 0.74   9.06                          
JPS      2021-04-22  2021-12-31 -1000.00      -850.00       -910.50    255.24    4389.50   -60.50 -7.12  -800.00  -800.00      224.26      3856.78     0.00  0.00  254 280.32 6.17   8.99                          
TOTAL                            4500.00      4150.00       4097.25    292.25    4389.50   -52.75 -1.27  3700.00  3600.00      256.78      3856.78  -100.00 -2.70      320.98        9.00    0.91     27.41  347.00
G TOTAL                          8900.00                    8103.45    601.65    8705.10                          7120.00      528.63      7648.63                     660.79                                      
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

	def testAddFiatConversionInfo_ETH_1_fiat_1_owner_1_deposit_french_language(self):
		"""
		ETH crypto, 1 owner with 1 deposit. Testing crypto yield amount,
		crypto yield amount in percent, day, month and year yields in CHF.
		ETH/CHF curr rate == 4000. Yield fixed rate of 10 % per year.
		"""
		PRINT = False

		sbAccountSheetFileName = 'test_ETH_SB_simplevalue_1_owner_1_deposit.xlsx'
		depositSheetFileName = 'test_Eth_CHF_simplevalue_1_owner_1_deposit.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_ETH
		testLanguage = FR
		fiat = 'CHF'

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName,
									   sbAccountSheetFiat=fiat)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(),
														  self.cryptoFiatCsvFilePathName),
								   language=testLanguage)

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

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			sbEarningsTotalDfExpectedStr = \
'''                         Type Currency Net amount
Local time                                       
2021-01-01 00:00:00  Earnings      ETH 0.00052232
2021-01-02 00:00:00  Earnings      ETH 0.00052245
2021-01-03 00:00:00  Earnings      ETH 0.00052259
2021-01-04 00:00:00  Earnings      ETH 0.00052273
2021-01-05 00:00:00  Earnings      ETH 0.00052286
2021-01-06 00:00:00  Earnings      ETH 0.00052300
2021-01-07 00:00:00  Earnings      ETH 0.00052313
2021-01-08 00:00:00  Earnings      ETH 0.00052327
2021-01-09 00:00:00  Earnings      ETH 0.00052341
2021-01-10 00:00:00  Earnings      ETH 0.00052354
2021-01-11 00:00:00  Earnings      ETH 0.00052368
2021-01-12 00:00:00  Earnings      ETH 0.00052382
2021-01-13 00:00:00  Earnings      ETH 0.00052395
2021-01-14 00:00:00  Earnings      ETH 0.00052409
2021-01-15 00:00:00  Earnings      ETH 0.00052423
2021-01-16 00:00:00  Earnings      ETH 0.00052437
2021-01-17 00:00:00  Earnings      ETH 0.00052450
2021-01-18 00:00:00  Earnings      ETH 0.00052464
2021-01-19 00:00:00  Earnings      ETH 0.00052478
2021-01-20 00:00:00  Earnings      ETH 0.00052491
2021-01-21 00:00:00  Earnings      ETH 0.00052505
2021-01-22 00:00:00  Earnings      ETH 0.00052519
2021-01-23 00:00:00  Earnings      ETH 0.00052532
2021-01-24 00:00:00  Earnings      ETH 0.00052546
2021-01-25 00:00:00  Earnings      ETH 0.00052560
2021-01-26 00:00:00  Earnings      ETH 0.00052574
2021-01-27 00:00:00  Earnings      ETH 0.00052587
2021-01-28 00:00:00  Earnings      ETH 0.00052601
2021-01-29 00:00:00  Earnings      ETH 0.00052615
2021-01-30 00:00:00  Earnings      ETH 0.00052629
2021-01-31 00:00:00  Earnings      ETH 0.00052642
2021-02-01 00:00:00  Earnings      ETH 0.00052656
2021-02-02 00:00:00  Earnings      ETH 0.00052670
2021-02-03 00:00:00  Earnings      ETH 0.00052684
2021-02-04 00:00:00  Earnings      ETH 0.00052697
2021-02-05 00:00:00  Earnings      ETH 0.00052711
2021-02-06 00:00:00  Earnings      ETH 0.00052725
2021-02-07 00:00:00  Earnings      ETH 0.00052739
2021-02-08 00:00:00  Earnings      ETH 0.00052752
2021-02-09 00:00:00  Earnings      ETH 0.00052766
2021-02-10 00:00:00  Earnings      ETH 0.00052780
2021-02-11 00:00:00  Earnings      ETH 0.00052794
2021-02-12 00:00:00  Earnings      ETH 0.00052808
2021-02-13 00:00:00  Earnings      ETH 0.00052821
2021-02-14 00:00:00  Earnings      ETH 0.00052835
2021-02-15 00:00:00  Earnings      ETH 0.00052849
2021-02-16 00:00:00  Earnings      ETH 0.00052863
2021-02-17 00:00:00  Earnings      ETH 0.00052877
2021-02-18 00:00:00  Earnings      ETH 0.00052890
2021-02-19 00:00:00  Earnings      ETH 0.00052904
2021-02-20 00:00:00  Earnings      ETH 0.00052918
2021-02-21 00:00:00  Earnings      ETH 0.00052932
2021-02-22 00:00:00  Earnings      ETH 0.00052946
2021-02-23 00:00:00  Earnings      ETH 0.00052959
2021-02-24 00:00:00  Earnings      ETH 0.00052973
2021-02-25 00:00:00  Earnings      ETH 0.00052987
2021-02-26 00:00:00  Earnings      ETH 0.00053001
2021-02-27 00:00:00  Earnings      ETH 0.00053015
2021-02-28 00:00:00  Earnings      ETH 0.00053029
2021-03-01 00:00:00  Earnings      ETH 0.00053043
2021-03-02 00:00:00  Earnings      ETH 0.00053056
2021-03-03 00:00:00  Earnings      ETH 0.00053070
2021-03-04 00:00:00  Earnings      ETH 0.00053084
2021-03-05 00:00:00  Earnings      ETH 0.00053098
2021-03-06 00:00:00  Earnings      ETH 0.00053112
2021-03-07 00:00:00  Earnings      ETH 0.00053126
2021-03-08 00:00:00  Earnings      ETH 0.00053140
2021-03-09 00:00:00  Earnings      ETH 0.00053153
2021-03-10 00:00:00  Earnings      ETH 0.00053167
2021-03-11 00:00:00  Earnings      ETH 0.00053181
2021-03-12 00:00:00  Earnings      ETH 0.00053195
2021-03-13 00:00:00  Earnings      ETH 0.00053209
2021-03-14 00:00:00  Earnings      ETH 0.00053223
2021-03-15 00:00:00  Earnings      ETH 0.00053237
2021-03-16 00:00:00  Earnings      ETH 0.00053251
2021-03-17 00:00:00  Earnings      ETH 0.00053265
2021-03-18 00:00:00  Earnings      ETH 0.00053278
2021-03-19 00:00:00  Earnings      ETH 0.00053292
2021-03-20 00:00:00  Earnings      ETH 0.00053306
2021-03-21 00:00:00  Earnings      ETH 0.00053320
2021-03-22 00:00:00  Earnings      ETH 0.00053334
2021-03-23 00:00:00  Earnings      ETH 0.00053348
2021-03-24 00:00:00  Earnings      ETH 0.00053362
2021-03-25 00:00:00  Earnings      ETH 0.00053376
2021-03-26 00:00:00  Earnings      ETH 0.00053390
2021-03-27 00:00:00  Earnings      ETH 0.00053404
2021-03-28 00:00:00  Earnings      ETH 0.00053418
2021-03-29 00:00:00  Earnings      ETH 0.00053432
2021-03-30 00:00:00  Earnings      ETH 0.00053446
2021-03-31 00:00:00  Earnings      ETH 0.00053460
TOTAL                                  0.04755894
'''
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(sbEarningsTotalDfActualStr)

			sys.stdout = stdout

			self.assertEqual(sbEarningsTotalDfExpectedStr, capturedStdoutStr.getvalue())

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents. All values checked !')
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values checked !')
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			yieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF: ', yieldFiat_CHF)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF: ', yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF: ', actValPlusYieldFiat_CHF)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF: ', capitalGainFiat_CHF)
			capitalGainFiat_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent: ', capitalGainFiat_CHF_percent)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_TOTAL: ', capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_TOTAL: ', capitalGainFiat_CHF_percent_TOTAL)
			yieldCrypto = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto: ', yieldCrypto)
			yieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent: ', yieldPercent)
			yearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent: ', yearlyYieldPercent)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent: ', averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount: ', dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount: ', monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount: ', yearlyYieldAmount)
		else:
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(8000, depWithdrTotal_CHF)
			yieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiat_CHF)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiat_CHF)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215,actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215,actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiat_CHF)
			capitalGainFiat_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiat_CHF_percent)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiat_CHF_percent_TOTAL)
			yieldCrypto = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.04755893617130358, yieldCrypto)
			yieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(2.377946808565179, yieldPercent)
			yearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001275, yearlyYieldPercent)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001275, averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			self.assertEqual(2.138944571576905, dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			self.assertEqual(64.41192244558276, monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(819.0235744686258, yearlyYieldAmount)

	def testAddFiatConversionInfo_ETH_2_fiats_1_owner_1_deposit_french_language(self):
		"""
		ETH crypto, 1 owner with 1 deposit. Testing crypto yield amount,
		crypto yield amount in percent, day, month and year yields in CHF.
		ETH/CHF curr rate == 4000. Yield fixed rate of 10 % per year.
		"""
		PRINT = False

		sbAccountSheetFileName = 'test_ETH_SB_simplevalue_1_owner_1_deposit.xlsx'
		depositSheetFileName = 'test_Eth_CHF_EUR_simplevalue_1_owner_1_deposit.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_ETH
		testLanguage = FR
		fiat = 'CHF'

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName,
									   sbAccountSheetFiat=fiat)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(),
														  self.cryptoFiatCsvFilePathName),
								   language=testLanguage)

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

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			sbEarningsTotalDfExpectedStr = \
'''                         Type Currency Net amount
Local time                                       
2021-01-01 00:00:00  Earnings      ETH 0.00052232
2021-01-02 00:00:00  Earnings      ETH 0.00052245
2021-01-03 00:00:00  Earnings      ETH 0.00052259
2021-01-04 00:00:00  Earnings      ETH 0.00052273
2021-01-05 00:00:00  Earnings      ETH 0.00052286
2021-01-06 00:00:00  Earnings      ETH 0.00052300
2021-01-07 00:00:00  Earnings      ETH 0.00052313
2021-01-08 00:00:00  Earnings      ETH 0.00052327
2021-01-09 00:00:00  Earnings      ETH 0.00052341
2021-01-10 00:00:00  Earnings      ETH 0.00052354
2021-01-11 00:00:00  Earnings      ETH 0.00052368
2021-01-12 00:00:00  Earnings      ETH 0.00052382
2021-01-13 00:00:00  Earnings      ETH 0.00052395
2021-01-14 00:00:00  Earnings      ETH 0.00052409
2021-01-15 00:00:00  Earnings      ETH 0.00052423
2021-01-16 00:00:00  Earnings      ETH 0.00052437
2021-01-17 00:00:00  Earnings      ETH 0.00052450
2021-01-18 00:00:00  Earnings      ETH 0.00052464
2021-01-19 00:00:00  Earnings      ETH 0.00052478
2021-01-20 00:00:00  Earnings      ETH 0.00052491
2021-01-21 00:00:00  Earnings      ETH 0.00052505
2021-01-22 00:00:00  Earnings      ETH 0.00052519
2021-01-23 00:00:00  Earnings      ETH 0.00052532
2021-01-24 00:00:00  Earnings      ETH 0.00052546
2021-01-25 00:00:00  Earnings      ETH 0.00052560
2021-01-26 00:00:00  Earnings      ETH 0.00052574
2021-01-27 00:00:00  Earnings      ETH 0.00052587
2021-01-28 00:00:00  Earnings      ETH 0.00052601
2021-01-29 00:00:00  Earnings      ETH 0.00052615
2021-01-30 00:00:00  Earnings      ETH 0.00052629
2021-01-31 00:00:00  Earnings      ETH 0.00052642
2021-02-01 00:00:00  Earnings      ETH 0.00052656
2021-02-02 00:00:00  Earnings      ETH 0.00052670
2021-02-03 00:00:00  Earnings      ETH 0.00052684
2021-02-04 00:00:00  Earnings      ETH 0.00052697
2021-02-05 00:00:00  Earnings      ETH 0.00052711
2021-02-06 00:00:00  Earnings      ETH 0.00052725
2021-02-07 00:00:00  Earnings      ETH 0.00052739
2021-02-08 00:00:00  Earnings      ETH 0.00052752
2021-02-09 00:00:00  Earnings      ETH 0.00052766
2021-02-10 00:00:00  Earnings      ETH 0.00052780
2021-02-11 00:00:00  Earnings      ETH 0.00052794
2021-02-12 00:00:00  Earnings      ETH 0.00052808
2021-02-13 00:00:00  Earnings      ETH 0.00052821
2021-02-14 00:00:00  Earnings      ETH 0.00052835
2021-02-15 00:00:00  Earnings      ETH 0.00052849
2021-02-16 00:00:00  Earnings      ETH 0.00052863
2021-02-17 00:00:00  Earnings      ETH 0.00052877
2021-02-18 00:00:00  Earnings      ETH 0.00052890
2021-02-19 00:00:00  Earnings      ETH 0.00052904
2021-02-20 00:00:00  Earnings      ETH 0.00052918
2021-02-21 00:00:00  Earnings      ETH 0.00052932
2021-02-22 00:00:00  Earnings      ETH 0.00052946
2021-02-23 00:00:00  Earnings      ETH 0.00052959
2021-02-24 00:00:00  Earnings      ETH 0.00052973
2021-02-25 00:00:00  Earnings      ETH 0.00052987
2021-02-26 00:00:00  Earnings      ETH 0.00053001
2021-02-27 00:00:00  Earnings      ETH 0.00053015
2021-02-28 00:00:00  Earnings      ETH 0.00053029
2021-03-01 00:00:00  Earnings      ETH 0.00053043
2021-03-02 00:00:00  Earnings      ETH 0.00053056
2021-03-03 00:00:00  Earnings      ETH 0.00053070
2021-03-04 00:00:00  Earnings      ETH 0.00053084
2021-03-05 00:00:00  Earnings      ETH 0.00053098
2021-03-06 00:00:00  Earnings      ETH 0.00053112
2021-03-07 00:00:00  Earnings      ETH 0.00053126
2021-03-08 00:00:00  Earnings      ETH 0.00053140
2021-03-09 00:00:00  Earnings      ETH 0.00053153
2021-03-10 00:00:00  Earnings      ETH 0.00053167
2021-03-11 00:00:00  Earnings      ETH 0.00053181
2021-03-12 00:00:00  Earnings      ETH 0.00053195
2021-03-13 00:00:00  Earnings      ETH 0.00053209
2021-03-14 00:00:00  Earnings      ETH 0.00053223
2021-03-15 00:00:00  Earnings      ETH 0.00053237
2021-03-16 00:00:00  Earnings      ETH 0.00053251
2021-03-17 00:00:00  Earnings      ETH 0.00053265
2021-03-18 00:00:00  Earnings      ETH 0.00053278
2021-03-19 00:00:00  Earnings      ETH 0.00053292
2021-03-20 00:00:00  Earnings      ETH 0.00053306
2021-03-21 00:00:00  Earnings      ETH 0.00053320
2021-03-22 00:00:00  Earnings      ETH 0.00053334
2021-03-23 00:00:00  Earnings      ETH 0.00053348
2021-03-24 00:00:00  Earnings      ETH 0.00053362
2021-03-25 00:00:00  Earnings      ETH 0.00053376
2021-03-26 00:00:00  Earnings      ETH 0.00053390
2021-03-27 00:00:00  Earnings      ETH 0.00053404
2021-03-28 00:00:00  Earnings      ETH 0.00053418
2021-03-29 00:00:00  Earnings      ETH 0.00053432
2021-03-30 00:00:00  Earnings      ETH 0.00053446
2021-03-31 00:00:00  Earnings      ETH 0.00053460
TOTAL                                  0.04755894
'''
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(sbEarningsTotalDfActualStr)

			sys.stdout = stdout

			self.assertEqual(sbEarningsTotalDfExpectedStr, capturedStdoutStr.getvalue())

		if PRINT:
			print('\nOwner detailed deposit/withdrawal yield totals and percents. All values checked !')
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values NOT checked !')
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			yieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF: ', yieldFiat_CHF)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF: ', yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' ']['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF: ', actValPlusYieldFiat_CHF)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' ']['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' ']['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			yieldCrypto = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			capitalGainFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF: ', capitalGainFiat_CHF)
			capitalGainFiat_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent: ', capitalGainFiat_CHF_percent)
			print('yieldCrypto: ', yieldCrypto)
			yieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent: ', yieldPercent)
			yearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent: ', yearlyYieldPercent)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent: ', averageYearlyYieldPercent)
			dailyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]][0]
			print('dailyYieldAmount_CHF: ', dailyYieldAmount_CHF)
			monthlyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]][0]
			print('monthlyYieldAmount_CHF: ', monthlyYieldAmount_CHF)
			yearlyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + 'CHF' + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_CHF: ', yearlyYieldAmount_CHF)
			dailyYieldAmount_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]][1]
			print('dailyYieldAmount_EUR: ', dailyYieldAmount_EUR)
			monthlyYieldAmount_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]][1]
			print('monthlyYieldAmount_EUR: ', monthlyYieldAmount_EUR)
			yearlyYieldAmount_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + 'EUR' + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_EUR: ', yearlyYieldAmount_EUR)
		else:
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(8000, depWithdrTotal_CHF)
			yieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiat_CHF)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' ']['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiat_CHF)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' ']['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' ']['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiat_CHF)
			capitalGainFiat_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiat_CHF_percent)
			yieldCrypto = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.04755893617130358, yieldCrypto)
			yieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(151.42857142857142, yieldPercent)
			yearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001275, yearlyYieldPercent)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001275, averageYearlyYieldPercent)
			dailyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]][0]
			self.assertEqual(2.138944571576905, dailyYieldAmount_CHF)
			monthlyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]][0]
			self.assertEqual(64.41192244558276, monthlyYieldAmount_CHF)
			yearlyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + 'CHF' + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(819.0235744686258, yearlyYieldAmount_CHF)
			dailyYieldAmount_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]][1]
			self.assertEqual(1.8822712229876761, dailyYieldAmount_EUR)
			monthlyYieldAmount_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]][1]
			self.assertEqual(56.682491752112824, monthlyYieldAmount_EUR)
			yearlyYieldAmount_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + 'EUR' + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(720.7407455323907, yearlyYieldAmount_EUR)

	def testAddFiatConversionInfo_ETH_1_fiat_1_owner_2_deposits_english_language(self):
		"""
		ETH crypto, 1 owner with 2 deposits. Testing crypto yield amount,
		crypto yield amount in percent, day, month and year yields in CHF.
		ETH/CHF curr rate == 4000. Yield fixed rate of 10 % per year.
		"""
		PRINT = False

		sbAccountSheetFileName = 'test_ETH_SB_simplevalue_1_owner_2_deposits.xlsx'
		depositSheetFileName = 'test_Eth_CHF_simplevalue_1_owner_2_deposits.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_ETH
		testLanguage = GB
		fiat = 'CHF'

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName,
									   sbAccountSheetFiat=fiat)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(),
														  self.cryptoFiatCsvFilePathName),
								   language=testLanguage)

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

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			sbEarningsTotalDfExpectedStr = \
'''                         Type Currency Net amount
Local time                                       
2021-01-01 00:00:00  Earnings      ETH 0.00052232
2021-01-02 00:00:00  Earnings      ETH 0.00052245
2021-01-03 00:00:00  Earnings      ETH 0.00052259
2021-01-04 00:00:00  Earnings      ETH 0.00052273
2021-01-05 00:00:00  Earnings      ETH 0.00052286
2021-01-06 00:00:00  Earnings      ETH 0.00052300
2021-01-07 00:00:00  Earnings      ETH 0.00052313
2021-01-08 00:00:00  Earnings      ETH 0.00052327
2021-01-09 00:00:00  Earnings      ETH 0.00052341
2021-01-10 00:00:00  Earnings      ETH 0.00052354
2021-01-11 00:00:00  Earnings      ETH 0.00052368
2021-01-12 00:00:00  Earnings      ETH 0.00052382
2021-01-13 00:00:00  Earnings      ETH 0.00052395
2021-01-14 00:00:00  Earnings      ETH 0.00052409
2021-01-15 00:00:00  Earnings      ETH 0.00052423
2021-01-16 00:00:00  Earnings      ETH 0.00052437
2021-01-17 00:00:00  Earnings      ETH 0.00052450
2021-01-18 00:00:00  Earnings      ETH 0.00052464
2021-01-19 00:00:00  Earnings      ETH 0.00052478
2021-01-20 00:00:00  Earnings      ETH 0.00052491
2021-01-21 00:00:00  Earnings      ETH 0.00052505
2021-01-22 00:00:00  Earnings      ETH 0.00052519
2021-01-23 00:00:00  Earnings      ETH 0.00052532
2021-01-24 00:00:00  Earnings      ETH 0.00052546
2021-01-25 00:00:00  Earnings      ETH 0.00052560
2021-01-26 00:00:00  Earnings      ETH 0.00052574
2021-01-27 00:00:00  Earnings      ETH 0.00052587
2021-01-28 00:00:00  Earnings      ETH 0.00052601
2021-01-29 00:00:00  Earnings      ETH 0.00052615
2021-01-30 00:00:00  Earnings      ETH 0.00052629
2021-01-31 00:00:00  Earnings      ETH 0.00052642
2021-02-01 00:00:00  Earnings      ETH 0.00052656
2021-02-02 00:00:00  Earnings      ETH 0.00052670
2021-02-03 00:00:00  Earnings      ETH 0.00052684
2021-02-04 00:00:00  Earnings      ETH 0.00052697
2021-02-05 00:00:00  Earnings      ETH 0.00052711
2021-02-06 00:00:00  Earnings      ETH 0.00052725
2021-02-07 00:00:00  Earnings      ETH 0.00052739
2021-02-08 00:00:00  Earnings      ETH 0.00052752
2021-02-09 00:00:00  Earnings      ETH 0.00052766
2021-02-10 00:00:00  Earnings      ETH 0.00052780
2021-02-11 00:00:00  Earnings      ETH 0.00052794
2021-02-12 00:00:00  Earnings      ETH 0.00052808
2021-02-13 00:00:00  Earnings      ETH 0.00052821
2021-02-14 00:00:00  Earnings      ETH 0.00052835
2021-02-15 00:00:00  Earnings      ETH 0.00052849
2021-02-16 00:00:00  Earnings      ETH 0.00052863
2021-02-17 00:00:00  Earnings      ETH 0.00052877
2021-02-18 00:00:00  Earnings      ETH 0.00052890
2021-02-19 00:00:00  Earnings      ETH 0.00052904
2021-02-20 00:00:00  Earnings      ETH 0.00052918
2021-02-21 00:00:00  Earnings      ETH 0.00052932
2021-02-22 00:00:00  Earnings      ETH 0.00052946
2021-02-23 00:00:00  Earnings      ETH 0.00052959
2021-02-24 00:00:00  Earnings      ETH 0.00052973
2021-02-25 00:00:00  Earnings      ETH 0.00052987
2021-02-26 00:00:00  Earnings      ETH 0.00053001
2021-02-27 00:00:00  Earnings      ETH 0.00053015
2021-02-28 00:00:00  Earnings      ETH 0.00053029
2021-03-01 00:00:00  Earnings      ETH 0.00053043
2021-03-02 00:00:00  Earnings      ETH 0.00053056
2021-03-03 00:00:00  Earnings      ETH 0.00053070
2021-03-04 00:00:00  Earnings      ETH 0.00053084
2021-03-05 00:00:00  Earnings      ETH 0.00053098
2021-03-06 00:00:00  Earnings      ETH 0.00053112
2021-03-07 00:00:00  Earnings      ETH 0.00053126
2021-03-08 00:00:00  Earnings      ETH 0.00053140
2021-03-09 00:00:00  Earnings      ETH 0.00053153
2021-03-10 00:00:00  Earnings      ETH 0.00053167
2021-03-11 00:00:00  Earnings      ETH 0.00053181
2021-03-12 00:00:00  Earnings      ETH 0.00053195
2021-03-13 00:00:00  Earnings      ETH 0.00053209
2021-03-14 00:00:00  Earnings      ETH 0.00053223
2021-03-15 00:00:00  Earnings      ETH 0.00053237
2021-03-16 00:00:00  Earnings      ETH 0.00053251
2021-03-17 00:00:00  Earnings      ETH 0.00053265
2021-03-18 00:00:00  Earnings      ETH 0.00053278
2021-03-19 00:00:00  Earnings      ETH 0.00053292
2021-03-20 00:00:00  Earnings      ETH 0.00053306
2021-03-21 00:00:00  Earnings      ETH 0.00053320
2021-03-22 00:00:00  Earnings      ETH 0.00053334
2021-03-23 00:00:00  Earnings      ETH 0.00053348
2021-03-24 00:00:00  Earnings      ETH 0.00053362
2021-03-25 00:00:00  Earnings      ETH 0.00053376
2021-03-26 00:00:00  Earnings      ETH 0.00053390
2021-03-27 00:00:00  Earnings      ETH 0.00053404
2021-03-28 00:00:00  Earnings      ETH 0.00053418
2021-03-29 00:00:00  Earnings      ETH 0.00053432
2021-03-30 00:00:00  Earnings      ETH 0.00053446
2021-03-31 00:00:00  Earnings      ETH 0.00053460
2021-04-01 00:00:00  Earnings      ETH 0.00079589
2021-04-02 00:00:00  Earnings      ETH 0.00079610
2021-04-03 00:00:00  Earnings      ETH 0.00079631
2021-04-04 00:00:00  Earnings      ETH 0.00079652
2021-04-05 00:00:00  Earnings      ETH 0.00079673
2021-04-06 00:00:00  Earnings      ETH 0.00079693
2021-04-07 00:00:00  Earnings      ETH 0.00079714
2021-04-08 00:00:00  Earnings      ETH 0.00079735
2021-04-09 00:00:00  Earnings      ETH 0.00079756
2021-04-10 00:00:00  Earnings      ETH 0.00079777
2021-04-11 00:00:00  Earnings      ETH 0.00079798
2021-04-12 00:00:00  Earnings      ETH 0.00079818
2021-04-13 00:00:00  Earnings      ETH 0.00079839
2021-04-14 00:00:00  Earnings      ETH 0.00079860
2021-04-15 00:00:00  Earnings      ETH 0.00079881
2021-04-16 00:00:00  Earnings      ETH 0.00079902
2021-04-17 00:00:00  Earnings      ETH 0.00079923
2021-04-18 00:00:00  Earnings      ETH 0.00079943
2021-04-19 00:00:00  Earnings      ETH 0.00079964
2021-04-20 00:00:00  Earnings      ETH 0.00079985
2021-04-21 00:00:00  Earnings      ETH 0.00080006
2021-04-22 00:00:00  Earnings      ETH 0.00080027
2021-04-23 00:00:00  Earnings      ETH 0.00080048
2021-04-24 00:00:00  Earnings      ETH 0.00080069
2021-04-25 00:00:00  Earnings      ETH 0.00080090
2021-04-26 00:00:00  Earnings      ETH 0.00080111
2021-04-27 00:00:00  Earnings      ETH 0.00080132
2021-04-28 00:00:00  Earnings      ETH 0.00080153
2021-04-29 00:00:00  Earnings      ETH 0.00080173
2021-04-30 00:00:00  Earnings      ETH 0.00080194
2021-05-01 00:00:00  Earnings      ETH 0.00080215
2021-05-02 00:00:00  Earnings      ETH 0.00080236
2021-05-03 00:00:00  Earnings      ETH 0.00080257
2021-05-04 00:00:00  Earnings      ETH 0.00080278
2021-05-05 00:00:00  Earnings      ETH 0.00080299
2021-05-06 00:00:00  Earnings      ETH 0.00080320
2021-05-07 00:00:00  Earnings      ETH 0.00080341
2021-05-08 00:00:00  Earnings      ETH 0.00080362
2021-05-09 00:00:00  Earnings      ETH 0.00080383
2021-05-10 00:00:00  Earnings      ETH 0.00080404
2021-05-11 00:00:00  Earnings      ETH 0.00080425
2021-05-12 00:00:00  Earnings      ETH 0.00080446
2021-05-13 00:00:00  Earnings      ETH 0.00080467
2021-05-14 00:00:00  Earnings      ETH 0.00080488
2021-05-15 00:00:00  Earnings      ETH 0.00080509
2021-05-16 00:00:00  Earnings      ETH 0.00080530
2021-05-17 00:00:00  Earnings      ETH 0.00080551
2021-05-18 00:00:00  Earnings      ETH 0.00080572
2021-05-19 00:00:00  Earnings      ETH 0.00080593
2021-05-20 00:00:00  Earnings      ETH 0.00080614
2021-05-21 00:00:00  Earnings      ETH 0.00080635
2021-05-22 00:00:00  Earnings      ETH 0.00080656
2021-05-23 00:00:00  Earnings      ETH 0.00080677
2021-05-24 00:00:00  Earnings      ETH 0.00080699
2021-05-25 00:00:00  Earnings      ETH 0.00080720
2021-05-26 00:00:00  Earnings      ETH 0.00080741
2021-05-27 00:00:00  Earnings      ETH 0.00080762
2021-05-28 00:00:00  Earnings      ETH 0.00080783
2021-05-29 00:00:00  Earnings      ETH 0.00080804
2021-05-30 00:00:00  Earnings      ETH 0.00080825
2021-05-31 00:00:00  Earnings      ETH 0.00080846
2021-06-01 00:00:00  Earnings      ETH 0.00080867
2021-06-02 00:00:00  Earnings      ETH 0.00080888
2021-06-03 00:00:00  Earnings      ETH 0.00080910
2021-06-04 00:00:00  Earnings      ETH 0.00080931
2021-06-05 00:00:00  Earnings      ETH 0.00080952
2021-06-06 00:00:00  Earnings      ETH 0.00080973
2021-06-07 00:00:00  Earnings      ETH 0.00080994
2021-06-08 00:00:00  Earnings      ETH 0.00081015
2021-06-09 00:00:00  Earnings      ETH 0.00081036
2021-06-10 00:00:00  Earnings      ETH 0.00081058
2021-06-11 00:00:00  Earnings      ETH 0.00081079
2021-06-12 00:00:00  Earnings      ETH 0.00081100
2021-06-13 00:00:00  Earnings      ETH 0.00081121
2021-06-14 00:00:00  Earnings      ETH 0.00081142
2021-06-15 00:00:00  Earnings      ETH 0.00081163
2021-06-16 00:00:00  Earnings      ETH 0.00081185
2021-06-17 00:00:00  Earnings      ETH 0.00081206
2021-06-18 00:00:00  Earnings      ETH 0.00081227
2021-06-19 00:00:00  Earnings      ETH 0.00081248
2021-06-20 00:00:00  Earnings      ETH 0.00081270
2021-06-21 00:00:00  Earnings      ETH 0.00081291
2021-06-22 00:00:00  Earnings      ETH 0.00081312
2021-06-23 00:00:00  Earnings      ETH 0.00081333
2021-06-24 00:00:00  Earnings      ETH 0.00081354
2021-06-25 00:00:00  Earnings      ETH 0.00081376
2021-06-26 00:00:00  Earnings      ETH 0.00081397
2021-06-27 00:00:00  Earnings      ETH 0.00081418
2021-06-28 00:00:00  Earnings      ETH 0.00081439
2021-06-29 00:00:00  Earnings      ETH 0.00081461
2021-06-30 00:00:00  Earnings      ETH 0.00081482
TOTAL                                  0.12084309
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
			print('\nAll values checked !')
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_1: ', yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_2: ', yieldFiat_CHF_2)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF: ', yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_1: ', actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_2: ', actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_1: ', capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_1: ', capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_2: ', capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_2: ', capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_TOTAL: ', capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_TOTAL: ', capitalGainFiat_CHF_percent_TOTAL)
			yieldCrypto_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_1: ', yieldCrypto_1)
			yieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_1: ', yieldPercent_1)
			yieldCrypto_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_2: ', yieldCrypto_2)
			yieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_2: ', yieldPercent_2)
			yearlyYieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_1: ', yearlyYieldPercent_1)
			yearlyYieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_2: ', yearlyYieldPercent_2)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent: ', averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount: ', dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount: ', monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount: ', yearlyYieldAmount)
		else:
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(12000, depWithdrTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(293.13660166886103, yieldFiat_CHF_2)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(483.3723463540753, yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(483.3723463540753, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(12483.372346354075, actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(12483.372346354075,actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(12483.372346354075,actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(2000.0, capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(100.0, capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(7000.0, capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(140.0, capitalGainFiat_CHF_percent_TOTAL)
			yieldCrypto_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.04755893617130358, yieldCrypto_1)
			yieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(2.377946808565179, yieldPercent_1)
			yieldCrypto_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.07328415041721525, yieldCrypto_2)
			yieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(2.4046836157099327, yieldPercent_2)
			yearlyYieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001275, yearlyYieldPercent_1)
			yearlyYieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001453, yearlyYieldPercent_2)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001364, averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			self.assertEqual(3.2601310081378543, dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			self.assertEqual(98.17519745441653, monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(1248.3372346355777, yearlyYieldAmount)


	def testAddFiatConversionInfo_ETH_1_fiat_1_owner_3_deposits_french_language(self):
		"""
		ETH crypto, 1 owner with 3 deposits. Testing crypto yield amount,
		crypto yield amount in percent, day, month and year yields in CHF.
		ETH/CHF curr rate == 4000. Yield fixed rate of 10 % per year.
		"""
		PRINT = False

		sbAccountSheetFileName = 'test_ETH_SB_simplevalue_1_owner_3_deposits.xlsx'
		depositSheetFileName = 'test_Eth_CHF_simplevalue_1_owner_3_deposits.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_ETH
		testLanguage = FR
		fiat = 'CHF'

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName,
									   sbAccountSheetFiat=fiat)

		self.processor = Processor(self.yieldRateComputer,
								   self.ownerDepositYieldComputer,
								   CryptoFiatRateComputer(PriceRequesterTestStub(),
														  self.cryptoFiatCsvFilePathName),
								   language=testLanguage)

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

		if PRINT:
			if PRINT_SB_EARNING_TOTALS:
				print(sbEarningsTotalDfActualStr)
		else:
			sbEarningsTotalDfExpectedStr = \
'''                         Type Currency Net amount
Local time                                       
2021-01-01 00:00:00  Earnings      ETH 0.00052232
2021-01-02 00:00:00  Earnings      ETH 0.00052245
2021-01-03 00:00:00  Earnings      ETH 0.00052259
2021-01-04 00:00:00  Earnings      ETH 0.00052273
2021-01-05 00:00:00  Earnings      ETH 0.00052286
2021-01-06 00:00:00  Earnings      ETH 0.00052300
2021-01-07 00:00:00  Earnings      ETH 0.00052313
2021-01-08 00:00:00  Earnings      ETH 0.00052327
2021-01-09 00:00:00  Earnings      ETH 0.00052341
2021-01-10 00:00:00  Earnings      ETH 0.00052354
2021-01-11 00:00:00  Earnings      ETH 0.00052368
2021-01-12 00:00:00  Earnings      ETH 0.00052382
2021-01-13 00:00:00  Earnings      ETH 0.00052395
2021-01-14 00:00:00  Earnings      ETH 0.00052409
2021-01-15 00:00:00  Earnings      ETH 0.00052423
2021-01-16 00:00:00  Earnings      ETH 0.00052437
2021-01-17 00:00:00  Earnings      ETH 0.00052450
2021-01-18 00:00:00  Earnings      ETH 0.00052464
2021-01-19 00:00:00  Earnings      ETH 0.00052478
2021-01-20 00:00:00  Earnings      ETH 0.00052491
2021-01-21 00:00:00  Earnings      ETH 0.00052505
2021-01-22 00:00:00  Earnings      ETH 0.00052519
2021-01-23 00:00:00  Earnings      ETH 0.00052532
2021-01-24 00:00:00  Earnings      ETH 0.00052546
2021-01-25 00:00:00  Earnings      ETH 0.00052560
2021-01-26 00:00:00  Earnings      ETH 0.00052574
2021-01-27 00:00:00  Earnings      ETH 0.00052587
2021-01-28 00:00:00  Earnings      ETH 0.00052601
2021-01-29 00:00:00  Earnings      ETH 0.00052615
2021-01-30 00:00:00  Earnings      ETH 0.00052629
2021-01-31 00:00:00  Earnings      ETH 0.00052642
2021-02-01 00:00:00  Earnings      ETH 0.00052656
2021-02-02 00:00:00  Earnings      ETH 0.00052670
2021-02-03 00:00:00  Earnings      ETH 0.00052684
2021-02-04 00:00:00  Earnings      ETH 0.00052697
2021-02-05 00:00:00  Earnings      ETH 0.00052711
2021-02-06 00:00:00  Earnings      ETH 0.00052725
2021-02-07 00:00:00  Earnings      ETH 0.00052739
2021-02-08 00:00:00  Earnings      ETH 0.00052752
2021-02-09 00:00:00  Earnings      ETH 0.00052766
2021-02-10 00:00:00  Earnings      ETH 0.00052780
2021-02-11 00:00:00  Earnings      ETH 0.00052794
2021-02-12 00:00:00  Earnings      ETH 0.00052808
2021-02-13 00:00:00  Earnings      ETH 0.00052821
2021-02-14 00:00:00  Earnings      ETH 0.00052835
2021-02-15 00:00:00  Earnings      ETH 0.00052849
2021-02-16 00:00:00  Earnings      ETH 0.00052863
2021-02-17 00:00:00  Earnings      ETH 0.00052877
2021-02-18 00:00:00  Earnings      ETH 0.00052890
2021-02-19 00:00:00  Earnings      ETH 0.00052904
2021-02-20 00:00:00  Earnings      ETH 0.00052918
2021-02-21 00:00:00  Earnings      ETH 0.00052932
2021-02-22 00:00:00  Earnings      ETH 0.00052946
2021-02-23 00:00:00  Earnings      ETH 0.00052959
2021-02-24 00:00:00  Earnings      ETH 0.00052973
2021-02-25 00:00:00  Earnings      ETH 0.00052987
2021-02-26 00:00:00  Earnings      ETH 0.00053001
2021-02-27 00:00:00  Earnings      ETH 0.00053015
2021-02-28 00:00:00  Earnings      ETH 0.00053029
2021-03-01 00:00:00  Earnings      ETH 0.00053043
2021-03-02 00:00:00  Earnings      ETH 0.00053056
2021-03-03 00:00:00  Earnings      ETH 0.00053070
2021-03-04 00:00:00  Earnings      ETH 0.00053084
2021-03-05 00:00:00  Earnings      ETH 0.00053098
2021-03-06 00:00:00  Earnings      ETH 0.00053112
2021-03-07 00:00:00  Earnings      ETH 0.00053126
2021-03-08 00:00:00  Earnings      ETH 0.00053140
2021-03-09 00:00:00  Earnings      ETH 0.00053153
2021-03-10 00:00:00  Earnings      ETH 0.00053167
2021-03-11 00:00:00  Earnings      ETH 0.00053181
2021-03-12 00:00:00  Earnings      ETH 0.00053195
2021-03-13 00:00:00  Earnings      ETH 0.00053209
2021-03-14 00:00:00  Earnings      ETH 0.00053223
2021-03-15 00:00:00  Earnings      ETH 0.00053237
2021-03-16 00:00:00  Earnings      ETH 0.00053251
2021-03-17 00:00:00  Earnings      ETH 0.00053265
2021-03-18 00:00:00  Earnings      ETH 0.00053278
2021-03-19 00:00:00  Earnings      ETH 0.00053292
2021-03-20 00:00:00  Earnings      ETH 0.00053306
2021-03-21 00:00:00  Earnings      ETH 0.00053320
2021-03-22 00:00:00  Earnings      ETH 0.00053334
2021-03-23 00:00:00  Earnings      ETH 0.00053348
2021-03-24 00:00:00  Earnings      ETH 0.00053362
2021-03-25 00:00:00  Earnings      ETH 0.00053376
2021-03-26 00:00:00  Earnings      ETH 0.00053390
2021-03-27 00:00:00  Earnings      ETH 0.00053404
2021-03-28 00:00:00  Earnings      ETH 0.00053418
2021-03-29 00:00:00  Earnings      ETH 0.00053432
2021-03-30 00:00:00  Earnings      ETH 0.00053446
2021-03-31 00:00:00  Earnings      ETH 0.00053460
2021-04-01 00:00:00  Earnings      ETH 0.00079589
2021-04-02 00:00:00  Earnings      ETH 0.00079610
2021-04-03 00:00:00  Earnings      ETH 0.00079631
2021-04-04 00:00:00  Earnings      ETH 0.00079652
2021-04-05 00:00:00  Earnings      ETH 0.00079673
2021-04-06 00:00:00  Earnings      ETH 0.00079693
2021-04-07 00:00:00  Earnings      ETH 0.00079714
2021-04-08 00:00:00  Earnings      ETH 0.00079735
2021-04-09 00:00:00  Earnings      ETH 0.00079756
2021-04-10 00:00:00  Earnings      ETH 0.00079777
2021-04-11 00:00:00  Earnings      ETH 0.00079798
2021-04-12 00:00:00  Earnings      ETH 0.00079818
2021-04-13 00:00:00  Earnings      ETH 0.00079839
2021-04-14 00:00:00  Earnings      ETH 0.00079860
2021-04-15 00:00:00  Earnings      ETH 0.00079881
2021-04-16 00:00:00  Earnings      ETH 0.00079902
2021-04-17 00:00:00  Earnings      ETH 0.00079923
2021-04-18 00:00:00  Earnings      ETH 0.00079943
2021-04-19 00:00:00  Earnings      ETH 0.00079964
2021-04-20 00:00:00  Earnings      ETH 0.00079985
2021-04-21 00:00:00  Earnings      ETH 0.00080006
2021-04-22 00:00:00  Earnings      ETH 0.00080027
2021-04-23 00:00:00  Earnings      ETH 0.00080048
2021-04-24 00:00:00  Earnings      ETH 0.00080069
2021-04-25 00:00:00  Earnings      ETH 0.00080090
2021-04-26 00:00:00  Earnings      ETH 0.00080111
2021-04-27 00:00:00  Earnings      ETH 0.00080132
2021-04-28 00:00:00  Earnings      ETH 0.00080153
2021-04-29 00:00:00  Earnings      ETH 0.00080173
2021-04-30 00:00:00  Earnings      ETH 0.00080194
2021-05-01 00:00:00  Earnings      ETH 0.00080215
2021-05-02 00:00:00  Earnings      ETH 0.00080236
2021-05-03 00:00:00  Earnings      ETH 0.00080257
2021-05-04 00:00:00  Earnings      ETH 0.00080278
2021-05-05 00:00:00  Earnings      ETH 0.00080299
2021-05-06 00:00:00  Earnings      ETH 0.00080320
2021-05-07 00:00:00  Earnings      ETH 0.00080341
2021-05-08 00:00:00  Earnings      ETH 0.00080362
2021-05-09 00:00:00  Earnings      ETH 0.00080383
2021-05-10 00:00:00  Earnings      ETH 0.00080404
2021-05-11 00:00:00  Earnings      ETH 0.00080425
2021-05-12 00:00:00  Earnings      ETH 0.00080446
2021-05-13 00:00:00  Earnings      ETH 0.00080467
2021-05-14 00:00:00  Earnings      ETH 0.00080488
2021-05-15 00:00:00  Earnings      ETH 0.00080509
2021-05-16 00:00:00  Earnings      ETH 0.00080530
2021-05-17 00:00:00  Earnings      ETH 0.00080551
2021-05-18 00:00:00  Earnings      ETH 0.00080572
2021-05-19 00:00:00  Earnings      ETH 0.00080593
2021-05-20 00:00:00  Earnings      ETH 0.00080614
2021-05-21 00:00:00  Earnings      ETH 0.00080635
2021-05-22 00:00:00  Earnings      ETH 0.00080656
2021-05-23 00:00:00  Earnings      ETH 0.00080677
2021-05-24 00:00:00  Earnings      ETH 0.00080699
2021-05-25 00:00:00  Earnings      ETH 0.00080720
2021-05-26 00:00:00  Earnings      ETH 0.00080741
2021-05-27 00:00:00  Earnings      ETH 0.00080762
2021-05-28 00:00:00  Earnings      ETH 0.00080783
2021-05-29 00:00:00  Earnings      ETH 0.00080804
2021-05-30 00:00:00  Earnings      ETH 0.00080825
2021-05-31 00:00:00  Earnings      ETH 0.00080846
2021-06-01 00:00:00  Earnings      ETH 0.00080867
2021-06-02 00:00:00  Earnings      ETH 0.00080888
2021-06-03 00:00:00  Earnings      ETH 0.00080910
2021-06-04 00:00:00  Earnings      ETH 0.00080931
2021-06-05 00:00:00  Earnings      ETH 0.00080952
2021-06-06 00:00:00  Earnings      ETH 0.00080973
2021-06-07 00:00:00  Earnings      ETH 0.00080994
2021-06-08 00:00:00  Earnings      ETH 0.00081015
2021-06-09 00:00:00  Earnings      ETH 0.00081036
2021-06-10 00:00:00  Earnings      ETH 0.00081058
2021-06-11 00:00:00  Earnings      ETH 0.00081079
2021-06-12 00:00:00  Earnings      ETH 0.00081100
2021-06-13 00:00:00  Earnings      ETH 0.00081121
2021-06-14 00:00:00  Earnings      ETH 0.00081142
2021-06-15 00:00:00  Earnings      ETH 0.00081163
2021-06-16 00:00:00  Earnings      ETH 0.00081185
2021-06-17 00:00:00  Earnings      ETH 0.00081206
2021-06-18 00:00:00  Earnings      ETH 0.00081227
2021-06-19 00:00:00  Earnings      ETH 0.00081248
2021-06-20 00:00:00  Earnings      ETH 0.00081270
2021-06-21 00:00:00  Earnings      ETH 0.00081291
2021-06-22 00:00:00  Earnings      ETH 0.00081312
2021-06-23 00:00:00  Earnings      ETH 0.00081333
2021-06-24 00:00:00  Earnings      ETH 0.00081354
2021-06-25 00:00:00  Earnings      ETH 0.00081376
2021-06-26 00:00:00  Earnings      ETH 0.00081397
2021-06-27 00:00:00  Earnings      ETH 0.00081418
2021-06-28 00:00:00  Earnings      ETH 0.00081439
2021-06-29 00:00:00  Earnings      ETH 0.00081461
2021-06-30 00:00:00  Earnings      ETH 0.00081482
2021-07-01 00:00:00  Earnings      ETH 0.00107619
2021-07-02 00:00:00  Earnings      ETH 0.00107647
2021-07-03 00:00:00  Earnings      ETH 0.00107675
2021-07-04 00:00:00  Earnings      ETH 0.00107703
2021-07-05 00:00:00  Earnings      ETH 0.00107732
2021-07-06 00:00:00  Earnings      ETH 0.00107760
2021-07-07 00:00:00  Earnings      ETH 0.00107788
2021-07-08 00:00:00  Earnings      ETH 0.00107816
2021-07-09 00:00:00  Earnings      ETH 0.00107844
2021-07-10 00:00:00  Earnings      ETH 0.00107872
2021-07-11 00:00:00  Earnings      ETH 0.00107900
2021-07-12 00:00:00  Earnings      ETH 0.00107929
2021-07-13 00:00:00  Earnings      ETH 0.00107957
2021-07-14 00:00:00  Earnings      ETH 0.00107985
2021-07-15 00:00:00  Earnings      ETH 0.00108013
2021-07-16 00:00:00  Earnings      ETH 0.00108041
2021-07-17 00:00:00  Earnings      ETH 0.00108070
2021-07-18 00:00:00  Earnings      ETH 0.00108098
2021-07-19 00:00:00  Earnings      ETH 0.00108126
2021-07-20 00:00:00  Earnings      ETH 0.00108154
2021-07-21 00:00:00  Earnings      ETH 0.00108183
2021-07-22 00:00:00  Earnings      ETH 0.00108211
2021-07-23 00:00:00  Earnings      ETH 0.00108239
2021-07-24 00:00:00  Earnings      ETH 0.00108267
2021-07-25 00:00:00  Earnings      ETH 0.00108296
2021-07-26 00:00:00  Earnings      ETH 0.00108324
2021-07-27 00:00:00  Earnings      ETH 0.00108352
2021-07-28 00:00:00  Earnings      ETH 0.00108380
2021-07-29 00:00:00  Earnings      ETH 0.00108409
2021-07-30 00:00:00  Earnings      ETH 0.00108437
2021-07-31 00:00:00  Earnings      ETH 0.00108465
TOTAL                                  0.15433602
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
			print('\nAll values checked !')
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_1: ', yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_2: ', yieldFiat_CHF_2)
			yieldFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_3: ', yieldFiat_CHF_3)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF: ', yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_1: ', actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_2: ', actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_3: ',actValPlusYieldFiat_CHF_3)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_1: ', capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_1: ', capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_2: ', capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_2: ', capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_3: ', capitalGainFiat_CHF_3)
			capitalGainFiat_CHF_percent_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_3: ', capitalGainFiat_CHF_percent_3)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_TOTAL: ', capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_TOTAL: ', capitalGainFiat_CHF_percent_TOTAL)
			yieldCrypto_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_1: ', yieldCrypto_1)
			yieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_1: ', yieldPercent_1)
			yieldCrypto_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_2: ', yieldCrypto_2)
			yieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_2: ', yieldPercent_2)
			yieldCrypto_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_3: ', yieldCrypto_3)
			yieldPercent_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_3: ', yieldPercent_3)
			yearlyYieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_1: ', yearlyYieldPercent_1)
			yearlyYieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_2: ', yearlyYieldPercent_2)
			yearlyYieldPercent_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_3: ', yearlyYieldPercent_3)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent: ', averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount: ', dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount: ', monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount: ', yearlyYieldAmount)
		else:
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(16000, depWithdrTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(293.13660166886103, yieldFiat_CHF_2)
			yieldFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(133.97172355601228, yieldFiat_CHF_3)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(617.3440699100876, yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(617.3440699100876, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(12483.372346354075, actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(16617.344069910087,actValPlusYieldFiat_CHF_3)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(16617.344069910087,actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][' '][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(16617.344069910087,actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(2000.0, capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(100.0, capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(1000.0, capitalGainFiat_CHF_3)
			capitalGainFiat_CHF_percent_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(33.33333333333333, capitalGainFiat_CHF_percent_3)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(8000.0, capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(100.0, capitalGainFiat_CHF_percent_TOTAL)
			yieldCrypto_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.04755893617130358, yieldCrypto_1)
			yieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(2.377946808565179, yieldPercent_1)
			yieldCrypto_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.07328415041721525, yieldCrypto_2)
			yieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(2.4046836157099327, yieldPercent_2)
			yieldCrypto_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.03349293088900307, yieldCrypto_3)
			yieldPercent_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(0.812768896685424, yieldPercent_3)
			yearlyYieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001275, yearlyYieldPercent_1)
			yearlyYieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001453, yearlyYieldPercent_2)
			yearlyYieldPercent_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.00000000000032, yearlyYieldPercent_3)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001211, averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			self.assertEqual(4.339750283186255, dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			self.assertEqual(130.68672390500907, monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(1661.7344069912094, yearlyYieldAmount)

if __name__ == '__main__':
	if os.name == 'posix':
		unittest.main()
	else:
		tst = TestProcessorNewStructure()
		# tst.testAddFiatConversionInfo_USDC_2_fiats_simple_values_2_owners_2_deposits_bug_french_language()
		# tst.testAddFiatConversionInfo_USDC_2_fiats_simple_values_2_owners_2_deposits_bug_english_language()
		# tst.testAddFiatConversionInfo_ETH_1_fiat_2_owners_1_and_2_deposits_french_language()
		# tst.testAddFiatConversionInfo_ETH_1_fiat_2_owners_1_and_2_deposits_english_language()
		# tst.testAddFiatConversionInfo_ETH_1_fiat_1_owner_1_deposit_french_language()
		tst.testAddFiatConversionInfo_ETH_2_fiats_1_owner_1_deposit_french_language()
		# tst.testAddFiatConversionInfo_ETH_1_fiat_1_owner_2_deposits_english_language()
		# tst.testAddFiatConversionInfo_ETH_1_fiat_1_owner_3_deposits_french_language()
