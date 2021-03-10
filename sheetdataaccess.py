import numpy as np
import pandas as pd

SB_ACCOUNT_SHEET_FIAT = 'USD'
SB_ACCOUNT_SHEET_NAME = 'Transactions'
SB_ACCOUNT_SHEET_SKIP_ROWS = 8
SB_ACCOUNT_SHEET_HEADER_DATE = 'Local time'
SB_ACCOUNT_SHEET_HEADER_EARNING = 'Net amount ({})'.format(SB_ACCOUNT_SHEET_FIAT)
SB_ACCOUNT_SHEET_HEADER_TYPE = 'Type'
SB_ACCOUNT_SHEET_HEADER_CURRENCY = 'Currency'
SB_ACCOUNT_SHEET_UNUSED_COLUMNS_LIST = ['Time in UTC',
                                        'Fee',
                                        'Fee ({})'.format(SB_ACCOUNT_SHEET_FIAT),
                                        'Gross amount',
                                        'Gross amount ({})'.format(SB_ACCOUNT_SHEET_FIAT),
                                        'Note']

SB_ACCOUNT_SHEET_HEADER_CAPITAL = 'CAPITAL'
SB_ACCOUNT_SHEET_HEADER_BUY_SELL = 'BUY/SELL'

SB_ACCOUNT_SHEET_TYPE_EARNING = 'Earnings'
SB_ACCOUNT_SHEET_CURRENCY = 'USDC'

class SheetDataAccess:
	def __init__(self, configMgr):
		self.configMgr = configMgr
		
	def loadSBEarningSheet(self, sbAccountSheetFilePathName):
		xls = pd.ExcelFile(sbAccountSheetFilePathName)
		
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
		sbEarningsDf.insert(loc=0, column=SB_ACCOUNT_SHEET_HEADER_CAPITAL, value=[0.0 for i in range(sbEarningsDf.shape[0])])
		sbEarningsDf.insert(loc=0, column=SB_ACCOUNT_SHEET_HEADER_BUY_SELL, value=[0.0 for i in range(sbEarningsDf.shape[0])])

		
		return sbEarningsDf
