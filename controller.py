import os

from processor import Processor
from ownerdeposityieldcomputer import *
from pricerequester import PriceRequester
from cryptofiatratecomputer import CryptoFiatRateComputer

class Controller:
	def computeYield(self,
					 sbAccountSheetFileName,
					 yieldCrypto,
					 language):
		if yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_USDC:
			depositSheetFileName = 'depositUsdc_20210407.csv'
		elif yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_CHSB:
			depositSheetFileName = 'depositChsb_20210407.csv'
		elif yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_ETH:
			depositSheetFileName = 'depositEth_20210407.csv'
		else:
			raise ValueError('Yield crypto {} not supported. Program closed.'.format(yieldCrypto))

		cryptoFiatCsvFileName = 'cryptoFiatExchange.csv'

		if os.name == 'posix':
			dataPath = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/data/'
			sbAccountSheetFilePathName = dataPath + sbAccountSheetFileName
			depositSheetFilePathName = dataPath + depositSheetFileName
		else:
			dataPath = 'D:\\Development\\Python\\SByield\\data\\'
			sbAccountSheetFilePathName = dataPath + sbAccountSheetFileName
			depositSheetFilePathName = dataPath + depositSheetFileName

		sbYieldRateComputer = SBYieldRateComputer(sbAccountSheetFilePathName=sbAccountSheetFilePathName,
												  sbAccountSheetFiat='CHF',
		                                          depositSheetFilePathName=depositSheetFilePathName)
		self.ownerDepositYieldComputer = OwnerDepositYieldComputer(sbYieldRateComputer)

		cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName
		processor = Processor(sbYieldRateComputer,
		                      self.ownerDepositYieldComputer,
							  CryptoFiatRateComputer(PriceRequester(),
													 cryptoFiatCsvFilePathName),
							  language)

		#processor.activateHelpStarsAddition()

		return processor.addFiatConversionInfo()

	def printHelpLines(self, language):
		print()
		print(' * ' + PROC_TOTAL_INCLUDE_YIELD_HELP[language])
		print('** ' + PROC_CURRENT_RATE_HELP[language])

if __name__ == '__main__':
	formatDic = {SB_ACCOUNT_SHEET_CURRENCY_USDC: '.2f',
				 SB_ACCOUNT_SHEET_CURRENCY_CHSB: '.8f',
	             SB_ACCOUNT_SHEET_CURRENCY_ETH: '.8f'}

	sbAccountSheetFileName = 'Swissborg_account_statement_20201101_20210504.xlsx'

#	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
#	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_ETH
	language = FR
	ctr = Controller()

	sbYieldRatesWithTotalDf, \
	yieldOwnerWithTotalsSummaryDf, \
	yieldOwnerWithTotalsDetailDf, \
	yieldOwnerWithTotalsDetaiAndFiatlDfStr, \
	depositCrypto = ctr.computeYield(sbAccountSheetFileName,
									 yieldCrypto,
									 language)
	
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

	print('\nOwner fiat detailed deposit/withdrawal yield totals ...')
	print(yieldOwnerWithTotalsDetaiAndFiatlDfStr)
	ctr.printHelpLines(language)

	
	



