import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from configmanager import ConfigManager
from sheetdataaccess import SheetDataAccess

class TestSheetDataAccess(unittest.TestCase):
	def setUp(self):
		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
		else:
			configPath = 'c:\\temp\\sbyield.ini'

		configMgr = ConfigManager(configPath)
		self.sheetDataAccess = SheetDataAccess(configMgr)

	def testLoadSBEarningSheet(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'

		if os.name == 'posix':
			sbAccountSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + sbAccountSheetFileName
		else:
			sbAccountSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + sbAccountSheetFileName

		sbEarningsDf = self.sheetDataAccess.loadSBEarningSheet(sbAccountSheetFilePathName)
		self.assertEqual((9, 5), sbEarningsDf.shape)
		
		print('\nsbEarningsDf')
		print(sbEarningsDf.info())
		print(sbEarningsDf)

	def testLoadDepositSheet(self):
		depositSheetFileName = 'testDepositUsdc.csv'

		if os.name == 'posix':
			depositSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + depositSheetFileName
		else:
			depositSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + depositSheetFileName

		depositDf = self.sheetDataAccess.loadDepositSheet(depositSheetFilePathName)
		self.assertEqual((3, 1), depositDf.shape)
		
		print('\ndepositDf')
		print(depositDf.info())
		print(depositDf)
		
	def testMergeEarningAndDeposit(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc.csv'

		if os.name == 'posix':
			sbAccountSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + sbAccountSheetFileName
			depositSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + depositSheetFileName
		else:
			sbAccountSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + sbAccountSheetFileName
			depositSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + depositSheetFileName

		sbEarningsDf = self.sheetDataAccess.loadSBEarningSheet(sbAccountSheetFilePathName)
		depositDf = self.sheetDataAccess.loadDepositSheet(depositSheetFilePathName)
		
		mergedEarningDeposit = self.sheetDataAccess.mergeEarningAndDeposit(sbEarningsDf, depositDf)
		self.assertEqual((12, 5), mergedEarningDeposit.shape)

		print('\nmergedEarningDeposit')
		print(mergedEarningDeposit.info())
		print(mergedEarningDeposit)

if __name__ == '__main__':
    unittest.main()
	#tst = TestSheetDataAccess()
	#tst.setUp()
	#tst.testLoadSBEarningSheet()
	#tst.setUp()
	#tst.testMergeEarningAndDeposit()