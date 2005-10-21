#Copyright (c) 2005, Ilja Booij (ibooij@gmail.com)
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without 
#modification, are permitted provided that the following conditions are met:
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
"""
HAC4TourDataReader is used for reading information from a single tour
"""
# $Rev
__revision__ = "$LastChangedRevision"

from time import localtime

from model.HAC4TourList import HAC4TourList

# tourdata begins at record 153
TOURS_BEGIN = 153
# tourdata ends at record 16385
TOURS_END = 16385

class HAC4TourDataReader:
    """read information on several tours. Uses model.HAC4TourFactory
    to make individual tours"""
    
    def __init__(self, weight):
        """construct a new HAC4TourDataReader."""
        self._weight = weight
        self._year = localtime().tm_year 
        self._tourdata = []
        self._tourBoundaries = []
        self._tours = []
           
    def read(self, data):
        self._tourdata = data[TOURS_BEGIN:TOURS_END]
        self._find_tour_boundaries()
        tours = []
        
        for tourBoundary in self._tourBoundaries:
            if tourBoundary[0] < tourBoundary[1]:
                singleTourData = self._tourdata[tourBoundary[0]: tourBoundary[1]]
            else:
                singleTourData = (self._tourdata[tourBoundary[0]:] + 
                    self._tourdata[:tourBoundary[1]])
            assert(len(singleTourData) % 8 == 0)
            from model.HAC4TourFactory import HAC4TourFactory
            tourFactory = HAC4TourFactory(self._year)
            tours.append(tourFactory.constructTour(singleTourData, 
                          self._weight))
        
        tours.sort()
        
        return tours
        
    def get_number_of_tours(self):
        return len(self._tourBoundaries)
        
    def _find_tour_boundaries(self):
        self.tourBoundaries = []
        for index in range(0, len(self._tourdata)):
            block = self._tourdata[index]
            if block[2:] == 'AA':
                # tourStart found
                tourStart = index
                tourEnd = self._find_tour_end(tourStart)
                self._tourBoundaries.append((tourStart, tourEnd))
    
    def _find_tour_end(self, tourStart):
        searchIndex = tourStart
        while 1:
            searchIndex += 8
            if searchIndex >= len(self._tourdata):
                searchIndex = searchIndex - len(self._tourdata)
            if self._tourdata[searchIndex][2:] == 'DD':
                # end of your found
                break
        return searchIndex
        
if __name__ == '__main__':
    import sys
    sys.path.append("..")
    f = file('../data/testdatafile.dat', 'rb')
    data = [line.strip() for line in f.readlines()]
    f.close()
    
    reader = HAC4TourDataReader(75)
    tours = reader.read(data)
    for tour in tours:
        print tour    
            
        
        
    
        
    
        
    