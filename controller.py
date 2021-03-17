import os,sys,inspect

from configmanager import ConfigManager
from processor import Processor
from sbyieldratecomputer import SBYieldRateComputer
from ownerdeposityieldcomputer import OwnerDepositYieldComputer

class Controller:
	def __init__(self):
		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
		else:
			configPath = 'c:\\temp\\sbyield.ini'

		configMgr = ConfigManager(configPath)
		self.sbYieldRateComputer = SBYieldRateComputer(configMgr)
		self.sbDepositYieldComputer = OwnerDepositYieldComputer(configMgr, self.sbYieldRateComputer)

		self.processor = Processor(configMgr)
