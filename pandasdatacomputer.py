# generic headers
DATAFRAME_HEADER_TOTAL = 'TOTAL'
DATAFRAME_HEADER_GRAND_TOTAL = 'G TOTAL'
DATAFRAME_HEADER_DEPOSIT_WITHDRAW = 'DEP/WITHDR'
DATAFRAME_HEADER_INDEX = 'IDX'

DEPOSIT_SHEET_PARM_FIAT = 'FIAT_'


class PandasDataComputer:
	"""
	This class contains code used by its subclasses.
	"""
	def _replaceDateIndexByIntIndex(self, dataFrame, savedDateColumnName, intIndexColumnName):
		"""
		Replaces the date index column in the passed dataFrame by an integer index with
		value starting at 1. The initial date index is saved as an ordinary date column.
		
		:param dataFrame:
		:param savedDateColumnName:
		:param intIndexColumnName:
		
		:return: the modified data frame
		"""
		modifiedDataFrame = dataFrame
		
		# save old DATE index Column
		modifiedDataFrame[savedDateColumnName] = modifiedDataFrame.index
		
		# set integer index
		modifiedDataFrame[intIndexColumnName] = range(1, len(modifiedDataFrame) + 1)
		modifiedDataFrame = modifiedDataFrame.set_index(intIndexColumnName)
		
		return modifiedDataFrame
	
	def _insertEmptyFloatColumns(self, dataFrame, position, newColNameLst):
		"""
		Inserts in the passed dataFrame empty float64 columns at the passed position.
		The last column in the newColNameLst will be inserted before the previous column
		in the newColNameLst.
		
		If the passed position is None, the columns are appended to the right of the
		dataFrame.
		
		:param dataFrame:
		:param position: 0 based. If None, the columns are appended to the right of the
						 dataFrame
		:param newColNameLst:
		"""
		for colName in newColNameLst:
			if position == None:
				dataFrame[colName] = [0.0 for i in range(dataFrame.shape[0])]
			else:
				dataFrame.insert(loc=position,
								 column=colName,
								 value=[0.0 for i in range(dataFrame.shape[0])])
	
	def _appendEmptyColumns(self, dataFrame, newColNameLst):
		"""
		Append empty columns to the right of the passed	dataFrame.
		
		:param dataFrame:
		:param newColNameLst:
		"""
		for colName in newColNameLst:
			dataFrame[colName] = ''
	
	def _determineDepositSheetSkipRowsAndCrypto(self,
												csvSheetFilePathName,
												firstHeaderColumnName,
												cryptoParmKey = None):
		"""
		Determines the number of comment lines above the column headers which must be
		skipped as well as return the deposit csv file crypto, currently USDC, CHSB
		or ETH.
		
		:param csvSheetFilePathName
		:param firstHeaderColumnName
		:param cryptoParmKey
		
		:return line to skip number, deposit csv file crypto
		"""
		with open(csvSheetFilePathName, 'r') as f:
			fileLines = f.readlines()
			commentLinesNb = 0
			crypto = None

			for line in fileLines:
				if firstHeaderColumnName in line:
					return commentLinesNb, crypto
				else:
					commentLinesNb += 1
				if cryptoParmKey is not None and cryptoParmKey in line:
					crypto = line.rstrip('\n').replace(cryptoParmKey, '').upper()

		return commentLinesNb, crypto
	
	def getDataframeStrWithFormattedColumns(self, dataFrame, colFormatDic):
		"""
		Returns a string representation of the passed dataFrame enabling to define a
		specific format for any column since Pandas by default format all float
		columns with a same format.
		
		This method is useful if we want to set a specific precision to float64
		columns.
		
		:param dataFrame:
		:param colFormatDic: Example: {MERGED_SHEET_HEADER_YIELD_RATE: '.8f'}
		:return:
		"""
		formatDic = {}
		
		for colHeader, formatStr in colFormatDic.items():
			pandasFormatStr = '{:,' + formatStr + '}' # example: '{:.8f}
			formatDic[colHeader] = pandasFormatStr.format
		
		# replacing NaN by identical empty size string. NaN is the values of the
		# non float elements of the TOTAL row. Using fillna('') in
		# OwnerDepositYieldComputer._computeYieldOwnerDetailTotals() was removed since
		# it caused an error in the DataFrame.to_string() with formatting the CAPITAL
		# column values due to the fact that a '' string in the TOTAL row could not be
		# formatted as a float ! If a value is NaN, the formatting of this value as float
		# is mastered by Pandas !
		
		# The second replaqe is required on Android !

		return dataFrame.to_string(formatters=formatDic).replace('NaN', '   ').replace('nan', '   ')
