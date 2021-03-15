from sbyieldratecomputer import *
from pandasdatacomputer import PandasDataComputer
from toolatedepositdateerror import TooLateDepositDateError

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
		lastYieldTimeStamp = yieldRatesDataframe.index[-1]
		lastYieldDate = lastYieldTimeStamp.date()
		maxIdxValue = len(modifiedDepositDf)
		for i in range(1, maxIdxValue + 1):
			if modifiedDepositDf.loc[i, DEPOSIT_SHEET_HEADER_OWNER]	!= currentOwner:
				currentOwner = modifiedDepositDf.loc[i, DEPOSIT_SHEET_HEADER_OWNER]
				currentCapital = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DEPOSIT_WITHDRAW]
				modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_CAPITAL] = currentCapital

				if i > 1:
					if i == maxIdxValue:
						# setting yield date to as well as yield day number
						modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldDate
						dateToMinusDateFromTimeDelta = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] - \
						                               modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
						yieldDayNumber = dateToMinusDateFromTimeDelta.days
						if yieldDayNumber < 0:
							raise TooLateDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
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
							raise TooLateDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
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
				yieldDayNumber = dateToMinusDateFromTimeDelta.days
				if yieldDayNumber < 0:
					raise TooLateDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
					                              currentOwner,
					                              modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM],
					                              modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DEPOSIT_WITHDRAW],
					                              lastYieldDate)
				modifiedDepositDf.loc[i - 1, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber

				# setting yield date to as well as yield day number for current line
				modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] = lastYieldDate
				dateToMinusDateFromTimeDelta = modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_TO] - \
				                               modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM]
				yieldDayNumber = dateToMinusDateFromTimeDelta.days
				if yieldDayNumber < 0:
					raise TooLateDepositDateError(self.sbYieldRateComputer.depositSheetFilePathName,
					                              currentOwner,
					                              modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DATE_FROM],
					                              modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_DEPOSIT_WITHDRAW],
					                              lastYieldDate)
				modifiedDepositDf.loc[i, DEPOSIT_YIELD_HEADER_YIELD_DAY_NUMBER] = yieldDayNumber
		
		return modifiedDepositDf
