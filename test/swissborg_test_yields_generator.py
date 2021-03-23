import pandas as pd
import numpy as np

dayNumber = 5

# generating day date list
dayDates = pd.date_range("2021-01-01", periods=dayNumber, freq="D")

depWithdrArray = [0.0] * dayNumber
capitalArray = [0.0] * dayNumber

depWithdrArray[0] = 19571.69
depWithdrArray[2] = -19581.69

zeroYieldArray = [0.0] * dayNumber

DATE = 'DATE'
RATE = 'RATE'
DEPWITHDR = 'DEP/WITHDR'
CAPITAL = 'EARNING CAPITAL'
YIELD = 'YIELD'
TOTAL = 'TOTAL'

lastRowIdx = dayNumber - 1

def computeYields(df):
	for i in range(0, dayNumber):
		currentDepWithdr = df.loc[i, DEPWITHDR]
		if currentDepWithdr >= 0:
			currentCapital = df.loc[i, CAPITAL] + currentDepWithdr
			df.loc[i, CAPITAL] = currentCapital
			capitalPlusYield = currentCapital * df.loc[i, 'RATE']
			yieldAmount = capitalPlusYield - currentCapital
			df.loc[i, YIELD] = yieldAmount
			if i < lastRowIdx:
				df.loc[i + 1, CAPITAL] = capitalPlusYield
		else:
			currentCapital = df.loc[i, CAPITAL]
			capitalPlusYield = currentCapital * df.loc[i, 'RATE']
			yieldAmount = capitalPlusYield - currentCapital
			df.loc[i, YIELD] = yieldAmount
			if i < lastRowIdx:
				# in case of withdrawal, the witdrawn amount continues to generate revenue
				# during the withdrawal date ! So, the capital amount minus the withdrawal
				# amount is set to the next day (next row).
				df.loc[i + 1, CAPITAL] = capitalPlusYield + currentDepWithdr

	df.loc[TOTAL] = df.sum(numeric_only=True, axis=0)[
		[YIELD]]

	return df.to_string(formatters={YIELD: '{:.10f}'.format}).replace('NaT', '   ').replace('NaN', '   ')

# generating an array of random values in the range of 1.15 - 1.25,
# i.e. returns between 15 % and 25 % per annum
randomYearlyInterestRates = np.random.uniform(low=1.15, high=1.25, size=(dayNumber))

# obtaining an array of corresponding daily interest rates which are 
# 365th root of a yearly interest rate
randomDailyInterestRates = np.power(randomYearlyInterestRates, 1/365)

dfRandom = pd.DataFrame({DATE: dayDates, DEPWITHDR: depWithdrArray, CAPITAL: capitalArray, RATE: randomDailyInterestRates, YIELD: zeroYieldArray})

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
