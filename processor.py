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
		self.addHelpStars = False
	
	def addFiatConversionInfo(self):
		"""

		@return:
		"""
		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDf, \
		depositCrypto = self.ownerDepositYieldComputer.computeDepositsYields()

		yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailDf.columns.tolist()

		# moving date from/to col names at list start position
		yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailColNameLst[2:4] + \
											   yieldOwnerWithTotalsDetailColNameLst[:2] + \
											   yieldOwnerWithTotalsDetailColNameLst[4:]

		# if deposits/withdrawals defined in the deposit CSV file are
		# completed by fiat values, then the yieldOwnerWithTotalsDetailDf
		# is completed at its right side by fiat amount columns ...
		fiatColLst = [col for col in yieldOwnerWithTotalsDetailColNameLst if 'AMT' in col and 'YIELD' not in col]
		fiatLst = list(map(lambda x: x.replace(' AMT', ''), fiatColLst))

		# obtaining the current crypto/fiat rates as a crypto/fiat pair dic
		cryptoFiatRateDic = self._getCurrentCryptoFiatRateValues(depositCrypto, fiatLst)

		dfNewColPosition = 2
		levelTwoUniqueColNameModifier = ''

		helpStar = ''
		helpStars = ''

		if self.addHelpStars:
			helpStar = '*'
			helpStars = '**'

		capitalGainUniqueColNameLst = []
		capitalGainPercentUniqueColNameLst = []

		for fiatColName in fiatColLst:
			# removing the no longer used fiat col name
			yieldOwnerWithTotalsDetailColNameLst.remove(fiatColName)

			dfNewColPosition += 1
			yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailColNameLst[:dfNewColPosition] + \
				[fiatColName] + yieldOwnerWithTotalsDetailColNameLst[dfNewColPosition:]

			# updating the yieldOwnerWithTotalsDetailDf with the new column list
			yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf[yieldOwnerWithTotalsDetailColNameLst]

			# renaming the fiat column

			fiat = fiatColName.replace(' AMT', '')
			dateFromRateUniqueColName = fiat
			yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.rename(columns={fiatColName: dateFromRateUniqueColName})

			# inserting DEP/WITHDR fiat current rate column

			dfNewColPosition += 1
			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			depositWithdrawalCryptoValueLst = yieldOwnerWithTotalsDetailDf[DATAFRAME_HEADER_DEPOSIT_WITHDRAW].tolist()
			depWithdrCurrentFiatValueVector = list(map(lambda x: x * cryptoFiatCurrentRate, depositWithdrawalCryptoValueLst))
			levelTwoUniqueColNameModifier += '_'
			currentRateUniqueColName = levelTwoUniqueColNameModifier + fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=currentRateUniqueColName, value=depWithdrCurrentFiatValueVector)

			# inserting DEP/WITHDR fiat capital gain column with capital gain values

			dfNewColPosition += 1
			depositWithdrawalDateFromFiatValueLst = yieldOwnerWithTotalsDetailDf[dateFromRateUniqueColName].tolist()
			depositWithdrawalFiatCapitalGainValuesVector = np.subtract(depWithdrCurrentFiatValueVector,
															  depositWithdrawalDateFromFiatValueLst)
			levelTwoUniqueColNameModifier += '_'
			capitalGainUniqueColName = levelTwoUniqueColNameModifier + fiat
			capitalGainUniqueColNameLst.append(capitalGainUniqueColName)
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=capitalGainUniqueColName, value=depositWithdrawalFiatCapitalGainValuesVector)

			# inserting DEP/WITHDR fiat capital gain % column with capital gain % values

			dfNewColPosition += 1
			depositWithdrawalCurrentFiatVector = np.array(depWithdrCurrentFiatValueVector)
			depositWithdrawalDateFromFiatVector = np.array(depositWithdrawalDateFromFiatValueLst)
			capitalGainVector = depositWithdrawalCurrentFiatVector - depositWithdrawalDateFromFiatVector

			# computing withdrawal cap gain % values
			depositWithdrawalDateFromFiatSignVector = np.sign(depositWithdrawalCurrentFiatVector)
			depositWithdrawalDateFromFiatPositiveValuesVector = depositWithdrawalDateFromFiatVector * depositWithdrawalDateFromFiatSignVector
			depositWithdrawalFiatCapitalGainPercentVector = ((capitalGainVector) / depositWithdrawalDateFromFiatPositiveValuesVector) * 100

			capitalPercentGainUniqueColName = levelTwoUniqueColNameModifier + PROC_CAPITAL_GAIN_PERCENT[self.language]
			capitalGainPercentUniqueColNameLst.append(capitalPercentGainUniqueColName)
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=capitalPercentGainUniqueColName, value=depositWithdrawalFiatCapitalGainPercentVector.tolist())

			levelTwoUniqueColNameModifier += '_'
			yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailDf.columns.tolist()

		# insert YIELD AMT FIAT CUR RATE and DEP/WITHDR + YIELD AMT FIAT CUR RATE columns

		dfNewColPosition += 2

		dfNewColPosition = 5

		for fiat in fiatLst:
			# insert YIELD AMT FIAT CUR RATE column

			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			yieldAmountValueVector = np.array(yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT].tolist())
			yieldAmountCurrentFiatValueVector = yieldAmountValueVector * cryptoFiatCurrentRate
			fiatUniqueColName = PROC_YIELD_SHORT[self.language] + fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=fiatUniqueColName, value=yieldAmountCurrentFiatValueVector)
			dfNewColPosition += 1

			# insert DEP/WITHDR + YIELD AMT FIAT CUR RATE column
			depWithdrCryptoValueVector = np.array(yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_CAPITAL].tolist())
			depWithdrCurrentFiatValueVector = depWithdrCryptoValueVector * cryptoFiatCurrentRate
			depWithdrPlusYieldCurrentFiatValueVector = depWithdrCurrentFiatValueVector + yieldAmountCurrentFiatValueVector
			fiatUniqueColName = PROC_TOTAL + fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=fiatUniqueColName, value=depWithdrPlusYieldCurrentFiatValueVector)
			dfNewColPosition += 1

		# renaming the yieldOwnerWithTotalsDetailDf columns

		formatDic = {DEPOSIT_YIELD_HEADER_CAPITAL: depositCrypto,
					 DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER: PROC_YIELD_DAYS[self.language],
					 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: levelTwoUniqueColNameModifier + depositCrypto,
					 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: PROC_YIELD_AMT_PERCENT[self.language],
					 DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: PROC_YEAR_YIELD_PERCENT[self.language]
					 }

		yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.rename(
			columns=formatDic)

		fiatNb = len(fiatColLst)
		depWithdrFiatColNb = 4 * fiatNb
		capitalFiatColNb = fiatNb

		# completing totals for fiat conversion columns

		fiatColNameDic = self._buildFiatColNameDic(capitalGainUniqueColNameLst, fiatLst, len(fiatLst))
		fiatColNameSumDic = dict.fromkeys(fiatColNameDic, 'sum')

		# removing total rows before groupby.agg application
		nonTotalRow = ~yieldOwnerWithTotalsDetailDf.index.str.contains(DATAFRAME_HEADER_TOTAL)
		yieldOwnerWithoutTotalsDetailDf = yieldOwnerWithTotalsDetailDf[nonTotalRow]

		# now summing specified columns by owners
		yieldOwnerGroupTotalDf = yieldOwnerWithoutTotalsDetailDf.groupby([DEPOSIT_SHEET_HEADER_OWNER[GB]]).agg(fiatColNameSumDic).reset_index()

		# setting the previously computed total values to the owners total row
		yieldOwnerGroupTotalDfIndex = 0

		yieldOwnerWithTotalsDetailDf.reset_index(inplace=True)

		for index, row in yieldOwnerWithTotalsDetailDf.iterrows():
			if row.loc[DEPOSIT_SHEET_HEADER_OWNER[GB]] == DATAFRAME_HEADER_TOTAL:
				# totals must be completed only on total rows
				for colName in fiatColNameDic.keys():
					total = yieldOwnerGroupTotalDf.iloc[yieldOwnerGroupTotalDfIndex][colName]
					yieldOwnerWithTotalsDetailDf.loc[index, colName] = total

				# computing capital gain percent total
				uniqueColNameModifier = ''

				for fiat, capitalGainUniqueColName, capitalGainPercentUniqueColName in zip(fiatLst, capitalGainUniqueColNameLst, capitalGainPercentUniqueColNameLst):
					capGainPercentTotal = yieldOwnerWithTotalsDetailDf.loc[index,capitalGainUniqueColName] / \
										  yieldOwnerWithTotalsDetailDf.loc[index, fiat] * 100
					yieldOwnerWithTotalsDetailDf.loc[index, capitalGainPercentUniqueColName] = capGainPercentTotal
					uniqueColNameModifier += '_'

				yieldOwnerGroupTotalDfIndex += 1

		yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.rename(columns=
																		   {PROC_DEPWITHDR[GB]: depositCrypto,
																			DEPOSIT_SHEET_HEADER_OWNER[GB]: DEPOSIT_SHEET_HEADER_OWNER[self.language],
																			DEPOSIT_YIELD_HEADER_DATE_FROM[GB]: DEPOSIT_YIELD_HEADER_DATE_FROM[self.language],
																			DEPOSIT_YIELD_HEADER_DATE_TO[GB]: DEPOSIT_YIELD_HEADER_DATE_TO[self.language]})
		yieldOwnerWithTotalsDetailDf.set_index(DEPOSIT_SHEET_HEADER_OWNER[self.language], inplace=True)

		# defining multi level language dependent index rows

		if len(fiatLst) > 1:
			multiIndexLevelZeroLst = [' '] * (depWithdrFiatColNb - 5) + [PROC_DEP[self.language], PROC_WITHDR[self.language]] + [' '] * 15
		else:
			multiIndexLevelZeroLst = [' '] * (depWithdrFiatColNb - 1) + [PROC_DEP[self.language],
																   PROC_WITHDR[self.language]] + [' '] * 11
		levelOneDepWithdrFiatArray = [PROC_DATE_FROM_RATE[self.language], PROC_CURRENT_RATE[self.language]]

		if len(fiatLst) > 1:
			levelOneUniqueColNameModifier = ' '
		else:
			levelOneUniqueColNameModifier = ''

		for fiat in fiatLst:
			levelOneDepWithdrFiatArray += [levelOneUniqueColNameModifier + PROC_CURRENT_RATE[self.language]]
			levelOneUniqueColNameModifier += ' '
			levelOneDepWithdrFiatArray += [levelOneUniqueColNameModifier + PROC_CURRENT_RATE[self.language]]
			levelOneUniqueColNameModifier += ' '

		levelOneDepWithdrFiatArray += [PROC_CAPITAL_GAIN[self.language]]
		multiIndexLevelOneLst = [' ', ' ', PROC_AMOUNT[self.language]] + levelOneDepWithdrFiatArray + [' '] * capitalFiatColNb + [' ', ' ', ' '] + [' '] * (fiatNb) + [
			PROC_YIELD[self.language]] + [' ', ' ', ' ']
		multiIndexLevelTwoLst = yieldOwnerWithTotalsDetailDf.columns.tolist()
		multiIndexLevelTwoLst = [x.replace('_', '') for x in multiIndexLevelTwoLst]

		# variables for debugging only ...
		l1 = len(multiIndexLevelZeroLst)
		l2 = len(multiIndexLevelOneLst)
		l3 = len(multiIndexLevelTwoLst)

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

	def activateHelpStarsAddition(self):
		'''
		Calling this method before calling addfiatConversionInfo() will add
		help stars to the subject to help columns.

		@return:
		'''
		self.addHelpStars = True

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

	def _buildFiatColNameDic(self, capitalGainUniqueColNameLst, fiatColNameLst, fiatNb):
		"""

		@param capitalGainUniqueColNameLst:
		@param fiatNb:
		@return:
		"""
		colNameDic = {}

		for colName in capitalGainUniqueColNameLst:
			colNameDic[colName] = None

		# prevents                  CAPITAL
		#          CHSB       CHF       USD
		# columns to be summed
		for fiatColName in fiatColNameLst:
			colNameDic[fiatColName] = None

		return colNameDic
