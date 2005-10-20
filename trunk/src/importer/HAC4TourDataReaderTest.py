import unittest

ROOT_PATH = ".."
DEFAULT_WEIGHT = 75

class HAC4TourDataReaderTestCase(unittest.TestCase):
    def setUp(self):
        from HAC4TourDataReader import HAC4TourDataReader
        self.reader = HAC4TourDataReader(DEFAULT_WEIGHT)
    
    def testReadTestDataFile(self):
        f = file(ROOT_PATH + '/data/testdatafile.dat', 'rb')
        data = [line.strip() for line in f.readlines()]
        
        self.reader.read(data)
        
        self.assertEqual(self.reader.getNumberOfTours(), 19)
        
if __name__ == '__main__':
    import sys
    sys.path.append("..")
    unittest.main()
         