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
        self._tourBoundaries = []
        self._tours = []
           
    def read(self, data):
        self._tourdata = data[TOURS_BEGIN:TOURS_END]
        self._findTourBoundaries()
        tours = []
        
        for tourBoundary in self._tourBoundaries:
            if tourBoundary[0] < tourBoundary[1]:
                singleTourData = self._tourdata[tourBoundary[0]: tourBoundary[1]]
            else:
                singleTourData = self._tourdata[tourBoundary[0]:] + self._tourdata[:tourBoundary[1]]
            assert(len(singleTourData) % 8 == 0)
            from model.HAC4TourFactory import HAC4TourFactory
            tourFactory = HAC4TourFactory(self._year)
            tours.append(tourFactory.constructTour(singleTourData, 
                          self._weight))
        
        tours.sort()
        return tours
        
    def getNumberOfTours(self):
        return len(self._tourBoundaries)
        
    def _findTourBoundaries(self):
        self.tourBoundaries = []
        for index in range(0, len(self._tourdata)):
            block = self._tourdata[index]
            if block[2:] == 'AA':
                # tourStart found
                tourStart = index
                tourEnd = self._findTourEnd(tourStart)
                self._tourBoundaries.append((tourStart, tourEnd))
    
    def _findTourEnd(self, tourStart):
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
            
        
        
    
        
    
        
    