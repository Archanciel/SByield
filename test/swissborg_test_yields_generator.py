import pandas as pd
import numpy as np

RANDOM_YIELD_RATE_LOW = 1.15
RANDOM_YIELD_RATE_HIGH = 1.25

dayNumber = 5

# generating day date list
dayDates = pd.date_range("2021-01-01", periods=dayNumber, freq="D")

depWithdrArray = [0.0] * dayNumber
capitalArray = [0.0] * dayNumber

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
depWithdrArray[0] = 30000

zeroYieldArray = [0.0] * dayNumber

DATE = 'DATE'
RATE_DAILY = 'D RATE'
RATE_YEARLY = 'Y RATE'
DEPWITHDR = 'DEP/WITHDR'
CAPITAL = 'EARNING CAPITAL'
YIELD_DAILY = 'D YIELD'
YIELD_SUM = 'YIELD SUM'
TOTAL = 'TOTAL'

def computeYields(df):
	lastRowIdx = dayNumber - 1
	yieldSum = 0.0
	
	for i in range(0, dayNumber):
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
			capitalPlusYield = currentCapital * df.loc[i, RATE_DAILY]
			yieldAmount = capitalPlusYield - currentCapital
			df.loc[i, YIELD_DAILY] = yieldAmount
			if i < lastRowIdx:
				# in case of withdrawal, the witdrawn amount continues to generate revenue
				# during the withdrawal date ! So, the capital amount minus the withdrawal
				# amount is set to the next day (next row).
				df.loc[i + 1, CAPITAL] = capitalPlusYield + currentDepWithdr
		yieldSum += yieldAmount
		df.loc[i, YIELD_SUM] = yieldSum

	df.loc[TOTAL] = df.sum(numeric_only=True, axis=0)[
		[YIELD_DAILY]]

	return df.to_string(formatters={RATE_DAILY: '{:.8f}'.format, YIELD_DAILY: '{:.14f}'.format, YIELD_SUM: '{:.14f}'.format}).replace('NaT', '   ').replace('NaN', '   ')

# generating an array of random values in the range of 1.15 - 1.25,
# i.e. returns between 15 % and 25 % per annum
randomYearlyInterestRates = np.random.uniform(low=RANDOM_YIELD_RATE_LOW, high=RANDOM_YIELD_RATE_HIGH, size=(dayNumber))

# obtaining an array of corresponding daily interest rates which are 
# 365th root of a yearly interest rate
randomDailyInterestRates = np.power(randomYearlyInterestRates, 1/365)

dfRandom = pd.DataFrame({DATE: dayDates, DEPWITHDR: depWithdrArray, CAPITAL: capitalArray, RATE_YEARLY: randomYearlyInterestRates, RATE_DAILY: randomDailyInterestRates, YIELD_DAILY: zeroYieldArray, YIELD_SUM: zeroYieldArray})

print('Random yields\n')		
print(computeYields(dfRandom))

fixedYearlyInterestRate = 1.2

# generating an array of fixed interest rate values
fixedYearlyInterestRates = [fixedYearlyInterestRate] * dayNumber

# obtaining an array of corresponding daily interest rates which are 
# 365th root of the yearly interest rate
fixedDailyInterestRates = np.power(fixedYearlyInterestRate, 1/365)

dfFixed = pd.DataFrame({DATE: dayDates, DEPWITHDR: depWithdrArray, CAPITAL: capitalArray, RATE_YEARLY: fixedYearlyInterestRates,  RATE_DAILY: fixedDailyInterestRates, YIELD_DAILY: zeroYieldArray})

#print('\nFixed yield of {} % per year\n'.format(round((fixedYearlyInterestRate - 1) * 100)))
#print(computeYields(dfFixed))
