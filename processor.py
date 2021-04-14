from ownerdeposityieldcomputer import *
from datetimeutil import DateTimeUtil
from pricerequester import PriceRequester
from resultdata import ResultData

class Processor:
	def __init__(self,
	             sbYieldRateComputer,
	             ownerDepositYieldComputer,
				 cryptoFiatRateXomputer):
		self.sbYieldRateComputer = sbYieldRateComputer
		self.ownerDepositYieldComputer = ownerDepositYieldComputer
		self.cryptoFiatRateXomputer = cryptoFiatRateXomputer
	
	def addFiatConversionInfo(self):
		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDf, \
		depositCrypto = self.ownerDepositYieldComputer.computeDepositsYields()

		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf,
			{
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
				DEPOSIT_YIELD_HEADER_CAPITAL: '.2f',
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'})

		print(yieldOwnerWithTotalsDetailDfActualStr)

		return sbYieldRatesWithTotalDf, \
			   yieldOwnerWithTotalsSummaryDf, \
			   yieldOwnerWithTotalsDetailDf, \
			   depositCrypto