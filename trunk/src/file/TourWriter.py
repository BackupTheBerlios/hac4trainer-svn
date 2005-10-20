"""Author: Ilja Booij
Date: 2 oktober 2005"""

XML = """<tour type="%(type)s" startTime="%(startTime)s">
<initialPulse>%(pulse)s</initialPulse>
<initialAltitude>%(altitude)s</initialAltitude>
<recordingTime>%(recordingTime)s</recordingTime>
<temperatures>%(temperatures)s</temperatures>
</tour>
"""

class TourWriter:
    """class used to write a tour to an XML string"""
    
    def __init__(self):
        """construct a new TourWriter"""
        pass
    
    def getXMLString(self, tour):
        dic = self.combineDictionaries(self.getTourHeader(tour),
            self.getHead(tour))
        return XML % dic
    
    def getTourHeader(self, tour):
        return {'type' : tour.getType(), 'startTime' : tour.getStartTime()}

    def getTourTemperatures(self, tour):
        return ",".join(map(str,tour.getTemperatures()))
    def getHead(self, tour):
        return {'pulse' : tour.getInitialPulse(),
            'altitude' : tour.getInitialAltitude(),
            'recordingTime' : tour.getRecordingTime(),
            'temperatures' : self.getTourTemperatures(tour)}
    
        
    def combineDictionaries(self, *args):
        """combine all dictionaries to one"""
        dic = {}
        for arg in args:
            for key, val in arg.items():
                dic[key] = val
        return dic