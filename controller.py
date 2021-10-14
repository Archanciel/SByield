import os

from processor import Processor
from ownerdeposityieldcomputer import *
from pricerequester import PriceRequester
from cryptofiatratecomputer import CryptoFiatRateComputer

class Controller:
	def computeYield(self,
	                 sbAccountSheetFileName,
	                 yieldCrypto,
	                 sbAccountSheetFiat,
	                 language):
		if yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_USDC:
			depositSheetFileName = 'depositUsdc.csv'
		elif yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_CHSB:
			depositSheetFileName = 'depositChsb.csv'
		elif yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_ETH:
			depositSheetFileName = 'depositEth.csv'
		elif yieldCrypto == SB_ACCOUNT_SHEET_CURRENCY_BNB:
			depositSheetFileName = 'depositBnb.csv'
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
		                                          sbAccountSheetFiat=sbAccountSheetFiat,
		                                          depositSheetFilePathName=depositSheetFilePathName)
		self.ownerDepositYieldComputer = OwnerDepositYieldComputer(sbYieldRateComputer)

		cryptoFiatCsvFilePathName = dataPath + cryptoFiatCsvFileName
		processor = Processor(sbYieldRateComputer,
		                      self.ownerDepositYieldComputer,
		                      CryptoFiatRateComputer(PriceRequester(),
													 cryptoFiatCsvFilePathName),
		                      sbAccountSheetFiat,
		                      language)

		processor.activateHelpNumbers()

		return processor.addFiatConversionInfo()

	def printHelpLines(self, language):
		print()
		print('(1) ' + PROC_HELP_TXT_1[language])
		print('(2) ' + PROC_HELP_TXT_2[language])
		print('(3) ' + PROC_HELP_TXT_3[language])
		print('(4) ' + PROC_HELP_TXT_4[language])

if __name__ == '__main__':
	formatDic = {SB_ACCOUNT_SHEET_CURRENCY_USDC: '.2f',
				 SB_ACCOUNT_SHEET_CURRENCY_CHSB: '.8f',
	             SB_ACCOUNT_SHEET_CURRENCY_ETH: '.8f',
	             SB_ACCOUNT_SHEET_CURRENCY_BNB: '.8f'}

#	sbAccountSheetFiat = 'USD'  # fiat of the Swissborg_account_statement Excel file
	sbAccountSheetFiat = 'CHF'  # fiat of the Swissborg_account_statement Excel file
	sbAccountSheetFileName = 'Swissborg_account_statement_20201101_20211004_{}.xlsx'.format(sbAccountSheetFiat)

#	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC
#	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_CHSB
	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_ETH
#	yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_BNB
	language = FR
	ctr = Controller()

	sbYieldRatesWithTotalDf, \
	yieldOwnerWithTotalsSummaryDf, \
	yieldOwnerWithTotalsDetailDf, \
	yieldOwnerWithTotalsDetaiAndFiatlDfStr, \
	depositCrypto = ctr.computeYield(sbAccountSheetFileName,
	                                 yieldCrypto,
	                                 sbAccountSheetFiat,
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

	
	



