from ownerdeposityieldcomputer import *


class Processor:
	def __init__(self,
				 sbYieldRateComputer,
				 ownerDepositYieldComputer,
				 cryptoFiatRateComputer,
				 cryptoRateFiat='USD',
				 language=GB):
		self.sbYieldRateComputer = sbYieldRateComputer
		self.ownerDepositYieldComputer = ownerDepositYieldComputer
		self.cryptoFiatRateComputer = cryptoFiatRateComputer
		self.cryptoRateFiat = cryptoRateFiat
		self.language = language

		self.PROC_HELP_1 = ''
		self.PROC_HELP_2 = ''
		self.PROC_HELP_3 = ''
		self.PROC_HELP_4 = ''

	def addFiatConversionInfo(self):
		"""
		This method add fiat information to the deposits/withdrawals and yields dataframe.
		For the method to work correctly, the deposit csv file must contain fiat deposit
		amounts. At least one fiat must be specified in the deposit csv file. More than
		one fiat can be added to the deposit/withdrawal lines.

		@return:
		"""
		sbYieldRatesWithTotalDf, \
		yieldOwnerWithTotalsSummaryDf, \
		yieldOwnerWithTotalsDetailDf, \
		depositCrypto = self.ownerDepositYieldComputer.computeDepositsYields()

		# if deposits/withdrawals defined in the deposit CSV file are
		# completed by fiat values, then the yieldOwnerWithTotalsDetailDf
		# is completed at its right side by fiat amount columns ...
		yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailDf.columns.tolist()
		fiatColLst = [col for col in yieldOwnerWithTotalsDetailColNameLst if 'AMT' in col and 'YIELD' not in col]
		fiatLst = list(map(lambda x: x.replace(' AMT', ''), fiatColLst))

		# obtaining the current crypto/fiat rates as a crypto/fiat pair dic
		cryptoFiatRateDic = self._getCurrentCryptoFiatRateValues(depositCrypto, fiatLst)

		# inserting deposit/withdrawal date crypto/fiat rate column and current date
		# crypto/fiat rate column

		cryptoFiatDateFromRateColName = CRYPTO_FIAT_DATE_FROM_RATE.format(depositCrypto, self.cryptoRateFiat)
		yieldOwnerWithTotalsDetailDf.insert(loc=1, column=cryptoFiatDateFromRateColName, value=0.0)
		cryptoFiatCurrentRateColName = CRYPTO_FIAT_CURRENT_RATE.format(depositCrypto, self.cryptoRateFiat)
		yieldOwnerWithTotalsDetailDf.insert(loc=2, column=cryptoFiatCurrentRateColName, value=0.0)
		cryptoFiatCurrentRate = cryptoFiatRateDic[self.cryptoRateFiat]

		# now computing the values of the crypto/fiat rate columns

		yieldOwnerWithTotalsDetailDf.reset_index(inplace=True)

		for index, row in yieldOwnerWithTotalsDetailDf.iterrows():
			if DATAFRAME_HEADER_TOTAL not in row[DEPOSIT_SHEET_HEADER_OWNER[GB]]:
				# obtaining the first fiat symbol specified in the deposit csv file
				firstFiatColNameInDepositFile = fiatColLst[0]
				fiat = firstFiatColNameInDepositFile.replace(' AMT', '')

				depositDateFrom = str(row.loc[DEPOSIT_YIELD_HEADER_DATE_FROM[GB]])
				depositCryptoAmount = row.loc[DATAFRAME_HEADER_DEPOSIT_WITHDRAW]
				depositFiatAmount = row.loc[firstFiatColNameInDepositFile]
				cryptoDateFromFiatRate = depositFiatAmount / depositCryptoAmount

				if self.cryptoRateFiat in fiatLst:
					cryptoRateFiatIndex = fiatLst.index(self.cryptoRateFiat)
					depositFiatAmount = row.loc[fiatColLst[cryptoRateFiatIndex]]
					cryptoFiatDateFromRate = depositFiatAmount / depositCryptoAmount
				else:
					cryptoFiatRate = \
						self.cryptoFiatRateComputer.computeCryptoFiatRate(self.cryptoRateFiat,
																		  fiat,
																		  depositDateFrom)

					cryptoFiatDateFromRate = cryptoDateFromFiatRate / cryptoFiatRate

				yieldOwnerWithTotalsDetailDf.loc[index, cryptoFiatDateFromRateColName] = cryptoFiatDateFromRate
				yieldOwnerWithTotalsDetailDf.loc[index, cryptoFiatCurrentRateColName] = cryptoFiatCurrentRate

		# resetting index to OWNER column
		yieldOwnerWithTotalsDetailDf.set_index(DEPOSIT_SHEET_HEADER_OWNER[GB], inplace=True)

		yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailDf.columns.tolist()

		# moving date from/to col names at list start position
		yieldOwnerWithTotalsDetailColNameLst = yieldOwnerWithTotalsDetailColNameLst[4:6] + \
											   yieldOwnerWithTotalsDetailColNameLst[:4] + \
											   yieldOwnerWithTotalsDetailColNameLst[6:]

		dfNewColPosition = 4
		levelTwoUniqueColNameModifier = ''
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
			depositWithdrawalCryptoValueVector = np.array(yieldOwnerWithTotalsDetailDf[DATAFRAME_HEADER_DEPOSIT_WITHDRAW].tolist())
			depWithdrCurrentFiatValueVector = depositWithdrawalCryptoValueVector * cryptoFiatCurrentRate
			levelTwoUniqueColNameModifier += '_'
			currentRateUniqueColName = levelTwoUniqueColNameModifier + fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=currentRateUniqueColName, value=depWithdrCurrentFiatValueVector)

			# inserting DEP/WITHDR fiat capital gain column with capital gain values

			dfNewColPosition += 1
			depositWithdrawalDateFromFiatValueLst = yieldOwnerWithTotalsDetailDf[dateFromRateUniqueColName].tolist()
			depositWithdrawalFiatCapitalGainValuesVector = np.subtract(depWithdrCurrentFiatValueVector,
															  depositWithdrawalDateFromFiatValueLst)
			levelTwoUniqueColNameModifier += '_'
			capitalGainUniqueColName = levelTwoUniqueColNameModifier + PROC_CAPITAL_SHORT[self.language] + fiat
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

		dfNewColPosition = 7
		uniqueColNameModifier = ''

		for fiat in fiatLst:
			# insert YIELD AMT FIAT CUR RATE column + values

			cryptoFiatCurrentRate = cryptoFiatRateDic[fiat]
			yieldAmountValueVector = np.array(yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT].tolist())
			yieldAmountCurrentFiatValueVector = yieldAmountValueVector * cryptoFiatCurrentRate
			fiatUniqueColName = PROC_YIELD_SHORT[self.language] + fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=fiatUniqueColName, value=yieldAmountCurrentFiatValueVector)
			dfNewColPosition += 1

			# insert DEP/WITHDR + YIELD AMT FIAT CUR RATE column + values
			depWithdrCryptoValueVector = np.array(yieldOwnerWithTotalsDetailDf[DEPOSIT_YIELD_HEADER_CAPITAL].tolist())
			depWithdrCurrentFiatValueVector = depWithdrCryptoValueVector * cryptoFiatCurrentRate
			depWithdrPlusYieldCurrentFiatValueVector = depWithdrCurrentFiatValueVector + yieldAmountCurrentFiatValueVector
			fiatUniqueColName = PROC_TOTAL_SHORT + fiat
			yieldOwnerWithTotalsDetailDf.insert(loc=dfNewColPosition, column=fiatUniqueColName, value=depWithdrPlusYieldCurrentFiatValueVector)

			# adding daily, monthly and yearly fiat interest amount columns with values

			yieldOwnerWithTotalsDetailDf.reset_index(inplace=True)

			for index, row in yieldOwnerWithTotalsDetailDf.iterrows():
				if row[DEPOSIT_SHEET_HEADER_OWNER[GB]] == DATAFRAME_HEADER_TOTAL:
					depWithdrPlusYieldCurrentFiatValue = yieldOwnerWithTotalsDetailDf.iloc[index - 1][fiatUniqueColName]

					# adding the total deposit value + total generated yield taken
					# from the previous row to the TOTAL row
					yieldOwnerWithTotalsDetailDf.loc[index, fiatUniqueColName] = depWithdrPlusYieldCurrentFiatValue

					# the yearly yield average % was computed in the
					# OwnerDepositYieldComputer._createYieldOwnerWithTotalsDetailDf()
					# method and set to the TOTAL row Y YIELD % cell !
					yieldYearlyAveragePercent = row[DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT]
					yieldYearlyAverageRate = 1 + (yieldYearlyAveragePercent / 100)

					# in order to differentiate by fiat the daily, monthly and
					# yearly fiat interest columns, a low case fiat symbol is
					# added to the added column names. Later, when the level 2
					# multi index column names will be defined, this low case
					# fiat symbol will be simply removed.
					fiatLowCase = fiat.lower()

					# daily fiat interest
					generatedYieldAmountDaily = (np.power(yieldYearlyAverageRate, 1 / 365) - 1) * depWithdrPlusYieldCurrentFiatValue
					yieldOwnerWithTotalsDetailDf.loc[index, PROC_PER_DAY[self.language] + fiatLowCase] = generatedYieldAmountDaily

					# monthly fiat interest
					generatedYieldAmountMonthly = (np.power(yieldYearlyAverageRate, 30 / 365) - 1) * depWithdrPlusYieldCurrentFiatValue
					yieldOwnerWithTotalsDetailDf.loc[index, PROC_PER_MONTH[self.language] + fiatLowCase] = generatedYieldAmountMonthly

					# yearly fiat interest
					generatedYieldAmountYearly = (yieldYearlyAverageRate - 1) * depWithdrPlusYieldCurrentFiatValue
					yieldOwnerWithTotalsDetailDf.loc[index, PROC_PER_YEAR[self.language] + fiatLowCase] = generatedYieldAmountYearly

			# resetting index to OWNER column
			yieldOwnerWithTotalsDetailDf.set_index(DEPOSIT_SHEET_HEADER_OWNER[GB], inplace=True)

			# now, compute dep withdr + yield value G TOTAL with sum of dep withdr + yield value TOTAL's

			# filtering the 'TOTAL' rows only
			filterTotalRowsOnlyArray = yieldOwnerWithTotalsDetailDf.index.isin([DATAFRAME_HEADER_TOTAL])
			dfTotalRowsOnly = yieldOwnerWithTotalsDetailDf.loc[filterTotalRowsOnlyArray]

			# now summing the TOTAL fiatUniqueColName cells
			aggDic = {fiatUniqueColName: 'sum'}
			groupByDfTotalRowsOnly = dfTotalRowsOnly.groupby(level=0).agg(aggDic)

			yieldOwnerWithTotalsDetailDf.loc[DATAFRAME_HEADER_GRAND_TOTAL, fiatUniqueColName] = groupByDfTotalRowsOnly.iloc[0][fiatUniqueColName]

			uniqueColNameModifier += '_'
			dfNewColPosition += 5

		# removing no longer used DEPOSIT_YIELD_HEADER_CAPITAL column
		yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.drop(columns=[DEPOSIT_YIELD_HEADER_CAPITAL])

		# replace crypto/USD zero value rate in TotAL rows by np.nan since total in those
		# columns has no sense
		cryptoRateColNames = [cryptoFiatDateFromRateColName, cryptoFiatCurrentRateColName]
		yieldOwnerWithTotalsDetailDf[cryptoRateColNames] = yieldOwnerWithTotalsDetailDf[cryptoRateColNames].replace({'0': np.nan, 0: np.nan})

		# renaming the yieldOwnerWithTotalsDetailDf columns

		formatDic = {DEPOSIT_YIELD_HEADER_CAPITAL: depositCrypto,
					 DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER: PROC_INTEREST,
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
		
		# completing GRAND TOTAL row values with missing grand total values
		
		additionalGrandTotalRowValues = yieldOwnerWithTotalsDetailDf.loc[yieldOwnerWithTotalsDetailDf.index == DATAFRAME_HEADER_TOTAL].sum(numeric_only=True, axis=0)[
			fiatColNameDic.keys()]
		
		for index, value in additionalGrandTotalRowValues.items():
			yieldOwnerWithTotalsDetailDf.loc[DATAFRAME_HEADER_GRAND_TOTAL, index] = value
		
		# defining multi level language dependent index rows

		if len(fiatLst) > 1:
			multiIndexLevelZeroLst = [' ', ' '] + [' '] * (depWithdrFiatColNb - 5) + [PROC_DEP[self.language], PROC_WITHDR[self.language]] + [self.PROC_HELP_2, self.PROC_HELP_3, self.PROC_HELP_4] + [' '] * 20
		else:
			multiIndexLevelZeroLst = [' ', ' '] + [' '] * (depWithdrFiatColNb - 1) + [PROC_DEP[self.language], PROC_WITHDR[self.language]] + [self.PROC_HELP_2, self.PROC_HELP_3, self.PROC_HELP_4] + [' '] * 9

		levelOneDepWithdrFiatArray = []

		if len(fiatLst) > 1:
			levelOneUniqueColNameModifier = ' '
		else:
			levelOneUniqueColNameModifier = ''

		for _ in fiatLst:
			levelOneDepWithdrFiatArray += [PROC_DATE_FROM_RATE[self.language], PROC_CURRENT_RATE[self.language]]
			levelOneDepWithdrFiatArray += [levelOneUniqueColNameModifier + PROC_CURRENT_RATE[self.language]]
			levelOneUniqueColNameModifier += ' '
			levelOneDepWithdrFiatArray += [levelOneUniqueColNameModifier + PROC_CURRENT_RATE[self.language]]
			levelOneUniqueColNameModifier += ' '
			levelOneDepWithdrFiatArray += [PROC_CAPITAL_GAIN[self.language]]
			levelOneDepWithdrFiatArray += [' ']

		multiIndexLevelOneLst = [' ', ' ', PROC_AMOUNT[self.language]] + [PROC_DEP_RATE[self.language], PROC_CUR_RATE[self.language]] + levelOneDepWithdrFiatArray + [PROC_YIELD_DAYS[self.language]] + [PROC_INTEREST] + [' ', ' ']

		for fiat in fiatLst:
			multiIndexLevelOneLst += [PROC_AMOUNT[self.language], PROC_YIELD[self.language], PROC_IN[self.language] + fiat.upper() + ' ']

		multiIndexLevelTwoLst = yieldOwnerWithTotalsDetailDf.columns.tolist()
		multiIndexLevelTwoLst = [x.replace('_', '') for x in multiIndexLevelTwoLst]

		multiIndexLevelTwoLst[5] = self.PROC_HELP_1 + multiIndexLevelTwoLst[5]
		# in order to differentiate by fiat the daily, monthly and
		# yearly fiat interest columns inserted into the
		# yieldOwnerWithTotalsDetailDf, a low case fiat symbol was
		# added to the added column names. Now, when defining the
		# level 2 multi index column names, this low case fiat symbol
		# is simply removed, since the multi level indexes do not have
		# to be unique.
		for fiat in fiatLst:
			fiatLowCase = fiat.lower()
			multiIndexLevelTwoLst = [x.replace(fiatLowCase, '') for x in multiIndexLevelTwoLst]

		# variables for debugging purpose only ...
		# l1 = len(multiIndexLevelZeroLst)
		# l2 = len(multiIndexLevelOneLst)
		# l3 = len(multiIndexLevelTwoLst)

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
		pd.options.display.float_format = '{:.2f}'.format

		yieldOwnerWithTotalsDetaiAndFiatlDfStr = self.ownerDepositYieldComputer.getDataframeStrWithFormattedColumns(
			yieldOwnerWithTotalsDetailDf, {})

		# resetting the pandas global float format so that the unit tests
		# are not impacted by the previous global float format setting
		pd.reset_option('display.float_format')

		return sbYieldRatesWithTotalDf, \
			   yieldOwnerWithTotalsSummaryDf, \
			   yieldOwnerWithTotalsDetailDf, \
			   yieldOwnerWithTotalsDetaiAndFiatlDfStr, \
			   depositCrypto

	def activateHelpNumbers(self):
		'''
		Calling this method before calling addfiatConversionInfo() will add
		help numbers to the concerned columns.

		@return:
		'''
		self.PROC_HELP_1 = '(1)  '
		self.PROC_HELP_2 = '(2)'
		self.PROC_HELP_3 = '(3)'
		self.PROC_HELP_4 = '(4)'

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
			cryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, fiat)
			cryptoFiatRateDic[fiat] = cryptoFiatRate

		if not self.cryptoRateFiat in fiatlLst:
			# since the cryptoRateFiat current rate will be used for inserting the
			# current crypto/fiat rate column, it is added to the returned
			# cryptoFiatRateDic
			cryptoFiatRate = self.cryptoFiatRateComputer.computeCryptoFiatRate(crypto, self.cryptoRateFiat)
			cryptoFiatRateDic[self.cryptoRateFiat] = cryptoFiatRate

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
