import numpy as np
import pandas as pd

# Swissborg account statement sheet parameters
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

# two new columns to add to the Swissborg account statement sheet
SB_ACCOUNT_SHEET_HEADER_EARNING_CAPITAL = 'EARNING CAP'
SB_ACCOUNT_SHEET_HEADER_DEPOSIT_WITHDRAW = 'DEP/WITHDR'

SB_ACCOUNT_SHEET_TYPE_EARNING = 'Earnings'  # used to filter rows
SB_ACCOUNT_SHEET_CURRENCY = 'USDC'          # used to filter rows. USDC or CHSB

# Deposit/Withdrawal sheet parameters
DEPOSIT_SHEET_HEADER_DATE = SB_ACCOUNT_SHEET_HEADER_DATE
DEPOSIT_SHEET_HEADER_DEPOSIT_WITHDRAW = SB_ACCOUNT_SHEET_HEADER_DEPOSIT_WITHDRAW

# Swissborg account statement merged with deposit/withdrawal sheet parameters
MERGED_SHEET_HEADER_DATE = SB_ACCOUNT_SHEET_HEADER_DATE
MERGED_SHEET_HEADER_INDEX = 'IDX'
MERGED_SHEET_HEADER_EARNING_CAPITAL = SB_ACCOUNT_SHEET_HEADER_EARNING_CAPITAL
MERGED_SHEET_HEADER_DEPOSIT_WITHDRAW = DEPOSIT_SHEET_HEADER_DEPOSIT_WITHDRAW
MERGED_SHEET_HEADER_EARNING = SB_ACCOUNT_SHEET_HEADER_EARNING
MERGED_SHEET_HEADER_DATE_NEW_NAME = 'DATE'
MERGED_SHEET_HEADER_EARNING_NEW_NAME = 'EARNINGS'
MERGED_SHEET_HEADER_YIELD_RATE = 'DAILY YIELD RATE'

# columns which can be removed from the merged data frame
MERGED_SHEET_UNUSED_COLUMNS_LIST = [SB_ACCOUNT_SHEET_HEADER_TYPE,
                                    SB_ACCOUNT_SHEET_HEADER_CURRENCY]

class SByieldRateComputer:
	"""
	This class loads the Swissborg account statement xlsl sheet and the Deposit/Withdrawal
	csv files.
	
	It merges the two files, creating a Pandas data frame containing computed data used
	later to distribute the earnings according to the deposits/withdrawals.
	"""
	def __init__(self, configMgr):
		"""
		Currently, the configMgr is not used. Constants are used in place.
		
		:param configMgr:
		"""
		self.configMgr = configMgr
		
	def loadSBEarningSheet(self, sbAccountSheetFilePathName):
		"""
		Creates a Pandas data frame from the Swissborg account statement sheet, removing
		unused columns. It then selects only the earning type rows. Finally, it adds
		two new columns for later usage.
		
		:param sbAccountSheetFilePathName:
		:return:
		"""
		xls = pd.ExcelFile(sbAccountSheetFilePathName,
						   engine='openpyxl') # this parm is required on Android !
		
		sbEarningsDf = xls.parse(SB_ACCOUNT_SHEET_NAME,
		                         skiprows=SB_ACCOUNT_SHEET_SKIP_ROWS,
		                         parse_dates=[SB_ACCOUNT_SHEET_HEADER_DATE])
		sbEarningsDf = sbEarningsDf.set_index([SB_ACCOUNT_SHEET_HEADER_DATE])

		# drop unused columns
		sbEarningsDf = sbEarningsDf.drop(columns=SB_ACCOUNT_SHEET_UNUSED_COLUMNS_LIST)
		
		# filter useful rows
		isTypeEarning = sbEarningsDf[SB_ACCOUNT_SHEET_HEADER_TYPE] == SB_ACCOUNT_SHEET_TYPE_EARNING
		isTargetCurrency = sbEarningsDf[SB_ACCOUNT_SHEET_HEADER_CURRENCY] == SB_ACCOUNT_SHEET_CURRENCY
		sbEarningsDf = sbEarningsDf[isTypeEarning & isTargetCurrency]
		
		# inserting two empty columns
		sbEarningsDf.insert(loc=0, column=SB_ACCOUNT_SHEET_HEADER_EARNING_CAPITAL, value=[0.0 for i in range(sbEarningsDf.shape[0])])
		sbEarningsDf.insert(loc=0, column=SB_ACCOUNT_SHEET_HEADER_DEPOSIT_WITHDRAW, value=[0.0 for i in range(sbEarningsDf.shape[0])])
		
		return sbEarningsDf
	
	def loadDepositSheet(self, sbDepositSheetFilePathName):
		"""
		Creates a Pandas data frame from the Deposit/Withdrawal sheet.
		
		:param sbDepositSheetFilePathName:
		:return:
		"""
		depositsDf = pd.read_csv(sbDepositSheetFilePathName, parse_dates=[DEPOSIT_SHEET_HEADER_DATE], dtype={DEPOSIT_SHEET_HEADER_DEPOSIT_WITHDRAW: np.float64})
		depositsDf = depositsDf.set_index([DEPOSIT_SHEET_HEADER_DATE])
		
		return depositsDf

	def mergeEarningAndDeposit(self, earningDf, depositDf):
		"""
		Merges Deposit/Withdrawal dataframe into the Swissborg account statement dataframe.
		Then computes the earning capital values as well as the daily yield rates.
		
		:param earningDf:
		:param depositDf:
		:return:
		"""
		# appending depositDf to earningDf, then sorting and converting NaN to zero
		mergedDf = earningDf.append(depositDf).sort_index().fillna(0)

		# drop unused columns
		mergedDf = mergedDf.drop(columns=MERGED_SHEET_UNUSED_COLUMNS_LIST)

		# replace DATE index with integer index
		
			# save old DATE index Column
		mergedDf[MERGED_SHEET_HEADER_DATE] = mergedDf.index
		
			# reposition the DATE column to the left of the data frame
		cols = mergedDf.columns.to_list()
		cols = cols[-1:] + cols[:-1]
		mergedDf = mergedDf[cols]
		
		# set integer index
		mergedDf[MERGED_SHEET_HEADER_INDEX] = range(1, len(mergedDf) + 1)
		mergedDf = mergedDf.set_index(MERGED_SHEET_HEADER_INDEX)

		# adding yield column
		mergedDf.insert(loc=mergedDf.shape[1], column=MERGED_SHEET_HEADER_YIELD_RATE, value=[0.0 for i in range(mergedDf.shape[0])])

		# computing the earning capital value as well as the daily yield rate
		for i in range(2, len(mergedDf) + 1):
			mergedDf.loc[i, MERGED_SHEET_HEADER_EARNING_CAPITAL] = mergedDf.loc[i - 1, MERGED_SHEET_HEADER_EARNING_CAPITAL] + \
			                                                       mergedDf.loc[i - 1, MERGED_SHEET_HEADER_DEPOSIT_WITHDRAW] + \
			                                                       mergedDf.loc[i - 1, MERGED_SHEET_HEADER_EARNING]
			earningCapital = mergedDf.loc[i, MERGED_SHEET_HEADER_EARNING_CAPITAL]
			earning = mergedDf.loc[i, MERGED_SHEET_HEADER_EARNING]
			
			if earningCapital > 0 and earning > 0:
				mergedDf.loc[i, MERGED_SHEET_HEADER_YIELD_RATE] = 1 + \
				                                                  earning / \
				                                                  earningCapital
				
		mergedDf = mergedDf.rename(columns={MERGED_SHEET_HEADER_DATE: MERGED_SHEET_HEADER_DATE_NEW_NAME, MERGED_SHEET_HEADER_EARNING: MERGED_SHEET_HEADER_EARNING_NEW_NAME})
		
		return mergedDf
	
	def getDataframeStrWithFormattedColumns(self, dataFrame, colFormatDic):
		"""
		Returns a string representation of the passed dataFrame enabling to define a
		specific format for any column since Pandas by default format all float
		columns with a same format.
		
		This method is useful if we want to set a specific precision to float64
		columns.
		
		:param dataFrame:
		:param colFormatDic: Example: {MERGED_SHEET_HEADER_YIELD_RATE: '.8f'}
		:return:
		"""
		formatDic = {}
		
		for colHeader, formatStr in colFormatDic.items():
			pandasFormatter = '{:,' + formatStr + '}'
			formatDic[colHeader] = pandasFormatter.format
			
		return dataFrame.to_string(formatters=formatDic)
	
	def getDailyYieldRatesDataframe(self, sbAccountSheetFilePathName, depositSheetFilePathName):
		sbEarningsDf = self.loadSBEarningSheet(sbAccountSheetFilePathName)
		depositDf = self.loadDepositSheet(depositSheetFilePathName)
		
		mergedEarningDeposit = self.mergeEarningAndDeposit(sbEarningsDf, depositDf)

		# extract only MERGED_SHEET_HEADER_DATE_NEW_NAME and MERGED_SHEET_HEADER_YIELD_RATE columns
		yieldRatesDataframe = mergedEarningDeposit[mergedEarningDeposit.columns[[0, 4]]]
		
		# set MERGED_SHEET_HEADER_DATE_NEW_NAME column as index
		yieldRatesDataframe = yieldRatesDataframe.set_index(MERGED_SHEET_HEADER_DATE_NEW_NAME)
		
		# keep only non 0 MERGED_SHEET_HEADER_YIELD_RATE rows
		isYieldRateNonZero = yieldRatesDataframe[MERGED_SHEET_HEADER_YIELD_RATE] != 0
		yieldRatesDataframe = yieldRatesDataframe[isYieldRateNonZero]

		return yieldRatesDataframe
