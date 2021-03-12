import numpy as np
import pandas as pd

from sbyieldratecomputer import *

class SBDepositYieldComputer:
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
		self.configMgr = configMgr
		self.sbYieldRateComputer = sbYieldRateComputer

	def computeDepositsYields(self, yieldCrypto):
		depositDf, yieldRatesDataframe = self.sbYieldRateComputer.getDepositsAndDailyYieldRatesDataframes(yieldCrypto)
		
		# sorting deposits by owner and by deposit date
		sortedDepositDF = depositDf.sort_values([DEPOSIT_SHEET_HEADER_OWNER, DEPOSIT_SHEET_HEADER_DATE], axis=0)

		return sortedDepositDF