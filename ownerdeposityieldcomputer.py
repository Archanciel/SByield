from datetime import timedelta
from sbyieldratecomputer import *
from pandasdatacomputer import PandasDataComputer
from depositdateafterlastyieldpaymenterror import DepositDateAfterLastYieldPaymentError

DEPOSIT_YIELD_HEADER_CAPITAL = 'CAPITAL'
DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER = 'YIELD DAYS'
DEPOSIT_YIELD_HEADER_YIELD_AMOUNT = 'YIELD AMT'
DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT = 'YIELD AMT %'
DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT = 'Y YIELD %'

class OwnerDepositYieldComputer(PandasDataComputer):
	"""
	This class spreads out the Swissborg daily earnings proportionally to the
	deposit/withdrawal amounts invested by the different yield subscription
	amounts owners.
	"""
	def __init__(self,
				 sbYieldRateComputer):
		"""
		Currently, the configMgr is not used. Constants are used in place.
		
		:param configMgr:
		"""
		super().__init__()
		self.sbYieldRateComputer = sbYieldRateComputer

	def computeDepositsYields(self):
		"""
		From the deposit/withdrawal csv file and the Swissborg account statement sheet,
		computes the yields for each owner. Returns the computed daily and yearly
		Swissborg yield rates as well as a summary and a detailed owner yield amount
		and total capital amount data frame.

		Can raise InvalidDepositDateError in case the deposit csv file contains a deposit or withdrawal
		whose date is after the last Swissborg yield payment date.

		:return: sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf

		sbYieldRatesWithTotalDf example:

					  EARNINGS  D YIELD RATE  Y YIELD RATE
		DATE
		2021-01-01   15.023631      1.000501      1.200504
		2021-01-02   14.337142      1.000409      1.161162
		2021-01-03   24.776591      1.000476      1.189786
		2021-01-04   28.664574      1.000597      1.243164
		2021-01-05   27.450686      1.000571      1.231608
		TOTAL       110.252623           NaN           NaN

		yieldOwnerWithTotalsSummaryDf example:

			   DEP/WITHDR   YIELD AMT         TOTAL
		OWNER
		Béa        2000.0    3.289022   2003.289022
		JPS       22000.0   47.349361  22047.349361
		Papa      24000.0   59.614241  24059.614241
		TOTAL     48000.0  110.252623  48110.252623

		yieldOwnerWithTotalsDetailDf example:

			  DEP/WITHDR   CAPITAL        FROM          TO YIELD DAYS   YIELD AMT  YIELD AMT %  Y YIELD %
		OWNER
		Béa     2,000.00  2,000.00  2021-01-03  2021-01-05          3  3.28902191     0.164451  22.130240
		TOTAL   2,003.29                                               3.28902191
		JPS    10,000.00 10,000.00  2021-01-01  2021-01-01          1  5.00787687     0.050079  20.050434
		JPS     5,000.00 15,005.01  2021-01-02  2021-01-02          1  6.14390374     0.040946  16.116194
		JPS     7,000.00 22,011.15  2021-01-03  2021-01-05          3 36.19758018     0.164451  22.130240
		TOTAL  22,047.35                                              47.34936079
		Papa   20,000.00 20,000.00  2021-01-01  2021-01-02          2 18.20899240     0.091045  18.066928
		Papa    8,000.00 28,018.21  2021-01-03  2021-01-03          1 13.34238365     0.047620  18.978557
		Papa   -4,000.00 24,031.55  2021-01-04  2021-01-05          2 28.06286451     0.116775  23.737252
		TOTAL  24,059.61       NaN         NaN         NaN            59.61424056          NaN        NaN
		"""
		depositDf, depositCrypto, sbYieldRatesDf = self.sbYieldRateComputer.getDepositsAndDailyYieldRatesDataframes()

		# sorting deposits by owner and by deposit date
		ownerDateSortedDepositDf = depositDf.sort_values([DEPOSIT_SHEET_HEADER_OWNER[GB], DEPOSIT_SHEET_HEADER_DATE], axis=0)

		# replace DATE index with integer index
		ownerDateSortedDepositDf = self._replaceDateIndexByIntIndex(ownerDateSortedDepositDf, DEPOSIT_SHEET_HEADER_DATE, DATAFRAME_HEADER_INDEX)

		# insert DEPOSIT_YIELD_HEADER_CAPITAL column
		self._insertEmptyFloatColumns(ownerDateSortedDepositDf,
									  2,
									  [DEPOSIT_YIELD_HEADER_CAPITAL])

		# rename date column
		ownerDateSortedDepositDf = ownerDateSortedDepositDf.rename(columns={DEPOSIT_SHEET_HEADER_DATE: DEPOSIT_YIELD_HEADER_DATE_FROM[GB]})

		# remove time component
		ownerDateSortedDepositDf[DEPOSIT_YIELD_HEADER_DATE_FROM[GB]] = pd.to_datetime(ownerDateSortedDepositDf[
																					  DEPOSIT_YIELD_HEADER_DATE_FROM[GB]]).dt.date

		# insert empty columns
		self._appendEmptyColumns(ownerDateSortedDepositDf,
								 [DEPOSIT_YIELD_HEADER_DATE_TO[GB], DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER])

		self._insertEmptyFloatColumns(ownerDateSortedDepositDf,
									  None,
									  [DEPOSIT_YIELD_HEADER_YIELD_AMOUNT])

		# compute capital, date to and yield day number
		previousRowOwner = None
		currentRowCapital = 0.0
		firstYieldPaymentDate = sbYieldRatesDf.index[0]
		lastYieldPaymentDate = sbYieldRatesDf.index[-1]
		maxIdxValue = len(ownerDateSortedDepositDf)
		ownerDateSortedDepositBeforeUpdateDf = ownerDateSortedDepositDf.copy()

		for i in range(1, maxIdxValue + 1):
			currentRowOwner = ownerDateSortedDepositDf.loc[i, DEPOSIT_SHEET_HEADER_OWNER[GB]]
			currentRowDateFrom = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM[GB]]
			if currentRowDateFrom > lastYieldPaymentDate:
				# the case if an erroneous deposit/withdrawal date which is greater than
				# the Swissborg last payment date was defined in the deposit csv file
				raise DepositDateAfterLastYieldPaymentError(self.sbYieldRateComputer.depositSheetFilePathName,
															ownerDateSortedDepositDf.loc[i, DEPOSIT_SHEET_HEADER_OWNER[GB]],
															currentRowDateFrom,
															ownerDateSortedDepositDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW],
															lastYieldPaymentDate)
			if currentRowDateFrom < firstYieldPaymentDate:
				# the case if the application is run on a Swissborg earning sheet which was downloaded
				# with specifying a start date later than the first deposits dates. This does not cause
				# any problem
				currentRowDateFrom = firstYieldPaymentDate
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM[GB]] = currentRowDateFrom
			if currentRowOwner != previousRowOwner:
				previousRowOwner = currentRowOwner
				currentRowCapital = ownerDateSortedDepositDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW]
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL] = currentRowCapital

				# initializing the dateTo and day value in the ownerDateSortedDepositDf.
				# This is useful if only 1 deposit is defined for this owner
				# in the deposit csv file ! Otherwise, this value will be
				# overwritten when handling the next deposit for the same
				# owner...
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO[GB]] = lastYieldPaymentDate
				previousRowDateToMinusPreviousRowDateFromTimeDelta = lastYieldPaymentDate - currentRowDateFrom
				yieldDayNumber = previousRowDateToMinusPreviousRowDateFromTimeDelta.days + 1
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
				if i > 1:
					# setting yield date to as well as yield day number
					# IMPORTANT: the data computed below (date to, yield day
					# number, yield percent, yearly yield percent will be
					# recalculated and overwritten if the current owner has
					# more than 1 deposit !
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO[GB]] = lastYieldPaymentDate
					previousRowDateToMinusPreviousRowDateFromTimeDelta = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO[GB]] - \
												   currentRowDateFrom
					yieldDayNumber = previousRowDateToMinusPreviousRowDateFromTimeDelta.days + 1
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
					yieldAmount, yieldPercent, yearlyYieldPercent = self._computeCapitalYieldAmountAndPercents(
						sbYieldRatesDf,
						currentRowCapital,
						currentRowDateFrom,
						lastYieldPaymentDate,
						yieldDayNumber)
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = yieldAmount
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT] = yieldPercent
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = yearlyYieldPercent
				else:
					# i == 1 means we are handling the first deposit of the first
					# owner in the sorted deposit csv file.
					# IMPORTANT: the data computed below (date to, yield day
					# number, yield percent, yearly yield percent will be
					# recalculated and overwritten if the first owner has more
					# than 1 deposit !
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO[GB]] = lastYieldPaymentDate
					previousRowDateToMinusPreviousRowDateFromTimeDelta = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO[GB]] - \
												   currentRowDateFrom
					yieldDayNumber = previousRowDateToMinusPreviousRowDateFromTimeDelta.days + 1
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
					yieldAmount, yieldPercent, yearlyYieldPercent = self._computeCapitalYieldAmountAndPercents(
						sbYieldRatesDf,
						currentRowCapital,
						currentRowDateFrom,
						lastYieldPaymentDate,
						yieldDayNumber)
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = yieldAmount
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT] = yieldPercent
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = yearlyYieldPercent
			else:
				# handling additional deposits for current owner

				# resetting yield date to as well as yield day number, yield
				# percent and yearly yield percent for previous deposit of
				# current owner
				previousRowDateTo = currentRowDateFrom - timedelta(days=1)
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO[GB]] = previousRowDateTo
				previousRowDateFrom = ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM[GB]]
				previousRowDateToMinusPreviousRowDateFromTimeDelta = previousRowDateTo - \
																	 previousRowDateFrom
				previousRowYieldDayNumber = previousRowDateToMinusPreviousRowDateFromTimeDelta.days + 1

				if previousRowYieldDayNumber <= 0:
					# the case if in the deposit csv file the first deposit for an owner
					# is defined with a date before the first yield payment date and
					# the next deposit is defined with a date equal to the first yield
					# payment date like in the example below. First yield is payed on
					# 2020/12/22:
					#
					# JPS,2020/11/15 00:00:00,2000
					# JPS,2020/11/17 00:00:00,300
					# JPS,2020/11/19 00:00:00,200
					# JPS,2020/12/22 00:00:00,100
					# JPS,2020/12/23 00:00:00,50
					ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM[GB]] = \
						ownerDateSortedDepositBeforeUpdateDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM[GB]]

				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = previousRowYieldDayNumber
				previousRowCapital = ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_CAPITAL]

				previousRowYieldAmount, previousRowYieldPercent, previousRowYearlyYieldPercent = \
					self._computeCapitalYieldAmountAndPercents(sbYieldRatesDf,
															   previousRowCapital,
															   previousRowDateFrom,
															   previousRowDateTo,
															   previousRowYieldDayNumber)
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = previousRowYieldAmount
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT] = previousRowYieldPercent
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = previousRowYearlyYieldPercent
				currentRowCapital = currentRowCapital + ownerDateSortedDepositDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW]
				currentRowCapital += previousRowYieldAmount
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL] = currentRowCapital

				# setting yield dateTo as well as yield day number for current
				# row.
				# IMPORTANT: the data computed below (date to, yield day
				# number, yield percent, yearly yield percent will be
				# recalculated and overwritten if the current owner has
				# additional deposits !
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO[GB]] = lastYieldPaymentDate
				dateToMinusDateFromTimeDelta = lastYieldPaymentDate - currentRowDateFrom
				yieldDayNumber = dateToMinusDateFromTimeDelta.days + 1
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
				yieldAmount, yieldPercent, yearlyYieldPercent = self._computeCapitalYieldAmountAndPercents(sbYieldRatesDf,
																										   currentRowCapital,
																										   currentRowDateFrom,
																										   lastYieldPaymentDate,
																										   yieldDayNumber)
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = yieldAmount
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT] = yieldPercent
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = yearlyYieldPercent

		yieldOwnerWithTotalsSummaryDf = self._createYieldOwnerWithTotalsSummaryDf(ownerDateSortedDepositDf)

		# creating the yieldOwnerWithTotalsDetailDf column name list including
		# optional fiat amount column names
		yieldOwnerWithTotalsDetailDfColNameLst, fiatAmountColNameLst = self._createYieldOwnerWithTotalsDetailDfColumnLst(ownerDateSortedDepositDf)

		# creating yieldOwnerWithTotalsDetailDf with ownerDateSortedDepositDf
		# rows and TOTAL rows and the G TOTAL row
		yieldOwnerWithTotalsDetailDf = self._createYieldOwnerWithTotalsDetailDf(ownerDateSortedDepositDf,
																				yieldOwnerWithTotalsDetailDfColNameLst,
																				fiatAmountColNameLst)

		sbYieldRatesWithTotalDf = sbYieldRatesDf.copy()

		lastRowCapitalPlusEarningValue = sbYieldRatesWithTotalDf.iloc[-1][MERGED_SHEET_HEADER_EARNING_CAPITAL] + \
										 sbYieldRatesWithTotalDf.iloc[-1][MERGED_SHEET_HEADER_EARNING_NEW_NAME[GB]]

		# removing 00:00:00 time component from the sbYieldRatesDf index.
		sbYieldRatesWithTotalDf.index = pd.to_datetime(sbYieldRatesWithTotalDf.index).strftime('%Y-%m-%d')

		# adding TOTAL row to SB yield rates data frame for MERGED_SHEET_HEADER_EARNING_NEW_NAME column only
		sbYieldRatesWithTotalDf.loc[DATAFRAME_HEADER_TOTAL] = \
			sbYieldRatesWithTotalDf[[MERGED_SHEET_HEADER_EARNING_NEW_NAME[GB]]].sum(numeric_only=True)

		sbYieldRatesWithTotalDf.loc[DATAFRAME_HEADER_TOTAL, MERGED_SHEET_HEADER_EARNING_CAPITAL] = lastRowCapitalPlusEarningValue

		return sbYieldRatesWithTotalDf, \
			   yieldOwnerWithTotalsSummaryDf, \
			   yieldOwnerWithTotalsDetailDf, \
			   depositCrypto

	def _computeCapitalYieldAmountAndPercents(self,
											  sbYieldRatesDf,
											  capital,
											  dateFrom,
											  dateTo,
											  yieldDayNumber):
		firstPaymentDate = dateFrom
		lastPaymentDate = dateTo
		yieldRatesDataframeSubSet = sbYieldRatesDf.loc[firstPaymentDate:lastPaymentDate]
		capitalPlusYield = capital

		for index, row in yieldRatesDataframeSubSet.iterrows():
			yieldRate = row[2]
			capitalPlusYield = capitalPlusYield * yieldRate

		yieldAmount = capitalPlusYield - capital
		amountByCapital = yieldAmount / capital
		yieldAmountPercent = amountByCapital * 100

		if yieldAmount > 0:
			yearlyYieldRate = np.power(amountByCapital + 1, 365 / yieldDayNumber)
			yearlyYieldPercent = (yearlyYieldRate - 1) * 100
		else:
			yearlyYieldPercent = 0

		return yieldAmount, yieldAmountPercent, yearlyYieldPercent

	def _createYieldOwnerWithTotalsSummaryDf(self, depositsYieldsDf):
		yieldOwnerSummaryTotals = depositsYieldsDf.groupby([DEPOSIT_SHEET_HEADER_OWNER[GB]]).sum().reset_index()[[DEPOSIT_SHEET_HEADER_OWNER[GB], DATAFRAME_HEADER_DEPOSIT_WITHDRAW, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]]

		# adding the TOTAL column
		for index in range(0, len(yieldOwnerSummaryTotals)):
			yieldOwnerSummaryTotals.loc[index, DATAFRAME_HEADER_TOTAL] = \
				yieldOwnerSummaryTotals.loc[index, DATAFRAME_HEADER_DEPOSIT_WITHDRAW] + \
				yieldOwnerSummaryTotals.loc[index, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]

		# resetting index to OWNER column
		yieldOwnerSummaryTotals = yieldOwnerSummaryTotals.set_index(DEPOSIT_SHEET_HEADER_OWNER[GB])

		# adding the TOTAL row
		yieldOwnerSummaryTotals.loc[DATAFRAME_HEADER_TOTAL] = \
			yieldOwnerSummaryTotals.sum(numeric_only=True, axis=0)[[
				DATAFRAME_HEADER_DEPOSIT_WITHDRAW,
				DEPOSIT_YIELD_HEADER_YIELD_AMOUNT,
				DATAFRAME_HEADER_TOTAL]]

		return yieldOwnerSummaryTotals

	def _createYieldOwnerWithTotalsDetailDf(self,
											ownerDateSortedDepositDf,
											yieldOwnerWithTotalsDetailDfColNameLst,
											fiatAmountColNameLst):
		'''
		This method creates the yield owner with TOTAL and G TOTAL rows
		dataframe.

		First, it adds the passed deposit yield dataframe rows to the created
		dataframe. Then, it computes the TOTAL row values and add the TOTAL
		row to the created dataframe.

		The yearly yield rate of the added TOTAL row is in fact the average
		yield rate computed from the different deposit yearly yield ratey.

		Finally, the G TOTAL row is added to the created dataframe.

		@param ownerDateSortedDepositDf:
		@param yieldOwnerWithTotalsDetailDfColNameLst:
		@param fiatAmountColNameLst:

		@return: yield owner with total and grand total rows dataframe
		'''
		yieldOwnerWithTotalsDetailDf = pd.DataFrame(columns=yieldOwnerWithTotalsDetailDfColNameLst)

		# initializing  to the first owner in the sorted deposit yield dataframe
		currentOwner = ownerDateSortedDepositDf.loc[1, DEPOSIT_SHEET_HEADER_OWNER[GB]]

		# creating a groupby owner sum dataframe
		ownerGroupTotalDf = ownerDateSortedDepositDf.groupby([DEPOSIT_SHEET_HEADER_OWNER[GB]]).agg({DATAFRAME_HEADER_DEPOSIT_WITHDRAW: 'sum',
																									DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: 'sum', }).reset_index()

		ownerGroupTotalIndex = 0

		# deactivating SettingWithCopyWarning caused by totalRow[DEPOSIT_SHEET_HEADER_OWNER] += ' total'
		pd.set_option('mode.chained_assignment', None)

		yieldDayNumberTotal = 0
		yearlyYieldPercentTimeYieldDayNumberTotal = 0

		for index, row in ownerDateSortedDepositDf.iterrows():
			# creating a dictionary for the fiat columns, if they exist
			fiatAmountColDic = {}

			# creating a fiat amount column dic with as key the optional
			# deposit CSV file fiat columns and as value the corresponding
			# column value of the current row
			for colName in fiatAmountColNameLst:
				fiatAmountColDic[colName] = row[colName]

			# creating the yieldOwnerWithTotalsDetailDf column dic with as key
			# the yieldOwnerWithTotalsDetailDf column names and as value the
			# corresponding column value of the current row
			appendDic = {DEPOSIT_SHEET_HEADER_OWNER[GB]: row[DEPOSIT_SHEET_HEADER_OWNER[GB]],
						 DATAFRAME_HEADER_DEPOSIT_WITHDRAW: row[DATAFRAME_HEADER_DEPOSIT_WITHDRAW],
						 DEPOSIT_YIELD_HEADER_CAPITAL: row[DEPOSIT_YIELD_HEADER_CAPITAL],
						 DEPOSIT_YIELD_HEADER_DATE_FROM[GB]: row[DEPOSIT_YIELD_HEADER_DATE_FROM[GB]],
						 DEPOSIT_YIELD_HEADER_DATE_TO[GB]: row[DEPOSIT_YIELD_HEADER_DATE_TO[GB]],
						 DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER: row[
							DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER],
						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: row[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT],
						 DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: row[
							DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT],
						 DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: row[
							DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT]}

			# adding the fiatAmountColDic to the appendDic
			appendDic.update(fiatAmountColDic)

			yieldDayNumber = row[DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER]

			if currentOwner == row[DEPOSIT_SHEET_HEADER_OWNER[GB]]:
				# computing values used for calculating the yearly yield % average
				# rate used in Processor to compute daily, monthly and yearly generated
				# yield amounts
				yieldDayNumberTotal += yieldDayNumber
				yearlyYieldPercentTimeYieldDayNumberTotal += row[DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] * yieldDayNumber

				# adding the yieldOwnerWithTotalsDetailDf row for the current
				# owner
				yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.append(appendDic, ignore_index=True)
			else:
				# as owner has changed, adding the total row for the previous
				# owner
				totalRow = ownerGroupTotalDf.loc[ownerGroupTotalIndex]

				# computing the yearly yield % average rate used in Processor to
				# compute daily, monthly and yearly generated yield amounts.
				# Those values have sense only in the owner total row !
				yearlyYieldPercentAverage = yearlyYieldPercentTimeYieldDayNumberTotal / yieldDayNumberTotal
				totalRow[DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = yearlyYieldPercentAverage
				totalRow[DEPOSIT_SHEET_HEADER_OWNER[GB]] = DATAFRAME_HEADER_TOTAL
				yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.append(totalRow, ignore_index=True)
				ownerGroupTotalIndex += 1

				# now adding the first yieldOwnerWithTotalsDetailDf row for
				# the current owner
				yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.append(appendDic, ignore_index=True)
				currentOwner = row[DEPOSIT_SHEET_HEADER_OWNER[GB]]

		# appending last owner total row
		totalRow = ownerGroupTotalDf.loc[ownerGroupTotalIndex]

		# computing the yearly yield % average rate used in Processor to
		# compute daily, monthly and yearly generated yield amounts.
		# Those values have sense only in the owner total row !
		yearlyYieldPercentAverage = yearlyYieldPercentTimeYieldDayNumberTotal / yieldDayNumberTotal
		totalRow[DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = yearlyYieldPercentAverage
		totalRow[DEPOSIT_SHEET_HEADER_OWNER[GB]] = DATAFRAME_HEADER_TOTAL
		yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.append(totalRow, ignore_index=True)

		# appending grand total row
		grandTotalRow = ownerGroupTotalDf.sum(numeric_only=True, axis=0)[[DATAFRAME_HEADER_DEPOSIT_WITHDRAW, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]]
		yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.append(grandTotalRow, ignore_index=True)
		yieldOwnerWithTotalsDetailDf.loc[len(yieldOwnerWithTotalsDetailDf) - 1, DEPOSIT_SHEET_HEADER_OWNER[GB]] = DATAFRAME_HEADER_GRAND_TOTAL

		# reseting index to OWNER column
		yieldOwnerWithTotalsDetailDf = yieldOwnerWithTotalsDetailDf.set_index(DEPOSIT_SHEET_HEADER_OWNER[GB])

		return yieldOwnerWithTotalsDetailDf

	def _createYieldOwnerWithTotalsDetailDfColumnLst(self, depositsYieldsDf):
		'''
		This method creates the list of yieldOwnerWithTotalsDetailDf column
		names. It adds At the end of the list the column names for the fiat
		defined in the deposit CSV file. 0 or n fiats can be specified in
		the deposit CSV file, which justifies the current method.
		'''
		yieldOwnerWithTotalsDetailDfColNameLst = [DEPOSIT_SHEET_HEADER_OWNER[GB],
												  DATAFRAME_HEADER_DEPOSIT_WITHDRAW,
												  DEPOSIT_YIELD_HEADER_CAPITAL,
												  DEPOSIT_YIELD_HEADER_DATE_FROM[GB],
												  DEPOSIT_YIELD_HEADER_DATE_TO[GB],
												  DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER,
												  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT,
												  DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT,
												  DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT]

		# adding the deposit CSV file fiat amount column names.
		# Ex of deposit file header: OWNER,DATE,DEP/WITHDR,USD AMT,CHF AMT
		fiatAmountColNameLst = [col for col in depositsYieldsDf.columns if 'AMT' in col and 'YIELD' not in col]
		yieldOwnerWithTotalsDetailDfColNameLst.extend(fiatAmountColNameLst)

		return yieldOwnerWithTotalsDetailDfColNameLst, fiatAmountColNameLst
