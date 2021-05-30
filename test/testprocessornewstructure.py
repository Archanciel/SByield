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
		testLanguage = FR
		fiat = 'CHF'

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

		self.processor.activateHelpNumbers()

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
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values NOT checked !')
			depWithdrDateFrom_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom_owner_1: ', str(depWithdrDateFrom_owner_1))
			depWithdrDateTo_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo_owner_1: ', str(depWithdrDateTo_owner_1))
			depWithdrDateFrom_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom_owner_2: ', str(depWithdrDateFrom_owner_2))
			depWithdrDateTo_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo_owner_2: ', str(depWithdrDateTo_owner_2))
			depWithdr_ETH_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH_owner_1: ', depWithdr_ETH_owner_1)
			depWithdrTotal_ETH_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrTotal_ETH_owner_1: ', depWithdrTotal_ETH_owner_1)
			depWithdr_ETH_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH_owner_2: ', depWithdr_ETH_owner_2)
			depWithdrTotal_ETH_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrTotal_ETH_owner_2: ', depWithdrTotal_ETH_owner_2)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrGrandTotal_ETH: ', depWithdrGrandTotal_ETH)
			depWithdr_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_owner_1: ', depWithdr_CHF_owner_1)
			depWithdrTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdrTotal_CHF_owner_1: ', depWithdrTotal_CHF_owner_1)
			depWithdrActualValue_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_owner_1: ', depWithdrActualValue_CHF_owner_1)
			depWithdrActualValueTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF_owner_1: ', depWithdrActualValueTotal_CHF_owner_1)
			depWithdrActualValue_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_owner_2: ', depWithdrActualValue_CHF_owner_2)
			depWithdrActualValueTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF_owner_2: ', depWithdrActualValueTotal_CHF_owner_2)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueGrandTotal_CHF: ', depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_owner_1: ', yieldFiat_CHF_owner_1)
			yieldFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF_owner_1: ', yieldFiatTotal_CHF_owner_1)
			yieldFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_owner_2: ', yieldFiat_CHF_owner_2)
			yieldFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF_owner_2: ', yieldFiatTotal_CHF_owner_2)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_owner_1: ', actValPlusYieldFiat_CHF_owner_1)
			actValPlusYieldFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF_owner_1: ', actValPlusYieldFiatTotal_CHF_owner_1)
			actValPlusYieldFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_owner_2: ', actValPlusYieldFiat_CHF_owner_2)
			actValPlusYieldFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF_owner_2: ', actValPlusYieldFiatTotal_CHF_owner_2)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_owner_1: ', capitalGainFiat_CHF_owner_1)
			capitalGainFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiatTotal_CHF_owner_1: ', capitalGainFiatTotal_CHF_owner_1)
			capitalGainFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_owner_2: ', capitalGainFiat_CHF_owner_2)
			capitalGainFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiatTotal_CHF_owner_2: ', capitalGainFiatTotal_CHF_owner_2)
			capitalGainFiat_CHF_percent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_owner_1: ', capitalGainFiat_CHF_percent_owner_1)
			capitalGainFiatTotal_CHF_percent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiatTotal_CHF_percent_owner_1: ', capitalGainFiatTotal_CHF_percent_owner_1)
			capitalGainFiat_CHF_percent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_owner_2: ', capitalGainFiat_CHF_percent_owner_2)
			capitalGainFiatTotal_CHF_percent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiatTotal_CHF_percent_owner_2: ', capitalGainFiatTotal_CHF_percent_owner_2)
			yieldDays_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_owner_1: ', yieldDays_owner_1)
			yieldDays_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_owner_2: ', yieldDays_owner_2)
			yieldCrypto_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_owner_1: ', yieldCrypto_owner_1)
			yieldCryptoTotal_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal_owner_1: ', yieldCryptoTotal_owner_1)
			yieldCrypto_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_owner_2: ', yieldCrypto_owner_2)
			yieldCryptoTotal_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal_owner_2: ', yieldCryptoTotal_owner_2)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoGrandTotal: ', yieldCryptoGrandTotal)
			yieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_owner_1: ', yieldPercent_owner_1)
			yieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_owner_2: ', yieldPercent_owner_2)
			yearlyYieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_owner_1: ', yearlyYieldPercent_owner_1)
			averageYearlyYieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent_owner_1: ', averageYearlyYieldPercent_owner_1)
			yearlyYieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_owner_2: ', yearlyYieldPercent_owner_2)
			averageYearlyYieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent_owner_2: ', averageYearlyYieldPercent_owner_2)
			dailyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount_owner_1: ', dailyYieldAmount_owner_1)
			monthlyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount_owner_1: ', monthlyYieldAmount_owner_1)
			yearlyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_owner_1: ', yearlyYieldAmount_owner_1)
			dailyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount_owner_2: ', dailyYieldAmount_owner_2)
			monthlyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount_owner_2: ', monthlyYieldAmount_owner_2)
			yearlyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_owner_2: ', yearlyYieldAmount_owner_2)
		else:
			yieldOwnerWithTotalsDetailDfExpectedStr = \
'''                                                           DÉPÔTS  /  RETRAITS     (2)      (3)      (4)                                                            
                                MONTANT DAT DÉP  DAT ACT VAL DAT DÉP   VAL ACT VAL ACT  VAL ACT PLUS-VAL         JOURS  INT                 MONTANT INTÉRÊTS EN CHF 
                 DE           A     ETH ETH/USD  ETH/USD    (1)  CHF       CHF INT CHF  TOT CHF  CAP CHF   EN %    INT  ETH EN %  % ANNUEL PAR JOUR PAR MOIS  PAR AN
PROPR                                                                                                                                                               
Béa      2021-03-23  2021-05-04    0.40 1593.36  4400.00      600.00   1594.25   20.09  1614.34   994.25 165.71     43 0.01 1.26     11.21                          
TOTAL                              0.40                       600.00   1594.25   20.09  1614.34   994.25 165.71        0.01          11.21     0.47    14.16  181.03
Papa     2021-03-20  2021-05-04    4.59 1772.12  4400.00     7583.15  18351.66  256.21 18607.88 10768.51 142.01     46 0.06 1.40     11.63                          
TOTAL                              4.59                      7583.15  18351.66  256.21 18607.88 10768.51 142.01        0.06          11.21     5.42   163.27 2086.68
G TOTAL                            4.99                               19945.92  276.30 20222.22                        0.07                                         
'''
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(yieldOwnerWithTotalsDetailDfActualStr)

			sys.stdout = stdout

			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, capturedStdoutStr.getvalue())

			depWithdrDateFrom_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-03-23', str(depWithdrDateFrom_owner_1))
			depWithdrDateTo_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-05-04', str(depWithdrDateTo_owner_1))
			depWithdrDateFrom_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-03-20', str(depWithdrDateFrom_owner_2))
			depWithdrDateTo_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-05-04', str(depWithdrDateTo_owner_2))
			depWithdr_ETH_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(0.3985632, depWithdr_ETH_owner_1)
			depWithdrTotal_ETH_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(0.3985632, depWithdrTotal_ETH_owner_1)
			depWithdr_ETH_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(4.5879162, depWithdr_ETH_owner_2)
			depWithdrTotal_ETH_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(4.5879162, depWithdrTotal_ETH_owner_2)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(4.9864794, depWithdrGrandTotal_ETH)
			depWithdr_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(600.0, depWithdr_CHF_owner_1)
			depWithdrTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(600.0, depWithdrTotal_CHF_owner_1)
			depWithdrActualValue_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(1594.2528, depWithdrActualValue_CHF_owner_1)
			depWithdrActualValueTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(1594.2528, depWithdrActualValueTotal_CHF_owner_1)
			depWithdrActualValue_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(18351.664800000002, depWithdrActualValue_CHF_owner_2)
			depWithdrActualValueTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(18351.664800000002, depWithdrActualValueTotal_CHF_owner_2)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(19945.9176, depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(20.087631670829165, yieldFiat_CHF_owner_1)
			yieldFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(20.087631670829165, yieldFiatTotal_CHF_owner_1)
			yieldFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(256.21356832915865, yieldFiat_CHF_owner_2)
			yieldFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(256.21356832915865, yieldFiatTotal_CHF_owner_2)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(276.30119999998783, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(1614.340431670829, actValPlusYieldFiat_CHF_owner_1)
			actValPlusYieldFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(1614.340431670829, actValPlusYieldFiatTotal_CHF_owner_1)
			actValPlusYieldFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(18607.878368329162, actValPlusYieldFiat_CHF_owner_2)
			actValPlusYieldFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(18607.878368329162, actValPlusYieldFiatTotal_CHF_owner_2)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(20222.21879999999, actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(994.2528, capitalGainFiat_CHF_owner_1)
			capitalGainFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(994.2528, capitalGainFiatTotal_CHF_owner_1)
			capitalGainFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(10768.514800000003, capitalGainFiat_CHF_owner_2)
			capitalGainFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(10768.514800000003, capitalGainFiatTotal_CHF_owner_2)
			capitalGainFiat_CHF_percent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(165.7088, capitalGainFiat_CHF_percent_owner_1)
			capitalGainFiatTotal_CHF_percent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(165.7088, capitalGainFiatTotal_CHF_percent_owner_1)
			capitalGainFiat_CHF_percent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(142.00582607491614, capitalGainFiat_CHF_percent_owner_2)
			capitalGainFiatTotal_CHF_percent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(142.00582607491614, capitalGainFiatTotal_CHF_percent_owner_2)
			yieldDays_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(43, yieldDays_owner_1)
			yieldDays_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(46, yieldDays_owner_2)
			yieldCrypto_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.005021907917707291, yieldCrypto_owner_1)
			yieldCryptoTotal_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.005021907917707291, yieldCryptoTotal_owner_1)
			yieldCrypto_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.06405339208228966, yieldCrypto_owner_2)
			yieldCryptoTotal_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.06405339208228966, yieldCryptoTotal_owner_2)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.06907529999999695, yieldCryptoGrandTotal)
			yieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(1.2600029098791086, yieldPercent_owner_1)
			yieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(1.3961325641102524, yieldPercent_owner_2)
			yearlyYieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(11.213938294514758, yearlyYieldPercent_owner_1)
			averageYearlyYieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(11.213938294514758, averageYearlyYieldPercent_owner_1)
			yearlyYieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(11.629357415484364, yearlyYieldPercent_owner_2)
			averageYearlyYieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(11.213938294514758, averageYearlyYieldPercent_owner_2)
			dailyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			self.assertEqual(0.4701534690830087, dailyYieldAmount_owner_1)
			monthlyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			self.assertEqual(14.16432886342779, monthlyYieldAmount_owner_1)
			yearlyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(181.03113987096995, yearlyYieldAmount_owner_1)
			dailyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			self.assertEqual(5.419277368956154, dailyYieldAmount_owner_2)
			monthlyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			self.assertEqual(163.2667456559256, monthlyYieldAmount_owner_2)
			yearlyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(2086.6759981427917, yearlyYieldAmount_owner_2)

	def testAddFiatConversionInfo_ETH_1_fiat_2_owners_1_and_2_deposits_english_language(self):
		"""
		ETH crypto, 2 owners, 1 with 1 deposit and the other with 2 deposits
		"""
		PRINT = False

		sbAccountSheetFileName = 'test_ETH_SB_account_statement.xlsx'
		depositSheetFileName = 'test_Eth_2_owners_1_and_2_deposits.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_ETH
		testLanguage = GB
		fiat = 'CHF'

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

		self.processor.activateHelpNumbers()

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
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values NOT checked !')
			depWithdrDateFrom_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom_owner_1: ', str(depWithdrDateFrom_owner_1))
			depWithdrDateTo_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo_owner_1: ', str(depWithdrDateTo_owner_1))
			depWithdrDateFrom_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom_owner_2: ', str(depWithdrDateFrom_owner_2))
			depWithdrDateTo_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo_owner_2: ', str(depWithdrDateTo_owner_2))
			depWithdr_ETH_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH_owner_1: ', depWithdr_ETH_owner_1)
			depWithdrTotal_ETH_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrTotal_ETH_owner_1: ', depWithdrTotal_ETH_owner_1)
			depWithdr_ETH_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH_owner_2: ', depWithdr_ETH_owner_2)
			depWithdrTotal_ETH_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrTotal_ETH_owner_2: ', depWithdrTotal_ETH_owner_2)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrGrandTotal_ETH: ', depWithdrGrandTotal_ETH)
			depWithdr_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_owner_1: ', depWithdr_CHF_owner_1)
			depWithdrTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdrTotal_CHF_owner_1: ', depWithdrTotal_CHF_owner_1)
			depWithdrActualValue_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_owner_1: ', depWithdrActualValue_CHF_owner_1)
			depWithdrActualValueTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF_owner_1: ', depWithdrActualValueTotal_CHF_owner_1)
			depWithdrActualValue_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_owner_2: ', depWithdrActualValue_CHF_owner_2)
			depWithdrActualValueTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF_owner_2: ', depWithdrActualValueTotal_CHF_owner_2)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueGrandTotal_CHF: ', depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_owner_1: ', yieldFiat_CHF_owner_1)
			yieldFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF_owner_1: ', yieldFiatTotal_CHF_owner_1)
			yieldFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_owner_2: ', yieldFiat_CHF_owner_2)
			yieldFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF_owner_2: ', yieldFiatTotal_CHF_owner_2)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_owner_1: ', actValPlusYieldFiat_CHF_owner_1)
			actValPlusYieldFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF_owner_1: ', actValPlusYieldFiatTotal_CHF_owner_1)
			actValPlusYieldFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_owner_2: ', actValPlusYieldFiat_CHF_owner_2)
			actValPlusYieldFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF_owner_2: ', actValPlusYieldFiatTotal_CHF_owner_2)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_owner_1: ', capitalGainFiat_CHF_owner_1)
			capitalGainFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiatTotal_CHF_owner_1: ', capitalGainFiatTotal_CHF_owner_1)
			capitalGainFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_owner_2: ', capitalGainFiat_CHF_owner_2)
			capitalGainFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiatTotal_CHF_owner_2: ', capitalGainFiatTotal_CHF_owner_2)
			capitalGainFiat_CHF_percent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_owner_1: ', capitalGainFiat_CHF_percent_owner_1)
			capitalGainFiatTotal_CHF_percent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiatTotal_CHF_percent_owner_1: ', capitalGainFiatTotal_CHF_percent_owner_1)
			capitalGainFiat_CHF_percent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_owner_2: ', capitalGainFiat_CHF_percent_owner_2)
			capitalGainFiatTotal_CHF_percent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiatTotal_CHF_percent_owner_2: ', capitalGainFiatTotal_CHF_percent_owner_2)
			yieldDays_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_owner_1: ', yieldDays_owner_1)
			yieldDays_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_owner_2: ', yieldDays_owner_2)
			yieldCrypto_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_owner_1: ', yieldCrypto_owner_1)
			yieldCryptoTotal_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal_owner_1: ', yieldCryptoTotal_owner_1)
			yieldCrypto_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_owner_2: ', yieldCrypto_owner_2)
			yieldCryptoTotal_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal_owner_2: ', yieldCryptoTotal_owner_2)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoGrandTotal: ', yieldCryptoGrandTotal)
			yieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_owner_1: ', yieldPercent_owner_1)
			yieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_owner_2: ', yieldPercent_owner_2)
			yearlyYieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_owner_1: ', yearlyYieldPercent_owner_1)
			averageYearlyYieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent_owner_1: ', averageYearlyYieldPercent_owner_1)
			yearlyYieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_owner_2: ', yearlyYieldPercent_owner_2)
			averageYearlyYieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent_owner_2: ', averageYearlyYieldPercent_owner_2)
			dailyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount_owner_1: ', dailyYieldAmount_owner_1)
			monthlyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount_owner_1: ', monthlyYieldAmount_owner_1)
			yearlyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_owner_1: ', yearlyYieldAmount_owner_1)
			dailyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount_owner_2: ', dailyYieldAmount_owner_2)
			monthlyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount_owner_2: ', monthlyYieldAmount_owner_2)
			yearlyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_owner_2: ', yearlyYieldAmount_owner_2)
		else:
			yieldOwnerWithTotalsDetailDfExpectedStr = \
'''                                                         DEPOSITS   /   WITHDRAWALS      (2)       (3)      (4)                                                       
                                AMOUNT DEP RATE CUR RATE     DEP RATE      CUR RATE CUR RATE  CUR RATE CAP GAIN        DAYS  INT              AMOUNT INTERESTS IN CHF 
               FROM          TO    ETH  ETH/USD  ETH/USD     (1)  CHF           CHF  YLD CHF   TOT CHF ONLY CHF   IN %  INT  ETH IN % YRLY % PER DAY PER MONTH  PER YR
OWNER                                                                                                                                                                 
Béa      2021-03-23  2021-05-04   0.40  1593.36  4400.00       600.00       1594.25    20.09   1614.34   994.25 165.71   43 0.01 1.26  11.21                          
TOTAL                             0.40                         600.00       1594.25    20.09   1614.34   994.25 165.71      0.01       11.21    0.47     14.16  181.03
Papa     2021-03-20  2021-05-04   4.59  1772.12  4400.00      7583.15      18351.66   256.21  18607.88 10768.51 142.01   46 0.06 1.40  11.63                          
TOTAL                             4.59                        7583.15      18351.66   256.21  18607.88 10768.51 142.01      0.06       11.21    5.42    163.27 2086.68
G TOTAL                           4.99                                     19945.92   276.30  20222.22                      0.07                                      
'''
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(yieldOwnerWithTotalsDetailDfActualStr)

			sys.stdout = stdout

			self.assertEqual(yieldOwnerWithTotalsDetailDfExpectedStr, capturedStdoutStr.getvalue())

			depWithdrDateFrom_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-03-23', str(depWithdrDateFrom_owner_1))
			depWithdrDateTo_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-05-04', str(depWithdrDateTo_owner_1))
			depWithdrDateFrom_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-03-20', str(depWithdrDateFrom_owner_2))
			depWithdrDateTo_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-05-04', str(depWithdrDateTo_owner_2))
			depWithdr_ETH_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(0.3985632, depWithdr_ETH_owner_1)
			depWithdrTotal_ETH_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(0.3985632, depWithdrTotal_ETH_owner_1)
			depWithdr_ETH_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(4.5879162, depWithdr_ETH_owner_2)
			depWithdrTotal_ETH_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(4.5879162, depWithdrTotal_ETH_owner_2)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(4.9864794, depWithdrGrandTotal_ETH)
			depWithdr_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(600.0, depWithdr_CHF_owner_1)
			depWithdrTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(600.0, depWithdrTotal_CHF_owner_1)
			depWithdrActualValue_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(1594.2528, depWithdrActualValue_CHF_owner_1)
			depWithdrActualValueTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(1594.2528, depWithdrActualValueTotal_CHF_owner_1)
			depWithdrActualValue_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(18351.664800000002, depWithdrActualValue_CHF_owner_2)
			depWithdrActualValueTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(18351.664800000002, depWithdrActualValueTotal_CHF_owner_2)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(19945.9176, depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(20.087631670829165, yieldFiat_CHF_owner_1)
			yieldFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(20.087631670829165, yieldFiatTotal_CHF_owner_1)
			yieldFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(256.21356832915865, yieldFiat_CHF_owner_2)
			yieldFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(256.21356832915865, yieldFiatTotal_CHF_owner_2)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(276.30119999998783, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(1614.340431670829, actValPlusYieldFiat_CHF_owner_1)
			actValPlusYieldFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(1614.340431670829, actValPlusYieldFiatTotal_CHF_owner_1)
			actValPlusYieldFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(18607.878368329162, actValPlusYieldFiat_CHF_owner_2)
			actValPlusYieldFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(18607.878368329162, actValPlusYieldFiatTotal_CHF_owner_2)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(20222.21879999999, actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(994.2528, capitalGainFiat_CHF_owner_1)
			capitalGainFiatTotal_CHF_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(994.2528, capitalGainFiatTotal_CHF_owner_1)
			capitalGainFiat_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(10768.514800000003, capitalGainFiat_CHF_owner_2)
			capitalGainFiatTotal_CHF_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(10768.514800000003, capitalGainFiatTotal_CHF_owner_2)
			capitalGainFiat_CHF_percent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(165.7088, capitalGainFiat_CHF_percent_owner_1)
			capitalGainFiatTotal_CHF_percent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(165.7088, capitalGainFiatTotal_CHF_percent_owner_1)
			capitalGainFiat_CHF_percent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(142.00582607491614, capitalGainFiat_CHF_percent_owner_2)
			capitalGainFiatTotal_CHF_percent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(142.00582607491614, capitalGainFiatTotal_CHF_percent_owner_2)
			yieldDays_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(43, yieldDays_owner_1)
			yieldDays_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(46, yieldDays_owner_2)
			yieldCrypto_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.005021907917707291, yieldCrypto_owner_1)
			yieldCryptoTotal_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.005021907917707291, yieldCryptoTotal_owner_1)
			yieldCrypto_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.06405339208228966, yieldCrypto_owner_2)
			yieldCryptoTotal_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.06405339208228966, yieldCryptoTotal_owner_2)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.06907529999999695, yieldCryptoGrandTotal)
			yieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(1.2600029098791086, yieldPercent_owner_1)
			yieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(1.3961325641102524, yieldPercent_owner_2)
			yearlyYieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(11.213938294514758, yearlyYieldPercent_owner_1)
			averageYearlyYieldPercent_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(11.213938294514758, averageYearlyYieldPercent_owner_1)
			yearlyYieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(11.629357415484364, yearlyYieldPercent_owner_2)
			averageYearlyYieldPercent_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(11.213938294514758, averageYearlyYieldPercent_owner_2)
			dailyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			self.assertEqual(0.4701534690830087, dailyYieldAmount_owner_1)
			monthlyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			self.assertEqual(14.16432886342779, monthlyYieldAmount_owner_1)
			yearlyYieldAmount_owner_1 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(181.03113987096995, yearlyYieldAmount_owner_1)
			dailyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			self.assertEqual(5.419277368956154, dailyYieldAmount_owner_2)
			monthlyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			self.assertEqual(163.2667456559256, monthlyYieldAmount_owner_2)
			yearlyYieldAmount_owner_2 = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(2086.6759981427917, yearlyYieldAmount_owner_2)

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

		self.processor.activateHelpNumbers()

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
'''                                                              DÉPÔTS  /  RETRAITS      (2)       (3)      (4)                                                                                                                                                 
                                 MONTANT  DAT DÉP   DAT ACT VAL DAT DÉP   VAL ACT  VAL ACT   VAL ACT PLUS-VAL       VAL DAT DÉP VAL ACT    VAL ACT     VAL ACT PLUS-VAL        JOURS    INT                 MONTANT INTÉRÊTS EN CHF   MONTANT INTÉRÊTS EN EUR 
                 DE           A     USDC USDC/USD  USDC/USD    (1)  CHF       CHF  INT CHF   TOT CHF  CAP CHF  EN %         EUR     EUR    INT EUR     TOT EUR  CAP EUR  EN %    INT   USDC EN %  % ANNUEL PAR JOUR PAR MOIS  PAR AN PAR JOUR PAR MOIS  PAR AN
PROPR                                                                                                                                                                                                                                                         
Béa      2021-02-20  2021-12-31  4400.00     1.02      1.00     4000.00   4006.20   309.40   4315.60     6.20  0.15     2800.00 3520.00     271.85     3791.85   720.00 25.71    315 339.82 7.72      9.00                                                    
TOTAL                            4400.00                        4000.00   4006.20   309.40   4315.60     6.20  0.15     2800.00 3520.00     271.85     3791.85   720.00 25.71        339.82           9.00     1.02    30.69  388.52     0.90    26.96  341.37
JPS      2021-03-22  2021-04-21  5500.00     0.97      1.00     5000.00   5007.75    37.01   5044.76     7.75  0.15     4500.00 4400.00      32.52     4432.52  -100.00 -2.22     31  40.65 0.74      9.06                                                    
JPS      2021-04-22  2021-12-31 -1000.00     0.92      1.00     -850.00   -910.50   255.24   4389.50   -60.50 -7.12     -800.00 -800.00     224.26     3856.78     0.00  0.00    254 280.32 6.17      8.99                                                    
TOTAL                            4500.00                        4150.00   4097.25   292.25   4389.50   -52.75 -1.27     3700.00 3600.00     256.78     3856.78  -100.00 -2.70        320.98           9.00     1.04    31.19  394.92     0.91    27.41  347.00
G TOTAL                          8900.00                                  8103.45   601.65   8705.10                            7120.00     528.63     7648.63                       660.79                                                                   
'''
		if PRINT:
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

		self.processor.activateHelpNumbers()

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
'''                                                            DEPOSITS   /   WITHDRAWALS       (2)        (3)      (4)                                                                                                                                            
                                  AMOUNT DEP RATE  CUR RATE     DEP RATE      CUR RATE  CUR RATE   CUR RATE CAP GAIN       DEP RATE CUR RATE    CUR RATE     CUR RATE CAP GAIN       DAYS    INT              AMOUNT INTERESTS IN CHF   AMOUNT INTERESTS IN EUR 
               FROM          TO     USDC USDC/USD  USDC/USD     (1)  CHF           CHF   YLD CHF    TOT CHF ONLY CHF  IN %      EUR      EUR     YLD EUR      TOT EUR ONLY EUR  IN %  INT   USDC IN % YRLY % PER DAY PER MONTH  PER YR PER DAY PER MONTH  PER YR
OWNER                                                                                                                                                                                                                                                           
Béa      2021-02-20  2021-12-31  4400.00     1.02      1.00      4000.00       4006.20    309.40    4315.60     6.20  0.15  2800.00  3520.00      271.85      3791.85   720.00 25.71  315 339.82 7.72   9.00                                                    
TOTAL                            4400.00                         4000.00       4006.20    309.40    4315.60     6.20  0.15  2800.00  3520.00      271.85      3791.85   720.00 25.71      339.82        9.00    1.02     30.69  388.52    0.90     26.96  341.37
JPS      2021-03-22  2021-04-21  5500.00     0.97      1.00      5000.00       5007.75     37.01    5044.76     7.75  0.15  4500.00  4400.00       32.52      4432.52  -100.00 -2.22   31  40.65 0.74   9.06                                                    
JPS      2021-04-22  2021-12-31 -1000.00     0.92      1.00      -850.00       -910.50    255.24    4389.50   -60.50 -7.12  -800.00  -800.00      224.26      3856.78     0.00  0.00  254 280.32 6.17   8.99                                                    
TOTAL                            4500.00                         4150.00       4097.25    292.25    4389.50   -52.75 -1.27  3700.00  3600.00      256.78      3856.78  -100.00 -2.70      320.98        9.00    1.04     31.19  394.92    0.91     27.41  347.00
G TOTAL                          8900.00                                       8103.45    601.65    8705.10                          7120.00      528.63      7648.63                     660.79                                                                
'''
		if PRINT:
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
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values checked !')
			depWithdrDateFrom = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom: ', str(depWithdrDateFrom))
			depWithdrDateTo = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo: ', depWithdrDateTo)
			depWithdr_ETH = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH: ', depWithdr_ETH)
			depWithdrTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrTotal_ETH: ', depWithdrTotal_ETH)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrGrandTotal_ETH: ', depWithdrGrandTotal_ETH)
			depWithdr_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF: ', depWithdr_CHF)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			depWithdrActualValue_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF: ', depWithdrActualValue_CHF)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF: ', depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueGrandTotal_CHF: ', depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF: ', yieldFiat_CHF)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF: ', yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF: ', actValPlusYieldFiat_CHF)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF: ', capitalGainFiat_CHF)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_TOTAL: ', capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent: ', capitalGainFiat_CHF_percent)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_TOTAL: ', capitalGainFiat_CHF_percent_TOTAL)
			yieldDays = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays: ', yieldDays)
			yieldCrypto = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto: ', yieldCrypto)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal: ', yieldCryptoTotal)
			yieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent: ', yieldPercent)
			yearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent: ', yearlyYieldPercent)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent: ', averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount_owner_1: ', dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount_owner_1: ', monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_owner_1: ', yearlyYieldAmount)
		else:
			dep_withdr_date_from = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-01-01', str(dep_withdr_date_from))
			depWithdrDateTo = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-03-31', str(depWithdrDateTo))
			depWithdr_ETH = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(2.0, depWithdr_ETH)
			depWithdrTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(2.0, depWithdrTotal_ETH)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(2.0, depWithdrGrandTotal_ETH)
			depWithdr_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(3000, depWithdr_CHF)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(3000, depWithdrTotal_CHF)
			depWithdrActualValue_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(8000, depWithdrActualValue_CHF)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(8000, depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(8000, depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiat_CHF)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiat_CHF)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215,actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215,actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiat_CHF)
			capitalGainFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiatTotal_CHF)
			capitalGainFiat_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiat_CHF_percent)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiat_CHF_percent_TOTAL)
			yieldDays = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(90, yieldDays)
			yieldCrypto = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.04755893617130358, yieldCrypto)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.04755893617130358, yieldCryptoTotal)
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

	def testAddFiatConversionInfo_CHSB_2_fiats_USD_CHF_1_owner_2_deposit_french_language(self):
		"""
		CHSB crypto, 1 owner with 2 deposits. Testing crypto yield amount,
		crypto yield amount in percent, day, month and year yields in CHF.
		CHSB/CHF curr rate == 1,70. Yield fixed rate of 10 % per year.
		"""
		PRINT = True

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner_no_withdrawal.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_2_fiats_USD_CHF_no_withdrawal.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
		testLanguage = FR
		sbAccountSheetFiat = 'USD'
		fiat = 'CHF'

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName,
									   sbAccountSheetFiat=sbAccountSheetFiat)

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
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values checked !')
			depWithdrDateFrom = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom: ', str(depWithdrDateFrom))
			depWithdrDateTo = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo: ', depWithdrDateTo)
			depWithdr_CHSB = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			print('depWithdr_CHSB: ', depWithdr_CHSB)
			depWithdrTotal_CHSB = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			print('depWithdrTotal_CHSB: ', depWithdrTotal_CHSB)
			depWithdrGrandTotal_CHSB = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			print('depWithdrGrandTotal_CHSB: ', depWithdrGrandTotal_CHSB)
			#depWithdr_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			depWithdr_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][' ' + fiat]
			print('depWithdr_CHF: ', depWithdr_CHF)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			depWithdrActualValue_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF: ', depWithdrActualValue_CHF)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF: ', depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueGrandTotal_CHF: ', depWithdrActualValueGrandTotal_CHF)
			#yieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			yieldFiat_USD = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]]['USD']
			print('yieldFiat_USD: ', yieldFiat_USD)
			#yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			yieldFiatTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]]['USD']
			print('yieldFiatTotal_USD: ', yieldFiatTotal_USD)
			#yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			yieldFiatGrandTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]]['USD']
			print('yieldFiatGrandTotal_USD: ', yieldFiatGrandTotal_USD)
			actValPlusYieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF: ', actValPlusYieldFiat_CHF)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF: ', capitalGainFiat_CHF)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_TOTAL: ', capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent: ', capitalGainFiat_CHF_percent)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_TOTAL: ', capitalGainFiat_CHF_percent_TOTAL)
			yieldDays = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays: ', yieldDays)
			yieldCrypto = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto: ', yieldCrypto)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal: ', yieldCryptoTotal)
			yieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent: ', yieldPercent)
			yearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent: ', yearlyYieldPercent)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent: ', averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount_owner_1: ', dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount_owner_1: ', monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_owner_1: ', yearlyYieldAmount)
		else:
			pass

	def testAddFiatConversionInfo_CHSB_2_fiats_CHF_USD_1_owner_2_deposit_french_language(self):
		"""
		CHSB crypto, 1 owner with 2 deposits. Testing crypto yield amount,
		crypto yield amount in percent, day, month and year yields in CHF.
		CHSB/CHF curr rate == 1,70. Yield fixed rate of 10 % per year.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner_no_withdrawal.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_2_fiats_CHF_USD_no_withdrawal.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
		testLanguage = FR
		sbAccountSheetFiat = 'USD'
		fiat = 'CHF'

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName,
									   sbAccountSheetFiat=sbAccountSheetFiat)

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
'''                         Type Currency     Net amount
Local time                                           
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
TOTAL                                  1,098.56475635
'''
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(sbEarningsTotalDfActualStr)

			sys.stdout = stdout

			self.assertEqual(sbEarningsTotalDfExpectedStr, capturedStdoutStr.getvalue())

		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values checked !')

			depWithdrDateFrom = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom: ', str(depWithdrDateFrom))
			depWithdrDateTo = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo: ', str(depWithdrDateTo))
			depWithdr_CHSB_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			print('depWithdr_CHSB_1: ', depWithdr_CHSB_1)
			depWithdr_CHSB_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			print('depWithdr_CHSB_2: ', depWithdr_CHSB_2)
			depWithdrTotal_CHSB = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			print('depWithdrTotal_CHSB: ', depWithdrTotal_CHSB)
			depWithdrGrandTotal_CHSB = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			print('depWithdrGrandTotal_CHSB: ', depWithdrGrandTotal_CHSB)
			datDepCHSB_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_DEP_RATE[testLanguage]][CRYPTO_USD_DATE_FROM_RATE.format('CHSB')]
			print('datDepCHSB_USD_1: ', datDepCHSB_USD_1)
			datDepCHSB_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CUR_RATE[testLanguage]][CRYPTO_USD_CURRENT_RATE.format('CHSB')]
			print('datDepCHSB_USD_2: ', datDepCHSB_USD_2)
			depWithdr_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_1: ', depWithdr_CHF_1)
			depWithdr_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_2: ', depWithdr_CHF_2)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			depWithdrActualValue_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_1: ', depWithdrActualValue_CHF_1)
			depWithdrActualValue_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_2: ', depWithdrActualValue_CHF_2)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF: ', depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueGrandTotal_CHF: ', depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_1: ', yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_2: ', yieldFiat_CHF_2)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF: ', yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_1: ', actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_2: ', actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_1: ', capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_2: ', capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_TOTAL: ', capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_1: ', capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_2: ', capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_TOTAL: ', capitalGainFiat_CHF_percent_TOTAL)
			depWithdr_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + 'USD']
			print('depWithdr_USD_1: ', depWithdr_USD_1)
			depWithdr_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + 'USD']
			print('depWithdr_USD_2: ', depWithdr_USD_2)
			depWithdrTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + 'USD']
			print('depWithdrTotal_USD: ', depWithdrTotal_USD)
			depWithdrActualValue_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CURRENT_RATE[testLanguage]]['USD']
			print('depWithdrActualValue_USD_1: ', depWithdrActualValue_USD_1)
			depWithdrActualValue_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CURRENT_RATE[testLanguage]]['USD']
			print('depWithdrActualValue_USD_2: ', depWithdrActualValue_USD_2)
			depWithdrActualValueTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CURRENT_RATE[testLanguage]]['USD']
			print('depWithdrActualValueTotal_USD: ', depWithdrActualValueTotal_USD)
			depWithdrActualValueGrandTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_CURRENT_RATE[testLanguage]]['USD']
			print('depWithdrActualValueGrandTotal_USD: ', depWithdrActualValueGrandTotal_USD)
			yieldFiat_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'USD']
			print('yieldFiat_USD_1: ', yieldFiat_USD_1)
			yieldFiat_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'USD']
			print('yieldFiat_USD_2: ', yieldFiat_USD_2)
			yieldFiatTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'USD']
			print('yieldFiatTotal_USD: ', yieldFiatTotal_USD)
			yieldFiatGrandTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[3][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'USD']
			print('yieldFiatGrandTotal_USD: ', yieldFiatGrandTotal_USD)
			actValPlusYieldFiat_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'USD']
			print('actValPlusYieldFiat_USD_1: ', actValPlusYieldFiat_USD_1)
			actValPlusYieldFiat_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'USD']
			print('actValPlusYieldFiat_USD_2: ', actValPlusYieldFiat_USD_2)
			actValPlusYieldFiatTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'USD']
			print('actValPlusYieldFiatTotal_USD: ', actValPlusYieldFiatTotal_USD)
			actValPlusYieldFiatGrandTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[3][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'USD']
			print('actValPlusYieldFiatGrandTotal_USD: ', actValPlusYieldFiatGrandTotal_USD)
			capitalGainFiat_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + 'USD']
			print('capitalGainFiat_USD_1: ', capitalGainFiat_USD_1)
			capitalGainFiat_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + 'USD']
			print('capitalGainFiat_USD_2: ', capitalGainFiat_USD_2)
			capitalGainFiat_USD_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + 'USD']
			print('capitalGainFiat_USD_TOTAL: ', capitalGainFiat_USD_TOTAL)
			capitalGainFiat_USD_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('capitalGainFiat_USD_percent_1: ', capitalGainFiat_USD_percent_1)
			capitalGainFiat_USD_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('capitalGainFiat_USD_percent_2: ', capitalGainFiat_USD_percent_2)
			capitalGainFiat_USD_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('capitalGainFiat_USD_percent_TOTAL: ', capitalGainFiat_USD_percent_TOTAL)
			yieldDays_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_1: ', yieldDays_1)
			yieldDays_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_2: ', yieldDays_2)
			yieldCrypto_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_1: ', yieldCrypto_1)
			yieldCrypto_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_2: ', yieldCrypto_2)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal: ', yieldCryptoTotal)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoGrandTotal: ', yieldCryptoGrandTotal)
			yieldCryptoPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YIELD_AMT_PERCENT[testLanguage]][2]
			print('yieldCryptoPercent_1: ', yieldCryptoPercent_1)
			yieldCryptoPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YIELD_AMT_PERCENT[testLanguage]][2]
			print('yieldCryptoPercent_2: ', yieldCryptoPercent_2)
			yearlyYieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_1: ', yearlyYieldPercent_1)
			yearlyYieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_2: ', yearlyYieldPercent_2)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent: ', averageYearlyYieldPercent)
			dailyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]][0]
			print('dailyYieldAmount_CHF: ', dailyYieldAmount_CHF)
			monthlyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]][0]
			print('monthlyYieldAmount_CHF: ', monthlyYieldAmount_CHF)
			yearlyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_CHF: ', yearlyYieldAmount_CHF)
			dailyYieldAmount_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]][1]
			print('dailyYieldAmount_USD: ', dailyYieldAmount_USD)
			monthlyYieldAmount_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]][1]
			print('monthlyYieldAmount_USD: ', monthlyYieldAmount_USD)
			yearlyYieldAmount_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_IN[testLanguage] + 'USD '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_USD: ', yearlyYieldAmount_USD)
		else:
			depWithdrDateFrom = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-01-01', str(depWithdrDateFrom))
			depWithdrDateTo = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-01-05', str(depWithdrDateTo))
			depWithdr_CHSB_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			self.assertEqual(10000.0, depWithdr_CHSB_1)
			depWithdr_CHSB_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			self.assertEqual(1000.0, depWithdr_CHSB_2)
			depWithdrTotal_CHSB = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			self.assertEqual(11000.0, depWithdrTotal_CHSB)
			depWithdrGrandTotal_CHSB = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			datDepCHSB_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_DEP_RATE[testLanguage]][CRYPTO_USD_DATE_FROM_RATE.format('CHSB')]
			self.assertEqual(0.5614192679092747, datDepCHSB_USD_1)
			datDepCHSB_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CUR_RATE[testLanguage]][CRYPTO_USD_CURRENT_RATE.format('CHSB')]
			self.assertEqual(1.6999999995, datDepCHSB_USD_2)
			self.assertEqual(11000.0, depWithdrGrandTotal_CHSB)
			depWithdr_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(5000.0, depWithdr_CHF_1)
			depWithdr_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(1000.0, depWithdr_CHF_2)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(6000.0, depWithdrTotal_CHF)
			depWithdrActualValue_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(15000.0, depWithdrActualValue_CHF_1)
			depWithdrActualValue_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(1500.0, depWithdrActualValue_CHF_2)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(16500.0, depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(16500.0, depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(19.59707389264895, yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(1628.250060636914, yieldFiat_CHF_2)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(1647.847134529563, yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(1647.847134529563, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(15019.597073892648, actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(18147.847134529562, actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(18147.847134529562, actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(18147.847134529562, actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(10000.0, capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(500.0, capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(10500.0, capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(200, capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(50, capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(175.0, capitalGainFiat_CHF_percent_TOTAL)
			depWithdr_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + 'USD']
			self.assertEqual(4800.0, depWithdr_USD_1)
			depWithdr_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + 'USD']
			self.assertEqual(980.0, depWithdr_USD_2)
			depWithdrTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + 'USD']
			self.assertEqual(5780.0, depWithdrTotal_USD)
			depWithdrActualValue_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CURRENT_RATE[testLanguage]]['USD']
			self.assertEqual(16999.999995, depWithdrActualValue_USD_1)
			depWithdrActualValue_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CURRENT_RATE[testLanguage]]['USD']
			self.assertEqual(1699.9999994999998, depWithdrActualValue_USD_2)
			depWithdrActualValueTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CURRENT_RATE[testLanguage]]['USD']
			self.assertEqual(18699.999994499998, depWithdrActualValueTotal_USD)
			depWithdrActualValueGrandTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_CURRENT_RATE[testLanguage]]['USD']
			self.assertEqual(18699.9999944999989, depWithdrActualValueGrandTotal_USD)
			yieldFiat_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'USD']
			self.assertEqual(22.21001707180312, yieldFiat_USD_1)
			yieldFiat_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'USD']
			self.assertEqual(1845.3500681790858, yieldFiat_USD_2)
			yieldFiatTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'USD']
			self.assertEqual(1867.560085250889, yieldFiatTotal_USD)
			yieldFiatGrandTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[3][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'USD']
			self.assertEqual(1867.560085250889, yieldFiatGrandTotal_USD)
			actValPlusYieldFiat_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'USD']
			self.assertEqual(17022.210012071802, actValPlusYieldFiat_USD_1)
			actValPlusYieldFiat_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'USD']
			self.assertEqual(20567.56007975089, actValPlusYieldFiat_USD_2)
			actValPlusYieldFiatTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'USD']
			self.assertEqual(20567.56007975089, actValPlusYieldFiatTotal_USD)
			actValPlusYieldFiatGrandTotal_USD = yieldOwnerWithTotalsDetailDf.iloc[3][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'USD']
			self.assertEqual(20567.56007975089, actValPlusYieldFiatGrandTotal_USD)
			capitalGainFiat_USD_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + 'USD']
			self.assertEqual(12199.999994999998, capitalGainFiat_USD_1)
			capitalGainFiat_USD_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + 'USD']
			self.assertEqual(719.9999994999998, capitalGainFiat_USD_2)
			capitalGainFiat_USD_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + 'USD']
			self.assertEqual(12919.999994499998, capitalGainFiat_USD_TOTAL)
			capitalGainFiat_USD_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(254.16666656249998, capitalGainFiat_USD_percent_1)
			capitalGainFiat_USD_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(73.46938770408161, capitalGainFiat_USD_percent_2)
			capitalGainFiat_USD_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(223.52941166955014, capitalGainFiat_USD_percent_TOTAL)
			yieldDays_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(5, yieldDays_1)
			yieldDays_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(360, yieldDays_2)
			yieldCrypto_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(13.064715928432634, yieldCrypto_1)
			yieldCrypto_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(1085.5000404246093, yieldCrypto_2)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(1098.564756353042, yieldCryptoTotal)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(1098.564756353042, yieldCryptoGrandTotal)
			yearlyYieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(9.999999999999698, yearlyYieldPercent_1)
			yearlyYieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001075, yearlyYieldPercent_2)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001057, averageYearlyYieldPercent)

			yieldCryptoPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YIELD_AMT_PERCENT[testLanguage]][2]
			self.assertEqual(0.13064715928432635, yieldCryptoPercent_1)
			yieldCryptoPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YIELD_AMT_PERCENT[testLanguage]][2]
			self.assertEqual(9.856475635293664, yieldCryptoPercent_2)

			dailyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]][0]
			self.assertEqual(4.739453212857599, dailyYieldAmount_CHF)
			monthlyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]][0]
			self.assertEqual(142.72333039279368, monthlyYieldAmount_CHF)
			yearlyYieldAmount_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(1814.784713453147, yearlyYieldAmount_CHF)
			dailyYieldAmount_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]][1]
			self.assertEqual(5.371380306325461, dailyYieldAmount_USD)
			monthlyYieldAmount_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]][1]
			self.assertEqual(161.75310773092505, monthlyYieldAmount_USD)
			yearlyYieldAmount_USD = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_IN[testLanguage] + 'USD '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(2056.7560079753052, yearlyYieldAmount_USD)

	def testAddFiatConversionInfo_CHSB_1_fiat_1_owner_2_deposit_french_language(self):
		"""
		CHSB crypto, 1 owner with 2 deposits. Testing crypto yield amount,
		crypto yield amount in percent, day, month and year yields in USD.
		CHSB/USD curr rate == 1.70. Yield fixed rate of 10 % per year.
		"""
		PRINT = False

		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner_no_withdrawal.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_1_fiat_no_withdrawal.csv'
		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
		testLanguage = FR
		sbAccountSheetFiat = 'USD'
		fiat = 'CHF'

		print(depositSheetFileName)

		self.initializeComputerClasses(sbAccountSheetFileName,
									   depositSheetFileName,
									   cryptoFiatCsvFileName,
									   sbAccountSheetFiat=sbAccountSheetFiat)

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
'''                         Type Currency     Net amount
Local time                                           
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
TOTAL                                  1,098.56475635
'''
			stdout = sys.stdout
			capturedStdoutStr = StringIO()
			sys.stdout = capturedStdoutStr

			print(sbEarningsTotalDfActualStr)

			sys.stdout = stdout
			self.maxDiff = None
			self.assertEqual(sbEarningsTotalDfExpectedStr, capturedStdoutStr.getvalue())

		if PRINT:
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values checked !')
			depWithdrDateFrom = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom: ', str(depWithdrDateFrom))
			depWithdrDateTo = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo: ', str(depWithdrDateTo))
			depWithdr_CHSB_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			print('depWithdr_CHSB_1: ', depWithdr_CHSB_1)
			depWithdrTotal_CHSB = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			print('depWithdrTotal_CHSB: ', depWithdrTotal_CHSB)
			depWithdrGrandTotal_CHSB = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			print('depWithdrGrandTotal_CHSB: ', depWithdrGrandTotal_CHSB)
			depWithdr_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_1: ', depWithdr_CHF_1)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			depWithdrActualValue_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_1: ', depWithdrActualValue_CHF_1)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF: ', depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueGrandTotal_CHF: ', depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_1: ', yieldFiat_CHF_1)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF: ', yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_1: ', actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_1: ', capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_TOTAL: ', capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_1: ', capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_TOTAL: ', capitalGainFiat_CHF_percent_TOTAL)
			yieldDays_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_1: ', yieldDays_1)
			yieldCrypto_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_1: ', yieldCrypto_1)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal: ', yieldCryptoTotal)
			yieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent: ', yieldPercent)
			yearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent: ', yearlyYieldPercent)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent: ', averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount: ', dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount: ', monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount: ', yearlyYieldAmount)
		else:
			depWithdrDateFrom = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-01-01', str(depWithdrDateFrom))
			depWithdrDateTo = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-01-05', str(depWithdrDateTo))
			depWithdr_CHSB_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			self.assertEqual(10000.0, depWithdr_CHSB_1)
			depWithdr_CHSB_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			self.assertEqual(1000.0, depWithdr_CHSB_2)
			depWithdrTotal_CHSB = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			self.assertEqual(11000.0, depWithdrTotal_CHSB)
			depWithdrGrandTotal_CHSB = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['CHSB']
			self.assertEqual(11000.0, depWithdrGrandTotal_CHSB)
			depWithdr_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(5000.0, depWithdr_CHF_1)
			depWithdr_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(1000.0, depWithdr_CHF_2)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(6000.0, depWithdrTotal_CHF)
			depWithdrActualValue_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(15000.0, depWithdrActualValue_CHF_1)
			depWithdrActualValue_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(1500.0, depWithdrActualValue_CHF_2)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(16500.0, depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(16500.0, depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(19.59707389264895, yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(1628.250060636914, yieldFiat_CHF_2)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(1647.847134529563, yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(1647.847134529563, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(15019.597073892648, actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(18147.847134529562, actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(18147.847134529562, actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(18147.847134529562, actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(10000.0, capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(500.0, capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(10500.0, capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(200, capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(50, capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(175.0, capitalGainFiat_CHF_percent_TOTAL)
			yieldDays_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(5, yieldDays_1)
			yieldDays_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(360, yieldDays_2)
			yieldCrypto_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(13.064715928432634, yieldCrypto_1)
			yieldCrypto_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(1085.5000404246093, yieldCrypto_2)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(1098.564756353042, yieldCryptoTotal)
			yieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(0.13064715928432635, yieldPercent)
			yearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(9.999999999999698, yearlyYieldPercent)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			self.assertEqual(10.000000000001075, averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			self.assertEqual(4.739453212857599, dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			self.assertEqual(142.72333039279368, monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			self.assertEqual(1814.784713453147, yearlyYieldAmount)

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
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values checked !')

			depWithdrDateFrom = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom: ', str(depWithdrDateFrom))
			depWithdrDateTo = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo: ', depWithdrDateTo)
			depWithdr_ETH = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH: ', depWithdr_ETH)
			depWithdrTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrTotal_ETH: ', depWithdrTotal_ETH)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrGrandTotal_ETH: ', depWithdrGrandTotal_ETH)
			depWithdr_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_1: ', depWithdr_CHF)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			depWithdrActualValue_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_1: ', depWithdrActualValue_CHF)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF: ', depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueGrandTotal_CHF: ', depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_1: ', yieldFiat_CHF)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF: ', yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_1: ', actValPlusYieldFiat_CHF)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_1: ', capitalGainFiat_CHF)
			capitalGainFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiatTotal_CHF: ', capitalGainFiatTotal_CHF)
			capitalGainFiat_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_1: ', capitalGainFiat_CHF_percent)
			capitalGainFiatTotal_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiatTotal_CHF_percent: ', capitalGainFiatTotal_CHF_percent)
			depWithdr_EUR = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_DATE_FROM_RATE[testLanguage]]['EUR']
			print('depWithdr_EUR: ', depWithdr_EUR)
			depWithdrTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_DATE_FROM_RATE[testLanguage]]['EUR']
			print('depWithdrTotal_EUR: ', depWithdrTotal_EUR)
			depWithdrActualValue_EUR = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CURRENT_RATE[testLanguage]]['EUR']
			print('depWithdrActualValue_EUR: ', depWithdrActualValue_EUR)
			depWithdrActualValueTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CURRENT_RATE[testLanguage]]['EUR']
			print('depWithdrActualValueTotal_EUR: ', depWithdrActualValueTotal_EUR)
			depWithdrActualValueGrandTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CURRENT_RATE[testLanguage]]['EUR']
			print('depWithdrActualValueGrandTotal_EUR: ', depWithdrActualValueGrandTotal_EUR)
			yieldFiat_EUR = yieldOwnerWithTotalsDetailDf.iloc[0][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'EUR']
			print('yieldFiat_EUR: ', yieldFiat_EUR)
			yieldFiatTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'EUR']
			print('yieldFiatTotal_EUR: ', yieldFiatTotal_EUR)
			yieldFiatGrandTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[2][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'EUR']
			print('yieldFiatGrandTotal_EUR: ', yieldFiatGrandTotal_EUR)
			actValPlusYieldFiat_EUR = yieldOwnerWithTotalsDetailDf.iloc[0][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'EUR']
			print('actValPlusYieldFiat_EUR: ', actValPlusYieldFiat_EUR)
			actValPlusYieldFiatTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'EUR']
			print('actValPlusYieldFiatTotal_EUR: ', actValPlusYieldFiatTotal_EUR)
			actValPlusYieldFiatGrandTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[2][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'EUR']
			print('actValPlusYieldFiatGrandTotal_EUR: ', actValPlusYieldFiatGrandTotal_EUR)
			capitalGainFiat_EUR = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + 'EUR']
			print('capitalGainFiat_EUR: ', capitalGainFiat_EUR)
			capitalGainFiatTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + 'EUR']
			print('capitalGainFiatTotal_EUR: ', capitalGainFiatTotal_EUR)
			capitalGainFiat_EUR_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('capitalGainFiat_EUR_percent: ', capitalGainFiat_EUR_percent)
			capitalGainFiat_EUR_totalPercent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('capitalGainFiat_EUR_totalPercent: ', capitalGainFiat_EUR_totalPercent)
			yieldDays = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_1: ', yieldDays)
			yieldCrypto = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_1: ', yieldCrypto)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal: ', yieldCryptoTotal)
			yieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YIELD_AMT_PERCENT[testLanguage]][2]
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
			dep_withdr_date_from = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-01-01', str(dep_withdr_date_from))
			depWithdrDateTo = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-03-31', str(depWithdrDateTo))
			depWithdr_ETH = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(2.0, depWithdr_ETH)
			depWithdrTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(2.0, depWithdrTotal_ETH)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(2.0, depWithdrGrandTotal_ETH)
			depWithdr_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(3000, depWithdr_CHF)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(3000, depWithdrTotal_CHF)
			depWithdrActualValue_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(8000, depWithdrActualValue_CHF)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(8000, depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(8000, depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiat_CHF)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiat_CHF)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3]['  ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiat_CHF)
			capitalGainFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiatTotal_CHF)
			capitalGainFiat_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiat_CHF_percent)
			capitalGainFiatTotal_CHF_percent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiatTotal_CHF_percent)
			depWithdr_EUR = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_DATE_FROM_RATE[testLanguage]]['EUR']
			self.assertEqual(2800.0, depWithdr_EUR)
			depWithdrTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_DATE_FROM_RATE[testLanguage]]['EUR']
			self.assertEqual(2800.0, depWithdrTotal_EUR)
			depWithdrActualValue_EUR = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CURRENT_RATE[testLanguage]]['EUR']
			self.assertEqual(7040.0, depWithdrActualValue_EUR)
			depWithdrActualValueTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CURRENT_RATE[testLanguage]]['EUR']
			self.assertEqual(7040.0, depWithdrActualValueTotal_EUR)
			depWithdrActualValueGrandTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_CURRENT_RATE[testLanguage]]['EUR']
			self.assertEqual(7040.0, depWithdrActualValueGrandTotal_EUR)
			yieldFiat_EUR = yieldOwnerWithTotalsDetailDf.iloc[0][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'EUR']
			self.assertEqual(167.4074553229886, yieldFiat_EUR)
			yieldFiatTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'EUR']
			self.assertEqual(167.4074553229886, yieldFiatTotal_EUR)
			yieldFiatGrandTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[2][' ']['   ' + PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + 'EUR']
			self.assertEqual(167.4074553229886, yieldFiatGrandTotal_EUR)
			actValPlusYieldFiat_EUR = yieldOwnerWithTotalsDetailDf.iloc[0][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'EUR']
			self.assertEqual(7207.407455322988, actValPlusYieldFiat_EUR)
			actValPlusYieldFiatTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'EUR']
			self.assertEqual(7207.407455322988, actValPlusYieldFiatTotal_EUR)
			actValPlusYieldFiatGrandTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[2][' ']['    ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + 'EUR']
			self.assertEqual(7207.407455322988, actValPlusYieldFiatGrandTotal_EUR)
			capitalGainFiat_EUR = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + 'EUR']
			self.assertEqual(4240.0, capitalGainFiat_EUR)
			capitalGainFiatTotal_EUR = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + 'EUR']
			self.assertEqual(4240.0, capitalGainFiatTotal_EUR)
			capitalGainFiat_EUR_percent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(151.42857142857142, capitalGainFiat_EUR_percent)
			capitalGainFiat_EUR_totalPercent = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(151.42857142857142, capitalGainFiat_EUR_totalPercent)
			yieldDays = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(90, yieldDays)
			yieldCrypto = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.04755893617130358, yieldCrypto)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.04755893617130358, yieldCryptoTotal)
			yieldPercent = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YIELD_AMT_PERCENT[testLanguage]][2]
			self.assertEqual(2.377946808565179, yieldPercent)
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
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values checked !')
			depWithdrDateFrom_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom_1: ', str(depWithdrDateFrom_1))
			depWithdrDateFrom_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom_2: ', str(depWithdrDateFrom_2))
			depWithdrDateTo_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo_1: ', depWithdrDateTo_1)
			depWithdrDateTo_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo_2: ', str(depWithdrDateTo_2))
			depWithdr_ETH_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH_1: ', depWithdr_ETH_1)
			depWithdr_ETH_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH_2: ', depWithdr_ETH_2)
			depWithdrTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrTotal_ETH: ', depWithdrTotal_ETH)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrGrandTotal_ETH: ', depWithdrGrandTotal_ETH)
			depWithdr_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_1: ', depWithdr_CHF_1)
			depWithdr_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_2: ', depWithdr_CHF_2)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			depWithdrActualValue_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_1: ', depWithdrActualValue_CHF_1)
			depWithdrActualValue_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_2: ', depWithdrActualValue_CHF_2)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF: ', depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueGrandTotal_CHF: ', depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_1: ', yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_2: ', yieldFiat_CHF_2)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF: ', yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_1: ', actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_2: ', actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_1: ', capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_1: ', capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_2: ', capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_2: ', capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_TOTAL: ', capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_TOTAL: ', capitalGainFiat_CHF_percent_TOTAL)
			yieldDays_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_1: ', yieldDays_1)
			yieldDays_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_2: ', yieldDays_2)
			yieldCrypto_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_1: ', yieldCrypto_1)
			yieldCrypto_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			print('yieldCrypto_2: ', yieldCrypto_2)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal: ', yieldCryptoTotal)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoGrandTotal: ', yieldCryptoGrandTotal)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoGrandTotal: ', yieldCryptoGrandTotal)
			yieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_1: ', yieldPercent_1)
			yieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			print('yieldPercent_2: ', yieldPercent_2)
			yearlyYieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_1: ', yearlyYieldPercent_1)
			yearlyYieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_2: ', yearlyYieldPercent_2)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent: ', averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount_owner_1: ', dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount_owner_1: ', monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_owner_1: ', yearlyYieldAmount)
		else:
			depWithdrDateFrom_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-01-01', str(depWithdrDateFrom_1))
			depWithdrDateFrom_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-04-01', str(depWithdrDateFrom_2))
			depWithdrDateTo_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-03-31', str(depWithdrDateTo_1))
			depWithdrDateTo_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-06-30', str(depWithdrDateTo_2))
			depWithdr_ETH_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(2.00, depWithdr_ETH_1)
			depWithdr_ETH_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(1.00, depWithdr_ETH_2)
			depWithdrTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(3.00, depWithdrTotal_ETH)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(3.00, depWithdrGrandTotal_ETH)
			depWithdr_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(3000, depWithdr_CHF_1)
			depWithdr_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(2000, depWithdr_CHF_2)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(5000, depWithdrTotal_CHF)
			depWithdrActualValue_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(8000, depWithdrActualValue_CHF_1)
			depWithdrActualValue_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(4000, depWithdrActualValue_CHF_2)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(12000, depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(12000, depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(293.13660166886103, yieldFiat_CHF_2)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(483.3723463540753, yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(483.3723463540753, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(12483.372346354075, actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(12483.372346354075,actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(12483.372346354075,actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(2000.0, capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(100.0, capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(7000.0, capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(140.0, capitalGainFiat_CHF_percent_TOTAL)
			yieldDays_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(90, yieldDays_1)
			yieldDays_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(91, yieldDays_2)
			yieldCrypto_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.04755893617130358, yieldCrypto_1)
			yieldCrypto_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.07328415041721525, yieldCrypto_2)
			yieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(2.377946808565179, yieldPercent_1)
			yieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][1]
			self.assertEqual(2.4046836157099327, yieldPercent_2)
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.12084308658851883, yieldCryptoTotal)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.12084308658851883, yieldCryptoGrandTotal)
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

		#self.processor.activateHelpNumbers()

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
			print(yieldOwnerWithTotalsDetailDfActualStr)
			print('\nAll values checked !')
			depWithdrDateFrom_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom_1: ', str(depWithdrDateFrom_1))
			depWithdrDateFrom_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom_2: ', str(depWithdrDateFrom_2))
			depWithdrDateFrom_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			print('depWithdrDateFrom_3: ', str(depWithdrDateFrom_3))
			depWithdrDateTo_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo_1: ', depWithdrDateTo_1)
			depWithdrDateTo_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo_2: ', str(depWithdrDateTo_2))
			depWithdrDateTo_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			print('depWithdrDateTo_3: ', str(depWithdrDateTo_3))
			depWithdr_ETH_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH_1: ', depWithdr_ETH_1)
			depWithdr_ETH_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH_2: ', depWithdr_ETH_2)
			depWithdr_ETH_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdr_ETH_3: ', depWithdr_ETH_3)
			depWithdrTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrTotal_ETH: ', depWithdrTotal_ETH)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_AMOUNT[testLanguage]]['ETH']
			print('depWithdrGrandTotal_ETH: ', depWithdrGrandTotal_ETH)
			depWithdr_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_1: ', depWithdr_CHF_1)
			depWithdr_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_2: ', depWithdr_CHF_2)
			depWithdr_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdr_CHF_3: ', depWithdr_CHF_3)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			print('depWithdrTotal_CHF: ', depWithdrTotal_CHF)
			depWithdrActualValue_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_1: ', depWithdrActualValue_CHF_1)
			depWithdrActualValue_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_2: ', depWithdrActualValue_CHF_2)
			depWithdrActualValue_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValue_CHF_3: ', depWithdrActualValue_CHF_3)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueTotal_CHF: ', depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			print('depWithdrActualValueGrandTotal_CHF: ', depWithdrActualValueGrandTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_1: ', yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_2: ', yieldFiat_CHF_2)
			yieldFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiat_CHF_3: ', yieldFiat_CHF_3)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatTotal_CHF: ', yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			print('yieldFiatGrandTotal_CHF: ', yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_1: ', actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_2: ', actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiat_CHF_3: ',actValPlusYieldFiat_CHF_3)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatTotal_CHF: ', actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			print('actValPlusYieldFiatGrandTotal_CHF: ', actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_1: ', capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_1: ', capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_2: ', capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_2: ', capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_3: ', capitalGainFiat_CHF_3)
			capitalGainFiat_CHF_percent_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_3: ', capitalGainFiat_CHF_percent_3)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			print('capitalGainFiat_CHF_TOTAL: ', capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			print('capitalGainFiat_CHF_percent_TOTAL: ', capitalGainFiat_CHF_percent_TOTAL)
			yieldDays_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_1: ', yieldDays_1)
			yieldDays_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_2: ', yieldDays_2)
			yieldDays_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			print('yieldDays_3: ', yieldDays_3)
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
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoTotal: ', yieldCryptoTotal)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_INTEREST][depositCrypto]
			print('yieldCryptoGrandTotal: ', yieldCryptoGrandTotal)
			yearlyYieldPercent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_1: ', yearlyYieldPercent_1)
			yearlyYieldPercent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_2: ', yearlyYieldPercent_2)
			yearlyYieldPercent_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('yearlyYieldPercent_3: ', yearlyYieldPercent_3)
			averageYearlyYieldPercent = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_YEAR_YIELD_PERCENT[testLanguage]]
			print('averageYearlyYieldPercent: ', averageYearlyYieldPercent)
			dailyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]][PROC_PER_DAY[testLanguage]]
			print('dailyYieldAmount_owner_1: ', dailyYieldAmount)
			monthlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_YIELD[testLanguage]][PROC_PER_MONTH[testLanguage]]
			print('monthlyYieldAmount_owner_1: ', monthlyYieldAmount)
			yearlyYieldAmount = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_IN[testLanguage] + fiat + ' '][PROC_PER_YEAR[testLanguage]]
			print('yearlyYieldAmount_owner_1: ', yearlyYieldAmount)
		else:
			depWithdrDateFrom_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-01-01', str(depWithdrDateFrom_1))
			depWithdrDateFrom_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-04-01', str(depWithdrDateFrom_2))
			depWithdrDateFrom_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_FROM[testLanguage]]
			self.assertEqual('2021-07-01', str(depWithdrDateFrom_3))
			depWithdrDateTo_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-03-31', str(depWithdrDateTo_1))
			depWithdrDateTo_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-06-30', str(depWithdrDateTo_2))
			depWithdrDateTo_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][DEPOSIT_YIELD_HEADER_DATE_TO[testLanguage]]
			self.assertEqual('2021-07-31', str(depWithdrDateTo_3))
			depWithdr_ETH_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(2.00, depWithdr_ETH_1)
			depWithdr_ETH_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(1.00, depWithdr_ETH_2)
			depWithdr_ETH_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(1.00, depWithdr_ETH_3)
			depWithdrTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(4.00, depWithdrTotal_ETH)
			depWithdrGrandTotal_ETH = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_AMOUNT[testLanguage]]['ETH']
			self.assertEqual(4.00, depWithdrGrandTotal_ETH)
			depWithdr_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(3000, depWithdr_CHF_1)
			depWithdr_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(2000, depWithdr_CHF_2)
			depWithdr_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(3000, depWithdr_CHF_3)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_DEP[testLanguage]][PROC_DATE_FROM_RATE[testLanguage]][self.processor.PROC_HELP_1 + fiat]
			self.assertEqual(8000, depWithdrTotal_CHF)
			depWithdrActualValue_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(8000, depWithdrActualValue_CHF_1)
			depWithdrActualValue_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(4000, depWithdrActualValue_CHF_2)
			depWithdrActualValue_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(4000, depWithdrActualValue_CHF_3)
			depWithdrActualValueTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(16000, depWithdrActualValueTotal_CHF)
			depWithdrActualValueGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(16000, depWithdrActualValueGrandTotal_CHF)
			depWithdrTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][PROC_WITHDR[testLanguage]][PROC_CURRENT_RATE[testLanguage]][fiat]
			self.assertEqual(16000, depWithdrTotal_CHF)
			yieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(190.2357446852143, yieldFiat_CHF_1)
			yieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(293.13660166886103, yieldFiat_CHF_2)
			yieldFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(133.97172355601228, yieldFiat_CHF_3)
			yieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(617.3440699100876, yieldFiatTotal_CHF)
			yieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_2][PROC_CURRENT_RATE[testLanguage]][PROC_YIELD_SHORT[testLanguage] + fiat]
			self.assertEqual(617.3440699100876, yieldFiatGrandTotal_CHF)
			actValPlusYieldFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(8190.235744685215, actValPlusYieldFiat_CHF_1)
			actValPlusYieldFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(12483.372346354075, actValPlusYieldFiat_CHF_2)
			actValPlusYieldFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(16617.344069910087,actValPlusYieldFiat_CHF_3)
			actValPlusYieldFiatTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(16617.344069910087,actValPlusYieldFiatTotal_CHF)
			actValPlusYieldFiatGrandTotal_CHF = yieldOwnerWithTotalsDetailDf.iloc[4][self.processor.PROC_HELP_3][' ' + PROC_CURRENT_RATE[testLanguage]][PROC_TOTAL_SHORT + fiat]
			self.assertEqual(16617.344069910087,actValPlusYieldFiatGrandTotal_CHF)
			capitalGainFiat_CHF_1 = yieldOwnerWithTotalsDetailDf.iloc[0][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(5000.0, capitalGainFiat_CHF_1)
			capitalGainFiat_CHF_percent_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(166.66666666666669, capitalGainFiat_CHF_percent_1)
			capitalGainFiat_CHF_2 = yieldOwnerWithTotalsDetailDf.iloc[1][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(2000.0, capitalGainFiat_CHF_2)
			capitalGainFiat_CHF_percent_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(100.0, capitalGainFiat_CHF_percent_2)
			capitalGainFiat_CHF_3 = yieldOwnerWithTotalsDetailDf.iloc[2][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(1000.0, capitalGainFiat_CHF_3)
			capitalGainFiat_CHF_percent_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(33.33333333333333, capitalGainFiat_CHF_percent_3)
			capitalGainFiat_CHF_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[3][self.processor.PROC_HELP_4][PROC_CAPITAL_GAIN[testLanguage]][PROC_CAPITAL_SHORT[testLanguage] + fiat]
			self.assertEqual(8000.0, capitalGainFiat_CHF_TOTAL)
			capitalGainFiat_CHF_percent_TOTAL = yieldOwnerWithTotalsDetailDf.iloc[3][' '][' '][PROC_CAPITAL_GAIN_PERCENT[testLanguage]][0]
			self.assertEqual(100.0, capitalGainFiat_CHF_percent_TOTAL)
			yieldDays_1 = yieldOwnerWithTotalsDetailDf.iloc[0][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(90, yieldDays_1)
			yieldDays_2 = yieldOwnerWithTotalsDetailDf.iloc[1][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(91, yieldDays_2)
			yieldDays_3 = yieldOwnerWithTotalsDetailDf.iloc[2][' '][PROC_YIELD_DAYS[testLanguage]][PROC_INTEREST]
			self.assertEqual(31, yieldDays_3)
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
			yieldCryptoTotal = yieldOwnerWithTotalsDetailDf.iloc[3][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.1543360174775219, yieldCryptoTotal)
			yieldCryptoGrandTotal = yieldOwnerWithTotalsDetailDf.iloc[4][' '][PROC_INTEREST][depositCrypto]
			self.assertEqual(0.1543360174775219, yieldCryptoGrandTotal)
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

		# value testing ok for the tsts below
		# tst.testAddFiatConversionInfo_ETH_1_fiat_1_owner_1_deposit_french_language()
		# tst.testAddFiatConversionInfo_ETH_2_fiats_1_owner_1_deposit_french_language()
		# tst.testAddFiatConversionInfo_ETH_1_fiat_1_owner_2_deposits_english_language()
		# tst.testAddFiatConversionInfo_ETH_1_fiat_1_owner_3_deposits_french_language()
		tst.testAddFiatConversionInfo_CHSB_2_fiats_CHF_USD_1_owner_2_deposit_french_language()
		# tst.testAddFiatConversionInfo_CHSB_1_fiat_1_owner_2_deposit_french_language()

	'''
		  COURS   COURS   COURS   COURS
		DEP USD ACT USD DEP CHF ACT CHF
		'''