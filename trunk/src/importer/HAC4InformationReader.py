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
from datetime import date, timedelta

infoDataInfo = [(0, 'DATA_4_HEX', 'wheelPerimeter'),
			(1, 'DATA_4_HEX', 'weight'),
			(2, 'DATA_4_HEX', 'homeAltitude'),
			(3, 'DATA_4_HEX', 'maxPulse1'),
			(4, 'DATA_4_HEX', 'minPulse1'),
			(5, 'DATA_4_HEX', 'maxPulse2'),
			(6, 'DATA_4_HEX', 'minPulse2'),
			(7, 'DATA_2_2_TIMEDELTA', 'countDown1'),
			(8, 'DATA_2_2_TIMEDELTA', 'countDown2'),
			(9, 'DATA_4_HEX', 'altitudeErrorCorrection'),
	        (10, 'DATA_4_4_HEX', 'totalDistance'),
	        (13, 'DATA_DATE_4_2_2', 'dateOfTransfer'),
	        (15, 'DATA_4_HEX', 'totalAscendedMeters'),
			(16, 'DATA_4_HEX', 'totalDescendedMeters'),
			(17, 'DATA_4_HEX', 'maxAltitude'),
			(18, 'DATA_2_2_2_2_TIMEDELTA', 'totalTravelTime')]
			
			
def read_hex(hexString):
	try:
		hexValue = int(hexString, 16)
	except ValueError:
		raise HAC4IncorrectInformationError("incorrect value string. This "
			"[%s] is not a Hexadecimal value" % (hexString))
	return hexValue

def read_dec(decimalString):
	try:
		decValue = int(decimalString, 10)
	except ValueError:
		raise HAC4IncorrectInformationError("incorrect value string. This "
			"[%s] is not a decimal value" % (decimalString))
	return decValue
	
class HAC4IncorrectInformationError(Exception):
	pass

class HAC4InformationReader:
	"""This class implements the general information received from a 
	HAC4 device. This includes information about wheel perimeter, weight
	of the rider etc"""

	def __init__(self):
		self._reset()
	
	def __getitem__(self, key):
		"""get an item from the info dict. Will generate a KeyError if
		the item does not exist"""
		return self._info[key]
	
	def __repr__(self):
		return repr(self._info)
		
	def _reset(self):
		self._info = {}
		
	def read(self, data):
		self._reset()
		infoData = data[130:151]
		
		for piece in infoDataInfo:
			index = piece[0]
			size = piece[1]
			if size == 'DATA_DATE_4_2_2':
				self.read_dec_date_value(infoData[index], infoData[index + 1],
					piece[2])
			elif size == 'DATA_4_4_HEX':
				self.readHex8Value(infoData[index], infoData[index + 1], 
					piece[2])
			elif size == 'DATA_4_HEX':
				self.read_Hex4_value(infoData[index], piece[2])
			elif size == 'DATA_2_2_TIMEDELTA':
				self.read_dec_time_delta_countdown(infoData[index], piece[2])
			elif size == 'DATA_2_2_2_2_TIMEDELTA':
				self.read_dec_time_delta_total_time(infoData[index],
						infoData[index + 1], piece[2])
			else:
				raise ValueError('unknown data type')
		
		from HAC4TourDataReader import HAC4TourDataReader
		tourReader = HAC4TourDataReader(self['weight'])
		tours = tourReader.read(data)
		
		
		return tours
	
	def read_dec_time_delta_total_time(self, hourString, secondsMinuteString, name):
		hours = read_dec(hourString[:2])
		hoursTimes100 = read_dec(hourString[2:]) 
		minutes = read_dec(secondsMinuteString[2:])
		seconds = read_dec(secondsMinuteString[:2])
		self._info[name] = timedelta(hours = hours + 100 * hoursTimes100,
									  minutes = minutes, seconds = seconds)
		
	def read_dec_date_value(self, yearString, monthDayString, name):
		year = read_dec(yearString)
		month = read_dec(monthDayString[:2])
		day = read_dec(monthDayString[2:])
		
		self._info[name] = date(year, month, day)
		
	def read_dec_time_delta_countdown(self, timeDeltaString, name):
		minutes = read_dec(timeDeltaString[:2])
		seconds = read_dec(timeDeltaString[2:])
		
		self._info[name] = timedelta(minutes = minutes, seconds = seconds)
		
	def readHex8Value(self, valueHighString, valueLowString, name):
		valueHigh = read_hex(valueHighString)
		valueLow = read_hex(valueLowString)
		
		self._info[name] = (int(pow(2, 16) * valueHigh)) + valueLow
	
	def read_Hex4_value(self, value, name):
		self._info[name] = read_hex(value)
	
	def read_hex2_value(self, valueString, number, name):
		if number == 1:
			value = valueString[:2]
		else:
			value = valueString[2:]
			
		self._info[name] = read_hex(value[:number*2])

	
if __name__ == '__main__':
	import sys
	sys.path.append('..')
	f = file('../data/testdatafile.dat', 'rb')
	data = [line.strip() for line in f.readlines()]
	f.close()
	reader = HAC4InformationReader()
	tours = reader.read(data)
	print tours
	print reader