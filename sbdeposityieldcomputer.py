from datetime import timedelta
from sbyieldratecomputer import *
from pandasdatacomputer import PandasDataComputer
from invaliddepositdateerror import InvalidDepositDateError

DEPOSIT_YIELD_HEADER_INDEX = 'IDX'
DEPOSIT_YIELD_HEADER_CAPITAL = 'CAPITAL'
DEPOSIT_YIELD_HEADER_DEPOSIT_WITHDRAW = MERGED_SHEET_HEADER_DEPOSIT_WITHDRAW
DEPOSIT_YIELD_HEADER_DATE_FROM = 'FROM'
DEPOSIT_YIELD_HEADER_DATE_TO = 'TO'
DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER = 'YIELD DAY NB'
DEPOSIT_YIELD_HEADER_YIELD_AMOUNT = 'YIELD AMOUNT'


class SBDepositYieldComputer(PandasDataComputer):
	"""
	This class loads the Swissborg account statement xlsl sheet and the Deposit/Withdrawal
	csv files.
	
	It merges the two files, creating a Pandas data frame containing computed data used
	later to distribute the earnings according to the deposits/withdrawals.
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
		
		Can raise InvalidDepositDateError in case the deposit csv file contains a deposi or withdrawal
		whose date is after the last Swissborg yield payment date.
		"""
		depositDf, yieldRatesDataframe = self.sbYieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)

		# sorting deposits by owner and by deposit date
		modifiedDepositDf = depositDf.sort_values([DEPOSIT_SHEET_HEADER_OWNER, DEPOSIT_SHEET_HEADER_DATE], axis=0)
		
		# replace DATE index with integer index
		modifiedDepositDf = self._replaceDateIndexByIntIndex(modifiedDepositDf, DEPOSIT_SHEET_HEADER_DATE, DEPOSIT_YIELD_HEADER_INDEX)

		# insert CAPITAL column
		self._insertEmptyFloatColumns(modifiedDepositDf,
		                              2,
		                              [DEPOSIT_YIELD_HEADER_CAPITAL])

		# rename date column
		modifiedDepositDf = modifiedDepositDf.rename(columns={DEPOSIT_SHEET_HEADER_DATE: DEPOSIT_YIELD_HEADER_DATE_FROM})

		# remove time component
		modifiedDepositDf[DEPOSIT_YIELD_HEADER_DATE_FROM] = pd.to_datetime(modifiedDepositDf[DEPOSIT_YIELD_HEADER_DATE_FROM]).dt.date

		# insert empty columns
		self._appendEmptyColumns(modifiedDepositDf,
		                         [DEPOSIT_YIELD_HEADER_DATE_TO, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER])

		self._insertEmptyFloatColumns(modifiedDepositDf, None, [DEPOSIT_YIELD_HEADER_YIELD_AMOUNT])

		currentOwner = None
		currentCapital = 0
		firstYieldTimeStamp = yieldRatesDataframe.index[0]
		firstYieldDate = firstYieldTimeStamp.date()
		lastYieldTimeStamp = yieldRatesDataframe.index[-1]
		lastYieldDate = lastYieldTimeStamp.date()
		maxIdxValue = len(modifiedDepositDf)
		
		# compute date to and yield day number
		for i in range(1, maxIdxValue + 1):
			if modifiedDepositDf.loc[i, DEPOSIT_SHEET_HEADER_OWNER]	!= currentOwner:
				currentOwner = modifiedDepositDf.loc[i, DEPOSIT_SHEET_HEADER_OWNER]
				currentCapital = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DEPOSIT_WITHDRAW]
				modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL] = currentCapital
				dateFrom = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
				dateFromMinusFirstYieldDateTimeDelta = dateFrom - firstYieldDate
				if dateFromMinusFirstYieldDateTimeDelta.days == -1:
					# the case if the current deposit is the oldest or very first deposit deposit
					dateFrom = dateFrom + timedelta(days=1)
					modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM] = dateFrom
				if i > 1:
					if i == maxIdxValue:
						# setting yield date to as well as yield day number
						modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldDate
						dateToMinusDateFromTimeDelta = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] - \
						                               modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
						yieldDayNumber = dateToMinusDateFromTimeDelta.days
						if yieldDayNumber < 0:
							raise InvalidDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
							                              currentOwner,
							                              modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM],
							                              modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DEPOSIT_WITHDRAW],
							                              lastYieldDate)
						modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
					else:
						# here, the owner has changed. This means that the previous owner capital
						# remains the same till the end of SB yield earnings
						
						# setting yield date to as well as yield day number
						modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldDate
						dateToMinusDateFromTimeDelta = modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO] - \
						                               modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM]
						yieldDayNumber = dateToMinusDateFromTimeDelta.days
						if yieldDayNumber < 0:
							raise InvalidDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
							                              modifiedDepositDf.loc[i - 1, DEPOSIT_SHEET_HEADER_OWNER],
							                              modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM],
							                              modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DEPOSIT_WITHDRAW],
							                              lastYieldDate)
						modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
			else:
				currentCapital = currentCapital + modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DEPOSIT_WITHDRAW]
				modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL] = currentCapital
				
				# setting yield date to as well as yield day number for previous line
				modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO] = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
				dateToMinusDateFromTimeDelta = modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_TO] - \
				                               modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_DATE_FROM]
				
				# here, yieldDayNumber can not be negative since the deposits/withdrawals are sorted by owner
				# and then by deposit date ! So, for the same owner, previous deposit date to is set to current
				# deposit date from which is greater than previous deposit date from (see deposit csv file
				# comment for justification)
				yieldDayNumber = dateToMinusDateFromTimeDelta.days
				modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber

				# setting yield date to as well as yield day number for current line
				modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldDate
				dateToMinusDateFromTimeDelta = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] - \
				                               modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
				yieldDayNumber = dateToMinusDateFromTimeDelta.days
				if yieldDayNumber < 0:
					raise InvalidDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
					                              currentOwner,
					                              modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM],
					                              modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DEPOSIT_WITHDRAW],
					                              lastYieldDate)
				modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber

		# finally, compute the yield amount
		for i in range(1, maxIdxValue + 1):
			dateFrom = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
			dateTo = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO]
			capital = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL]
			yieldAmount = self._computeYieldAmount(yieldRatesDataframe, capital, dateFrom, dateTo)
			modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_AMOUNT] = yieldAmount
			
		return modifiedDepositDf
	
	def _computeYieldAmount(self, yieldRatesDataframe, capital, dateFrom, dateTo):
		yieldRatesDataframeSubSet = yieldRatesDataframe.loc[dateFrom:dateTo]
		capitalPlusYield = capital
		
		for index, values in yieldRatesDataframeSubSet.iterrows():
			yieldRate = values[0]
			capitalPlusYield = capitalPlusYield * yieldRate
		
		return capitalPlusYield - capital
