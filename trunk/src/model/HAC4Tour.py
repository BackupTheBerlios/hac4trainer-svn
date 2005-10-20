from datetime import datetime, timedelta

class HAC4TourType:
    BIKE = 1
    OTHER = 2

HAC4_TOUR_TYPES = {HAC4TourType.BIKE : 'Bike', HAC4TourType.OTHER: 'Other'}

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
    
    def setWeight(self, weight):
        """set weight of rider"""
        assert(weight > 0)
        self._weight = weight
    
    def getWeight(self):
        return self._weight
    
    def setStartTime(self, startTime):
        """set start time of tour"""
        self._startTime = startTime
    
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
    
    def getRecordingTimeInSeconds(self):
        """get total recording time in seconds for tour"""
        # there is a recording every second
        return len(self._altitudeDeltas) * 20
    
    def getRecordingTime(self):
        """get total recording time as a timedelta object"""
        return timedelta(seconds = self.getRecordingTimeInSeconds())
    
    def getAverageSpeed(self):
        """get the average speed. This also counts when speed = 0"""
        return (float(self.getDistances()[-1] )
            / float(self.getRecordingTimeInSeconds())) * 3.6        
        
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
    
    def getStartTime(self):
        return self._startTime
        
    def __cmp__(self, tour):
        if self._startTime < tour.getStartTime():
            return -1
        elif self._startTime > tour.getStartTime():
            return 1
        else:
            return 0
        