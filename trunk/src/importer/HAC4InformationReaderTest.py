from HAC4InformationReader import HAC4InformationReader
from HAC4InformationReader import HAC4IncorrectInformationError

from math import pow
from datetime import date, timedelta

import unittest

class HAC4InformationReaderConstructorTestCase(unittest.TestCase):
	def testConstructor(self):
		reader = HAC4InformationReader()

class HAC4InformationReaderTestCase(unittest.TestCase):
	def setUp(self):
		self.reader = HAC4InformationReader()
	
	def testOKData(self):
		blocks = ['' for i in range(0, 16386)]
		
		# set blocks to known values
		blocks[130] = '0830' # wheel perimeter (2096)
		blocks[131] = '004b' # weight (75)
		blocks[132] = '0004' # home altitude (4)
		blocks[133] = '00c2' # max pulse 1 (194)
		blocks[134] = '00aa' # min pulse 1 (170)
		blocks[135] = '00af' # max pulse 2 (175)
		blocks[136] = '0078' # min pulse 2 (120)
		blocks[137] = '0300' # countdown 1 minute & second (3 & 0)
		blocks[138] = '0200' # countdown 1 minute & second (2 & 0)
		blocks[139] = '005a' # altitude error correction
		blocks[140] = '0000' # total distance, high part (0)
		blocks[141] = '1110' # total distance, low part (4386)
		# blocks[142] is not needed, signals next free memory slot
		blocks[143] = '2005' # year of transfer (2005)
		blocks[144] = '0920' # month and day of last transfer (09 & 20)
		blocks[145] = '7a64' # total climbed meters at end of last tour (31332)
		blocks[146] = '74d0' # total descended meters at end of last tour (29904)
		blocks[147] = '0007' # max altitude of last tour
		blocks[148] = '6701' # hours of travel time. First two number are
							 # hours, 2nd are hours * 100
		blocks[149] = '0325' # seconds and minutes of total travel time
		
		self.reader.read(blocks)
		
		self.assertEqual(self.reader['wheelPerimeter'], int(blocks[130], 16))
		self.assertEqual(self.reader['weight'], int(blocks[131], 16))
		self.assertEqual(self.reader['homeAltitude'], int(blocks[132], 16))
		self.assertEqual(self.reader['maxPulse1'], int(blocks[133], 16))
		self.assertEqual(self.reader['minPulse1'], int(blocks[134], 16))
		self.assertEqual(self.reader['maxPulse2'], int(blocks[135], 16))
		self.assertEqual(self.reader['minPulse2'], int(blocks[136], 16))
		self.assertEqual(self.reader['countDown1'],
									  timedelta(minutes=int(blocks[137][:2]),
											seconds=int(blocks[137][2:])))
		self.assertEqual(self.reader['countDown2'],
									  timedelta(minutes=int(blocks[138][:2]),
											seconds=int(blocks[138][2:])))
		self.assertEqual(self.reader['altitudeErrorCorrection'], 
									  int(blocks[139], 16))
		self.assertEqual(self.reader['totalDistance'], 
									   (int(pow(2, 16) * 
									   		int(blocks[140], 16))) +
									 (int(blocks[141], 16)))
		self.assertEqual(self.reader['dateOfTransfer'],
									  date(int(blocks[143]), 
										   int(blocks[144][:2]),
									       int(blocks[144][2:])))
		self.assertEqual(self.reader['totalAscendedMeters'], int(blocks[145], 16))
		self.assertEqual(self.reader['totalDescendedMeters'], int(blocks[146], 16))
		self.assertEqual(self.reader['maxAltitude'], int(blocks[147], 16))
		self.assertEqual(self.reader['totalTravelTime'], 
							timedelta(6, 84303))
																		  
	def testFaultyData(self):
		blocks = ['' for i in range(0, 16386)]
		
		# set blocks to known values
		blocks[130] = '0g30' # wheel perimeter (2096)
		blocks[131] = '004b' # weight (75)
	
		
		self.assertRaises(HAC4IncorrectInformationError, 
			self.reader.read, blocks)
		

if __name__ == '__main__':
	unittest.main()	