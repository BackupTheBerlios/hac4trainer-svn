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

class HAC4TourList:
    """implements a list of tours"""
    def __init__(self, tours = []):
        self._tours = tours
        self._tours.sort()
        self._tour_datetime_map = {}
        self._update_datetime_map()
    
    def merge_tours(self, new_tours):
        """merge(tours)
        
        merge new_tours with the tours currently stored so no double tours are
        stored. It returns the number of tours added."""
        original_size = len(self._tours)
        for tour in new_tours:
            start_time = tour.getStartTime()
            if start_time not in self._tour_datetime_map.keys():
                self._tours.append(tour)
        new_size = len(self._tours)
        
        self._tours.sort()
        self._update_datetime_map()
        return new_size - original_size
    
    def get_tours(self):
        """get list of tours"""
        return self._tours
    
    def _update_datetime_map(self):
        """update the datetime map with the tours currently stored"""
        self._tour_datetime_map = {}
        
        for tour in self._tours:
            self._tour_datetime_map[tour.getStartTime()] = tour
        