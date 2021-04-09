class ResultData:
	RESULT_KEY_CRYPTO = 'CRYPTO'
	RESULT_KEY_UNIT = 'UNIT'
	RESULT_KEY_EXCHANGE = 'EXCHANGE'
	RESULT_KEY_PRICE_TIME_STAMP = 'PRICE_TIMESTAMP'
	RESULT_KEY_PRICE = 'PRICE'
	RESULT_KEY_PRICE_TYPE = 'PRICE_TYPE'
	RESULT_KEY_ERROR_MSG = 'ERROR_MSG'
	RESULT_KEY_WARNINGS_DIC = 'WARNING_MSG'
	PRICE_TYPE_RT = 'REAL_TIME'

	def __init__(self, resultDataDic=None):
		if not resultDataDic:
			self._resultDataDic = {}
			self._resultDataDic[self.RESULT_KEY_CRYPTO] = None
			self._resultDataDic[self.RESULT_KEY_UNIT] = None
			self._resultDataDic[self.RESULT_KEY_EXCHANGE] = None
			self._resultDataDic[self.RESULT_KEY_PRICE_TIME_STAMP] = None
			self._resultDataDic[self.RESULT_KEY_PRICE] = None
			self._resultDataDic[self.RESULT_KEY_PRICE_TYPE] = None
			self._resultDataDic[self.RESULT_KEY_ERROR_MSG] = None
			self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC] = {}
		else:
			self._resultDataDic = resultDataDic

		self.requestInputString = ''
	
	def setValue(self, key, value):
		self._resultDataDic[key] = value


	def getValue(self, key):
		return self._resultDataDic[key]


	def setError(self, errorMessage):
		'''
		Set the error msg entry in the ResultData
		:param errorMessage:
		'''
		self._resultDataDic[self.RESULT_KEY_ERROR_MSG] = errorMessage


	def getErrorMessage(self):
		'''
		Returns the error msg entry in the ResultData
		'''
		return self._resultDataDic[self.RESULT_KEY_ERROR_MSG]


	def noError(self):
		return self._resultDataDic[self.RESULT_KEY_ERROR_MSG] == None


	def containsWarning(self, warningType):
		'''
		Return True if the ResultData contains a warning msg
		'''
		warningDic = self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC]

		if warningDic == {}:
			return False
		else:
			return warningType in warningDic.keys()


	def containsWarnings(self):
		'''
		Return True if the ResultData contains a warning msg
		'''
		return self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC] != {}


	def getWarningMessage(self, warningType):
		'''
		Return the warning msg contained in the ResultData
		:param warningType:
		'''
		return self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC][warningType]


	def setWarning(self, warningType, warningMessage):
		'''
		Set the warning msg entry in the ResultData
		:param warningType:
		'''
		warningsDic = self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC]
		warningsDic[warningType] = warningMessage


	def getAllWarningMessages(self):
		'''
		Return a list of warning messages.
		:return: list containing the warning msg strings
		'''

		return list(self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC].values())


	def __str__(self):
		strRepr = ''

		for key in self._resultDataDic.keys():
			val = self._resultDataDic.get(key)
			if val != None:
				strRepr += key + ': ' + str(val) + ' '
			else:
				strRepr += key + ': None '

		return strRepr

if __name__ == '__main__':
	pass
