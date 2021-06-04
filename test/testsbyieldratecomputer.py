import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from sbyieldratecomputer import *
from duplicatedepositdatetimeerror import DuplicateDepositDateTimeError
from invaliddepositdatetimeerror import InvalidDepositDateTimeError

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

		self.yieldRateComputer = SBYieldRateComputer(sbAccountSheetFilePathName=sbAccountSheetFilePathName,
													 sbAccountSheetFiat='USD',
		                                             depositSheetFilePathName=depositSheetFilePathName)

	def test_loadSBEarningSheetUSDC(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(yieldCrypto)
		self.assertEqual((9, 3), sbEarningsDf.shape)
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

	def test_loadDepositCsvFileWithFiatColumns_0(self):
		'''
		Test loading a deposit csv file in which the deposit withdrawal are
		defined with the addition of two corresponding converted fiat amount
		columns.
		'''
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		depositDf, depositCrypto, depositFiatLst = self.yieldRateComputer._loadDepositCsvFile()

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

		expectedFiatLst = []

		if PRINT:
			print(depositFiatLst)
			print(depositDf)
		else:
			self.assertEqual(expectedFiatLst, depositFiatLst)
			self.assertEqual(expectedStrDataframe, depositDf.to_string())

	def test_loadDepositCsvUSDCFileWithFiatColumns_2(self):
		'''
		Test loading a deposit csv file in which the deposit withdrawal are
		defined with the addition of two corresponding converted fiat amount
		columns.
		'''
		PRINT = False

		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_fiat_amount_2.csv'

		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
		expectedDepositFiatOne = DEPOSIT_FIAT_USD
		expectedDepositFiatTwo = DEPOSIT_FIAT_CHF

		depositDf, depositCrypto, depositFiatLst = self.yieldRateComputer._loadDepositCsvFile()

		if not PRINT:
			self.assertEqual((5, 4), depositDf.shape)
			self.assertEqual(expectedYieldCrypto, depositCrypto)
			self.assertEqual(expectedDepositFiatOne, depositFiatLst[0])
			self.assertEqual(expectedDepositFiatTwo, depositFiatLst[1])

		expectedStrDataframe = \
'                    OWNER  DEP/WITHDR  USD AMT  CHF AMT\n' + \
'DATE                                                   ' + \
'''
2020-11-21 00:00:00   JPS      2000.0   2000.0  1780.00
2020-12-25 00:00:00  Papa      4000.0   4000.0  3520.00
2020-12-25 00:00:01   Béa      1000.0   1000.0   902.95
2020-12-27 00:00:00  Papa      -500.0   -500.0  -450.00
2020-12-28 00:00:00   JPS      3000.0   3000.0  2730.00'''
		expectedFiatLst = ['USD', 'CHF']

		if PRINT:
			print(depositFiatLst)
			print(depositDf)
		else:
			self.assertEqual(expectedFiatLst, depositFiatLst)
			self.assertEqual(expectedStrDataframe, depositDf.to_string())

	def test_loadDepositCsvCHSBFileWithFiatColumns_2(self):
		'''
		Test loading a deposit csv file in which the deposit withdrawal are
		defined with the addition of two corresponding converted fiat amount
		columns.
		'''
		PRINT = False

		sbAccountSheetFileName = 'testSwissborg_account_statement_20201218_20210408.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_usd_chf.csv'

		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
		expectedDepositFiatOne = DEPOSIT_FIAT_USD
		expectedDepositFiatTwo = DEPOSIT_FIAT_CHF

		depositDf, depositCrypto, depositFiatLst = self.yieldRateComputer._loadDepositCsvFile()

		if not PRINT:
			self.assertEqual((6, 4), depositDf.shape)
			self.assertEqual(expectedYieldCrypto, depositCrypto)
			self.assertEqual(expectedDepositFiatOne, depositFiatLst[0])
			self.assertEqual(expectedDepositFiatTwo, depositFiatLst[1])

		expectedStrDataframe = \
'                    OWNER    DEP/WITHDR   USD AMT  CHF AMT\n' + \
'DATE                                                      ' + \
'''
2021-01-30 00:00:00  Papa  15941.626290   8938.09  7973.32
2021-01-30 00:00:01   JPS   4422.803299   2479.76  2212.10
2021-02-19 00:00:00   JPS    511.330000    456.60   408.04
2021-03-07 00:00:00  Papa   8973.340000  10421.37  9712.37
2021-03-08 00:00:00   JPS   2047.890000   2401.13  2239.89
2021-03-11 00:00:00   JPS    300.480000    430.55   397.92'''
		expectedFiatLst = ['USD', 'CHF']

		if PRINT:
			print(depositFiatLst)
			print(depositDf)
		else:
			self.assertEqual(expectedFiatLst, depositFiatLst)
			self.assertEqual(expectedStrDataframe, depositDf.to_string())

	def test_loadDepositCsvFileWithDuplicateDatetime(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1_duplDatetime.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		with self.assertRaises(DuplicateDepositDateTimeError) as e:
			self.yieldRateComputer._loadDepositCsvFile()
		
		self.assertEqual(
			'CSV file {} contains a deposit of 1000 for owner Béa with a deposit date 2020-12-25 00:00:00 which is identical to another deposit date. Change the date by increasing the time second by 1 and retry.'.format(
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
		
		with self.assertRaises(InvalidDepositDateTimeError) as e:
			self.yieldRateComputer._loadDepositCsvFile()
		
		self.assertEqual(
			'CSV file {} contains a deposit of 1000 for owner Béa with a deposit date of 2020/12/25 00:00: whose format is invalid. Correct the date time component and retry.'.format(
				self.testDataPath + depositSheetFileName), e.exception.message)
	
	def test_loadDepositCsvFileWithTimeComponentAfterNineOClock(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1_timeComponentAfter9oclock.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		with self.assertRaises(InvalidDepositDateTimeError) as e:
			self.yieldRateComputer._loadDepositCsvFile()
		
		self.assertEqual(
			'CSV file {} contains a deposit of 1000 for owner Béa with a deposit date of 2020-12-25 10:00:00 whose time component is later than the 09:00:00 Swissborg yield payment time. Set the time to a value before 09:00:00 and retry.'.format(
				self.testDataPath + depositSheetFileName), e.exception.message)
	
	def test_mergeEarningAndDeposit(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(expectedYieldCrypto)
		depositDf, depositCrypto, depositFiatLst = self.yieldRateComputer._loadDepositCsvFile()
		
		mergedEarningDeposit = self.yieldRateComputer._mergeEarningAndDeposit(sbEarningsDf, depositDf)

		if not PRINT:
			self.assertEqual((10, 6), mergedEarningDeposit.shape)
			self.assertEqual(expectedYieldCrypto, depositCrypto)

		expectedStrDataframe = \
'         DATE  DEP/WITHDR  EARNING CAP  EARNING  D YIELD RATE  Y YIELD RATE' + \
'''
0  2020-11-21      2000.0      2000.00     0.00      0.000000      0.000000
1  2020-12-22         0.0      2000.00     0.80      1.000400      1.157162
2  2020-12-23         0.0      2000.80     0.81      1.000405      1.159207
3  2020-12-24         0.0      2001.61     0.82      1.000410      1.161252
4  2020-12-25      5000.0      7002.43     0.78      1.000111      1.041493
5  2020-12-26         0.0      7003.21     2.80      1.000400      1.157085
6  2020-12-27      -500.0      6506.01     2.70      1.000415      1.163513
7  2020-12-28      3000.0      9508.71     2.75      1.000289      1.111317
8  2020-12-29         0.0      9511.46     4.00      1.000421      1.165869
9  2020-12-30         0.0      9515.46     4.10      1.000431      1.170272'''
		
		if PRINT:
			print(mergedEarningDeposit)
		else:
			self.assertEqual(expectedStrDataframe, mergedEarningDeposit.to_string())

	def test_mergeEarningAndDeposit_bug(self):
		PRINT = False
		self.maxDiff=None
		sbAccountSheetFileName = 'testDepositCHSB_simple_values_1_owner_no_withdrawal.xlsx'
		depositSheetFileName = 'testDepositChsb_fiat_chf_simple_values_1_owner_2_fiats_CHF_USD_no_withdrawal.csv'

		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)

		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB

		sbEarningsDf = self.yieldRateComputer._loadSBEarningSheet(expectedYieldCrypto)
		depositDf, depositCrypto, depositFiatLst = self.yieldRateComputer._loadDepositCsvFile()

		mergedEarningDeposit = self.yieldRateComputer._mergeEarningAndDeposit(sbEarningsDf, depositDf)

		if not PRINT:
			self.assertEqual((365, 8), mergedEarningDeposit.shape)
			self.assertEqual(expectedYieldCrypto, depositCrypto)

		expectedStrDataframe = \
'           DATE  DEP/WITHDR   EARNING CAP   EARNING  CHF AMT  USD AMT  D YIELD RATE  Y YIELD RATE' + \
'''
0    2021-01-01     10000.0  10000.000000  2.611579   5000.0   4800.0      1.000261           1.1
1    2021-01-02         0.0  10002.611579  2.612261      0.0      0.0      1.000261           1.1
2    2021-01-03         0.0  10005.223840  2.612943      0.0      0.0      1.000261           1.1
3    2021-01-04         0.0  10007.836783  2.613625      0.0      0.0      1.000261           1.1
4    2021-01-05         0.0  10010.450408  2.614308      0.0      0.0      1.000261           1.1
5    2021-01-06      1000.0  11013.064716  2.876149   1000.0    980.0      1.000261           1.1
6    2021-01-07         0.0  11015.940865  2.876900      0.0      0.0      1.000261           1.1
7    2021-01-08         0.0  11018.817764  2.877651      0.0      0.0      1.000261           1.1
8    2021-01-09         0.0  11021.695415  2.878403      0.0      0.0      1.000261           1.1
9    2021-01-10         0.0  11024.573818  2.879154      0.0      0.0      1.000261           1.1
10   2021-01-11         0.0  11027.452972  2.879906      0.0      0.0      1.000261           1.1
11   2021-01-12         0.0  11030.332878  2.880658      0.0      0.0      1.000261           1.1
12   2021-01-13         0.0  11033.213537  2.881411      0.0      0.0      1.000261           1.1
13   2021-01-14         0.0  11036.094947  2.882163      0.0      0.0      1.000261           1.1
14   2021-01-15         0.0  11038.977110  2.882916      0.0      0.0      1.000261           1.1
15   2021-01-16         0.0  11041.860026  2.883669      0.0      0.0      1.000261           1.1
16   2021-01-17         0.0  11044.743695  2.884422      0.0      0.0      1.000261           1.1
17   2021-01-18         0.0  11047.628117  2.885175      0.0      0.0      1.000261           1.1
18   2021-01-19         0.0  11050.513292  2.885929      0.0      0.0      1.000261           1.1
19   2021-01-20         0.0  11053.399220  2.886682      0.0      0.0      1.000261           1.1
20   2021-01-21         0.0  11056.285903  2.887436      0.0      0.0      1.000261           1.1
21   2021-01-22         0.0  11059.173339  2.888190      0.0      0.0      1.000261           1.1
22   2021-01-23         0.0  11062.061529  2.888944      0.0      0.0      1.000261           1.1
23   2021-01-24         0.0  11064.950473  2.889699      0.0      0.0      1.000261           1.1
24   2021-01-25         0.0  11067.840172  2.890454      0.0      0.0      1.000261           1.1
25   2021-01-26         0.0  11070.730626  2.891208      0.0      0.0      1.000261           1.1
26   2021-01-27         0.0  11073.621835  2.891964      0.0      0.0      1.000261           1.1
27   2021-01-28         0.0  11076.513798  2.892719      0.0      0.0      1.000261           1.1
28   2021-01-29         0.0  11079.406517  2.893474      0.0      0.0      1.000261           1.1
29   2021-01-30         0.0  11082.299991  2.894230      0.0      0.0      1.000261           1.1
30   2021-01-31         0.0  11085.194221  2.894986      0.0      0.0      1.000261           1.1
31   2021-02-01         0.0  11088.089207  2.895742      0.0      0.0      1.000261           1.1
32   2021-02-02         0.0  11090.984949  2.896498      0.0      0.0      1.000261           1.1
33   2021-02-03         0.0  11093.881447  2.897255      0.0      0.0      1.000261           1.1
34   2021-02-04         0.0  11096.778701  2.898011      0.0      0.0      1.000261           1.1
35   2021-02-05         0.0  11099.676713  2.898768      0.0      0.0      1.000261           1.1
36   2021-02-06         0.0  11102.575481  2.899525      0.0      0.0      1.000261           1.1
37   2021-02-07         0.0  11105.475006  2.900282      0.0      0.0      1.000261           1.1
38   2021-02-08         0.0  11108.375288  2.901040      0.0      0.0      1.000261           1.1
39   2021-02-09         0.0  11111.276328  2.901797      0.0      0.0      1.000261           1.1
40   2021-02-10         0.0  11114.178125  2.902555      0.0      0.0      1.000261           1.1
41   2021-02-11         0.0  11117.080680  2.903313      0.0      0.0      1.000261           1.1
42   2021-02-12         0.0  11119.983993  2.904071      0.0      0.0      1.000261           1.1
43   2021-02-13         0.0  11122.888065  2.904830      0.0      0.0      1.000261           1.1
44   2021-02-14         0.0  11125.792894  2.905588      0.0      0.0      1.000261           1.1
45   2021-02-15         0.0  11128.698483  2.906347      0.0      0.0      1.000261           1.1
46   2021-02-16         0.0  11131.604830  2.907106      0.0      0.0      1.000261           1.1
47   2021-02-17         0.0  11134.511936  2.907865      0.0      0.0      1.000261           1.1
48   2021-02-18         0.0  11137.419802  2.908625      0.0      0.0      1.000261           1.1
49   2021-02-19         0.0  11140.328427  2.909385      0.0      0.0      1.000261           1.1
50   2021-02-20         0.0  11143.237811  2.910144      0.0      0.0      1.000261           1.1
51   2021-02-21         0.0  11146.147956  2.910904      0.0      0.0      1.000261           1.1
52   2021-02-22         0.0  11149.058860  2.911665      0.0      0.0      1.000261           1.1
53   2021-02-23         0.0  11151.970524  2.912425      0.0      0.0      1.000261           1.1
54   2021-02-24         0.0  11154.882949  2.913186      0.0      0.0      1.000261           1.1
55   2021-02-25         0.0  11157.796135  2.913946      0.0      0.0      1.000261           1.1
56   2021-02-26         0.0  11160.710081  2.914707      0.0      0.0      1.000261           1.1
57   2021-02-27         0.0  11163.624789  2.915469      0.0      0.0      1.000261           1.1
58   2021-02-28         0.0  11166.540257  2.916230      0.0      0.0      1.000261           1.1
59   2021-03-01         0.0  11169.456487  2.916992      0.0      0.0      1.000261           1.1
60   2021-03-02         0.0  11172.373479  2.917753      0.0      0.0      1.000261           1.1
61   2021-03-03         0.0  11175.291232  2.918515      0.0      0.0      1.000261           1.1
62   2021-03-04         0.0  11178.209747  2.919278      0.0      0.0      1.000261           1.1
63   2021-03-05         0.0  11181.129025  2.920040      0.0      0.0      1.000261           1.1
64   2021-03-06         0.0  11184.049065  2.920802      0.0      0.0      1.000261           1.1
65   2021-03-07         0.0  11186.969867  2.921565      0.0      0.0      1.000261           1.1
66   2021-03-08         0.0  11189.891432  2.922328      0.0      0.0      1.000261           1.1
67   2021-03-09         0.0  11192.813761  2.923091      0.0      0.0      1.000261           1.1
68   2021-03-10         0.0  11195.736852  2.923855      0.0      0.0      1.000261           1.1
69   2021-03-11         0.0  11198.660707  2.924618      0.0      0.0      1.000261           1.1
70   2021-03-12         0.0  11201.585326  2.925382      0.0      0.0      1.000261           1.1
71   2021-03-13         0.0  11204.510708  2.926146      0.0      0.0      1.000261           1.1
72   2021-03-14         0.0  11207.436854  2.926910      0.0      0.0      1.000261           1.1
73   2021-03-15         0.0  11210.363764  2.927675      0.0      0.0      1.000261           1.1
74   2021-03-16         0.0  11213.291439  2.928439      0.0      0.0      1.000261           1.1
75   2021-03-17         0.0  11216.219879  2.929204      0.0      0.0      1.000261           1.1
76   2021-03-18         0.0  11219.149083  2.929969      0.0      0.0      1.000261           1.1
77   2021-03-19         0.0  11222.079052  2.930734      0.0      0.0      1.000261           1.1
78   2021-03-20         0.0  11225.009786  2.931500      0.0      0.0      1.000261           1.1
79   2021-03-21         0.0  11227.941286  2.932265      0.0      0.0      1.000261           1.1
80   2021-03-22         0.0  11230.873551  2.933031      0.0      0.0      1.000261           1.1
81   2021-03-23         0.0  11233.806582  2.933797      0.0      0.0      1.000261           1.1
82   2021-03-24         0.0  11236.740379  2.934563      0.0      0.0      1.000261           1.1
83   2021-03-25         0.0  11239.674943  2.935330      0.0      0.0      1.000261           1.1
84   2021-03-26         0.0  11242.610272  2.936096      0.0      0.0      1.000261           1.1
85   2021-03-27         0.0  11245.546368  2.936863      0.0      0.0      1.000261           1.1
86   2021-03-28         0.0  11248.483231  2.937630      0.0      0.0      1.000261           1.1
87   2021-03-29         0.0  11251.420861  2.938397      0.0      0.0      1.000261           1.1
88   2021-03-30         0.0  11254.359259  2.939165      0.0      0.0      1.000261           1.1
89   2021-03-31         0.0  11257.298423  2.939932      0.0      0.0      1.000261           1.1
90   2021-04-01         0.0  11260.238355  2.940700      0.0      0.0      1.000261           1.1
91   2021-04-02         0.0  11263.179055  2.941468      0.0      0.0      1.000261           1.1
92   2021-04-03         0.0  11266.120523  2.942236      0.0      0.0      1.000261           1.1
93   2021-04-04         0.0  11269.062759  2.943004      0.0      0.0      1.000261           1.1
94   2021-04-05         0.0  11272.005764  2.943773      0.0      0.0      1.000261           1.1
95   2021-04-06         0.0  11274.949537  2.944542      0.0      0.0      1.000261           1.1
96   2021-04-07         0.0  11277.894079  2.945311      0.0      0.0      1.000261           1.1
97   2021-04-08         0.0  11280.839390  2.946080      0.0      0.0      1.000261           1.1
98   2021-04-09         0.0  11283.785470  2.946849      0.0      0.0      1.000261           1.1
99   2021-04-10         0.0  11286.732319  2.947619      0.0      0.0      1.000261           1.1
100  2021-04-11         0.0  11289.679938  2.948389      0.0      0.0      1.000261           1.1
101  2021-04-12         0.0  11292.628327  2.949159      0.0      0.0      1.000261           1.1
102  2021-04-13         0.0  11295.577486  2.949929      0.0      0.0      1.000261           1.1
103  2021-04-14         0.0  11298.527415  2.950699      0.0      0.0      1.000261           1.1
104  2021-04-15         0.0  11301.478114  2.951470      0.0      0.0      1.000261           1.1
105  2021-04-16         0.0  11304.429584  2.952241      0.0      0.0      1.000261           1.1
106  2021-04-17         0.0  11307.381825  2.953012      0.0      0.0      1.000261           1.1
107  2021-04-18         0.0  11310.334837  2.953783      0.0      0.0      1.000261           1.1
108  2021-04-19         0.0  11313.288620  2.954554      0.0      0.0      1.000261           1.1
109  2021-04-20         0.0  11316.243174  2.955326      0.0      0.0      1.000261           1.1
110  2021-04-21         0.0  11319.198500  2.956098      0.0      0.0      1.000261           1.1
111  2021-04-22         0.0  11322.154598  2.956870      0.0      0.0      1.000261           1.1
112  2021-04-23         0.0  11325.111468  2.957642      0.0      0.0      1.000261           1.1
113  2021-04-24         0.0  11328.069110  2.958414      0.0      0.0      1.000261           1.1
114  2021-04-25         0.0  11331.027525  2.959187      0.0      0.0      1.000261           1.1
115  2021-04-26         0.0  11333.986712  2.959960      0.0      0.0      1.000261           1.1
116  2021-04-27         0.0  11336.946672  2.960733      0.0      0.0      1.000261           1.1
117  2021-04-28         0.0  11339.907405  2.961506      0.0      0.0      1.000261           1.1
118  2021-04-29         0.0  11342.868911  2.962280      0.0      0.0      1.000261           1.1
119  2021-04-30         0.0  11345.831190  2.963053      0.0      0.0      1.000261           1.1
120  2021-05-01         0.0  11348.794243  2.963827      0.0      0.0      1.000261           1.1
121  2021-05-02         0.0  11351.758070  2.964601      0.0      0.0      1.000261           1.1
122  2021-05-03         0.0  11354.722671  2.965375      0.0      0.0      1.000261           1.1
123  2021-05-04         0.0  11357.688047  2.966150      0.0      0.0      1.000261           1.1
124  2021-05-05         0.0  11360.654196  2.966924      0.0      0.0      1.000261           1.1
125  2021-05-06         0.0  11363.621121  2.967699      0.0      0.0      1.000261           1.1
126  2021-05-07         0.0  11366.588820  2.968474      0.0      0.0      1.000261           1.1
127  2021-05-08         0.0  11369.557294  2.969249      0.0      0.0      1.000261           1.1
128  2021-05-09         0.0  11372.526543  2.970025      0.0      0.0      1.000261           1.1
129  2021-05-10         0.0  11375.496568  2.970801      0.0      0.0      1.000261           1.1
130  2021-05-11         0.0  11378.467369  2.971576      0.0      0.0      1.000261           1.1
131  2021-05-12         0.0  11381.438945  2.972352      0.0      0.0      1.000261           1.1
132  2021-05-13         0.0  11384.411298  2.973129      0.0      0.0      1.000261           1.1
133  2021-05-14         0.0  11387.384426  2.973905      0.0      0.0      1.000261           1.1
134  2021-05-15         0.0  11390.358331  2.974682      0.0      0.0      1.000261           1.1
135  2021-05-16         0.0  11393.333013  2.975459      0.0      0.0      1.000261           1.1
136  2021-05-17         0.0  11396.308472  2.976236      0.0      0.0      1.000261           1.1
137  2021-05-18         0.0  11399.284708  2.977013      0.0      0.0      1.000261           1.1
138  2021-05-19         0.0  11402.261721  2.977790      0.0      0.0      1.000261           1.1
139  2021-05-20         0.0  11405.239511  2.978568      0.0      0.0      1.000261           1.1
140  2021-05-21         0.0  11408.218079  2.979346      0.0      0.0      1.000261           1.1
141  2021-05-22         0.0  11411.197425  2.980124      0.0      0.0      1.000261           1.1
142  2021-05-23         0.0  11414.177549  2.980902      0.0      0.0      1.000261           1.1
143  2021-05-24         0.0  11417.158452  2.981681      0.0      0.0      1.000261           1.1
144  2021-05-25         0.0  11420.140132  2.982460      0.0      0.0      1.000261           1.1
145  2021-05-26         0.0  11423.122592  2.983238      0.0      0.0      1.000261           1.1
146  2021-05-27         0.0  11426.105830  2.984018      0.0      0.0      1.000261           1.1
147  2021-05-28         0.0  11429.089848  2.984797      0.0      0.0      1.000261           1.1
148  2021-05-29         0.0  11432.074645  2.985576      0.0      0.0      1.000261           1.1
149  2021-05-30         0.0  11435.060221  2.986356      0.0      0.0      1.000261           1.1
150  2021-05-31         0.0  11438.046577  2.987136      0.0      0.0      1.000261           1.1
151  2021-06-01         0.0  11441.033713  2.987916      0.0      0.0      1.000261           1.1
152  2021-06-02         0.0  11444.021629  2.988696      0.0      0.0      1.000261           1.1
153  2021-06-03         0.0  11447.010326  2.989477      0.0      0.0      1.000261           1.1
154  2021-06-04         0.0  11449.999802  2.990258      0.0      0.0      1.000261           1.1
155  2021-06-05         0.0  11452.990060  2.991039      0.0      0.0      1.000261           1.1
156  2021-06-06         0.0  11455.981099  2.991820      0.0      0.0      1.000261           1.1
157  2021-06-07         0.0  11458.972918  2.992601      0.0      0.0      1.000261           1.1
158  2021-06-08         0.0  11461.965519  2.993383      0.0      0.0      1.000261           1.1
159  2021-06-09         0.0  11464.958902  2.994164      0.0      0.0      1.000261           1.1
160  2021-06-10         0.0  11467.953066  2.994946      0.0      0.0      1.000261           1.1
161  2021-06-11         0.0  11470.948013  2.995728      0.0      0.0      1.000261           1.1
162  2021-06-12         0.0  11473.943741  2.996511      0.0      0.0      1.000261           1.1
163  2021-06-13         0.0  11476.940252  2.997293      0.0      0.0      1.000261           1.1
164  2021-06-14         0.0  11479.937545  2.998076      0.0      0.0      1.000261           1.1
165  2021-06-15         0.0  11482.935621  2.998859      0.0      0.0      1.000261           1.1
166  2021-06-16         0.0  11485.934480  2.999642      0.0      0.0      1.000261           1.1
167  2021-06-17         0.0  11488.934123  3.000426      0.0      0.0      1.000261           1.1
168  2021-06-18         0.0  11491.934548  3.001209      0.0      0.0      1.000261           1.1
169  2021-06-19         0.0  11494.935757  3.001993      0.0      0.0      1.000261           1.1
170  2021-06-20         0.0  11497.937750  3.002777      0.0      0.0      1.000261           1.1
171  2021-06-21         0.0  11500.940527  3.003561      0.0      0.0      1.000261           1.1
172  2021-06-22         0.0  11503.944089  3.004346      0.0      0.0      1.000261           1.1
173  2021-06-23         0.0  11506.948434  3.005130      0.0      0.0      1.000261           1.1
174  2021-06-24         0.0  11509.953564  3.005915      0.0      0.0      1.000261           1.1
175  2021-06-25         0.0  11512.959479  3.006700      0.0      0.0      1.000261           1.1
176  2021-06-26         0.0  11515.966179  3.007485      0.0      0.0      1.000261           1.1
177  2021-06-27         0.0  11518.973665  3.008271      0.0      0.0      1.000261           1.1
178  2021-06-28         0.0  11521.981935  3.009056      0.0      0.0      1.000261           1.1
179  2021-06-29         0.0  11524.990992  3.009842      0.0      0.0      1.000261           1.1
180  2021-06-30         0.0  11528.000834  3.010628      0.0      0.0      1.000261           1.1
181  2021-07-01         0.0  11531.011462  3.011414      0.0      0.0      1.000261           1.1
182  2021-07-02         0.0  11534.022877  3.012201      0.0      0.0      1.000261           1.1
183  2021-07-03         0.0  11537.035078  3.012988      0.0      0.0      1.000261           1.1
184  2021-07-04         0.0  11540.048065  3.013774      0.0      0.0      1.000261           1.1
185  2021-07-05         0.0  11543.061840  3.014562      0.0      0.0      1.000261           1.1
186  2021-07-06         0.0  11546.076401  3.015349      0.0      0.0      1.000261           1.1
187  2021-07-07         0.0  11549.091750  3.016136      0.0      0.0      1.000261           1.1
188  2021-07-08         0.0  11552.107886  3.016924      0.0      0.0      1.000261           1.1
189  2021-07-09         0.0  11555.124810  3.017712      0.0      0.0      1.000261           1.1
190  2021-07-10         0.0  11558.142522  3.018500      0.0      0.0      1.000261           1.1
191  2021-07-11         0.0  11561.161022  3.019288      0.0      0.0      1.000261           1.1
192  2021-07-12         0.0  11564.180310  3.020077      0.0      0.0      1.000261           1.1
193  2021-07-13         0.0  11567.200387  3.020865      0.0      0.0      1.000261           1.1
194  2021-07-14         0.0  11570.221252  3.021654      0.0      0.0      1.000261           1.1
195  2021-07-15         0.0  11573.242907  3.022444      0.0      0.0      1.000261           1.1
196  2021-07-16         0.0  11576.265350  3.023233      0.0      0.0      1.000261           1.1
197  2021-07-17         0.0  11579.288583  3.024022      0.0      0.0      1.000261           1.1
198  2021-07-18         0.0  11582.312606  3.024812      0.0      0.0      1.000261           1.1
199  2021-07-19         0.0  11585.337418  3.025602      0.0      0.0      1.000261           1.1
200  2021-07-20         0.0  11588.363020  3.026392      0.0      0.0      1.000261           1.1
201  2021-07-21         0.0  11591.389412  3.027183      0.0      0.0      1.000261           1.1
202  2021-07-22         0.0  11594.416595  3.027973      0.0      0.0      1.000261           1.1
203  2021-07-23         0.0  11597.444568  3.028764      0.0      0.0      1.000261           1.1
204  2021-07-24         0.0  11600.473332  3.029555      0.0      0.0      1.000261           1.1
205  2021-07-25         0.0  11603.502887  3.030346      0.0      0.0      1.000261           1.1
206  2021-07-26         0.0  11606.533233  3.031138      0.0      0.0      1.000261           1.1
207  2021-07-27         0.0  11609.564371  3.031929      0.0      0.0      1.000261           1.1
208  2021-07-28         0.0  11612.596300  3.032721      0.0      0.0      1.000261           1.1
209  2021-07-29         0.0  11615.629021  3.033513      0.0      0.0      1.000261           1.1
210  2021-07-30         0.0  11618.662534  3.034305      0.0      0.0      1.000261           1.1
211  2021-07-31         0.0  11621.696839  3.035098      0.0      0.0      1.000261           1.1
212  2021-08-01         0.0  11624.731937  3.035890      0.0      0.0      1.000261           1.1
213  2021-08-02         0.0  11627.767827  3.036683      0.0      0.0      1.000261           1.1
214  2021-08-03         0.0  11630.804510  3.037476      0.0      0.0      1.000261           1.1
215  2021-08-04         0.0  11633.841986  3.038269      0.0      0.0      1.000261           1.1
216  2021-08-05         0.0  11636.880256  3.039063      0.0      0.0      1.000261           1.1
217  2021-08-06         0.0  11639.919319  3.039857      0.0      0.0      1.000261           1.1
218  2021-08-07         0.0  11642.959175  3.040650      0.0      0.0      1.000261           1.1
219  2021-08-08         0.0  11645.999826  3.041445      0.0      0.0      1.000261           1.1
220  2021-08-09         0.0  11649.041271  3.042239      0.0      0.0      1.000261           1.1
221  2021-08-10         0.0  11652.083509  3.043033      0.0      0.0      1.000261           1.1
222  2021-08-11         0.0  11655.126543  3.043828      0.0      0.0      1.000261           1.1
223  2021-08-12         0.0  11658.170371  3.044623      0.0      0.0      1.000261           1.1
224  2021-08-13         0.0  11661.214994  3.045418      0.0      0.0      1.000261           1.1
225  2021-08-14         0.0  11664.260412  3.046213      0.0      0.0      1.000261           1.1
226  2021-08-15         0.0  11667.306625  3.047009      0.0      0.0      1.000261           1.1
227  2021-08-16         0.0  11670.353635  3.047805      0.0      0.0      1.000261           1.1
228  2021-08-17         0.0  11673.401439  3.048601      0.0      0.0      1.000261           1.1
229  2021-08-18         0.0  11676.450040  3.049397      0.0      0.0      1.000261           1.1
230  2021-08-19         0.0  11679.499437  3.050193      0.0      0.0      1.000261           1.1
231  2021-08-20         0.0  11682.549630  3.050990      0.0      0.0      1.000261           1.1
232  2021-08-21         0.0  11685.600620  3.051787      0.0      0.0      1.000261           1.1
233  2021-08-22         0.0  11688.652407  3.052584      0.0      0.0      1.000261           1.1
234  2021-08-23         0.0  11691.704990  3.053381      0.0      0.0      1.000261           1.1
235  2021-08-24         0.0  11694.758371  3.054178      0.0      0.0      1.000261           1.1
236  2021-08-25         0.0  11697.812549  3.054976      0.0      0.0      1.000261           1.1
237  2021-08-26         0.0  11700.867525  3.055774      0.0      0.0      1.000261           1.1
238  2021-08-27         0.0  11703.923299  3.056572      0.0      0.0      1.000261           1.1
239  2021-08-28         0.0  11706.979871  3.057370      0.0      0.0      1.000261           1.1
240  2021-08-29         0.0  11710.037241  3.058168      0.0      0.0      1.000261           1.1
241  2021-08-30         0.0  11713.095409  3.058967      0.0      0.0      1.000261           1.1
242  2021-08-31         0.0  11716.154376  3.059766      0.0      0.0      1.000261           1.1
243  2021-09-01         0.0  11719.214142  3.060565      0.0      0.0      1.000261           1.1
244  2021-09-02         0.0  11722.274707  3.061364      0.0      0.0      1.000261           1.1
245  2021-09-03         0.0  11725.336072  3.062164      0.0      0.0      1.000261           1.1
246  2021-09-04         0.0  11728.398236  3.062964      0.0      0.0      1.000261           1.1
247  2021-09-05         0.0  11731.461199  3.063763      0.0      0.0      1.000261           1.1
248  2021-09-06         0.0  11734.524963  3.064564      0.0      0.0      1.000261           1.1
249  2021-09-07         0.0  11737.589526  3.065364      0.0      0.0      1.000261           1.1
250  2021-09-08         0.0  11740.654890  3.066164      0.0      0.0      1.000261           1.1
251  2021-09-09         0.0  11743.721055  3.066965      0.0      0.0      1.000261           1.1
252  2021-09-10         0.0  11746.788020  3.067766      0.0      0.0      1.000261           1.1
253  2021-09-11         0.0  11749.855786  3.068567      0.0      0.0      1.000261           1.1
254  2021-09-12         0.0  11752.924354  3.069369      0.0      0.0      1.000261           1.1
255  2021-09-13         0.0  11755.993722  3.070170      0.0      0.0      1.000261           1.1
256  2021-09-14         0.0  11759.063893  3.070972      0.0      0.0      1.000261           1.1
257  2021-09-15         0.0  11762.134865  3.071774      0.0      0.0      1.000261           1.1
258  2021-09-16         0.0  11765.206639  3.072576      0.0      0.0      1.000261           1.1
259  2021-09-17         0.0  11768.279215  3.073379      0.0      0.0      1.000261           1.1
260  2021-09-18         0.0  11771.352594  3.074181      0.0      0.0      1.000261           1.1
261  2021-09-19         0.0  11774.426776  3.074984      0.0      0.0      1.000261           1.1
262  2021-09-20         0.0  11777.501760  3.075787      0.0      0.0      1.000261           1.1
263  2021-09-21         0.0  11780.577547  3.076591      0.0      0.0      1.000261           1.1
264  2021-09-22         0.0  11783.654138  3.077394      0.0      0.0      1.000261           1.1
265  2021-09-23         0.0  11786.731532  3.078198      0.0      0.0      1.000261           1.1
266  2021-09-24         0.0  11789.809730  3.079002      0.0      0.0      1.000261           1.1
267  2021-09-25         0.0  11792.888731  3.079806      0.0      0.0      1.000261           1.1
268  2021-09-26         0.0  11795.968537  3.080610      0.0      0.0      1.000261           1.1
269  2021-09-27         0.0  11799.049147  3.081415      0.0      0.0      1.000261           1.1
270  2021-09-28         0.0  11802.130562  3.082219      0.0      0.0      1.000261           1.1
271  2021-09-29         0.0  11805.212781  3.083024      0.0      0.0      1.000261           1.1
272  2021-09-30         0.0  11808.295806  3.083829      0.0      0.0      1.000261           1.1
273  2021-10-01         0.0  11811.379635  3.084635      0.0      0.0      1.000261           1.1
274  2021-10-02         0.0  11814.464270  3.085440      0.0      0.0      1.000261           1.1
275  2021-10-03         0.0  11817.549710  3.086246      0.0      0.0      1.000261           1.1
276  2021-10-04         0.0  11820.635956  3.087052      0.0      0.0      1.000261           1.1
277  2021-10-05         0.0  11823.723009  3.087858      0.0      0.0      1.000261           1.1
278  2021-10-06         0.0  11826.810867  3.088665      0.0      0.0      1.000261           1.1
279  2021-10-07         0.0  11829.899532  3.089471      0.0      0.0      1.000261           1.1
280  2021-10-08         0.0  11832.989003  3.090278      0.0      0.0      1.000261           1.1
281  2021-10-09         0.0  11836.079281  3.091085      0.0      0.0      1.000261           1.1
282  2021-10-10         0.0  11839.170367  3.091893      0.0      0.0      1.000261           1.1
283  2021-10-11         0.0  11842.262259  3.092700      0.0      0.0      1.000261           1.1
284  2021-10-12         0.0  11845.354959  3.093508      0.0      0.0      1.000261           1.1
285  2021-10-13         0.0  11848.448467  3.094316      0.0      0.0      1.000261           1.1
286  2021-10-14         0.0  11851.542783  3.095124      0.0      0.0      1.000261           1.1
287  2021-10-15         0.0  11854.637907  3.095932      0.0      0.0      1.000261           1.1
288  2021-10-16         0.0  11857.733839  3.096741      0.0      0.0      1.000261           1.1
289  2021-10-17         0.0  11860.830579  3.097549      0.0      0.0      1.000261           1.1
290  2021-10-18         0.0  11863.928128  3.098358      0.0      0.0      1.000261           1.1
291  2021-10-19         0.0  11867.026487  3.099167      0.0      0.0      1.000261           1.1
292  2021-10-20         0.0  11870.125654  3.099977      0.0      0.0      1.000261           1.1
293  2021-10-21         0.0  11873.225631  3.100786      0.0      0.0      1.000261           1.1
294  2021-10-22         0.0  11876.326417  3.101596      0.0      0.0      1.000261           1.1
295  2021-10-23         0.0  11879.428014  3.102406      0.0      0.0      1.000261           1.1
296  2021-10-24         0.0  11882.530420  3.103216      0.0      0.0      1.000261           1.1
297  2021-10-25         0.0  11885.633636  3.104027      0.0      0.0      1.000261           1.1
298  2021-10-26         0.0  11888.737663  3.104837      0.0      0.0      1.000261           1.1
299  2021-10-27         0.0  11891.842500  3.105648      0.0      0.0      1.000261           1.1
300  2021-10-28         0.0  11894.948149  3.106459      0.0      0.0      1.000261           1.1
301  2021-10-29         0.0  11898.054608  3.107271      0.0      0.0      1.000261           1.1
302  2021-10-30         0.0  11901.161879  3.108082      0.0      0.0      1.000261           1.1
303  2021-10-31         0.0  11904.269961  3.108894      0.0      0.0      1.000261           1.1
304  2021-11-01         0.0  11907.378855  3.109706      0.0      0.0      1.000261           1.1
305  2021-11-02         0.0  11910.488561  3.110518      0.0      0.0      1.000261           1.1
306  2021-11-03         0.0  11913.599079  3.111330      0.0      0.0      1.000261           1.1
307  2021-11-04         0.0  11916.710409  3.112143      0.0      0.0      1.000261           1.1
308  2021-11-05         0.0  11919.822552  3.112956      0.0      0.0      1.000261           1.1
309  2021-11-06         0.0  11922.935507  3.113769      0.0      0.0      1.000261           1.1
310  2021-11-07         0.0  11926.049276  3.114582      0.0      0.0      1.000261           1.1
311  2021-11-08         0.0  11929.163857  3.115395      0.0      0.0      1.000261           1.1
312  2021-11-09         0.0  11932.279252  3.116209      0.0      0.0      1.000261           1.1
313  2021-11-10         0.0  11935.395461  3.117023      0.0      0.0      1.000261           1.1
314  2021-11-11         0.0  11938.512484  3.117837      0.0      0.0      1.000261           1.1
315  2021-11-12         0.0  11941.630320  3.118651      0.0      0.0      1.000261           1.1
316  2021-11-13         0.0  11944.748971  3.119465      0.0      0.0      1.000261           1.1
317  2021-11-14         0.0  11947.868436  3.120280      0.0      0.0      1.000261           1.1
318  2021-11-15         0.0  11950.988716  3.121095      0.0      0.0      1.000261           1.1
319  2021-11-16         0.0  11954.109811  3.121910      0.0      0.0      1.000261           1.1
320  2021-11-17         0.0  11957.231721  3.122725      0.0      0.0      1.000261           1.1
321  2021-11-18         0.0  11960.354446  3.123541      0.0      0.0      1.000261           1.1
322  2021-11-19         0.0  11963.477987  3.124357      0.0      0.0      1.000261           1.1
323  2021-11-20         0.0  11966.602344  3.125172      0.0      0.0      1.000261           1.1
324  2021-11-21         0.0  11969.727516  3.125989      0.0      0.0      1.000261           1.1
325  2021-11-22         0.0  11972.853505  3.126805      0.0      0.0      1.000261           1.1
326  2021-11-23         0.0  11975.980310  3.127622      0.0      0.0      1.000261           1.1
327  2021-11-24         0.0  11979.107931  3.128438      0.0      0.0      1.000261           1.1
328  2021-11-25         0.0  11982.236370  3.129255      0.0      0.0      1.000261           1.1
329  2021-11-26         0.0  11985.365625  3.130073      0.0      0.0      1.000261           1.1
330  2021-11-27         0.0  11988.495698  3.130890      0.0      0.0      1.000261           1.1
331  2021-11-28         0.0  11991.626588  3.131708      0.0      0.0      1.000261           1.1
332  2021-11-29         0.0  11994.758295  3.132526      0.0      0.0      1.000261           1.1
333  2021-11-30         0.0  11997.890821  3.133344      0.0      0.0      1.000261           1.1
334  2021-12-01         0.0  12001.024165  3.134162      0.0      0.0      1.000261           1.1
335  2021-12-02         0.0  12004.158327  3.134980      0.0      0.0      1.000261           1.1
336  2021-12-03         0.0  12007.293307  3.135799      0.0      0.0      1.000261           1.1
337  2021-12-04         0.0  12010.429106  3.136618      0.0      0.0      1.000261           1.1
338  2021-12-05         0.0  12013.565725  3.137437      0.0      0.0      1.000261           1.1
339  2021-12-06         0.0  12016.703162  3.138257      0.0      0.0      1.000261           1.1
340  2021-12-07         0.0  12019.841418  3.139076      0.0      0.0      1.000261           1.1
341  2021-12-08         0.0  12022.980495  3.139896      0.0      0.0      1.000261           1.1
342  2021-12-09         0.0  12026.120391  3.140716      0.0      0.0      1.000261           1.1
343  2021-12-10         0.0  12029.261107  3.141536      0.0      0.0      1.000261           1.1
344  2021-12-11         0.0  12032.402643  3.142357      0.0      0.0      1.000261           1.1
345  2021-12-12         0.0  12035.545000  3.143177      0.0      0.0      1.000261           1.1
346  2021-12-13         0.0  12038.688177  3.143998      0.0      0.0      1.000261           1.1
347  2021-12-14         0.0  12041.832175  3.144819      0.0      0.0      1.000261           1.1
348  2021-12-15         0.0  12044.976995  3.145641      0.0      0.0      1.000261           1.1
349  2021-12-16         0.0  12048.122635  3.146462      0.0      0.0      1.000261           1.1
350  2021-12-17         0.0  12051.269098  3.147284      0.0      0.0      1.000261           1.1
351  2021-12-18         0.0  12054.416381  3.148106      0.0      0.0      1.000261           1.1
352  2021-12-19         0.0  12057.564487  3.148928      0.0      0.0      1.000261           1.1
353  2021-12-20         0.0  12060.713415  3.149750      0.0      0.0      1.000261           1.1
354  2021-12-21         0.0  12063.863165  3.150573      0.0      0.0      1.000261           1.1
355  2021-12-22         0.0  12067.013738  3.151396      0.0      0.0      1.000261           1.1
356  2021-12-23         0.0  12070.165134  3.152219      0.0      0.0      1.000261           1.1
357  2021-12-24         0.0  12073.317353  3.153042      0.0      0.0      1.000261           1.1
358  2021-12-25         0.0  12076.470395  3.153865      0.0      0.0      1.000261           1.1
359  2021-12-26         0.0  12079.624260  3.154689      0.0      0.0      1.000261           1.1
360  2021-12-27         0.0  12082.778949  3.155513      0.0      0.0      1.000261           1.1
361  2021-12-28         0.0  12085.934462  3.156337      0.0      0.0      1.000261           1.1
362  2021-12-29         0.0  12089.090799  3.157161      0.0      0.0      1.000261           1.1
363  2021-12-30         0.0  12092.247960  3.157986      0.0      0.0      1.000261           1.1
364  2021-12-31         0.0  12095.405946  3.158811      0.0      0.0      1.000261           1.1'''

		if PRINT:
			print(mergedEarningDeposit.to_string())
		else:
			self.assertEqual(expectedStrDataframe, mergedEarningDeposit.to_string())

	def testGetDepositsAndDailyYieldRatesDataframes(self):
		PRINT = False
		
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc_1.csv'
		
		self.initializeComputerClasses(sbAccountSheetFileName, depositSheetFileName)
		
		expectedYieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		depositDataFrame, depositCrypto, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes()

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
		
		depositDataFrame, depositCrypto, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes()
		
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
		
		depositDataFrame, depositCrypto, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes()

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
		
		depositDataFrame, depositCrypto, yieldRatesDataframe = self.yieldRateComputer.getDepositsAndDailyYieldRatesDataframes()
		
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
	if os.name == 'posix':
		unittest.main()
	else:
		tst = TestSBYieldRateComputer()
		tst.setUp()
		#tst.test_mergeEarningAndDeposit()
		# tst.test_mergeEarningAndDeposit_bug()
#   	tst.testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_2_deposit()
#   	tst.testGetDepositsAndDailyYieldRatesDataframes_uniqueOwner_1_deposit_1_partial_withdr()
#   	tst.test_loadDepositCsvFileWithFiatColumns_2()
		tst.test_loadDepositCsvFileWithTimeComponentAfterNineOClock()
