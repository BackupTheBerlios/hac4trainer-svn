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

import sys
sys.path.append('..')
import logging
from model.HAC4Tour import HAC4Tour, HAC4TourType

HEAD_TEMPLATE = """HACtronic - Tour
3
1
0



%(startdate)s
%(starttime)s
0
%(distance)d
%(tourtime)d
UNKNOWN_NUMBER
%(maxheight)s
UKNOWN_DIFF_HEIGHT
%(avgclimbingrate)s
%(avgclimbinggrade)s
%(avgspeed)s
%(avgtemp)s
%(avgpulse)s
%(avgcadence)s
%(modus)s
UNKNOWN_NUMBER
UNKNOWN_ReserveA1
UNKNOWN_ReserveA2
UNKNOWN_ReserveA3
UNKNOWN_ReserveA4
UNKNOWN_ReserveA5
UNKNOWN_ReserveA6
UNKNOWN_ReserveA7
SURNAME
FIRST_NAME
BIRTH_DATE
CLUB
%(weight)s
%(upperlimit)s
%(lowerlimit)s
BIKE_NAME
BIKE_WEIGHT
%(odometer)s
%(totaltime)s
%(totalgained)s
%(totallost)s
UNKNOWN_ReserveA1
UNKNOWN_ReserveA2
UNKNOWN_ReserveA3
UNKNOWN_ReserveA4
UNKNOWN_ReserveA5
UNKNOWN_ReserveA6
UNKNOWN_ReserveA7
UNKNOWN_ReserveA8
UNKNOWN_ReserveA9
UNKNOWN_ReserveA10
%(nrsamples)s
"""

class TURTourIO:
    """implements saving of a tour to TUR Format"""
    
    def __init__(self):
        """construct new TURTourIO object"""
        pass
    
    def write_tour(self, tour, filename):
        """export a tour to a tur file"""
        (head, tail) = self.get_TUR_data(tour)
        sample_data = self.pack_samples(tour)
        
        print 'exporting...', filename
        # TODO catch possible IO exceptions     
        f = file(filename, 'wb')
        f.write(head)
        f.write(sample_data)
        f.write(tail)
        f.close()
    
    def get_TUR_data(self, tour):
        """get tur data, only head and tail of file."""
        data = self.gather_head_data(tour)
        head = HEAD_TEMPLATE % data
        bottom = "\n0\n"
        
        return (head, bottom)
        
    def gather_head_data(self, tour):
        """gather data for head of tur file"""
        data = {} 
        
        date = tour.getStartTime()
        
        data['startdate'] = "%02d.%02d.%4d" % (date.day, date.month, date.year)
        data['starttime'] = "%02d:%02d" % (date.hour, date.minute)
        data['distance'] = int(tour.getTotalDistance() * 100)
        data['tourtime'] = int(tour.getRecordingTimeInSeconds())
        data['maxheight'] = int(tour.getMaximumAltitude())
        data['avgclimbingrate'] = "%.4f" % (tour.getAverageClimbingRate())
        data['avgclimbinggrade'] = "%.4f" % (tour.getAverageClimbingGrade())
        data['avgspeed'] = "%.4f" % (tour.getAverageSpeedCorrected())
        data['avgtemp'] = "%.4f" % (tour.getAverageTemperature())
        data['avgpulse'] = "%d" % (tour.getAveragePulse())
        data['avgcadence'] = "%.4f" % (tour.getAverageCadence()) 
        type = tour.getType()
        if type == HAC4TourType.BIKE:
            type_nr = 2
        else:
            type_nr = 1
        data['modus'] = "%d" % (type_nr)
        data['weight'] = "%d" %(tour.getWeight())
        data['upperlimit'] = "%d" % (tour.getPulseLimits(2)[1])
        data['lowerlimit'] = "%d" % (tour.getPulseLimits(2)[0])
        data['odometer'] = "%d" % (tour.getOdometer())
        # this next value really needs to be checked. It does not match with HACTronic
        data['totaltime'] = "%d" % (tour.getTotalTime().days * 24 * 3600 + tour.getTotalTime().seconds)
        data['totalgained'] = "%d" % (tour.getTotalMetersGained())
        data['totallost'] = "%d" % (tour.getTotalMetersLost())
        data['nrsamples'] = "%d" % (len(tour.getDistances()))
        return data

    def pack_samples(self, tour):
        """packs the samples into a long binary blob of 20 bytes per sample"""
        from struct import pack
        blobs = []
        
        start_sample = pack('LLLhBBbh',
            0,0, 0, tour.getStartAltitude(),
            tour.getStartPulse(), 0, tour.getTemperatures()[0], 0)
        blobs.append(start_sample)
        for sample in tour.getSamples():
            try:
                sample_blob = pack('LLLhBBbh', 
                                0L, # datetime
                                0L, # time
                                sample['distance'] / 10,
                                sample['altitude'],
                                sample['pulse'],
                                sample['cadence'],
                                sample['temperature'], 0)
                
                
            except Exception, e:
                print e, sample
                
            blobs.append(sample_blob)
        return "".join(blobs)
                    
if __name__ == "__main__":
    import sys
    sys.path.append('..')
#    logging.basicConfig(level=logging.DEBUG)
    from importer.HAC4FileImporter import HAC4FileImporter
    importer = HAC4FileImporter('../data/download_30_09_05.dat')
    tours = importer.do_import()
    

    tur_writer = TURTourIO()
    tur_writer.write_tour(tours[5], "tt.tur")
   
            