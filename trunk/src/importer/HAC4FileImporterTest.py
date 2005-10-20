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
from HAC4FileImporter import HAC4FileImporter
from HAC4Importer import HAC4DataLengthError

import unittest

ROOT_PATH = '..'

class HAC4FileImporterConstructorTestCase(unittest.TestCase):
	def testNormalSetup(self):
		# get data from the file
		f = file(ROOT_PATH + "/data/testdatafile.dat")
		data = f.read()
		f.close()
		
		importer = HAC4FileImporter(ROOT_PATH + "/data/testdatafile.dat")
		importer.doImport()
		self.assertEqual(data, importer.getRawData())
	
	def testNonExistingDataFile(self):
		importer = HAC4FileImporter(ROOT_PATH + "/data/nonexistingfile.dat")
		
		self.assertRaises(IOError, importer.doImport)
	
	def testWrongLengthDataFile(self):
		importer = HAC4FileImporter(ROOT_PATH + "/data/wronglengthdatafile.dat")
		self.assertRaises(HAC4DataLengthError, importer.doImport)

class HAC4FileImporterMethodsTestCase(unittest.TestCase):
	def setUp(self):
		self.importer = HAC4FileImporter(ROOT_PATH + "/data/testdatafile.dat")
		
	def testDataGetterAndSetter(self):
		f = file(ROOT_PATH + "/data/testdatafile.dat")
		data = f.read()
		f.close()
		self.importer.setRawData(data)
		print len(data)
		print len(self.importer.getRawData())
		#self.assertEqual(data, self.importer.getRawData())
	
	def testDoImport(self):
		self.importer.doImport()
		
if __name__ == '__main__':
	unittest.main()