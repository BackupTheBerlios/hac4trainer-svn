"""Test TourWriter.py"""

import unittest
from datetime import datetime, timedelta
from TourWriter import TourWriter

TEST_XML = """<tour type="TESTTYPE" startTime="2005-01-01 00:00:00">
<initialPulse>120</initialPulse>
<initialAltitude>750</initialAltitude>
<recordingTime>1:00:00</recordingTime>
<temperatures>20,21,22,23,22,20</temperatures>
</tour>
"""

class TestTour:
    def getType(self):
        return 'TESTTYPE'
    def getStartTime(self):
        return datetime(2005, 1, 1, 0, 0)
    def getInitialPulse(self):
        return 120
    def getInitialAltitude(self):
        return 750
    def getRecordingTime(self):
        return timedelta(seconds=3600)
    def getTemperatures(self):
        return [20,21,22,23,22,20]
    
class TourWriterTest(unittest.TestCase):
    def setUp(self):
        self.tourWriter = TourWriter()
        self.testTour = TestTour()
    
    def testXML(self):
        xml = self.tourWriter.getXMLString(self.testTour)
        if xml != TEST_XML:
            print xml
            print TEST_XML
        self.assertEqual(xml, TEST_XML)

if __name__ == '__main__':
    unittest.main()    