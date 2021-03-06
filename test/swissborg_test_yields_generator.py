import pandas as pd
import numpy as np

GENERATE_XLSV_FILE = True
RANDOM_YEARLY_YIELD_RATE_LOW = 1.15
RANDOM_YEARLY_YIELD_RATE_HIGH = 1.25

# generating excel data for
# testDepositUsdc_uniqueOwner_1_deposit_1_almost_full_withdr_fixed_yield_rate_3_yield_days.csv
'''
OWNER,DATE,DEP/WITHDR
JPS,2021/01/01 00:00:00,1000
JPS,2021/01/03 00:00:00,-1001
'''
# FIXED_YEARLY_YIELD_RATE = np.power(1.001, 365)
# dayNumber = 3
# depWithdrArray = [0.0] * dayNumber
# depWithdrArray[0] = 1000
# depWithdrArray[2] = -1001

# generating excel data for testDepositUsdc_uniqueOwner_1_deposit_1_almost_full_withdr_fixed_yield_rate.csv
FIXED_YEARLY_YIELD_RATE = 1.1
TEST_DATA_PATH = 'D:\\Development\\Python\\SByield\\test\\testData\\'

dayNumber = 211
yearNumber = 1
depWithdrArray = [0.0] * ((dayNumber * yearNumber) + 1)


# generating day date list
dayDates = pd.date_range("2021-01-01", periods=((dayNumber * yearNumber) + 1), freq="D")

# daily yield withdrawal --> TOTAL == 953.22624764737157
#TOTAL_WITHDR = 'TOTAL DAILY WITHDRAWALS'
#depWithdrArray = [-2.61157876067773] * ((dayNumber * yearNumber) + 1)

# monthly yield withdrawal --> TOTAL == 957.98000736447830
# idx = 29
# withdrawAmount = -78.64477220619301
# TOTAL_WITHDR = 'TOTAL MONTHLY WITHDRAWALS'
#
# for i in range(12 * yearNumber):
# 	print('i = {}, index = {}, date = {}, withdrawal = {}'.format(i, idx, dayDates[idx], withdrawAmount))
# 	depWithdrArray[idx] = withdrawAmount
# 	idx += 30

# idx = 365
# withdrawAmount = -1002.61089670860747
TOTAL_WITHDR = 'TOTAL YEARLY WITHDRAWALS'
#
# for i in range(yearNumber):
# 	print('i = {}, index = {}, date = {}, withdrawal = {}'.format(i, idx, dayDates[idx], withdrawAmount))
# 	depWithdrArray[idx] = withdrawAmount
# 	idx += 365

depWithdrArray[0] = 11000
depWithdrArray[1] = 5000
# depWithdrArray[59] = -1000
# depWithdrArray[120] = -500
# depWithdrArray[151] = -500
# depWithdrArray[181] = -1000
#depWithdrArray[304] = -22531

xlsxFilePathName = TEST_DATA_PATH + 'GENERATED_testDepositCHSB_simple_values_2_owners_1_and_2_deposits_1_day_diff.xlsx'

capitalArray = [0.0] * ((dayNumber * yearNumber) + 1)

# WARNING: THE ARRAY MUST BE COHERENT WITH THE DEPOSIT/WITHDR DEFINED IN THE
# CORRESPONDING DEPOSIT CSV FILE !!!
'''
Depost and withdrawal example:

deposit.csv file

OWNER,DATE,DEP/WITHDR
JPS,2021/01/01 00:00:00,20000
JPS,2021/01/04 00:00:00,-10000

depWithdrArray corresponding setting

depWithdrArray[0] = 20000   # 2021/01/01
depWithdrArray[2] = -10000  # 2021/01/03

generated data

            DATE  DEP/WITHDR  EARNING CAPITAL    Y RATE    D RATE           D YIELD         YIELD SUM
0     2021-01-01     20000.0     20000.000000  1.204476  1.000510 10.19682672353156 10.19682672353156
1     2021-01-02         0.0     20010.196827  1.194205  1.000486  9.73227507534466 19.92910179887622
2     2021-01-03    -10000.0     20019.929102  1.208457  1.000519 10.38806214595388 30.31716394483010
3     2021-01-04         0.0     10030.317164  1.193944  1.000486  4.87240283804931 35.18956678287941
4     2021-01-05         0.0     10035.189567  1.191480  1.000480  4.81793888522043 40.00750566809984
TOTAL                                                             40.00750566809984
'''

zeroYieldArray = [0.0] * ((dayNumber * yearNumber) + 1)

DATE = 'DATE'
RATE_DAILY = 'D RATE'
RATE_YEARLY = 'Y RATE'
DEPWITHDR = 'DEP/WITHDR'
CAPITAL = 'EARNING CAPITAL'
YIELD_DAILY = 'D YIELD'
YIELD_SUM = 'YIELD SUM'
TOTAL = 'TOTAL YIELD'

def computeYields(df):
	lastRowIdx = (dayNumber * yearNumber)
	yieldSum = 0.0
	
	for i in range(0, (dayNumber * yearNumber) + 1):
		currentDepWithdr = df.loc[i, DEPWITHDR]
		if currentDepWithdr >= 0:
			# handling a deposit
			currentCapital = df.loc[i, CAPITAL] + currentDepWithdr
			df.loc[i, CAPITAL] = currentCapital
			capitalPlusYield = currentCapital * df.loc[i, RATE_DAILY]
			yieldAmount = capitalPlusYield - currentCapital
			df.loc[i, YIELD_DAILY] = yieldAmount
			if i < lastRowIdx:
				df.loc[i + 1, CAPITAL] = capitalPlusYield
		else:
			# handling a withdrawal
			currentCapital = df.loc[i, CAPITAL]
			currentCapital = currentCapital + currentDepWithdr
			capitalPlusYield = currentCapital * df.loc[i, RATE_DAILY]
			yieldAmount = capitalPlusYield - currentCapital
			df.loc[i, YIELD_DAILY] = yieldAmount
			if i < lastRowIdx:
				# in case of withdrawal, the withdrawn amount continues to generate revenue
				# during the withdrawal date ! So, the capital amount minus the withdrawal
				# amount is set to the next day (next row).
				df.loc[i, CAPITAL] = capitalPlusYield

#				df.loc[i + 1, CAPITAL] = capitalPlusYield * df.loc[i + 1, RATE_DAILY]

				# required if daily yield is withdrawn every day. Otherwise, computation is not correct
				df.loc[i + 1, CAPITAL] = (capitalPlusYield + df.loc[i + 1, DEPWITHDR]) * df.loc[i + 1, RATE_DAILY]
			elif i == lastRowIdx:
				df.loc[i, CAPITAL] = capitalPlusYield

		yieldSum += yieldAmount
		df.loc[i, YIELD_SUM] = yieldSum

	df.loc[TOTAL] = df.sum(numeric_only=True, axis=0)[
		[YIELD_DAILY]]
	df.loc[TOTAL_WITHDR] = df.iloc[:,1:2].where(df.iloc[:,1:2] < 0).sum()

	return df,\
		   df.to_string(formatters={RATE_DAILY: '{:.8f}'.format, YIELD_DAILY: '{:.14f}'.format, YIELD_SUM: '{:.14f}'.format}).replace('NaT', '   ').replace('NaN', '   ').replace('nan', '   ')

# generating an array of random values in the range of 1.15 - 1.25,
# i.e. returns between 15 % and 25 % per annum
randomYearlyInterestRates = np.random.uniform(low=RANDOM_YEARLY_YIELD_RATE_LOW, high=RANDOM_YEARLY_YIELD_RATE_HIGH, size=(dayNumber * yearNumber) + 1)

# obtaining an array of corresponding daily interest rates which are 
# 365th root of a yearly interest rate
randomDailyInterestRates = np.power(randomYearlyInterestRates, 1/365)

dfRandom = pd.DataFrame({DATE: dayDates, DEPWITHDR: depWithdrArray, CAPITAL: capitalArray, RATE_YEARLY: randomYearlyInterestRates, RATE_DAILY: randomDailyInterestRates, YIELD_DAILY: zeroYieldArray, YIELD_SUM: zeroYieldArray})

#print('Random yields\n')
#print(computeYields(dfRandom))

# generating an array of fixed interest rate values
fixedYearlyInterestRates = [FIXED_YEARLY_YIELD_RATE] * ((dayNumber * yearNumber) + 1)

# obtaining an array of corresponding daily interest rates which are 
# 365th root of the yearly interest rate
fixedDailyInterestRates = np.power(FIXED_YEARLY_YIELD_RATE, 1 / 365)

dfFixed = pd.DataFrame({DATE: dayDates, DEPWITHDR: depWithdrArray, CAPITAL: capitalArray, RATE_YEARLY: fixedYearlyInterestRates,  RATE_DAILY: fixedDailyInterestRates, YIELD_DAILY: zeroYieldArray})

if GENERATE_XLSV_FILE:
	dfFixed, _ = computeYields(dfFixed)
	dfFixed.to_excel(xlsxFilePathName)
	print(xlsxFilePathName + ' created')
else:
	print('\nFixed yield of {} % per year\n'.format(round((FIXED_YEARLY_YIELD_RATE - 1) * 100)))
	dfFixed, dfFixedStr = computeYields(dfFixed)
	print(dfFixedStr)