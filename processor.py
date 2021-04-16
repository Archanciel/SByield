from ownerdeposityieldcomputer import *
from datetimeutil import DateTimeUtil
from pricerequester import PriceRequester
from resultdata import ResultData

DEPWITHDR = 'DEP/WITHDR'
CAPITAL = 'CAPITAL'
CHSB_DP_I = 'CHSB'
USD_DP_I = 'USD'
CHF_DP_I = 'CHF'
USD_DP_C = ' USD'
CHF_DP_C = ' CHF'
CHSB_C_C = ' CHSB'
USD_C_C = '  USD'
CHF_C_C = '  CHF'
CHSB_Y = '  CHSB'
USD_Y = '   USD'
CHF_Y = '   CHF'
YIELD = 'YIELD AMT'
INIT = 'DF RATE'
CURR = 'CUR RATE'


class Processor:
	def __init__(self,
	             sbYieldRateComputer,
	             ownerDepositYieldComputer,
				 cryptoFiatRateComputer):
		self.sbYieldRateComputer = sbYieldRateComputer
		self.ownerDepositYieldComputer = ownerDepositYieldComputer
		self.cryptoFiatRateComputer = cryptoFiatRateComputer
	
	def addFiatConversionInfo(self):
		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDf, \
		depositCrypto = self.ownerDepositYieldComputer.computeDepositsYields()

		yieldOwnerWithTotalsDetailDfColNameLst = yieldOwnerWithTotalsDetailDf.columns.tolist()
		fiatColLst = [col for col in yieldOwnerWithTotalsDetailDfColNameLst if 'AMT' in col and 'YIELD' not in col]
		fiatLst = list(map(lambda x: x.replace(' AMT', ''), fiatColLst))
		cryptoFiatRateDic = self.getCurrentCryptoFiatRateValues(depositCrypto, fiatColLst)

		i = 0
		addedFiatDepWithdrColumns = 0
		print(yieldOwnerWithTotalsDetailDfColNameLst)

		for fiatColName in fiatColLst:
			fiatColIndex = yieldOwnerWithTotalsDetailDfColNameLst.index(fiatColName)

			# removing the fiat col name before inserting it in the right position
			# in the yieldOwnerWithTotalsDetailDfColNameLst
			del yieldOwnerWithTotalsDetailDfColNameLst[fiatColIndex]

			i += addedFiatDepWithdrColumns
			yieldOwnerWithTotalsDetailDfColNameLst = yieldOwnerWithTotalsDetailDfColNameLst[:i + 1] + [fiatColName] + yieldOwnerWithTotalsDetailDfColNameLst[i + 1:]
			addedFiatDepWithdrColumns += 1
			print(yieldOwnerWithTotalsDetailDfColNameLst)

			# updating the yieldOwnerWithTotalsDetailDf with the new column
			# list
			yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf[yieldOwnerWithTotalsDetailDfColNameLst]

			# insert DEP/WITHDR CUR RATE columns
			fiat = fiatColName.replace(' AMT', '')

			i += 1
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			depositWithdrawalValueLst = yieldOwnerWithTotalsDetailDf[DATAFRAME_HEADER_DEPOSIT_WITHDRAW].tolist()
			newColValues = list(map(lambda x: x * cryptoFiatCurrentRate, depositWithdrawalValueLst))
			yieldOwnerWithTotalsDetailDf.insert(loc=i, column=' ' + fiat, value=newColValues)

			i += 1
		# insert CAPITAL CUR RATE columns
		for fiat in fiatLst:
			i += 1
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			capitalValueLst = yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_CAPITAL].tolist()
			newColValues = list(map(lambda x: x * cryptoFiatCurrentRate, capitalValueLst))
			yieldOwnerWithTotalsDetailDf.insert(loc=i, column='   ' + fiat, value=newColValues)

		i += 4
		# insert YIELD AMT CUR RATE columns
		for fiat in fiatLst:
			i += 1
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			yieldAmountValueLst = yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT].tolist()
			newColValues = list(map(lambda x: x * cryptoFiatCurrentRate, yieldAmountValueLst))
			yieldOwnerWithTotalsDetailDf.insert(loc=i, column='    ' + fiat, value=newColValues)

		arrays = [
			np.array([' ', ' ', ' ', ' ', DEPWITHDR, ' ', ' ', CAPITAL, ' ', ' ', ' ', ' ', ' ', YIELD, ' ', ' ']),
			np.array([' ', ' ', INIT, ' ', CURR, ' ', ' ', CURR,'  ', ' ', ' ', ' ', ' ', CURR, ' ', ' ']),
			np.array([CHSB_DP_I, USD_DP_I, CHF_DP_I, USD_DP_C, CHF_DP_C, CHSB_C_C, USD_C_C, CHF_C_C, 'DATE FROM', 'DATE TO', 'YIELD DAYS', CHSB_Y, USD_Y, CHF_Y, 'YIELD AMT %', 'Y YIELD AMT %', ' '])
		]
		tuples = list(zip(*arrays))
		index = pd.MultiIndex.from_tuples(tuples)
		yieldOwnerWithTotalsDetailDf.columns = index

		return sbYieldRatesWithTotalDf, \
			   yieldOwnerWithTotalsSummaryDf, \
			   yieldOwnerWithTotalsDetailDf, \
			   depositCrypto

	def getCurrentCryptoFiatRateValues(self,
									   crypto,
									   fiatColLst):
		cryptoFiatRateDic = {}

		for colName in fiatColLst:
			fiat = colName.replace(' AMT', '')
			cryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatCurrentRate(crypto, fiat)
			cryptoFiatRateDic[fiat] = cryptoFiatRate

		return cryptoFiatRateDic