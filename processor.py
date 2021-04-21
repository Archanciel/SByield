from ownerdeposityieldcomputer import *

PROC_CAPITAL = 'CAPITAL'


class Processor:
	def __init__(self,
				 sbYieldRateComputer,
				 ownerDepositYieldComputer,
				 cryptoFiatRateComputer,
				 language=GB):
		self.sbYieldRateComputer = sbYieldRateComputer
		self.ownerDepositYieldComputer = ownerDepositYieldComputer
		self.cryptoFiatRateComputer = cryptoFiatRateComputer
		self.language = language
	
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
			dateFromRateUniqueColName = levelTwoColNameSpace + PROC_DATE_FROM_RATE[self.language]
			yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.rename(columns={fiatColName: dateFromRateUniqueColName})

			fiat = fiatColName.replace(' AMT', '')

			# inserting DEP/WITHDR fiat current rate column

			dfNewColPosition += 1
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			depositWithdrawalCryptoValueLst = yieldOwnerWithTotalsDetailDf[DATAFRAME_HEADER_DEPOSIT_WITHDRAW].tolist()
			capitalCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, depositWithdrawalCryptoValueLst))
			currentRateUniqueColName = levelTwoColNameSpace + PROC_CURRENT_RATE[self.language]
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=currentRateUniqueColName, value=capitalCurrentFiatValueLst)

			# inserting DEP/WITHDR fiat capital gain column

			dfNewColPosition += 1
			depositWithdrawalDateFromFiatValueLst = yieldOwnerWithTotalsDetailDf[dateFromRateUniqueColName].tolist()
			depositWithdrawalFiatCapitalGainLst = np.subtract(capitalCurrentFiatValueLst,
															  depositWithdrawalDateFromFiatValueLst)
			capitalGainUniqueColName = levelTwoColNameSpace + PROC_CAPITAL_GAIN[self.language]
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=capitalGainUniqueColName, value=depositWithdrawalFiatCapitalGainLst)

			# inserting DEP/WITHDR fiat capital gain % column

			dfNewColPosition += 1
			depositWithdrawalCurrentFiatVector = np.array(capitalCurrentFiatValueLst)
			depositWithdrawalDateFromFiatVector = np.array(depositWithdrawalDateFromFiatValueLst)
			capitalGainVector = depositWithdrawalCurrentFiatVector - depositWithdrawalDateFromFiatVector

			# handling withdrawal cap gain %
			depositWithdrawalDateFromFiatVectorSign = np.sign(depositWithdrawalCurrentFiatVector)
			depositWithdrawalDateFromFiatVectorPositiveValues = depositWithdrawalDateFromFiatVector * depositWithdrawalDateFromFiatVectorSign
			depositWithdrawalFiatCapitalGainPercentVector = ((capitalGainVector) / depositWithdrawalDateFromFiatVectorPositiveValues) * 100

			capitalGainUniqueColName = levelTwoColNameSpace + PROC_CAPITAL_GAIN_PERCENT[self.language]
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=capitalGainUniqueColName, value=depositWithdrawalFiatCapitalGainPercentVector.tolist())

			levelTwoColNameSpace += ' '
			yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailDf.columns.tolist()

		# insert CAPITAL CUR RATE columns

		dfNewColPosition += 2

		for fiat in fiatLst:
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			capitalCryptoValueLst = yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_CAPITAL].tolist()
			capitalCurrentFiatValueLst = list(map(lambda x: x * cryptoFiatCurrentRate, capitalCryptoValueLst))
			fiatUniqueColName = fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=fiatUniqueColName, value=capitalCurrentFiatValueLst)
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

		formatDic = {DEPOSIT_YIELD_HEADER_CAPITAL: depositCrypto,
					 DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER: PROC_YIELD_DAYS[self.language],
					 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: ' ' + depositCrypto,
					 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: PROC_YIELD_AMT_PERCENT[self.language],
					 DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: PROC_YEAR_YIELD_PERCENT[self.language]
					 }

		yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.rename(
			columns=formatDic)

		fiatNb = len(fiatColLst)
		depWithdrFiatColNb = 4 * fiatNb
		capitalFiatColNb = fiatNb

		# completing totals for fiat conversion columns

		fiatColNameDic = self._buildFiatColNameDic([PROC_DATE_FROM_RATE[self.language], PROC_CAPITAL_GAIN[self.language]], fiatLst + [depositCrypto], len(fiatLst))
		fiatColNameSumDic = dict.fromkeys(fiatColNameDic, 'sum')

		yieldOwnerGroupTotalDf = yieldOwnerWithTotalsDetailDf.groupby([DEPOSIT_SHEET_HEADER_OWNER[GB]]).agg(fiatColNameSumDic).reset_index()
		yieldOwnerGroupTotalDfIndex = 1

		yieldOwnerWithTotalsDetailDf.reset_index(inplace=True)

		for index, row in yieldOwnerWithTotalsDetailDf.iterrows():
			if row.loc[DEPOSIT_SHEET_HEADER_OWNER[GB]] == DATAFRAME_HEADER_TOTAL:
				# totals must be completed only on total rows
				for colName in fiatColNameDic.keys():
					total = yieldOwnerGroupTotalDf.iloc[yieldOwnerGroupTotalDfIndex][colName]
					yieldOwnerWithTotalsDetailDf.loc[index, colName] = total

				# computing capital gain percent total
				colNameSpace = ''

				for _ in fiatLst:
					capGainPecentTotal = yieldOwnerWithTotalsDetailDf.loc[index, colNameSpace + PROC_CAPITAL_GAIN[self.language]] / \
										 yieldOwnerWithTotalsDetailDf.loc[index, colNameSpace + PROC_DATE_FROM_RATE[self.language]] * 100
					yieldOwnerWithTotalsDetailDf.loc[index, colNameSpace + PROC_CAPITAL_GAIN_PERCENT[self.language]] = capGainPecentTotal
					colNameSpace += ' '

				yieldOwnerGroupTotalDfIndex += 1

		yieldOwnerWithTotalsDetailDf.set_index(DEPOSIT_SHEET_HEADER_OWNER[GB], inplace=True)

		# defining multi level index rows

		multiIndexLevelZeroLst = [' '] * depWithdrFiatColNb + [PROC_DEPWITHDR[self.language]] + [' '] * 11

		levelOneDepWithdrFiatArray = []

		for fiat in fiatLst:
			levelOneDepWithdrFiatArray += [' '] * 3 + ['  ' + fiat]

		multiIndexLevelOneLst = [depositCrypto] + levelOneDepWithdrFiatArray + [' '] * capitalFiatColNb + [PROC_CAPITAL] + [' '] + ['DATE'] + [' '] * (fiatNb + 1) + [
			PROC_YIELD[self.language]] + [' ', ' ', ' ', ' ']
		multiIndexLevelTwoLst = yieldOwnerWithTotalsDetailDf.columns.tolist()
		multiIndexLevelTwoLst[0] = PROC_TOTAL_INCLUDE_YIELD[self.language]

		arrays = [
			np.array(multiIndexLevelZeroLst),
			np.array(multiIndexLevelOneLst),
			np.array(multiIndexLevelTwoLst)
		]

		tuples = list(zip(*arrays))
		index = pd.MultiIndex.from_tuples(tuples)
		yieldOwnerWithTotalsDetailDf.columns = index

		# simple way of printing all float multi index columns with 2
		# decimal places
		pd.options.display.float_format = '{:,.2f}'.format

		yieldOwnerWithTotalsDetaiAndFiatlDfStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf, {})

		# resetting the pandas global float format so that the unit tests
		# are not impacted by the previous global float format setting
		pd.reset_option('display.float_format')

		return sbYieldRatesWithTotalDf, \
			   yieldOwnerWithTotalsSummaryDf, \
			   yieldOwnerWithTotalsDetaiAndFiatlDfStr, \
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

	def _buildFiatColNameDic(self, colNameLst, fiatColNameLst, fiatNb):
		"""

		@param colNameLst:
		@param fiatNb:
		@return:
		"""
		colNameSpace = ''

		# prevents                  CAPITAL
		#          CHSB       CHF       USD
		# columns to be summed
		fiatColNameSpace = ' '

		colNameDic = {}

		for i in range(0, fiatNb):
			for colName in colNameLst:
				colNameDic[colNameSpace + colName] = None

			colNameSpace += ' '

		# prevents                  CAPITAL
		#          CHSB       CHF       USD
		# columns to be summed
		for fiatColName in fiatColNameLst:
			colNameDic[fiatColNameSpace + fiatColName] = None

		return colNameDic
