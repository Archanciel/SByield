import os

from ownerdeposityieldcomputer import *

DEPWITHDR = 'DEP/WITHDR'
DEPWITHDR_SHORT = 'DEP/WDR'
DATE_FROM_RATE = 'DF RATE'
CAPITAL_GAIN = 'CAP GAIN'
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
		"""

		@return:
		"""
		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDf, \
		depositCrypto = self.ownerDepositYieldComputer.computeDepositsYields()

		yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailDf.columns.tolist()

		# if deposits/withdrawals defined in the deposit CSV file are
		# completed by fiat values, then the yieldOwnerWithTotalsDetailDf
		# is completed at its right side by fiat amount columns ...
		fiatColLst = [col for col in yieldOwnerWithTotalsDetailColNameLst if 'AMT' in col and 'YIELD' not in col]
		fiatLst = list(map(lambda x: x.replace(' AMT', ''), fiatColLst))

		# obtaining the current crypto/fiat rates as a crypto/fiat pair dic
		cryptoFiatRateDic = self._getCurrentCryptoFiatRateValues(depositCrypto, fiatLst)

		dfNewColPosition = 0
		levelTwoColNameSpace = ''

		for fiatColName in fiatColLst:
			# removing the no longer used fiat col name
			yieldOwnerWithTotalsDetailColNameLst.remove(fiatColName)

			dfNewColPosition += 1
			yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailColNameLst[:dfNewColPosition] + \
				[fiatColName] + yieldOwnerWithTotalsDetailColNameLst[dfNewColPosition:]

			# updating the yieldOwnerWithTotalsDetailDf with the new column list
			yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf[yieldOwnerWithTotalsDetailColNameLst]

			# renaming the fiat column
			dateFromRateUniqueColName = levelTwoColNameSpace + DATE_FROM_RATE
			yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.rename(columns={fiatColName: dateFromRateUniqueColName})

			fiat = fiatColName.replace(' AMT', '')

			# inserting DEP/WITHDR fiat current rate column

			dfNewColPosition += 1
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			depositWithdrawalCryptoValueLst = yieldOwnerWithTotalsDetailDf[DATAFRAME_HEADER_DEPOSIT_WITHDRAW].tolist()
			capitallCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, depositWithdrawalCryptoValueLst))
			currentRateUniqueColName = levelTwoColNameSpace + 'CUR RATE'
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=currentRateUniqueColName, value=capitallCurrentFiatValueLst)

			# inserting DEP/WITHDR fiat capital gain column

			dfNewColPosition += 1
			depositWithdrawalDateFromFiatValueLst = yieldOwnerWithTotalsDetailDf[dateFromRateUniqueColName].tolist()
			depositWithdrawalFiatCapitalGainLst = np.subtract(capitallCurrentFiatValueLst,
															  depositWithdrawalDateFromFiatValueLst)
			capitalGainUniqueColName = levelTwoColNameSpace + CAPITAL_GAIN
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=capitalGainUniqueColName, value=depositWithdrawalFiatCapitalGainLst)

			# inserting DEP/WITHDR fiat capital gain % column

			dfNewColPosition += 1
			depositWithdrawalCurrentFiatVector = np.array(capitallCurrentFiatValueLst)
			depositWithdrawalDateFromFiatVector = np.array(depositWithdrawalDateFromFiatValueLst)
			capitalGainVector = depositWithdrawalCurrentFiatVector - depositWithdrawalDateFromFiatVector

			# handling withdrawal cap gain %
			depositWithdrawalDateFromFiatVectorSign = np.sign(depositWithdrawalCurrentFiatVector)
			depositWithdrawalDateFromFiatVectorPositiveValues = depositWithdrawalDateFromFiatVector * depositWithdrawalDateFromFiatVectorSign
			depositWithdrawalFiatCapitalGainPercentVector = ((capitalGainVector) / depositWithdrawalDateFromFiatVectorPositiveValues) * 100

			capitalGainUniqueColName = levelTwoColNameSpace + 'CAP GAIN %'
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=capitalGainUniqueColName, value=depositWithdrawalFiatCapitalGainPercentVector.tolist())

			levelTwoColNameSpace += ' '
			yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailDf.columns.tolist()

		# insert CAPITAL CUR RATE columns

		dfNewColPosition += 2

		for fiat in fiatLst:
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			capitalCryptoValueLst = yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_CAPITAL].tolist()
			capitallCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, capitalCryptoValueLst))
			fiatUniqueColName = fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=fiatUniqueColName, value=capitallCurrentFiatValueLst)
			dfNewColPosition += 1

		# insert YIELD AMT CUR RATE columns

		dfNewColPosition += 4
		levelTwoColNameSpace = ' '

		for fiat in fiatLst:
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			yieldAmountValueLst = yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT].tolist()
			yieldAmountllCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, yieldAmountValueLst))
			fiatUniqueColName = levelTwoColNameSpace + fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=fiatUniqueColName, value=yieldAmountllCurrentFiatValueLst)
			dfNewColPosition += 1

		# renaming the yieldOwnerWithTotalsDetailDf columns

		if os.name == 'posix':
			# since the Android tablet available print space is smaller than
			# the space available on Windows, the some col names are reduced
			formatDic = {DEPOSIT_YIELD_HEADER_CAPITAL: depositCrypto,
						 DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER: YIELD_DAYS,
						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: ' ' + depositCrypto,
						 DATAFRAME_HEADER_DEPOSIT_WITHDRAW: DEPWITHDR_SHORT,
						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: YIELD_AMT_PERCENT,
						 DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: YEAR_YIELD_PERCENT_SHORT
			}
		else:
			formatDic = {DEPOSIT_YIELD_HEADER_CAPITAL: depositCrypto,
						 DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER: YIELD_DAYS,
						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: ' ' + depositCrypto,
						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: YIELD_AMT_PERCENT,
						 DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: YEAR_YIELD_PERCENT
						 }

		yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.rename(
			columns=formatDic)

		fiatNb = len(fiatColLst)
		depWithdrFiatColNb = 4 * fiatNb
		capitalFiatColNb = fiatNb

		# completing totals for fiat conversion columns

		fiatColNameDic = self._buildFiatColNameDic([DATE_FROM_RATE, CAPITAL_GAIN] + fiatLst + [depositCrypto], len(fiatLst))
		fiatColNameDic = dict.fromkeys(fiatColNameDic, 'sum')

		ownerGroupTotalDf = yieldOwnerWithTotalsDetailDf.groupby([DEPOSIT_SHEET_HEADER_OWNER]).agg(fiatColNameDic).reset_index()

		ownerGroupTotalDfIndex = 1

		yieldOwnerWithTotalsDetailDf.reset_index(inplace=True)

		for index, row in yieldOwnerWithTotalsDetailDf.iterrows():
			if row.loc[DEPOSIT_SHEET_HEADER_OWNER] == DATAFRAME_HEADER_TOTAL:
				for colName in fiatColNameDic.keys():
					total = ownerGroupTotalDf.iloc[ownerGroupTotalDfIndex][colName]
					yieldOwnerWithTotalsDetailDf.loc[index, colName] = total
				ownerGroupTotalDfIndex += 1

		yieldOwnerWithTotalsDetailDf.set_index(DEPOSIT_SHEET_HEADER_OWNER, inplace=True)

		# defining multi level index rows

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

		# simpler way of printing all float columns multi index with 2
		# decimal places
		pd.options.display.float_format = '{:,.2f}'.format

		yieldOwnerWithTotalsDetailDfActualStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf, {})

		# resetting the pandas global float format so that the other unit test
		# are not impacted by the previous global float format setting
		pd.reset_option('display.float_format')

		return sbYieldRatesWithTotalDf, \
			   yieldOwnerWithTotalsSummaryDf, \
			   yieldOwnerWithTotalsDetailDf, \
			   yieldOwnerWithTotalsDetailDfActualStr, \
			   depositCrypto

	def _getCurrentCryptoFiatRateValues(self,
										crypto,
										fiatlLst):
		"""
		Return the current crypto/fiat rates for the fiat contained in
		the passed fiatLst as a crypto/fiat pair dic.

		@param crypto:
		@param fiatlLst:

		@return: crypto/fiat pair dic
		"""
		cryptoFiatRateDic = {}

		for fiat in fiatlLst:
			cryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatCurrentRate(crypto, fiat)
			cryptoFiatRateDic[fiat] = cryptoFiatRate

		return cryptoFiatRateDic

	def _buildFiatColNameDic(self, colNameLst, fiatNb):
		"""

		@param colNameLst:
		@param fiatNb:
		@return:
		"""
		colNameSpace = ''
		colNameDic = {}

		for i in range(0, fiatNb):
			for colName in colNameLst:
				colNameDic[colNameSpace + colName] = None
			colNameSpace += ' '

		return colNameDic
