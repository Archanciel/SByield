import numpy as np

from ownerdeposityieldcomputer import *

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
		levelThreeColNameSpace = ''

		for fiatColName in fiatColLst:
			# removing the no longer used fiat col name
			yieldOwnerWithTotalsDetailDfColNameLst.remove(fiatColName)

			addedFiatDepWithdrColumns += 1
			yieldOwnerWithTotalsDetailDfColNameLst = yieldOwnerWithTotalsDetailDfColNameLst[:addedFiatDepWithdrColumns] + \
				[fiatColName] + yieldOwnerWithTotalsDetailDfColNameLst[addedFiatDepWithdrColumns:]
			print(yieldOwnerWithTotalsDetailDfColNameLst)

			# updating the yieldOwnerWithTotalsDetailDf with the new column list
			yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf[yieldOwnerWithTotalsDetailDfColNameLst]

			# renaming the fiat column
			dateFromRateUniqueColName = levelThreeColNameSpace + 'DF RATE'
			yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.rename(columns={fiatColName: dateFromRateUniqueColName})

			fiat = fiatColName.replace(' AMT', '')

			# inserting DEP/WITHDR fiat current rate column

			addedFiatDepWithdrColumns += 1
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			depositWithdrawalCryptoValueLst = yieldOwnerWithTotalsDetailDf[DATAFRAME_HEADER_DEPOSIT_WITHDRAW].tolist()
			capitallCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, depositWithdrawalCryptoValueLst))
			currentRateUniqueColName = levelThreeColNameSpace + 'CUR RATE'
			yieldOwnerWithTotalsDetailDf.insert(loc=addedFiatDepWithdrColumns, column=currentRateUniqueColName, value=capitallCurrentFiatValueLst)

			# inserting DEP/WITHDR fiat capital gain column

			addedFiatDepWithdrColumns += 1
			depositWithdrawalDateFromFiatValueLst = yieldOwnerWithTotalsDetailDf[dateFromRateUniqueColName].tolist()
			depositWithdrawalFiatCapitalGainLst = np.subtract(capitallCurrentFiatValueLst,
														  	  depositWithdrawalDateFromFiatValueLst)
			capitalGainUniqueColName = levelThreeColNameSpace + 'CAPITAL GAIN'
			yieldOwnerWithTotalsDetailDf.insert(loc=addedFiatDepWithdrColumns, column=capitalGainUniqueColName, value=depositWithdrawalFiatCapitalGainLst)

			# inserting DEP/WITHDR fiat capital gain % column

			addedFiatDepWithdrColumns += 1
			depositWithdrawalCurrentFiatVector = np.array(capitallCurrentFiatValueLst)
			depositWithdrawalDateFromFiatVector = np.array(depositWithdrawalDateFromFiatValueLst)
			depositWithdrawalFiatCapitalGainPercentVector = ((depositWithdrawalCurrentFiatVector -
															 depositWithdrawalDateFromFiatVector) / depositWithdrawalDateFromFiatVector) * 100

			capitalGainUniqueColName = levelThreeColNameSpace + 'CAPITAL GAIN %'
			yieldOwnerWithTotalsDetailDf.insert(loc=addedFiatDepWithdrColumns, column=capitalGainUniqueColName, value=depositWithdrawalFiatCapitalGainPercentVector.tolist())

			levelThreeColNameSpace += ' '
			yieldOwnerWithTotalsDetailDfColNameLst = yieldOwnerWithTotalsDetailDf.columns.tolist()

		# insert CAPITAL CUR RATE columns

		addedFiatDepWithdrColumns += 2
		levelThreeColNameSpace = ''

		for fiat in fiatLst:
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			capitalCryptoValueLst = yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_CAPITAL].tolist()
			capitallCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, capitalCryptoValueLst))
			fiatUniqueColName = levelThreeColNameSpace + fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=addedFiatDepWithdrColumns, column=fiatUniqueColName, value=capitallCurrentFiatValueLst)
			addedFiatDepWithdrColumns += 1

		i += 4
		# insert YIELD AMT CUR RATE columns
		for fiat in fiatLst:
			i += 1
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			yieldAmountValueLst = yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT].tolist()
			capitallCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, yieldAmountValueLst))
			yieldOwnerWithTotalsDetailDf.insert(loc=i, column='    ' + fiat, value=capitallCurrentFiatValueLst)

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