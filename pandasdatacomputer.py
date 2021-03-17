# generic headers
DATAFRAME_HEADER_TOTAL = 'TOTAL'
DATAFRAME_HEADER_DEPOSIT_WITHDRAW = 'DEP/WITHDR'
DATAFRAME_HEADER_INDEX = 'IDX'


class PandasDataComputer:
	"""
	This class contains code used by its subclasses.
	"""
	def __init__(self, configMgr):
		self.configMgr = configMgr
		
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
			pandasFormatter = '{:,' + formatStr + '}'
			formatDic[colHeader] = pandasFormatter.format
			
		return dataFrame.to_string(formatters=formatDic)
