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