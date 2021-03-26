import numpy as np
import pandas as pd

# Swissborg account statement sheet parameters
from pandasdatacomputer import *


SB_ACCOUNT_SHEET_FIAT = 'USD'           # earning fiat: USD or CHF as defined when downloading the account statement Excel sheet
SB_ACCOUNT_SHEET_NAME = 'Transactions'  # name of the spreadsheet
SB_ACCOUNT_SHEET_SKIP_ROWS = 8          # number of lines above the column headers to skip

# Swissborg account statement sheet column headers
SB_ACCOUNT_SHEET_HEADER_DATE = 'Local time'     # yyyy-mm-dd hh:mm
SB_ACCOUNT_SHEET_HEADER_EARNING = 'Net amount'  # column containing the daily earning in USDC or CHSB for example
SB_ACCOUNT_SHEET_HEADER_TYPE = 'Type'           # row type: Earnings or Deposit for example
SB_ACCOUNT_SHEET_HEADER_CURRENCY = 'Currency'   # USDC or CHSB for example

# Swissborg account statement sheet columns to remove
SB_ACCOUNT_SHEET_UNUSED_COLUMNS_LIST = ['Time in UTC',
										'Fee',
										'Fee ({})'.format(SB_ACCOUNT_SHEET_FIAT),
										'Gross amount ({})'.format(SB_ACCOUNT_SHEET_FIAT),
										'Gross amount',
										'Net amount ({})'.format(SB_ACCOUNT_SHEET_FIAT),
										'Note']

# columns which can be later removed from the Swissborg account statement data frame
SB_ACCOUNT_SHEET_NO_LONGER_USED_COLUMNS_LIST = [SB_ACCOUNT_SHEET_HEADER_TYPE,
                                                SB_ACCOUNT_SHEET_HEADER_CURRENCY]

# two new columns to add to the Swissborg account statement sheet
SB_ACCOUNT_SHEET_HEADER_EARNING_CAPITAL = 'EARNING CAP'

SB_ACCOUNT_SHEET_TYPE_EARNING = 'Earnings'  # used to filter rows
SB_ACCOUNT_SHEET_CURRENCY_USDC = 'USDC'     # used to filter rows
SB_ACCOUNT_SHEET_CURRENCY_CHSB = 'CHSB'     # used to filter rows
SB_ACCOUNT_SHEET_CURRENCY_ETH = 'ETH'       # used to filter rows

# Deposit/Withdrawal sheet parameters
DEPOSIT_SHEET_HEADER_DATE = 'DATE'
DEPOSIT_SHEET_HEADER_OWNER = 'OWNER'

# Swissborg account statement merged with deposit/withdrawal sheet parameters
MERGED_SHEET_HEADER_DATE = SB_ACCOUNT_SHEET_HEADER_DATE
MERGED_SHEET_HEADER_EARNING_CAPITAL = SB_ACCOUNT_SHEET_HEADER_EARNING_CAPITAL
MERGED_SHEET_HEADER_EARNING = SB_ACCOUNT_SHEET_HEADER_EARNING
MERGED_SHEET_HEADER_DATE_NEW_NAME = 'DATE'
MERGED_SHEET_HEADER_EARNING_NEW_NAME = 'EARNINGS'
MERGED_SHEET_HEADER_DAILY_YIELD_RATE = 'DAILY YIELD RATE'
MERGED_SHEET_HEADER_YEARLY_YIELD_RATE = 'YEARLY YIELD RATE'

class SBYieldRateComputer(PandasDataComputer):
	"""
	This class loads the Swissborg account statement xlsl sheet and the Deposit/Withdrawal
	csv file. The Swissborg account statement xlsl sheet contains the yield earnings
	payed daily by Swissborg. The Deposit/Withdrawal csv file contains the deposits and
	withdrawals done for the different owners at the date when they start (for deposits) or
	stop (for withdrawals) to earn Swissborg yield amounts.
	
	The class uses the deposit/withdrawal amount and date to compute the daily capital
	amounts which generate earnings. It can then compute the daily yield rates which
	are stored in the returned daily yield rates dataframe.
	
	The daily yield rates will be used by the OwnerDepositYieldComputer class to spread
	out the Swissborg daily earnings proportionally to the deposit/withdrawal amounts
	invested by the different yield subscription amounts owners.
	"""
	def __init__(self, configMgr, sbAccountSheetFilePathName, depositSheetFilePathName):
		"""
		Currently, the configMgr is not used. Constants are used in place.
		
		:param configMgr:
		"""
		super().__init__(configMgr)
		self.sbAccountSheetFilePathName = sbAccountSheetFilePathName
		self.depositSheetFilePathName = depositSheetFilePathName
	
	def _loadSBEarningSheet(self, yieldCrypto):
		"""
		Creates a Pandas data frame from the Swissborg account statement sheet, removing
		unused columns. It then selects only the 'Earnings' type rows for the passed
		yieldCrypto (currently USDC or CHSB).
		
		:param sbAccountSheetFilePathName:
		:param yieldCrypto: used to filter SB sheet rows. currently USDC or CHSB
		:return:
		"""
		xls = pd.ExcelFile(self.sbAccountSheetFilePathName,
						   engine='openpyxl') # this parm is required on Android !
		
		sbEarningsDf = xls.parse(SB_ACCOUNT_SHEET_NAME,
								 skiprows=SB_ACCOUNT_SHEET_SKIP_ROWS,
								 parse_dates=[SB_ACCOUNT_SHEET_HEADER_DATE])
		sbEarningsDf = sbEarningsDf.set_index([SB_ACCOUNT_SHEET_HEADER_DATE])

		# drop unused columns
		sbEarningsDf = sbEarningsDf.drop(columns=SB_ACCOUNT_SHEET_UNUSED_COLUMNS_LIST)
		
		# filter useful rows
		isTypeEarning = sbEarningsDf[SB_ACCOUNT_SHEET_HEADER_TYPE] == SB_ACCOUNT_SHEET_TYPE_EARNING
		isTargetCurrency = sbEarningsDf[SB_ACCOUNT_SHEET_HEADER_CURRENCY] == yieldCrypto
		sbEarningsDf = sbEarningsDf[isTypeEarning & isTargetCurrency]
		
		return sbEarningsDf
	
	def _loadDepositSheet(self):
		"""
		Creates a Pandas data frame from the Deposit/Withdrawal sheet.
		
		:param sbDepositSheetFilePathName:
		:return:
		"""
		depositSheetSkipRows = self._determineDepositSheetSkipRows(self.depositSheetFilePathName,
		                                                           DEPOSIT_SHEET_HEADER_OWNER)
		depositsDf = pd.read_csv(self.depositSheetFilePathName,
		                         skiprows=depositSheetSkipRows,
		                         parse_dates=[DEPOSIT_SHEET_HEADER_DATE],
		                         dtype={DATAFRAME_HEADER_DEPOSIT_WITHDRAW: np.float64})
		depositsDf = depositsDf.set_index([DEPOSIT_SHEET_HEADER_DATE])
		
		return depositsDf

	def _mergeEarningAndDeposit(self, earningDf, depositDf):
		"""
		Merges Deposit/Withdrawal dataframe into the Swissborg account statement dataframe.
		Then computes the daily capital amounts which will be used tocompute the daily yield
		rates.
		
		:param earningDf:
		:param depositDf:
		
		:return example:
		                   DATE  DEP/WITHDR  EARNING CAP  EARNINGS  DAILY YIELD RATE
		IDX
		1   2020-12-21 10:00:00      2000.0      2000.00      0.00          0.000000
		2   2020-12-22 09:00:00         0.0      2000.00      0.80          1.000400
		5   2020-12-23 09:00:00         0.0      2002.43      0.78          1.000390
		6   2020-12-24 10:00:00      4000.0      6003.21      0.00          0.000000
		"""
		# inserting 2 empty columns to the loaded Swissborg earning sheet
		self._insertEmptyFloatColumns(earningDf,
		                              0,
		                              [SB_ACCOUNT_SHEET_HEADER_EARNING_CAPITAL, DATAFRAME_HEADER_DEPOSIT_WITHDRAW])
		
		# drop no longer unusefull type and  currency columns from the SB earning data frame
		earningDf = earningDf.drop(columns=SB_ACCOUNT_SHEET_NO_LONGER_USED_COLUMNS_LIST)
		
		# removing unusefull owner column from the deposit data frame
		depositDf = depositDf.drop(columns=DEPOSIT_SHEET_HEADER_OWNER)
		
		# appending depositDf to earningDf, then sorting on datetime index and converting NaN to zero
		mergedDf = earningDf.append(depositDf).sort_index().fillna(0)

		# replace DATE index with integer index
		mergedDf = self._replaceDateIndexByIntIndex(mergedDf, MERGED_SHEET_HEADER_DATE, DATAFRAME_HEADER_INDEX)

		# reposition the DATE column to the left of the data frame
		cols = mergedDf.columns.to_list()
		cols = cols[-1:] + cols[:-1]
		mergedDf = mergedDf[cols]

		# adding daily yield rate and yearly yield rate column
		self._insertEmptyFloatColumns(mergedDf,
		                              None,
		                              [MERGED_SHEET_HEADER_DAILY_YIELD_RATE, MERGED_SHEET_HEADER_YEARLY_YIELD_RATE])

		# computing the earning capital value as well as the daily yield rate
		currentCapital = 0
		previousEarning = 0
		
		for i in range(1, len(mergedDf) + 1):
			if i > 1:
				previousEarning = mergedDf.loc[i - 1, MERGED_SHEET_HEADER_EARNING]
			currentCapital = currentCapital + \
			                 mergedDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW] + \
			                 previousEarning
			mergedDf.loc[i, MERGED_SHEET_HEADER_EARNING_CAPITAL] = currentCapital
			earning = mergedDf.loc[i, MERGED_SHEET_HEADER_EARNING]
			
			if currentCapital > 0 and earning > 0:
				dailyYieldRate = 1 + earning / currentCapital
				mergedDf.loc[i, MERGED_SHEET_HEADER_DAILY_YIELD_RATE] = dailyYieldRate
				mergedDf.loc[i, MERGED_SHEET_HEADER_YEARLY_YIELD_RATE] = np.power(dailyYieldRate, 365)

		mergedDf = mergedDf.rename(columns={MERGED_SHEET_HEADER_DATE: MERGED_SHEET_HEADER_DATE_NEW_NAME, MERGED_SHEET_HEADER_EARNING: MERGED_SHEET_HEADER_EARNING_NEW_NAME})
		#print(self.getDataframeStrWithFormattedColumns(mergedDf, {MERGED_SHEET_HEADER_DAILY_YIELD_RATE: '.8f', MERGED_SHEET_HEADER_YEARLY_YIELD_RATE: '.8f'}))

		return mergedDf
	
	def getDepositsAndDailyYieldRatesDataframes(self,
												yieldCrypto):
		"""
		Loads the Swissborg account statement sheet and the Deposit/Withdrawal sheet
		in order to compute the daily yield rates which will be used to compute the daily
		earnings to be distributed in proportion of the deposits/withdrawals amounts
		invested by the different deposit owners.
		
		:param yieldCrypto:
		
		:return: loaded deposit data frame and computed yield rates data frame

		Loaded deposit data frame example
		
		                    OWNER DEP/WITHDR
		Local time
		2020-12-21 10:00:00   JPS   2,000.00
		2020-12-25 10:00:00  Papa   4,000.00
		2020-12-27 10:00:01  Papa    -500.00

		Computed yield rates data frame example
		
		           DAILY YIELD RATE
		DATE
		2020-12-22       1.00040000
		2020-12-23       1.00040484
		2020-12-24       1.00040967
		"""
		sbEarningsDf = self._loadSBEarningSheet(yieldCrypto)
		depositDf = self._loadDepositSheet()
		
		mergedEarningDeposit = self._mergeEarningAndDeposit(sbEarningsDf, depositDf)

		# extract only MERGED_SHEET_HEADER_DATE_NEW_NAME, MERGED_SHEET_HEADER_DAILY_YIELD_RATE and
		# MERGED_SHEET_HEADER_YEARLY_YIELD_RATE columns
		colDateIdx = mergedEarningDeposit.columns.get_loc(MERGED_SHEET_HEADER_DATE_NEW_NAME)
		colDailyYieldRateIdx = mergedEarningDeposit.columns.get_loc(MERGED_SHEET_HEADER_DAILY_YIELD_RATE)
		colYearlyYieldRateIdx = mergedEarningDeposit.columns.get_loc(MERGED_SHEET_HEADER_YEARLY_YIELD_RATE)
		dailyYieldRatesDataframe = mergedEarningDeposit[mergedEarningDeposit.columns[[colDateIdx, colDailyYieldRateIdx, colYearlyYieldRateIdx]]]

		# keep only non 0 MERGED_SHEET_HEADER_DAILY_YIELD_RATE rows
		isYieldRateNonZero = dailyYieldRatesDataframe[MERGED_SHEET_HEADER_DAILY_YIELD_RATE] != 0
		dailyYieldRatesDataframe = dailyYieldRatesDataframe[isYieldRateNonZero]

		# remove time component from date index
		dailyYieldRatesDataframe[MERGED_SHEET_HEADER_DATE_NEW_NAME] = pd.to_datetime(dailyYieldRatesDataframe[MERGED_SHEET_HEADER_DATE_NEW_NAME].dt.date)
		
		# set MERGED_SHEET_HEADER_DATE_NEW_NAME column as index
		dailyYieldRatesDataframe = dailyYieldRatesDataframe.set_index(MERGED_SHEET_HEADER_DATE_NEW_NAME)

		return depositDf, dailyYieldRatesDataframe

	def getSBEarningSheetTotalDf(self, yieldCrypto):
		"""
		Returns the Swissborg account statement sheet dataframe earnings for the passed
		yield crypto (USDC, CHSV, ...) with the addition of a total	earning row to it.

		:param yieldCrypto: USDC, CHSV, ... used to filter loaded Swissborg account
							statement sheet rows
							
		:return example:
		
				                         Type Currency  Net amount
		Local time
		2020-12-22 09:00:00  Earnings     USDC        2.40
		2020-12-23 09:00:00  Earnings     USDC        2.30
		2020-12-24 09:00:00  Earnings     USDC        2.25
		TOTAL                                         6.95
		"""
		sbEarningsDf = self._loadSBEarningSheet(yieldCrypto)

		# adding total row
		sbEarningsDf.loc[DATAFRAME_HEADER_TOTAL] = sbEarningsDf.sum(numeric_only=True)

		return sbEarningsDf.fillna('')