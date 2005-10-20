import unittest
from HAC4Importer import HAC4Importer

class	HAC4ImporterTestCase(unittest.TestCase):
	"""super class for all testcases here"""
	
	def testConstructorRaisesException(self):
		"""We should not be able to call instantiate a  HAC4Importer, 
		it should be implented in a subclass"""
		self.assertRaises(NotImplementedError,
			HAC4Importer)
		
if __name__ == '__main__':
	unittest.main()
	