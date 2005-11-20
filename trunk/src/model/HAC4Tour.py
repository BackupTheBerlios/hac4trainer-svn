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
from datetime import datetime, timedelta

import logging

class HAC4TourType:
    BIKE = 1
    OTHER = 2

HAC4_TOUR_TYPES = {HAC4TourType.BIKE : 'Bike', HAC4TourType.OTHER: 'Other'}

# 20 seconds per interval
RECORDING_TIME_PER_INTERVAL = 20 

class HAC4Tour:
    def __init__(self):
        # singular values
        self._type = None
        self._startTime = None
        self._startDistance = 0
        self._startAltitude = 0
        self._startPulse = 0
        self._weight = 0
        
        # lists of values
        self._temperatures = []
        self._cadences = []
        self._pulseDeltas = []
        self._altitudeDeltas = []
        self._distanceDeltas = []
        
    def setType(self, type):
        """set the type of tour (BIKE or OTHER)"""
        assert(type in HAC4_TOUR_TYPES)
        self._type = type
        
    def getType(self):
        """return type of tour"""
        return self._type
    
    def getTypeString(self):
        """return type of tour as string"""
        return HAC4_TOUR_TYPES[self._type]
    
    def setWeight(self, weight):
        """set weight of rider"""
        assert(weight > 0)
        self._weight = weight
    
    def getWeight(self):
        return self._weight
    
    def setStartTime(self, startTime):
        """set start time of tour"""
        self._startTime = startTime
    
    def getStartTime(self):
        """return start time of tour"""
        return self._startTime
    
    def setStartDistance(self, startDistance):
        """set the total distance travelled before start of this tour"""
        self._startDistance = startDistance
    
    def setStartAltitude(self, startAltitude):
        """set altitude at start of tour"""
        self._startAltitude = startAltitude
        
    def setStartPulse(self, startPulse):
        """set heart pulse at start of tour"""
        self._startPulse = startPulse
    
    def setTemperatures(self, temperatures):
        """set temperatures. temperatures is a list"""
        assert(isinstance(temperatures, list))
        self._temperatures = temperatures
   
    def setCadences(self, cadences):
        """set cadences (list)"""
        assert(isinstance(cadences, list))
        self._cadences = cadences
   
    def setPulseDeltas(self, pulseDeltas):
        """set pulseDeltas (list)"""
        assert(isinstance(pulseDeltas, list))
        self._pulseDeltas = pulseDeltas
        
    def getPulses(self):
        """Return a list of heart BPM's, starting at t=0"""
        pulses = [self._startPulse]
        for pulseDelta in self._pulseDeltas:
            pulses.append(pulses[-1] + pulseDelta)

    def setAltitudeDeltas(self, altitudeDeltas):
        """set altitudeDeltas (list)"""
        assert(isinstance(altitudeDeltas, list))
        self._altitudeDeltas = altitudeDeltas
    
    def getAltitudes(self):
        """Return a list of altitude at each point in time, starting at t = 0"""
        altitudes = [self._startAltitude]
        for altitudeDelta in self._altitudeDeltas:
            altitudes.append(altitudes[-1] + altitudeDelta)
   
    def setDistanceDeltas(self, distanceDeltas):
        """set pulseDeltas (list)"""
        assert(isinstance(distanceDeltas, list))
        self._distanceDeltas = distanceDeltas
       
    def getDistances(self):
        """get a list of distances at each point in time, starting at time = 0"""
        distances = [0]
        for distanceDelta in self._distanceDeltas:
            distances.append(distances[-1] + distanceDelta)
        return distances
    
    def getTotalDistance(self):
        """get total distance travelled, in km"""
        return self.getDistances()[-1]/ 1000.0
    
    def getRecordingTimeInSeconds(self):
        """get total recording time in seconds for tour"""
        # there is a recording every second
        return len(self._altitudeDeltas) * RECORDING_TIME_PER_INTERVAL
    
    def getMovingRecordingTimeInSeconds(self):
        """get recording time in seconds, but only count intervals where the
        bike was moving"""
        moving_distance_deltas = filter(lambda distance: distance > 0,
                                         self._distanceDeltas)
        recording_time_moving = (len(moving_distance_deltas) 
            * RECORDING_TIME_PER_INTERVAL)
        return recording_time_moving
    
    def getRecordingTime(self):
        """get total recording time as a timedelta object"""
        return timedelta(seconds = self.getRecordingTimeInSeconds())
    
    def getMovingRecordingTime(self):
        """get recording time, only counting when bike is moving"""
        return timedelta(seconds = self.getMovingRecordingTimeInSeconds())
    
    
    def getAverageSpeed(self):
        """get the average speed. This also counts when speed = 0"""
        return (float(self.getDistances()[-1] )
            / float(self.getRecordingTimeInSeconds())) * 3.6
    
    def getAverageSpeedCorrected(self):
        """get the average speed, but don't count intervals where speed 
        is zero"""
        distance_in_km = sum(self._distanceDeltas) / 1000.0
        logging.debug("km: " + distance_in_km)
        recording_time_moving = self.getMovingRecordingTimeInSeconds()
        logging.debug("time: " + recording_time_moving)
        if (recording_time_moving == 0):
            return 0
        average_speed = (distance_in_km / (float(recording_time_moving) / 60.0))
        
        return average_speed
             
    def __repr__(self):
        return ("Tour: " 
            + "Type: " + repr(HAC4_TOUR_TYPES[self.getType()]) 
            + ", Weight: " + repr(self._weight) 
            + ", Start: " + repr(self._startTime)
            + ", initialDistance: " + repr(self._startDistance)
            + ", initialAltitude: " + repr(self._startAltitude)
            + ", initialPulse: " + repr(self._startPulse)
            + ", average Speed: " + repr(self.getAverageSpeed())
            + ", recording Time: " + repr(self.getRecordingTimeInSeconds() / 60) + " minutes"
            + ", distance: " + repr(self.getDistances()[-1] / 1000.0))
        
    def __cmp__(self, tour):
        if tour == None:
            return 1
        if self._startTime < tour.getStartTime():
            return -1
        elif self._startTime > tour.getStartTime():
            return 1
        else:
            return 0
        