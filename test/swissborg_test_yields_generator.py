import pandas as pd
import numpy as np

dayNumber = 5

# generating day date list
dayDates = pd.date_range("2021-01-01", periods=dayNumber, freq="D")

capitalArray = [0.0] * dayNumber
capitalArray[0] = 19571.69

zeroYieldArray = [0.0] * dayNumber

DATE = 'DATE'
RATE = 'RATE'
CAPITAL = 'CAPITAL'
YIELD = 'YIELD'
TOTAL = 'TOTAL'

lastRowIdx = dayNumber - 1

def computeYields(df):
	for i in range(0, dayNumber):
		capital = df.loc[i, 'CAPITAL']
		capitalPlusYield = capital * df.loc[i, 'RATE']
		yieldAmount = capitalPlusYield - capital
		df.loc[i, YIELD] = yieldAmount
		if i < lastRowIdx:
			capitalBefore = df.loc[i + 1, CAPITAL]
			df.loc[i + 1, CAPITAL] = capitalBefore + capitalPlusYield

	df.loc[TOTAL] = df.sum(numeric_only=True, axis=0)[
		[YIELD]]

	return df.to_string(formatters={YIELD: '{:.10f}'.format}).replace('NaT', '   ').replace('NaN', '   ')

# generating an array of random values in the range of 1.15 - 1.25,
# i.e. returns between 15 % and 25 % per annum
randomYearlyInterestRates = np.random.uniform(low=1.15, high=1.25, size=(dayNumber))

# obtaining an array of corresponding daily interest rates which are 
# 365th root of a yearly interest rate
randomDailyInterestRates = np.power(randomYearlyInterestRates, 1/365)

dfRandom = pd.DataFrame({DATE: dayDates, CAPITAL: capitalArray, RATE: randomDailyInterestRates, YIELD: zeroYieldArray})

print('Random yields\n')		
print(computeYields(dfRandom))

fixedYearlyInterestRate = 1.2

# generating an array of fixed interest rate values
fixedYearlyInterestRates = [fixedYearlyInterestRate] * dayNumber

# obtaining an array of corresponding daily interest rates which are 
# 365th root of the yearly interest rate
fixedDailyInterestRates = np.power(fixedYearlyInterestRate, 1/365)

dfFixed = pd.DataFrame({DATE: dayDates, CAPITAL: capitalArray, RATE: fixedDailyInterestRates, YIELD: zeroYieldArray})

#print('\nFixed yield of {} % per year\n'.format(round((fixedYearlyInterestRate - 1) * 100)))
#print(computeYields(dfFixed))
