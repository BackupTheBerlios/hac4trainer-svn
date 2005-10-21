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
HAC4TourDataReader is used for reading information from several tours
"""
__revision__ = "$LastChangedRevision$"

from time import localtime

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
        self._tour_boundaries = []
        self._tours = []
           
    def read(self, data):
        """read(data) -> list of tours
        
        read information from raw data. Outputs a list of tours"""
        self._tourdata = data[TOURS_BEGIN:TOURS_END]
        self._find_tour_boundaries()
        tours = []
        
        for tour_boundary in self._tour_boundaries:
            if tour_boundary[0] < tour_boundary[1]:
                single_tour_data = self._tourdata[tour_boundary[0]: 
                    tour_boundary[1]]
            else:
                single_tour_data = (self._tourdata[tour_boundary[0]:] + 
                    self._tourdata[:tour_boundary[1]])
            assert(len(single_tour_data) % 8 == 0)
            from model.HAC4TourFactory import HAC4TourFactory
            tour_factory = HAC4TourFactory(self._year)
            tours.append(tour_factory.constructTour(single_tour_data, 
                          self._weight))
        
        tours.sort()
        
        return tours
        
    def get_number_of_tours(self):
        """get_number_of_tours()
        
        returns the number of tours in the data"""
        return len(self._tour_boundaries)
        
    def _find_tour_boundaries(self):
        """_find_tour_boundaries() -> void
            
        find boundaries (start & end) of all tours in the data"""
        self._tour_boundaries = []
        for index in range(0, len(self._tourdata)):
            block = self._tourdata[index]
            if block[2:] == 'AA':
                # tourStart found
                tour_start = index
                tour_end = self._find_tour_end(tour_start)
                self._tour_boundaries.append((tour_start, tour_end))
    
    def _find_tour_end(self, tour_start):
        """find_tour_end(tour_start) -> integer
        
        find end of tour started at tour_start"""
        search_index = tour_start
        while 1:
            search_index += 8
            if search_index >= len(self._tourdata):
                search_index = search_index - len(self._tourdata)
            if self._tourdata[search_index][2:] == 'DD':
                # end of your found
                break
        return search_index
        
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
            
        
        
    
        
    
        
    