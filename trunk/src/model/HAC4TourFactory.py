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
from model.HAC4Tour import HAC4Tour, HAC4_TOUR_TYPES, HAC4TourType
from datetime import datetime
import logging
class HAC4TourFactoryException(Exception):
    pass
    
class HAC4TourFactoryFaultyDataException(HAC4TourFactoryException):
    pass
    
class HAC4TourFactory:
    """factory for HAC4Tour objects"""
    
    def __init__(self, year = None):
        """construct a HAC4TourFactory"""
        if (year == None):
            import time
            year = time.localtime().tm_year
        
        self._year = year
        
    def constructTour(self, data, weight):
        """construct a HAC4Tour object from raw data"""
        logging.debug('starting HAC4TourFactory.constructTour()')
        tour = HAC4Tour()
        
        self._readAARecord(tour, data)
        self._readDataRecords(tour, self._splitDataRecords(data))
        
        # add weight to the tour.
        tour.setWeight(weight)
        return tour
        
        
    def _readAARecord(self, tour, data):
        """Reads the AA record. This record holds the type of the tour, start
        time, distance before the tour, initial altitude and the initial pulse
        """
        record = data[:8]
        
        tour.setType(self._readType(record))
        tour.setStartTime(self._readStartTime(record))
        tour.setStartDistance(self._readStartDistance(record))
        tour.setStartAltitude(self._readStartAltitude(record))
        tour.setStartPulse(self._readStartPulse(record))
    
    def _readDataRecords(self, tour, dataRecords):
        """Read all records after the AARecord. This wil put them
        into the HAC4Tour object"""
        temperatures = []
        cadences = []
        pulseDeltas = []
        altitudeDeltas = []
        distanceDeltas = []
        
        for record in dataRecords:
            recordValues = self._readDataRecord(record)
            temperatures.append(recordValues[0])
            cadences.append(recordValues[1])
            pulseDeltas += recordValues[2]
            altitudeDeltas += recordValues[3]
            distanceDeltas += recordValues[4]
        
        # put information in tour object
        tour.setTemperatures(temperatures)
        tour.setCadences(cadences)
        tour.setPulseDeltas(pulseDeltas)
        tour.setAltitudeDeltas(altitudeDeltas)
        tour.setDistanceDeltas(distanceDeltas)         
    
    def _readDataRecord(self, dataRecord):
        """Read one data record, BB or CC. A data record consist of 8 blocks,
        1 holding temperature and type of record (BB or CC), one holding a 
        marker (in case of a BB record, this is empty, in case of a CC record,
        it holds the exact ending second of the recording) and the cadence. The
        other 6 blocks hold recorded values.
        """
        if dataRecord[0][2:] != 'BB' and dataRecord[0][2:] != 'CC':
            # no BB or CC record. This is wrong!
            raise HAC4TourFactoryFaultyDataException
        temperature = int(dataRecord[0][:2], 16)
        cadence = int(dataRecord[1][2:], 16)
        if dataRecord[0][2:] == 'CC':
            timeToEnd = int(dataRecord[1][:2], 16)
            self._readDataValues(dataRecord[2:2+(int(timeToEnd)/20)])
        values = self._readDataValues(dataRecord[2:])
        
        return (temperature, cadence, values[0], values[1], values[2])
 
    def _readDataValues(self, record):
        """Read the recorded values for 2 minutes, divided into 20 second
        blocks of 4 bytes""" 
        assert(len(record) <= 6)
        pulseDeltas = []
        altitudeDeltas = []
        distanceDeltas = []
        for block in record:
            blockValue = int(block, 16)
            pulseDeltas.append(self._readPulse(blockValue))
            altitudeDeltas.append(self._readAltitude(blockValue))
            distanceDeltas.append(self._readDistance(blockValue))
        
        return (pulseDeltas, altitudeDeltas, distanceDeltas)
    
    def _readPulse(self, blockValue):
        """Reads pulse information from a block."""
        
        # take first four bits. Check if first bit is set, if it is, this
        # is a negative value
        if blockValue & 0x8000:
            heartPulseDelta = (((blockValue & 0x7000) >> 12) -8) * 2
        else:
            heartPulseDelta = ((blockValue & 0x7000) >> 12) * 2
       
        return heartPulseDelta
        
    def _readAltitude(self, blockValue):
        """Read altitude information from a block"""
        # next 6 bits (after first four bits for pulse)
        if blockValue & 0x0800:
            altitudeDelta = ((blockValue & 0x07C0) >> 6) - 32
            if altitudeDelta < -16:
                altitudeDelta = -16 + ((altitudeDelta + 16) * 7)
        else:
            altitudeDelta = (blockValue & 0x0FC0) >> 6
            if altitudeDelta > 16:
                altitudeDelta = 16 + ((altitudeDelta - 16) * 7)
        
        return altitudeDelta
        
    def _readDistance(self, blockValue):
        """Read distance information from a block"""
        # last six bits
        distanceDelta = (blockValue & 0x003F) * 10
        return distanceDelta
        
    def _splitDataRecords(self, data):
        """Splits all the blocks for a tour in 8 block records. Returns the
        records"""
        dataBlocks = data[8:]
        return [dataBlocks[begin:begin+8] 
            for begin in range(0,len(dataBlocks), 8)]
        
    def _readType(self, aaRecord):
        """Read type of tour from AA record. Currently, we only check for
        'A1', which signals a bike tour. If it's anything else, it will just
        be in the OTHER category"""
        tourTypeString = aaRecord[0][:2]
        if tourTypeString == 'A1':
           tourType = HAC4TourType.BIKE
        else:
            tourType = HAC4TourType.OTHER
        
        return tourType
        
    def _readStartTime(self, aaRecord):
        """Read the start time of the tour from the AA record"""
        #TODO: this function should compensate for the fact that the year is
        # not present in the file.    
        hour = int(aaRecord[2][:2])
        minute = int(aaRecord[2][2:])
        month = int(aaRecord[3][:2])
        day = int(aaRecord[3][2:])
        
        return datetime(self._year, month, day, hour, minute)
    
    def _readStartDistance(self, aaRecord):
        """Read the total distance travelled before this tour"""
        return int(aaRecord[4], 16)
        
    def _readStartAltitude(self, aaRecord):
        """Read altitude at begin of tour"""
        return int(aaRecord[6], 16)
        
    def _readStartPulse(self, aaRecord):
        """Read heart BPM at start of tour"""
        return int(aaRecord[7], 16)
    
    
    