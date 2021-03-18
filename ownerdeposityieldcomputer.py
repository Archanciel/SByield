from datetime import timedelta
from sbyieldratecomputer import *
from pandasdatacomputer import PandasDataComputer
from invaliddepositdateerror import InvalidDepositDateError

DEPOSIT_YIELD_HEADER_CAPITAL = 'CAPITAL'
DEPOSIT_YIELD_HEADER_DATE_FROM = 'FROM'
DEPOSIT_YIELD_HEADER_DATE_TO = 'TO'
DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER = 'YIELD DAYS'
DEPOSIT_YIELD_HEADER_YIELD_AMOUNT = 'YIELD AMOUNT'


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
		depositDf, yieldRatesDataframe = self.sbYieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)

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

		self._insertEmptyFloatColumns(ownerDateSortedDepositDf, None, [DEPOSIT_YIELD_HEADER_YIELD_AMOUNT])

		currentOwner = None
		currentCapital = 0
		firstYieldTimeStamp = yieldRatesDataframe.index[0]
		firstYieldDate = firstYieldTimeStamp.date()
		lastYieldTimeStamp = yieldRatesDataframe.index[-1]
		lastYieldPaymentDate = lastYieldTimeStamp.date()
		maxIdxValue = len(ownerDateSortedDepositDf)

		print(self.getDataframeStrWithFormattedColumns(yieldRatesDataframe,
		                                               {MERGED_SHEET_HEADER_YIELD_RATE: '.11f'}))
		print(self.getDataframeStrWithFormattedColumns(ownerDateSortedDepositDf,
		                                               {DATAFRAME_HEADER_DEPOSIT_WITHDRAW: '.2f',
		                                               DEPOSIT_YIELD_HEADER_YIELD_AMOUNT: '.8f'}))

		# compute capital, date to and yield day number
		for i in range(1, maxIdxValue + 1):
			if ownerDateSortedDepositDf.loc[i, DEPOSIT_SHEET_HEADER_OWNER]	!= currentOwner:
				currentOwner = ownerDateSortedDepositDf.loc[i, DEPOSIT_SHEET_HEADER_OWNER]
				currentCapital = ownerDateSortedDepositDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW]
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL] = currentCapital
				if i > 1:
					if i == maxIdxValue:
						# setting yield date to as well as yield day number
						ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldPaymentDate
						dateToMinusDateFromTimeDelta = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] - \
						                               ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
						yieldDayNumber = dateToMinusDateFromTimeDelta.days
						if yieldDayNumber < 0:
							raise InvalidDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
							                              currentOwner,
							                              ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM],
							                              ownerDateSortedDepositDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW],
							                              lastYieldPaymentDate)
						ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
					else:
						# here, the owner has changed. This means that the previous owner capital
						# remains the same till the end of SB yield earning payments
						
						# setting yield date to as well as yield day number for previous owner
						ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldPaymentDate
						dateToMinusDateFromTimeDelta = ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO] - \
						                               ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM]
						yieldDayNumber = dateToMinusDateFromTimeDelta.days
						if yieldDayNumber < 0:
							raise InvalidDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
							                              ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_SHEET_HEADER_OWNER],
							                              ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM],
							                              ownerDateSortedDepositDf.loc[i - 1, DATAFRAME_HEADER_DEPOSIT_WITHDRAW],
							                              lastYieldPaymentDate)
						ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
			else:
				# handling additional deposits for current owner
				currentCapital = currentCapital + ownerDateSortedDepositDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW]
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL] = currentCapital
				
				# setting yield date to as well as yield day number for previous line
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO] = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
				dateToMinusDateFromTimeDelta = ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO] - \
				                               ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM]
				
				# here, yieldDayNumber can not be negative since the deposits/withdrawals are sorted by owner
				# and then by deposit date ! So, for the same owner, previous deposit date to is set to current
				# deposit date from which is greater than previous deposit date from (see deposit csv file
				# comment for justification)
				yieldDayNumber = dateToMinusDateFromTimeDelta.days
				ownerDateSortedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber

				# setting yield date to as well as yield day number for current line
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldPaymentDate
				dateToMinusDateFromTimeDelta = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] - \
				                               ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
				yieldDayNumber = dateToMinusDateFromTimeDelta.days
				if yieldDayNumber < 0:
					raise InvalidDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
					                              currentOwner,
					                              ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM],
					                              ownerDateSortedDepositDf.loc[i, DATAFRAME_HEADER_DEPOSIT_WITHDRAW],
					                              lastYieldPaymentDate)
				ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber

		# finally, compute the yield amount
		for i in range(1, maxIdxValue + 1):
			dateFrom = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
			dateTo = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO]
			capital = ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL]
			yieldAmount = self._computeYieldAmount(yieldRatesDataframe, capital, dateFrom, dateTo)
			ownerDateSortedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = yieldAmount
		
		yieldOwnerSummaryTotals = self._computeYieldOwnerSummaryTotals(ownerDateSortedDepositDf)
		yieldOwnerDetailTotals = self._computeYieldOwnerDetailTotals(ownerDateSortedDepositDf)
		
		return ownerDateSortedDepositDf, yieldOwnerSummaryTotals, yieldOwnerDetailTotals
	
	def _computeYieldAmount(self, yieldRatesDataframe, capital, dateFrom, dateTo):
		yieldRatesDataframeSubSet = yieldRatesDataframe.loc[dateFrom:dateTo]
		capitalPlusYield = capital
		
		for index, values in yieldRatesDataframeSubSet.iterrows():
			yieldRate = values[0]
			capitalPlusYield = capitalPlusYield * yieldRate
		
		return capitalPlusYield - capital
	
	def _computeYieldOwnerSummaryTotals(self, depositsYieldsDataFrame):
		yieldOwnerSummaryTotals = depositsYieldsDataFrame.groupby([DEPOSIT_SHEET_HEADER_OWNER]).sum()[[DATAFRAME_HEADER_DEPOSIT_WITHDRAW, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]]
		yieldOwnerSummaryTotals.loc[DATAFRAME_HEADER_TOTAL] = yieldOwnerSummaryTotals.sum(numeric_only=True, axis=0)[[DATAFRAME_HEADER_DEPOSIT_WITHDRAW, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]]

		return yieldOwnerSummaryTotals
	
	def _computeYieldOwnerDetailTotals(self, depositsYieldsDataFrame):
		yieldOwnerDetailTotals = depositsYieldsDataFrame.copy()
		yieldOwnerDetailTotals.loc[DATAFRAME_HEADER_TOTAL] = depositsYieldsDataFrame.sum(numeric_only=True, axis=0)[
			[DATAFRAME_HEADER_DEPOSIT_WITHDRAW, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT]]

		return yieldOwnerDetailTotals.fillna('').to_string(index=False)
