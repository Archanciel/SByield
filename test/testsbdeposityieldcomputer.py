import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from configmanager import ConfigManager
from sbyieldratecomputer import *
from sbdeposityieldcomputer import SBDepositYieldComputer

class TestSBDepositYieldComputer(unittest.TestCase):
	def setUp(self):
		sbAccountSheetFileName = 'testSBEarningUsdc.xlsx'
		depositSheetFileName = 'testDepositUsdc.csv'

		if os.name == 'posix':
			configPath = '/sdcard/sbyield.ini'
			sbAccountSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + sbAccountSheetFileName
			depositSheetFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/SByield/test/testdata/' + depositSheetFileName
		else:
			configPath = 'c:\\temp\\sbyield.ini'
			sbAccountSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + sbAccountSheetFileName
			depositSheetFilePathName = 'D:\\Development\\Python\\SByield\\test\\testData\\' + depositSheetFileName

		configMgr = ConfigManager(configPath)
		self.yieldRateComputer = SBYieldRateComputer(configMgr,
		                                             sbAccountSheetFilePathName,
		                                             depositSheetFilePathName)
		self.depositYieldComputer = SBDepositYieldComputer(configMgr, self.yieldRateComputer)

	def testComputeDepositsYields(self):
		yieldCrypto = SB_ACCOUNT_SHEET_CURRENCY_USDC

		depositsYieldsDataFrame = self.depositYieldComputer.computeDepositsYields(yieldCrypto)
		self.assertEqual((5, 2), depositsYieldsDataFrame.shape)

		print(self.yieldRateComputer.getDataframeStrWithFormattedColumns(depositsYieldsDataFrame, {DEPOSIT_SHEET_HEADER_DEPOSIT_WITHDRAW: '.2f'}))

if __name__ == '__main__':
	#unittest.main()
	tst = TestSBDepositYieldComputer()
	tst.setUp()
	tst.testComputeDepositsYields()
