import math

class CompositeInterestComputer:
	@staticmethod
	def fiatSmartYieldResults(capital,
	                          yearlyRatePercent,
	                          withdrawCostPercent,
	                          withdrawCostMinAmount,
	                          withdrawCostMaxAmount,
	                          yearNb):
		dailyYieldRate = CompositeInterestComputer.calcDailyRate(yearlyRatePercent)
		withdrawCost = min(max(capital * withdrawCostPercent / 100, withdrawCostMinAmount), withdrawCostMaxAmount)
		withdrawCostCompensationYieldDayNumber = math.ceil(math.log10((capital + withdrawCost) / capital) / math.log10(dailyYieldRate))
		dailyYield = (dailyYieldRate * capital) - capital
		weeklyYield = (pow(dailyYieldRate, 7) * capital) - capital
		monthlyYield = (pow(dailyYieldRate, 30) * capital) - capital
		yearlyYield = (pow(dailyYieldRate, 365) * capital) - capital
		
		finalCapitalLst = []
		
		for year in range(1, yearNb + 1):
			finalCapitalLst.append(pow(dailyYieldRate, 365 * year) * capital)
		
		return (withdrawCostCompensationYieldDayNumber,
		        dailyYield,
		        weeklyYield,
		        monthlyYield,
		        yearlyYield) + tuple(finalCapitalLst)
	
	@staticmethod
	def calcDailyRate(yearlyRatePercent):
		return pow(1 + yearlyRatePercent / 100, 1 / 365)


if __name__ == '__main__':
	withdrawCostPercent = 0.1
	withdrawCostMinAmount = 4.5
	withdrawCostMaxAmount = 110
	
	input = input('Enter capital, yearly yield % and year number ')
	inputLst = input.split(' ')
	
	capital = float(inputLst[0])
	yieldRatePercent = float(inputLst[1])
	yearNb = int(inputLst[2])
	formattedCapital = (f"{capital:,}")
	
	print("\ncapital {} CHF, yieldRate {} %,\nwithdraw cost {} %, min {}/max {} CHF".format(
		formattedCapital,
		yieldRatePercent,
		withdrawCostPercent,
		withdrawCostMinAmount,
		withdrawCostMaxAmount
	))
	
	resultTuple = CompositeInterestComputer.fiatSmartYieldResults(capital,
	                                                              yieldRatePercent,
	                                                              withdrawCostPercent,
	                                                              withdrawCostMinAmount,
	                                                              withdrawCostMaxAmount,
	                                                              yearNb)
	                                                              
	formattedDailyYieldStr = "{:,.2f}".format(resultTuple[1])
	formattedWeeklyYieldStr = "{:,.2f}".format(resultTuple[2])
	formattedMonthlyYieldStr = "{:,.2f}".format(resultTuple[3])
	formattedYearlyYieldStr = "{:,.2f}".format(resultTuple[4])
	
	formattedFinalCapitalStrLst = ["{:,.2f}".format(x) for x in resultTuple[5:]]

	print("min days {}".format(resultTuple[0]))
	print("\nrevenues\n  daily {}".format(formattedDailyYieldStr))
	print("  weekly {}".format(formattedWeeklyYieldStr))
	print("  monthly {}".format(formattedMonthlyYieldStr))
	print("  yearly {}".format(formattedYearlyYieldStr))
	print("\nfinal capital and yearly revenue after year")
	
	year = 1
	
	for formattedFinalCapitalStr in formattedFinalCapitalStrLst:
		print("  {}: {}".format(year, formattedFinalCapitalStr))
		year += 1