import logging
from HAC4InformationReader import HAC4InformationReader

class HAC4DataError(Exception):
	pass

class HAC4DataLengthError(HAC4DataError):
	pass

class HAC4DataNotFromHAC4Error(HAC4DataError):
	pass

HAC4_DEVICE_SIG = (129, 'B735')

class HAC4Importer:
	"""Imports data from a HAC4 downloaded file"""

	# length of data from HAC4 is always 81930 bytes
	DATA_LENGTH = 81930
	# block length of data is 4 + 1 (1 is for newline character
	BLOCK_LEN = 5
	
	def __init__(self):
		raise NotImplementedError

	def setRawData(self, data):
		if len(data) != HAC4Importer.DATA_LENGTH:
				logging.error("data has wrong length, is %d but should be %d" % 
					(len(data), HAC4Importer.DATA_LENGTH))
				raise HAC4DataLengthError("data length is %d instead of %d"
					% (len(data), HAC4Importer.DATA_LENGTH))
		
		self._extractDataBlocks(data)
		if not self.identifyHAC4():
			logging.error("Data not from HAC4")
			raise HAC4DataNotFromHAC4Error("data not identified as coming from HAC4")
	
	def doImport(self):
		from HAC4InformationReader import HAC4InformationReader
		reader = HAC4InformationReader()
		tours = reader.read(self._dataBlocks)
		return tours
	
	def _extractDataBlocks(self, data):
		dataBlocks = data.split()
		if (len(dataBlocks) != 
				HAC4Importer.DATA_LENGTH / HAC4Importer.BLOCK_LEN):
			logging.error("data does not have the right amount of blocks. "
				"Nr of blocks is %d, should be %d" 
				% (len(dataBlocks), 
				HAC4Importer.DATA_LENGTH / HAC4Importer.BLOCK_LEN))
			raise HAC4DataNotFromHAC4Error("not the right amount of data"
				" blocks. Is %d, should be %d" % (len(dataBlocks),
				HAC4Importer.DATA_LENGTH / HAC4Importer.BLOCK_LEN))
		self._dataBlocks = dataBlocks
	
	def getRawData(self):
		"""return data"""
		return '\n'.join(self._dataBlocks) + '\n'
	
	def identifyHAC4(self):
		if self._dataBlocks[HAC4_DEVICE_SIG[0]] != HAC4_DEVICE_SIG[1]:
			return 0
		else:
			return 1
	
		