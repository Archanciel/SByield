import math

class CompositeInterestComputer:
	@staticmethod
	def fiatSmartYieldResults(capital,
	                          yearlyRatePercent,
	                          withdrawCostPercent,
	                          withdrawCostMinAmount,
	                          withdrawCostMaxAmount):
		dailyYieldRate = pow(1 + yearlyRatePercent / 100, 1/365)
		withdrawCost = min(max(capital * withdrawCostPercent / 100, withdrawCostMinAmount), withdrawCostMaxAmount)
		withdrawCostCompensationYieldDayNumber = math.ceil(math.log10((capital + withdrawCost) / capital) / math.log10(dailyYieldRate))
		dailyYield = (dailyYieldRate * capital) - capital
		monthlyYield = (pow(dailyYieldRate, 30) * capital) - capital
		yearlyYield = (pow(dailyYieldRate, 365) * capital) - capital
		
		return (withdrawCostCompensationYieldDayNumber,
		        dailyYield,
		        monthlyYield,
		        yearlyYield)
		
if __name__ == '__main__':
	capital = 1000
	yieldRatePercent = 11
	withdrawCostPercent = 0.1
	withdrawCostMinAmount = 4.5
	withdrawCostMaxAmount = 110
	
	print("\ncapital {} CHF,yieldRate {} %,withdraw cost {} %, min {} CHF, max {} CHF".format(
		capital,
		yieldRatePercent,
		withdrawCostPercent,
		withdrawCostMinAmount,
		withdrawCostMaxAmount,
		withdrawCostMaxAmount
	))
	
	resultTuple = CompositeInterestComputer.fiatSmartYieldResults(capital,
	                                                              yieldRatePercent,
	                                                              withdrawCostPercent,
	                                                              withdrawCostMinAmount,
	                                                              withdrawCostMaxAmount)
	                                                              
	formattedDailyYieldStr = "{:.2f}".format(round(resultTuple[1], 2))
	formattedMonthlyYieldStr = "{:.2f}".format(round(resultTuple[2], 2))
	formattedYearlyYieldStr = "{:.2f}".format(round(resultTuple[3], 2))
	
	print("min days {}, revenue daily {}, monthly {}, yearly {}".format(resultTuple[0],
	                                                                   formattedDailyYieldStr,
	                                                                   formattedMonthlyYieldStr,
	                                                                   formattedYearlyYieldStr))
