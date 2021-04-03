from datetime import timedelta
from sbyieldratecomputer import *
from pandasdatacomputer import PandasDataComputer
from invaliddepositdateerror import InvalidDepositDateError

DEPOSIT_YIELD_HEADER_CAPITAL = 'CAPITAL'
DEPOSIT_YIELD_HEADER_DATE_FROM = 'FROM'
DEPOSIT_YIELD_HEADER_DATE_TO = 'TO'
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
	def __init__(self, configMgr, sbYieldRateComputer):
		"""
		Currently, the configMgr is not used. Constants are used in place.
		
		:param configMgr:
		"""
		super().__init__(configMgr)
		self.sbYieldRateComputer = sbYieldRateComputer

	def computeDepositsYields(self, yieldCrypto):
		"""
		From the deposit/withdrawal csv file and the Swissborg account statement sheet,
		computes the yields for each owner. Returns the computed daily and yearly
		Swissborg yield rates aswell as a summary and a detailed owner yield amount
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
		depositDf, sbYieldRatesDf = self.sbYieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)

		# sorting deposits by owner and by deposit date
		ownerDateSortedDepositDf = depositDf.sort_values([DEPOSIT_SHEET_HEADER_OWNER, DEPOSIT_SHEET_HEADER_DATE], axis=0)
		
		# replace DATE index with integer index
		ownerDateSortedDepositDf = self._replaceDateIndexByIntIndex(ownerDateSortedDepositDf, DEPOSIT_SHEET_HEADER_DATE, DATAFRAME_HEADER_INDEX)

		# insert DEPOSIT_YIELD_HEADER_CAPITAL column
		self._insertEmptyFloatColumns(ownerDateSortedDepositDf,
		                              2,
		                              [DEPOSIT_YIELD_HEADER_CAPITAL])

		# rename date column
		ownerDateSortedDepositDf = ownerDateSortedDepositDf.rename(columns={DEPOSIT_SHEET_HEADER_DATE: DEPOSIT_YIELD_HEADER_DATE_FROM})

		# remove time component
		ownerDateSortedDepositDf[DEPOSIT_YIELD_HEADER_DATE_FROM] = pd.to_datetime(ownerDateSortedDepositDf[DEPOSIT_YIELD_HEADER_DATE_FROM]).dt.date

		# insert empty columns
		self._appendEmptyColumns(ownerDateSortedDepositDf,
		                         [DEPOSIT_YIELD_HEADER_DATE_TO, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER])

		self._insertEmptyFloatColumns(ownerDateSortedDepositDf,
		                              None,
		                              [DEPOSIT_YIELD_HEADER_YIELD_AMOUNT])

		# compute capital, date to and yield day number
		previousRowOwner = None
		currentRowCapital = 0.0
		firstYieldTimeStamp = sbYieldRatesDf.index[0]
		firstYieldPaymentDate = firstYieldTimeStamp.date()
		lastYieldTimeStamp = sbYieldRatesDf.index[-1]
		lastYieldPaymentDate = lastYieldTimeStamp.date()
		maxIdxValue = len(ownerDateSortedDepositDf)

		for i in range(1, maxIdxValue + 1):
			currentRowOwner = ownerDateSortedDepositDf.loc[i, DEPOSIT_SHEET_HEADER_OWNER]
			currentRowDateFrom = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
			if currentRowDateFrom > lastYieldPaymentDate:
				# the case if an erroneous deposit/withdrawal date which is greater than
				# the Swissborg last payment date was defined in the deposit csv file
				raise InvalidDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
				                              ownerDateSortedDepositDf.loc[i, DEPOSIT_SHEET_HEADER_OWNER],
				                              currentRowDateFrom,
				                              ownerDateSortedDepositDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW],
				                              lastYieldPaymentDate)
			if currentRowDateFrom < firstYieldPaymentDate:
				# the case if the application is run on a Swissborg earning sheet which was downloaded
				# with specifying a start date later than the first deposits dates. This does not cause
				# any problem
				currentRowDateFrom = firstYieldPaymentDate
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM] = currentRowDateFrom
			if currentRowOwner != previousRowOwner:
				previousRowOwner = currentRowOwner
				currentRowCapital = ownerDateSortedDepositDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW]
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL] = currentRowCapital
				
				# initializing the dateTo and day value in the ownerDateSortedDepositDf. This is useful if
				# only 1 deposit is defined in the deposit csv file ! Otherwise, this value will be
				# overwritten when handling the next deposit...
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldPaymentDate
				dateToMinusDateFromTimeDelta = lastYieldPaymentDate - currentRowDateFrom
				yieldDayNumber = dateToMinusDateFromTimeDelta.days + 1
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
				if i > 1:
					if i == maxIdxValue:
						# setting yield date to as well as yield day number
						ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldPaymentDate
						dateToMinusDateFromTimeDelta = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] - \
						                               currentRowDateFrom
						yieldDayNumber = dateToMinusDateFromTimeDelta.days + 1
						ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
						yieldAmount, yieldPercent, yearlyYieldPercent = self._computeCapitalYieldAmount(
							sbYieldRatesDf,
							currentRowCapital,
							currentRowDateFrom,
							lastYieldPaymentDate,
							yieldDayNumber)
						ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = yieldAmount
						ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT] = yieldPercent
						ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = yearlyYieldPercent
					else:
						# here, the owner has changed. This means that the previous owner capital
						# remains the same till the end of SB yield earning payments
						
						# setting yield dateTo as well as yield day number for previous owner
						ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldPaymentDate
						previousOwnerDateFrom = ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM]
						dateToMinusDateFromTimeDelta = lastYieldPaymentDate - \
						                               previousOwnerDateFrom
						yieldDayNumber = dateToMinusDateFromTimeDelta.days + 1
						ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
						previousOwnerCapital = ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_CAPITAL]
						yieldAmount, yieldPercent, yearlyYieldPercent = self._computeCapitalYieldAmount(
							sbYieldRatesDf,
							previousOwnerCapital,
							previousOwnerDateFrom,
							lastYieldPaymentDate,
							yieldDayNumber)
						ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = yieldAmount
						ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT] = yieldPercent
						ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = yearlyYieldPercent
				else:
					# if i == maxIdxValue:
					# 	# the case if the deposit csv file has only 1 line ...
					# 	# setting yield date to as well as yield day number
					# 	ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldPaymentDate
					# 	dateToMinusDateFromTimeDelta = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] - \
					# 	                               currentRowDateFrom
					# 	yieldDayNumber = dateToMinusDateFromTimeDelta.days + 1
					# 	ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
					# 	yieldAmount, yieldPercent, yearlyYieldPercent = self._computeCapitalYieldAmount(
					# 		sbYieldRatesDf,
					# 		currentRowCapital,
					# 		currentRowDateFrom,
					# 		lastYieldPaymentDate,
					# 		yieldDayNumber)
					# 	ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = yieldAmount
					# 	ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT] = yieldPercent
					# 	ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = yearlyYieldPercent
					# else:
					# handling the first deposit csv file line ...
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldPaymentDate
					dateToMinusDateFromTimeDelta = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] - \
					                               currentRowDateFrom
					yieldDayNumber = dateToMinusDateFromTimeDelta.days + 1
					ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
					yieldAmount, yieldPercent, yearlyYieldPercent = self._computeCapitalYieldAmount(
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
				currentRowCapital = currentRowCapital + ownerDateSortedDepositDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW]
				
				# setting yield date to as well as yield day number for previous line
				currentRowDateFromMinusOneDay = currentRowDateFrom - timedelta(days=1)
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO] = currentRowDateFromMinusOneDay
				previousRowDateFrom = ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM]
				dateToMinusDateFromTimeDelta = currentRowDateFromMinusOneDay - \
				                               previousRowDateFrom
				yieldDayNumber = dateToMinusDateFromTimeDelta.days + 1
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
				previousRowCapital = ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_CAPITAL]
				
				yieldAmount, yieldPercent, yearlyYieldPercent = self._computeCapitalYieldAmount(sbYieldRatesDf,
				                                                                                previousRowCapital,
				                                                                                previousRowDateFrom,
				                                                                                currentRowDateFromMinusOneDay,
				                                                                                yieldDayNumber)
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = yieldAmount
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT] = yieldPercent
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = yearlyYieldPercent
				currentRowCapital += yieldAmount
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL] = currentRowCapital

				# setting yield dateTo as well as yield day number for current line
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldPaymentDate
				dateToMinusDateFromTimeDelta = lastYieldPaymentDate - currentRowDateFrom
				yieldDayNumber = dateToMinusDateFromTimeDelta.days + 1
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
				yieldAmount, yieldPercent, yearlyYieldPercent = self._computeCapitalYieldAmount(sbYieldRatesDf,
				                                                                                currentRowCapital,
				                                                                                currentRowDateFrom,
				                                                                                lastYieldPaymentDate,
				                                                                                yieldDayNumber)
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = yieldAmount
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT] = yieldPercent
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT] = yearlyYieldPercent
		
		yieldOwnerWithTotalsSummaryDf = self._computeYieldOwnerSummaryTotals(ownerDateSortedDepositDf)
		yieldOwnerWithTotalsDetailDf = self._computeYieldOwnerDetailTotals(ownerDateSortedDepositDf)
		
		sbYieldRatesWithTotalDf = sbYieldRatesDf.copy()
		
		# removing 00:00:00 time component from the sbYieldRatesDf index.
		sbYieldRatesWithTotalDf.index = pd.to_datetime(sbYieldRatesWithTotalDf.index).strftime('%Y-%m-%d')
		
		# adding TOTAL row to SB yield rates data frame for MERGED_SHEET_HEADER_EARNING_NEW_NAME column only
		sbYieldRatesWithTotalDf.loc[DATAFRAME_HEADER_TOTAL] = sbYieldRatesWithTotalDf[[MERGED_SHEET_HEADER_EARNING_NEW_NAME]].sum(numeric_only=True)

		return sbYieldRatesWithTotalDf, yieldOwnerWithTotalsSummaryDf, yieldOwnerWithTotalsDetailDf
	
	def _computeCapitalYieldAmount(self,
	                               sbYieldRatesDf,
	                               capital,
	                               dateFrom,
	                               dateTo,
	                               yieldDayNumber):
		firstPaymentDate = dateFrom
		lastPaymentDate = dateTo
		yieldRatesDataframeSubSet = sbYieldRatesDf.loc[firstPaymentDate:lastPaymentDate]
		capitalPlusYield = capital

		for index, values in yieldRatesDataframeSubSet.iterrows():
			yieldRate = values[1]
			capitalPlusYield = capitalPlusYield * yieldRate

		yieldAmount = capitalPlusYield - capital
		yieldAmountPercent = yieldAmount / capital * 100
		
		if yieldAmount > 0:
			yearlyYieldPercent = np.power((yieldAmount / capital) + 1, 365 / yieldDayNumber)
			yearlyYieldPercent = (yearlyYieldPercent - 1) * 100
		else:
			yearlyYieldPercent = 0
		
		return yieldAmount, yieldAmountPercent, yearlyYieldPercent
	
	def _computeYieldOwnerSummaryTotals(self, depositsYieldsDf):
		yieldOwnerSummaryTotals = depositsYieldsDf.groupby([DEPOSIT_SHEET_HEADER_OWNER]).sum().reset_index()[[DEPOSIT_SHEET_HEADER_OWNER, DATAFRAME_HEADER_DEPOSIT_WITHDRAW, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]]
		
		# adding a TOTAL column
		for index in range(0, len(yieldOwnerSummaryTotals)):
			yieldOwnerSummaryTotals.loc[index, DATAFRAME_HEADER_TOTAL] = yieldOwnerSummaryTotals.loc[index, DATAFRAME_HEADER_DEPOSIT_WITHDRAW] + yieldOwnerSummaryTotals.loc[index, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]

		# reseting index to OWNER column
		yieldOwnerSummaryTotals = yieldOwnerSummaryTotals.set_index(DEPOSIT_SHEET_HEADER_OWNER)
		
		yieldOwnerSummaryTotals.loc[DATAFRAME_HEADER_TOTAL] = yieldOwnerSummaryTotals.sum(numeric_only=True, axis=0)[[DATAFRAME_HEADER_DEPOSIT_WITHDRAW, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT, DATAFRAME_HEADER_TOTAL]]

		return yieldOwnerSummaryTotals
	
	def _computeYieldOwnerDetailTotals(self, depositsYieldsDf):
		totalDf = pd.DataFrame(columns=[DEPOSIT_SHEET_HEADER_OWNER,
		                                DATAFRAME_HEADER_DEPOSIT_WITHDRAW,
		                                DEPOSIT_YIELD_HEADER_CAPITAL,
		                                DEPOSIT_YIELD_HEADER_DATE_FROM,
		                                DEPOSIT_YIELD_HEADER_DATE_TO,
		                                DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER,
		                                DEPOSIT_YIELD_HEADER_YIELD_AMOUNT,
		                                DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT,
		                                DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT])
		
		currentOwner = depositsYieldsDf.loc[1, DEPOSIT_SHEET_HEADER_OWNER]
		
		ownerGroupTotalDf = depositsYieldsDf.groupby([DEPOSIT_SHEET_HEADER_OWNER]).agg({DATAFRAME_HEADER_DEPOSIT_WITHDRAW: 'sum',
		                                                                                DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: 'sum'}).reset_index()
		ownerGroupTotalIndex = 0
		
		# deactivating SettingWithCopyWarning caueed by totalRow[DEPOSIT_SHEET_HEADER_OWNER] += ' total'
		pd.set_option('mode.chained_assignment', None)
		
		for index, row in depositsYieldsDf.iterrows():
			if currentOwner == row[DEPOSIT_SHEET_HEADER_OWNER]:
				totalDf = totalDf.append({DEPOSIT_SHEET_HEADER_OWNER: row[DEPOSIT_SHEET_HEADER_OWNER],
				                          DATAFRAME_HEADER_DEPOSIT_WITHDRAW: row[DATAFRAME_HEADER_DEPOSIT_WITHDRAW],
				                          DEPOSIT_YIELD_HEADER_CAPITAL: row[DEPOSIT_YIELD_HEADER_CAPITAL],
				                          DEPOSIT_YIELD_HEADER_DATE_FROM: row[DEPOSIT_YIELD_HEADER_DATE_FROM],
				                          DEPOSIT_YIELD_HEADER_DATE_TO: row[DEPOSIT_YIELD_HEADER_DATE_TO],
				                          DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER: row[
					                          DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER],
				                          DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: row[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT],
				                          DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: row[
					                          DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT],
				                          DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: row[
					                          DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT]}, ignore_index=True)
			else:
				totalRow = ownerGroupTotalDf.loc[ownerGroupTotalIndex]
				totalRow[DEPOSIT_SHEET_HEADER_OWNER] = DATAFRAME_HEADER_TOTAL
				totalRow[DATAFRAME_HEADER_DEPOSIT_WITHDRAW] += totalRow[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]
				totalDf = totalDf.append(totalRow, ignore_index=True)
				ownerGroupTotalIndex += 1
				totalDf = totalDf.append({DEPOSIT_SHEET_HEADER_OWNER: row[DEPOSIT_SHEET_HEADER_OWNER],
				                          DATAFRAME_HEADER_DEPOSIT_WITHDRAW: row[DATAFRAME_HEADER_DEPOSIT_WITHDRAW],
				                          DEPOSIT_YIELD_HEADER_CAPITAL: row[DEPOSIT_YIELD_HEADER_CAPITAL],
				                          DEPOSIT_YIELD_HEADER_DATE_FROM: row[DEPOSIT_YIELD_HEADER_DATE_FROM],
				                          DEPOSIT_YIELD_HEADER_DATE_TO: row[DEPOSIT_YIELD_HEADER_DATE_TO],
				                          DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER: row[
					                          DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER],
				                          DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: row[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT],
				                          DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT: row[
					                          DEPOSIT_YIELD_HEADER_YIELD_AMOUNT_PERCENT],
				                          DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT: row[
					                          DEPOSIT_YIELD_HEADER_YEARLY_YIELD_PERCENT]}, ignore_index=True)
				currentOwner = row[DEPOSIT_SHEET_HEADER_OWNER]
		
		totalRow = ownerGroupTotalDf.loc[ownerGroupTotalIndex]
		totalRow[DEPOSIT_SHEET_HEADER_OWNER] = DATAFRAME_HEADER_TOTAL
		totalRow[DATAFRAME_HEADER_DEPOSIT_WITHDRAW] += totalRow[DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]
		
		totalDf = totalDf.append(totalRow, ignore_index=True)
		
		# reseting index to OWNER column
		totalDf = totalDf.set_index(DEPOSIT_SHEET_HEADER_OWNER)

		return totalDf
