import math

class CompositeInterestComputer:
	@staticmethod
	def computeDayNumber(capital, yearlyRatePercent, withdrawCostPercent, withdrawCostMinimum, withdrawCostMaximum):
		daylyRate = pow(1 + yearlyRatePercent / 100, 1/365)
		withdrawCost = min(max(capital * withdrawCostPercent / 100,withdrawCostMinimum), withdrawCostMaximum)
		dayNumber = math.log10((capital + withdrawCost) / capital) / math.log10(daylyRate)
		
		return math.ceil(dayNumber)
		
if __name__ == '__main__':
	print(CompositeInterestComputer.computeDayNumber(800, 10.5, 0.1, 4.5, 110))