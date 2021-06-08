import os,sys,inspect
import re
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

class UtilityForTest:
	'''
	This class contains static utility methods used by some unit test classes. It avoids code duplication.
	'''
	@staticmethod
	def printDataFrameForAssertEqual(yieldOwnerWithTotalsDetailDfActualStr):
		stdout = sys.stdout
		capturedStdoutStr = StringIO()
		sys.stdout = capturedStdoutStr
		print()
		print(yieldOwnerWithTotalsDetailDfActualStr)
		sys.stdout = stdout
		# removing end of line spaces
		noEndSpaceActualDfString = ''
		for line in capturedStdoutStr.getvalue().splitlines():
			noEndSpaceActualDfString += line.rstrip() + '\n'
		return noEndSpaceActualDfString