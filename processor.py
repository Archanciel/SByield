import os

from ownerdeposityieldcomputer import *

DEPWITHDR = 'DEP/WITHDR'
DEPWITHDR_SHORT = 'DEP/WDR'
CAPITAL = 'CAPITAL'
YIELD = 'YIELD'
YIELD_DAYS = 'Y DAYS'
YIELD_AMT = 'Y AMT'
YIELD_AMT_PERCENT = 'Y %'
YEAR_YIELD_PERCENT = 'YR Y %'
YEAR_YIELD_PERCENT_SHORT = 'Y Y %'

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

		multiIndexLevelTwoLst = yieldOwnerWithTotalsDetailDf.columns.tolist()
		fiatColLst = [col for col in multiIndexLevelTwoLst if 'AMT' in col and 'YIELD' not in col]
		fiatLst = list(map(lambda x: x.replace(' AMT', ''), fiatColLst))
		cryptoFiatRateDic = self.getCurrentCryptoFiatRateValues(depositCrypto, fiatColLst)

		dfNewColPosition = 0
		levelThreeColNameSpace = ''

		for fiatColName in fiatColLst:
			# removing the no longer used fiat col name
			multiIndexLevelTwoLst.remove(fiatColName)

			dfNewColPosition += 1
			multiIndexLevelTwoLst = multiIndexLevelTwoLst[:dfNewColPosition] + \
				[fiatColName] + multiIndexLevelTwoLst[dfNewColPosition:]

			# updating the yieldOwnerWithTotalsDetailDf with the new column list
			yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf[multiIndexLevelTwoLst]

			# renaming the fiat column
			dateFromRateUniqueColName = levelThreeColNameSpace + 'DF RATE'
			yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.rename(columns={fiatColName: dateFromRateUniqueColName})

			fiat = fiatColName.replace(' AMT', '')

			# inserting DEP/WITHDR fiat current rate column

			dfNewColPosition += 1
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			depositWithdrawalCryptoValueLst = yieldOwnerWithTotalsDetailDf[DATAFRAME_HEADER_DEPOSIT_WITHDRAW].tolist()
			capitallCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, depositWithdrawalCryptoValueLst))
			currentRateUniqueColName = levelThreeColNameSpace + 'CUR RATE'
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=currentRateUniqueColName, value=capitallCurrentFiatValueLst)

			# inserting DEP/WITHDR fiat capital gain column

			dfNewColPosition += 1
			depositWithdrawalDateFromFiatValueLst = yieldOwnerWithTotalsDetailDf[dateFromRateUniqueColName].tolist()
			depositWithdrawalFiatCapitalGainLst = np.subtract(capitallCurrentFiatValueLst,
														  	  depositWithdrawalDateFromFiatValueLst)
			capitalGainUniqueColName = levelThreeColNameSpace + 'CAP GAIN'
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=capitalGainUniqueColName, value=depositWithdrawalFiatCapitalGainLst)

			# inserting DEP/WITHDR fiat capital gain % column

			dfNewColPosition += 1
			depositWithdrawalCurrentFiatVector = np.array(capitallCurrentFiatValueLst)
			depositWithdrawalDateFromFiatVector = np.array(depositWithdrawalDateFromFiatValueLst)
			depositWithdrawalFiatCapitalGainPercentVector = ((depositWithdrawalCurrentFiatVector -
															 depositWithdrawalDateFromFiatVector) / depositWithdrawalDateFromFiatVector) * 100

			capitalGainUniqueColName = levelThreeColNameSpace + 'CAP GAIN %'
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=capitalGainUniqueColName, value=depositWithdrawalFiatCapitalGainPercentVector.tolist())

			levelThreeColNameSpace += ' '
			multiIndexLevelTwoLst = yieldOwnerWithTotalsDetailDf.columns.tolist()

		# insert CAPITAL CUR RATE columns

		dfNewColPosition += 2
		levelThreeColNameSpace = ''

		for fiat in fiatLst:
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			capitalCryptoValueLst = yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_CAPITAL].tolist()
			capitallCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, capitalCryptoValueLst))
			fiatUniqueColName = levelThreeColNameSpace + fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=fiatUniqueColName, value=capitallCurrentFiatValueLst)
			dfNewColPosition += 1

		# insert YIELD AMT CUR RATE columns

		dfNewColPosition += 4
		levelThreeColNameSpace = ' '

		for fiat in fiatLst:
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			yieldAmountValueLst = yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT].tolist()
			yieldAmountllCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, yieldAmountValueLst))
			fiatUniqueColName = levelThreeColNameSpace + fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=fiatUniqueColName, value=yieldAmountllCurrentFiatValueLst)
			dfNewColPosition += 1

		if os.name == 'posix':
			formatDic = {DEPOSIT_YIELD_HEADER_CAPITAL: ' ' + depositCrypto,
						 DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER: YIELD_DAYS,
#						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: YIELD_AMT,
						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '  ' + depositCrypto,
						 DATAFRAME_HEADER_DEPOSIT_WITHDRAW: DEPWITHDR_SHORT,
						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: YIELD_AMT_PERCENT,
						 DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: YEAR_YIELD_PERCENT_SHORT
			}
		else:
			formatDic = {DEPOSIT_YIELD_HEADER_CAPITAL: ' ' + depositCrypto,
						 DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER: YIELD_DAYS,
						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '  ' + depositCrypto,
						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: YIELD_AMT_PERCENT,
						 DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: YEAR_YIELD_PERCENT
						 }

		yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.rename(
			columns=formatDic)
		fiatNb = len(fiatColLst)
		depWithdrFiatColNb = 4 * fiatNb
		capitalFiatColNb = fiatNb
		yieldAmountColNb = fiatNb + 3
		multiIndexLevelZeroLst = [' '] * depWithdrFiatColNb + [DEPWITHDR] + [' '] * 11

		levelOneDepWithdrFiatArray = []

		for fiat in fiatLst:
			levelOneDepWithdrFiatArray += [' '] * 3 + ['  ' + fiat]

		multiIndexLevelOneLst = [depositCrypto] + levelOneDepWithdrFiatArray + [' '] * capitalFiatColNb + [CAPITAL] + [' '] + ['DATE'] + [' '] * (fiatNb + 1) + [YIELD] + [' ', ' ', ' ', ' ']
		multiIndexLevelTwoLst = yieldOwnerWithTotalsDetailDf.columns.tolist()

		arrays = [
			np.array(multiIndexLevelZeroLst),
			np.array(multiIndexLevelOneLst),
			np.array(multiIndexLevelTwoLst)
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