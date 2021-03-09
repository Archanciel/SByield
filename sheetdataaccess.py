import numpy as np
import pandas as pd

SB_ACCOUNT_SHEET_NAME = 'Transactions'
SB_ACCOUNT_SHEET_SKIP_ROWS = 8
SB_ACCOUNT_SHEET_HEADER_DATE = 'Local time'
SB_ACCOUNT_SHEET_HEADER_EARNING = 'Gross amount (USD)'

SB_ACCOUNT_SHEET_HEADER_CAPITAL = 'CAPITAL'
SB_ACCOUNT_SHEET_HEADER_BUY_SELL = 'BUY/SELL'

class SheetDataAccess:
	def __init__(self, configMgr):
		self.configMgr = configMgr
		
	def loadSBEarningSheet(self, sbAccountSheetFilePathName):
		xls = pd.ExcelFile(sbAccountSheetFilePathName)
		
		sbEarningsDf = xls.parse(SB_ACCOUNT_SHEET_NAME, skiprows=SB_ACCOUNT_SHEET_SKIP_ROWS, parse_dates=[SB_ACCOUNT_SHEET_HEADER_DATE])
		sbEarningsDf = sbEarningsDf.set_index([SB_ACCOUNT_SHEET_HEADER_DATE])

		# inserting two empty columns
		sbEarningsDf.insert(loc=0, column=SB_ACCOUNT_SHEET_HEADER_CAPITAL, value=[0.0 for i in range(sbEarningsDf.shape[0])])
		sbEarningsDf.insert(loc=0, column=SB_ACCOUNT_SHEET_HEADER_BUY_SELL, value=[0.0 for i in range(sbEarningsDf.shape[0])])
		
		return sbEarningsDf
