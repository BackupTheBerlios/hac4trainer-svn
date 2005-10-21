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
sys.path.append('')

import unittest
import cPickle
import os
from PickleTourListIO import PickleTourListIO

TEST_DATA_FILE = 'testfile.hdf'
IMPORT_FILE = '../data/testdatafile.dat'

class PickleTourListWriteTestCase(unittest.TestCase):
    """Test Writer part"""
    
    def setUp(self):
        self.tourListIO = PickleTourListIO()
    
    def testWrite(self):
        """test if we can write a list of integers correctly"""
        tours = [1,2,3] # it does not matter that this is not a real tour list
        self.tourListIO.write_tour_list(tours, TEST_DATA_FILE)
        
        # verify contents
        data_file = file(TEST_DATA_FILE, 'rb')
        tours_read = cPickle.load(data_file)
        data_file.close()
        os.remove(TEST_DATA_FILE)
        
        self.assertEqual(tours, tours_read)
    
    def testWriteRealTours(self):
        from importer.HAC4FileImporter import HAC4FileImporter
        file_importer = HAC4FileImporter(IMPORT_FILE)
        from model.HAC4TourList import HAC4TourList
        tourList = HAC4TourList(file_importer.doImport())
        
        self.tourListIO.write_tour_list(tourList, TEST_DATA_FILE)
        
        #verify
        data_file = file(TEST_DATA_FILE, 'rb')
        tourListRead = cPickle.load(data_file)
        data_file.close()
        os.remove(TEST_DATA_FILE)
        
        self.assertEqual(tourList.get_tours(), tourListRead.get_tours())
        
class PickleTourListReadTestCase(unittest.TestCase):
    """Test Reader part"""
    
    def setUp(self):
        self.tourListIO = PickleTourListIO()
    
    def testRead(self):
        """test if we can read a list of integers correctly"""
        tours = [1,2,3]
        
        # write tours to a file
        data_file = file(TEST_DATA_FILE, 'wb')
        cPickle.dump(tours, data_file)
        data_file.close()
        
        # verify
        tours_read = self.tourListIO.read_tour_list(TEST_DATA_FILE)
        os.remove(TEST_DATA_FILE)
        
        self.assertEqual(tours, tours_read)
    
    def testWriteTourList(self):
        from importer.HAC4FileImporter import HAC4FileImporter
        file_importer = HAC4FileImporter(IMPORT_FILE)
        from model.HAC4TourList import HAC4TourList
        tourList = HAC4TourList(file_importer.doImport())
        
        # write tours to a file
        data_file = file(TEST_DATA_FILE, 'wb')
        cPickle.dump(tourList, data_file)
        data_file.close()
        
        tourListRead = self.tourListIO.read_tour_list(TEST_DATA_FILE)
        
        os.remove(TEST_DATA_FILE)
        
        self.assertEqual(tourList.get_tours(), tourListRead.get_tours())
        
if __name__ == '__main__':
    import sys
    sys.path.append('..')
    unittest.main()