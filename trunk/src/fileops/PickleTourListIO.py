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
import cPickle
import logging

class PickleTourListIO:
    """use pickle to write a list of tours."""
    
    def __init__(self):
        pass
    
    def write_tour_list(self, tours, filename):
        """write_tour_list(tours, filename)
        write a list of tours to file filename. 
        TODO: This method needs to catch exception from file() and 
        from the import pickle methods
        
        returns void"""
        write_file = file(filename, 'wb')
        cPickle.dump(tours, write_file)
        write_file.close()
    
    def read_tour_list(self, filename):
        """read_tour_list(filename)
        
        read a list of tours from a filename.
        
        returns: TourList object or none if there's an error"""
        try:
            read_file = file(filename, 'rb')
        except IOError, e:
            logging.error("Error opening file [%s]. It probably does not exist",
                           filename)
            return None
        
        tours = cPickle.load(read_file)
        read_file.close()
        
        return tours
    
        
        
        