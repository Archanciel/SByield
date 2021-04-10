from ownerdeposityieldcomputer import *
from datetimeutil import DateTimeUtil
from pricerequester import PriceRequester
from resultdata import ResultData

class Processor:
	def __init__(self,
	             sbYieldRateComputer,
	             ownerDepositYieldComputer,
				 priceRequester):
		self.sbYieldRateComputer = sbYieldRateComputer
		self.ownerDepositYieldComputer = ownerDepositYieldComputer
		self.priceRequester = priceRequester
	
	def computeYield(self, fiat):
		yieldCryptoIntermediateCryptoRate = None
		intermediateCryptoFiatRate = None

		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDf, \
		depositCrypto = self.ownerDepositYieldComputer.computeDepositsYields()

		if depositCrypto == SB_ACCOUNT_SHEET_CURRENCY_USDC:
			exchangeYieldCrypto = 'CCCAGG'
			resultDataYieldCryptoFiat = self.priceRequester.getCurrentPrice(depositCrypto, fiat, exchangeYieldCrypto)
			yieldCryptoIntermediateCryptoRate = resultDataYieldCryptoFiat.getValue(ResultData.RESULT_KEY_PRICE)
			intermediateCryptoFiatRate = 1
		elif depositCrypto == SB_ACCOUNT_SHEET_CURRENCY_CHSB:
			crypto = 'BTC'
			exchangeYieldCrypto = 'HitBtc'
			resultDataYieldCrypto = self.priceRequester.getCurrentPrice(depositCrypto, crypto, exchangeYieldCrypto)
			exchangeCryptoFiat = 'Kraken'
			resultDataCryptoFiat = self.priceRequester.getCurrentPrice(crypto, fiat, exchangeCryptoFiat)
			yieldCryptoIntermediateCryptoRate = resultDataYieldCrypto.getValue(ResultData.RESULT_KEY_PRICE)
			intermediateCryptoFiatRate = resultDataCryptoFiat.getValue(ResultData.RESULT_KEY_PRICE)
		elif depositCrypto == SB_ACCOUNT_SHEET_CURRENCY_ETH:
			exchangeYieldCrypto = 'Kraken'
			resultDataYieldCryptoFiat = self.priceRequester.getCurrentPrice(depositCrypto, fiat, exchangeYieldCrypto)
			yieldCryptoIntermediateCryptoRate = resultDataYieldCryptoFiat.getValue(ResultData.RESULT_KEY_PRICE)
			intermediateCryptoFiatRate = 1

		currentYieldCryptoFiatRate = yieldCryptoIntermediateCryptoRate * \
									 intermediateCryptoFiatRate

		fiatYieldOwnerWithTotalsDetailDf = self.buildFiatYieldOwnerWithTotalsDetailDf(yieldOwnerWithTotalsDetailDf,
																					  currentYieldCryptoFiatRate,
																					  depositCrypto,
																					  fiat)

		return sbYieldRatesWithTotalDf, \
			   yieldOwnerWithTotalsSummaryDf, \
			   yieldOwnerWithTotalsDetailDf, \
			   fiatYieldOwnerWithTotalsDetailDf

	def buildFiatYieldOwnerWithTotalsDetailDf(self,
											  cryptoYieldOwnerWithTotalsDetailDf,
											  currentYieldCryptoFiatRate,
											  crypto,
											  fiat):
		fiatYieldOwnerWithTotalsDetailDf = \
			cryptoYieldOwnerWithTotalsDetailDf.apply(lambda x: x * currentYieldCryptoFiatRate if x.name == DEPOSIT_YIELD_HEADER_YIELD_AMOUNT else x)

		fiatYieldOwnerWithTotalsDetailDf = fiatYieldOwnerWithTotalsDetailDf.drop(columns=[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT, DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT])
		fiatYieldOwnerWithTotalsDetailDf = fiatYieldOwnerWithTotalsDetailDf.reset_index()

		for index, row in fiatYieldOwnerWithTotalsDetailDf.iterrows():
			depWithdrDate = row[DEPOSIT_YIELD_HEADER_DATE_FROM]
			if not pd.isnull(depWithdrDate):
				depWithdrDate = depWithdrDate.strftime("%Y/%m/%d %H:%M:%S")
				timeStampLocalDepWithdrDate = DateTimeUtil.dateTimeStringToTimeStamp(depWithdrDate,
																					 'Europe/Zurich',
																					 "YYYY/MM/DD HH:mm:ss")
				timeStampUtcDepWithdrDate = DateTimeUtil.dateTimeStringToTimeStamp(depWithdrDate,
																				   'UTC',
																				   "YYYY/MM/DD HH:mm:ss")
				resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																				  fiat,
																				  timeStampLocalDepWithdrDate,
																				  'Europe/Zurich',
																				  timeStampUtcDepWithdrDate,
																				  'CCCAGG')
				if row[DEPOSIT_SHEET_HEADER_OWNER] == 'Béa':
					yieldCryptoIntermediateCryptoRate = 0.9029
				else:
					yieldCryptoIntermediateCryptoRate = resultData.getValue(ResultData.RESULT_KEY_PRICE)
			else:
				yieldCryptoIntermediateCryptoRate = currentYieldCryptoFiatRate

			fiatYieldOwnerWithTotalsDetailDf.loc[index, DATAFRAME_HEADER_DEPOSIT_WITHDRAW] = row[DATAFRAME_HEADER_DEPOSIT_WITHDRAW] * yieldCryptoIntermediateCryptoRate
			fiatYieldOwnerWithTotalsDetailDf.loc[index, DEPOSIT_YIELD_HEADER_CAPITAL] = row[DEPOSIT_YIELD_HEADER_CAPITAL] * yieldCryptoIntermediateCryptoRate

		return fiatYieldOwnerWithTotalsDetailDf
