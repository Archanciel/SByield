class Processor:
	def __init__(self,
	             configMgr,
	             sbYieldRateComputer,
	             ownerDepositYieldComputer):
		self.configMgr = configMgr
		self.sbYieldRateComputer = sbYieldRateComputer
		self.ownerDepositYieldComputer = ownerDepositYieldComputer
	
	def computeYield(self, yieldCrypto):
		return self.ownerDepositYieldComputer.computeDepositsYields(yieldCrypto)
