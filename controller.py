import os,sys,inspect

from configmanager import ConfigManager
from processor import Processor
from sbyieldratecomputer import SByieldRateComputer
from sbdeposityieldcomputer import SBDepositYieldComputer

class Controller:
	def __init__(self):
		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
		else:
			configPath = 'c:\\temp\\sbyield.ini'

		configMgr = ConfigManager(configPath)
		self.sbYieldRateComputer = SByieldRateComputer(configMgr)
		self.sbDepositYieldComputer = SBDepositYieldComputer(configMgr, self.sbYieldRateComputer)

		self.processor = Processor(configMgr)
