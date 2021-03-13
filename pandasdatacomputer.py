class PandasDataComputer:
	"""
	This class contains code used by its subclasses.
	"""
	def __init__(self, configMgr):
		self.configMgr = configMgr
		
	def _replaceDateIndexByIntIndex(self, dataFrame, savedDateColumnName, intIndexColumnName):
		modifiedDataFrame = dataFrame
		
		# save old DATE index Column
		modifiedDataFrame[savedDateColumnName] = modifiedDataFrame.index
		
		# set integer index
		modifiedDataFrame[intIndexColumnName] = range(1, len(modifiedDataFrame) + 1)
		modifiedDataFrame = modifiedDataFrame.set_index(intIndexColumnName)
		
		return modifiedDataFrame