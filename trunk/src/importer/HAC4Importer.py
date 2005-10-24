#Copyright (c) 2005, Ilja Booij (ibooij@gmail.com)
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, 
#are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#    * Neither the name of Ilja Booij nor the names of its contributors may be 
#    used to endorse or promote products derived from this software without 
#    specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

	def set_raw_data(self, data):
		if len(data) != HAC4Importer.DATA_LENGTH:
				logging.error("data has wrong length, is %d but should be %d" % 
					(len(data), HAC4Importer.DATA_LENGTH))
				raise HAC4DataLengthError("data length is %d instead of %d"
					% (len(data), HAC4Importer.DATA_LENGTH))
		
		self._extract_data_blocks(data)
		if not self.identify_HAC4():
			logging.error("Data not from HAC4")
			raise HAC4DataNotFromHAC4Error("data not identified as coming from HAC4")
	
	def do_import(self):
		from HAC4InformationReader import HAC4InformationReader
		reader = HAC4InformationReader()
		tours = reader.read(self._dataBlocks)
		return tours
	
	def _extract_data_blocks(self, data):
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

		# make sure all blocks are in uppercase
		dataBlocks = [block.upper() for block in dataBlocks]
		self._dataBlocks = dataBlocks
	
	def get_raw_data(self):
		"""return data"""
		return '\n'.join(self._dataBlocks) + '\n'
	
	def identify_HAC4(self):
		print len(self._dataBlocks[0])
		if self._dataBlocks[HAC4_DEVICE_SIG[0]].upper() != HAC4_DEVICE_SIG[1]:
			logging.error('data device signature = %s' %
				(self._dataBlocks[HAC4_DEVICE_SIG[0]]))
			return 0
		else:
			return 1
	
		