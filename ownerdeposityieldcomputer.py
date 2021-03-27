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
		
		Can raise InvalidDepositDateError in case the deposit csv file contains a deposit or withdrawal
		whose date is after the last Swissborg yield payment date.
		"""
		depositDf, sbYieldRatesDf = self.sbYieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)

		# sorting deposits by owner and by deposit date
		ownerDateSortedDepositDf = depositDf.sort_values([DEPOSIT_SHEET_HEADER_OWNER, DEPOSIT_SHEET_HEADER_DATE], axis=0)
		
		# replace DATE index with integer index
		ownerDateSortedDepositDf = self._replaceDateIndexByIntIndex(ownerDateSortedDepositDf, DEPOSIT_SHEET_HEADER_DATE, DATAFRAME_HEADER_INDEX)

		# insert CAPITAL column
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
				
				# initializing the dateTo and day value in the ownerDateSortedDepositDf. This is usefull if
				# only 1 deposit is defined in the deposit csv file ! Otherwise, this value will be
				# overwritten ...
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
						previousOwnerCapital = ownerDateSortedDepositDf.loc[i - 1, DATAFRAME_HEADER_DEPOSIT_WITHDRAW]
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
		
		yieldOwnerSummaryTotals = self._computeYieldOwnerSummaryTotals(ownerDateSortedDepositDf)
		yieldOwnerDetailTotals = self._computeYieldOwnerDetailTotals(ownerDateSortedDepositDf)
		
		# adding TOTAL row to SB yield rates data frame for MERGED_SHEET_HEADER_EARNING_NEW_NAME column only
		sbYieldRatesDf.loc[DATAFRAME_HEADER_TOTAL] = sbYieldRatesDf[[MERGED_SHEET_HEADER_EARNING_NEW_NAME]].sum(numeric_only=True)

		return sbYieldRatesDf, yieldOwnerSummaryTotals, yieldOwnerDetailTotals
	
	def _computeCapitalYieldAmount(self,
	                               yieldRatesDataframe,
	                               capital,
	                               dateFrom,
	                               dateTo,
	                               yieldDayNumber):
		firstPaymentDate = dateFrom
		lastPaymentDate = dateTo
		yieldRatesDataframeSubSet = yieldRatesDataframe.loc[firstPaymentDate:lastPaymentDate]
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
	
	def _computeYieldOwnerSummaryTotals(self, depositsYieldsDataFrame):
		yieldOwnerSummaryTotals = depositsYieldsDataFrame.groupby([DEPOSIT_SHEET_HEADER_OWNER]).sum()[[DATAFRAME_HEADER_DEPOSIT_WITHDRAW, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]]
		yieldOwnerSummaryTotals.loc[DATAFRAME_HEADER_TOTAL] = yieldOwnerSummaryTotals.sum(numeric_only=True, axis=0)[[DATAFRAME_HEADER_DEPOSIT_WITHDRAW, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]]

		return yieldOwnerSummaryTotals
	
	def _computeYieldOwnerDetailTotals(self, depositsYieldsDataFrame):
		yieldOwnerDetailTotals = depositsYieldsDataFrame.copy()
		
		yieldOwnerDetailTotals.loc[DATAFRAME_HEADER_TOTAL] = depositsYieldsDataFrame.sum(numeric_only=True, axis=0)[
			[DATAFRAME_HEADER_DEPOSIT_WITHDRAW, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]]

		return yieldOwnerDetailTotals
