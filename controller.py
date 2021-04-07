import os

from configmanager import ConfigManager
from processor import Processor
from sbyieldratecomputer import *
from ownerdeposityieldcomputer import *

class Controller:
	def __init__(self):
		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
		else:
			configPath = 'c:\\temp\\sbyield.ini'

		self.configMgr = ConfigManager(configPath)
		
	def computeYield(self, yieldCrypto):
		if yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_USDC:
			depositSheetFileName = 'depositUsdc_20210407.csv'
		elif yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_CHSB:
			depositSheetFileName = 'depositChsb_20210407.csv'
		elif yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_ETH:
			depositSheetFileName = 'depositEth_20210407.csv'
		else:
			raise ValueError('Yield crypto {} not supported. Program closed.'.format(yieldCrypto))
		
		sbAccountSheetFileName = 'Swissborg_account_statement_20201218_20210407.xlsx'
		
		if os.name == 'posix':
			dataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/data/'
			sbAccountSheetFilePathName = dataPath + sbAccountSheetFileName
			depositSheetFilePathName = dataPath + depositSheetFileName
		else:
			dataPath = 'D:\\Development\\Python\\SByield\\data\\'
			sbAccountSheetFilePathName = dataPath + sbAccountSheetFileName
			depositSheetFilePathName = dataPath + depositSheetFileName
		
		sbYieldRateComputer = SBYieldRateComputer(self.configMgr,
		                                          sbAccountSheetFilePathName,
		                                          depositSheetFilePathName)
		self.ownerDepositYieldComputer = OwnerDepositYieldComputer(self.configMgr, sbYieldRateComputer)
		
		processor = Processor(self.configMgr,
		                      sbYieldRateComputer,
		                      self.ownerDepositYieldComputer)
		
		return processor.computeYield(yieldCrypto)

if __name__ == '__main__':
	formatDic = {SB_ACCOUNT_SHEET_CURRENCY_USDC: '.2f',
				 SB_ACCOUNT_SHEET_CURRENCY_CHSB: '.8f',
	             SB_ACCOUNT_SHEET_CURRENCY_ETH: '.8f'}
	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
	ctr = Controller()
	sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf = \
		ctr.computeYield(yieldCrypto)
	
	sbYieldRatesWithTotalDfStr = ctr.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
		sbYieldRatesWithTotalDf,
		{
			SB_ACCOUNT_SHEET_HEADER_EARNING: '.8f'})
	print('\nComputed Swissborg yield rates using deposit/withdrawal owner amounts ...')
	print(sbYieldRatesWithTotalDfStr)

	yieldOwnerWithTotalsSummaryDfStr = ctr.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
		yieldOwnerWithTotalsSummaryDf,
		{
			DATAFRAME_HEADER_DEPOSIT_WITHDRAW: formatDic[yieldCrypto],
			DEPOSIT_YIELD_HEADER_CAPITAL: formatDic[yieldCrypto],
			DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})

	print('\nOwner summary deposit/withdrawal yield totals ...')
	print(yieldOwnerWithTotalsSummaryDfStr)

	yieldOwnerWithTotalsDetailDfStr = ctr.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
		yieldOwnerWithTotalsDetailDf,
		{
			DATAFRAME_HEADER_DEPOSIT_WITHDRAW: formatDic[yieldCrypto],
			DEPOSIT_YIELD_HEADER_CAPITAL: formatDic[yieldCrypto],
			DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})

	print('\nOwner detailed deposit/withdrawal yield totals and percents...')
	print(yieldOwnerWithTotalsDetailDfStr)

	
	



