import os

from processor import Processor
from ownerdeposityieldcomputer import *
from pricerequester import PriceRequester

class Controller:
	def computeYield(self, sbAccountSheetFileName, yieldCrypto, fiat):
		if yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_USDC:
			depositSheetFileName = 'depositUsdc_20210407.csv'
		elif yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_CHSB:
			depositSheetFileName = 'depositChsb_20210407.csv'
		elif yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_ETH:
			depositSheetFileName = 'depositEth_20210407.csv'
		else:
			raise ValueError('Yield crypto {} not supported. Program closed.'.format(yieldCrypto))

		if os.name == 'posix':
			dataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/data/'
			sbAccountSheetFilePathName = dataPath + sbAccountSheetFileName
			depositSheetFilePathName = dataPath + depositSheetFileName
		else:
			dataPath = 'D:\\Development\\Python\\SByield\\data\\'
			sbAccountSheetFilePathName = dataPath + sbAccountSheetFileName
			depositSheetFilePathName = dataPath + depositSheetFileName
		
		sbYieldRateComputer = SBYieldRateComputer(sbAccountSheetFilePathName,
		                                          depositSheetFilePathName)
		self.ownerDepositYieldComputer = OwnerDepositYieldComputer(sbYieldRateComputer)
		
		processor = Processor(sbYieldRateComputer,
		                      self.ownerDepositYieldComputer,
							  PriceRequester())
		
		return processor.computeYield(fiat)

if __name__ == '__main__':
	formatDic = {SB_ACCOUNT_SHEET_CURRENCY_USDC: '.2f',
				 SB_ACCOUNT_SHEET_CURRENCY_CHSB: '.8f',
	             SB_ACCOUNT_SHEET_CURRENCY_ETH: '.8f'}

	sbAccountSheetFileName = 'Swissborg_account_statement_20201218_20210408.xlsx'

	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
#	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
#	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_ETH
	fiat = 'CHF'
	ctr = Controller()
	sbYieldRatesWithTotalDf, \
	yieldOwnerWithTotalsSummaryDf, \
	yieldOwnerWithTotalsDetailDf, \
	fiatYieldOwnerWithTotalsDetailDf = ctr.computeYield(sbAccountSheetFileName,
														yieldCrypto,
														fiat)
	
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

	fiatYieldOwnerWithTotalsDetailDfStr = ctr.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
		fiatYieldOwnerWithTotalsDetailDf,
		{
			DATAFRAME_HEADER_DEPOSIT_WITHDRAW: formatDic[yieldCrypto],
			DEPOSIT_YIELD_HEADER_CAPITAL: formatDic[yieldCrypto],
			DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})

	print('\nOwner fiat detailed deposit/withdrawal yield totals ...')
	print(fiatYieldOwnerWithTotalsDetailDfStr)

	
	



