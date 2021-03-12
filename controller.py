import os,sys,inspect

from configmanager import ConfigManager
from processor import Processor
from sbyieldratecomputer import SByieldRateComputer

class Controller:
	def __init__(self):
		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
		else:
			configPath = 'c:\\temp\\sbyield.ini'

		configMgr = ConfigManager(configPath)
		self.sheetDataAccess = SByieldRateComputer(configMgr)
		
		self.processor = Processor(configMgr)
