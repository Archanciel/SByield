from ownerdeposityieldcomputer import *
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
			resultDataYieldCryptoFiat = self.priceRequester.getCurrentPrice(yieldCrypto, fiat, exchangeYieldCrypto)
			yieldCryptoIntermediateCryptoRate = resultDataYieldCryptoFiat.getValue(ResultData.RESULT_KEY_PRICE)
			intermediateCryptoFiatRate = 1
		elif depositCrypto == SB_ACCOUNT_SHEET_CURRENCY_CHSB:
			crypto = 'BTC'
			exchangeYieldCrypto = 'HitBtc'
			resultDataYieldCrypto = self.priceRequester.getCurrentPrice(yieldCrypto, crypto, exchangeYieldCrypto)
			exchangeCryptoFiat = 'Kraken'
			resultDataCryptoFiat = self.priceRequester.getCurrentPrice(crypto, fiat, exchangeCryptoFiat)
			yieldCryptoIntermediateCryptoRate = resultDataYieldCrypto.getValue(ResultData.RESULT_KEY_PRICE)
			intermediateCryptoFiatRate = resultDataCryptoFiat.getValue(ResultData.RESULT_KEY_PRICE)
		elif depositCrypto == SB_ACCOUNT_SHEET_CURRENCY_ETH:
			exchangeYieldCrypto = 'Kraken'
			resultDataYieldCryptoFiat = self.priceRequester.getCurrentPrice(yieldCrypto, fiat, exchangeYieldCrypto)
			yieldCryptoIntermediateCryptoRate = resultDataYieldCryptoFiat.getValue(ResultData.RESULT_KEY_PRICE)
			intermediateCryptoFiatRate = 1

		yieldCryptoFiatRate = yieldCryptoIntermediateCryptoRate * \
							  intermediateCryptoFiatRate

		return sbYieldRatesWithTotalDf, \
			   yieldOwnerWithTotalsSummaryDf, \
			   yieldOwnerWithTotalsDetailDf
