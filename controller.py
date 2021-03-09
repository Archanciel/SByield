import os,sys,inspect

from configmanager import ConfigManager
from processor import Processor
from sheetdataaccess import SheetDataAccess

class Controller:
	def __init__(self):
		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
		else:
			configPath = 'c:\\temp\\sbyield.ini'

		configMgr = ConfigManager(configPath)
		self.sheetDataAccess = SheetDataAccess(configMgr)
		
		self.processor = Processor(configMgr)
