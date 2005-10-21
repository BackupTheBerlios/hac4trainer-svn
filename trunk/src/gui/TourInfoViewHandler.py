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
"""handles the text view widget holding information on the tour"""
__revision__ = '$Rev$'

from HAC4TrainerEventHandler import HAC4TrainerEventHandler
import gtk
import logging

class TourInfoViewHandler(HAC4TrainerEventHandler):
    """handler for the TourTextView widget"""
    
    def __init__(self, application, widgets):
        HAC4TrainerEventHandler.__init__(self,application, widgets)
        
        self.get_application().add_selected_tour_observer(self)
        self.init_text_view()
    
    def signals_connect(self, widgets):
        pass
    
    def init_text_view(self):
        pass
    
    def set_label(self, label_string, value_string):
        label = self.get_widgets().get_widget(label_string)
        label.set_label(value_string)
        
    def set_weight_label(self, tour):
        self.set_label('weight_value_label', "%d kg" % (tour.getWeight()))
    
    def set_distance_label(self, tour):
        self.set_label('distance_value_label', "%d km" % (tour.getTotalDistance()))
    
    def set_date_label(self, tour):
        from time import strftime
        date_string = strftime("%A, %d, %H:%M", tour.getStartTime().timetuple())
        self.set_label('date_value_label', date_string)
    def notify_selected_tour(self):
        tour = self.get_application().get_selected_tour()
        self.set_weight_label(tour)
        self.set_distance_label(tour)
        self.set_date_label(tour)
        
        
    
    