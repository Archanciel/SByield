import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from configmanager import ConfigManager
from processor import Processor

class TestProcessor(unittest.TestCase):
	def setUp(self):
		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
		else:
			configPath = 'c:\\temp\\sbyield.ini'

		configMgr = ConfigManager(configPath)
		self.processor = Processor(configMgr)
