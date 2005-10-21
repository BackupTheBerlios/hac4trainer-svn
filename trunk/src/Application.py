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

"""Main application."""
import logging
from model.HAC4TourList import HAC4TourList

class ApplicationDispatcher:
    """Main application class. This is used to dispatch from the GUI to
    the backend application (and back in some cases)"""
    def __init__(self):
        self._tours = HAC4TourList()
        self._tour_list_observers = []
        self._save_filename_observers = []
        self._save_filename = None
    
    def import_from_file(self, filename):
        import importer.HAC4FileImporter# import HAC4Fileimporter
        try:
            fileImporter = importer.HAC4FileImporter.HAC4FileImporter(filename)
            self._tours.merge_tours(fileImporter.doImport())
            self.notify_tour_list_observers()
        except importer.HAC4Importer.HAC4DataLengthError, e:
            return "error, wrong datalength"
        except Exception, e:
            print e
    
    def get_tour_list(self):
        return self._tours
    
    def get_save_filename(self):
        """get the filename we save under by default"""
        return self._save_filename
    
    def set_save_filename(self, filename):
        """set the filename we save under by default"""
        self._save_filename = filename
        self.notify_save_filename_observers()
        
    def save_tour_list(self):
        """save the tour list to a file"""
        from fileops.PickleTourListIO import PickleTourListIO
        file_writer = PickleTourListIO()
        file_writer.write_tour_list(self._tours, self.get_save_filename())
    
    def open_tour_list(self):
        """save the tour list to a file"""
        from fileops.PickleTourListIO import PickleTourListIO
        file_reader = PickleTourListIO()
        self._tours = file_reader.read_tour_list(self.get_save_filename())
        self.notify_tour_list_observers()
        
    def add_tour_list_observer(self, observer):    
        if observer not in self._tour_list_observers:
            self._tour_list_observers.append(observer)
    
    def notify_tour_list_observers(self):
        for listener in self._tour_list_observers:
            listener.notify_tour_list()
    
    def add_save_filename_observer(self, observer):
        if observer not in self._save_filename_observers:
            self._save_filename_observers.append(observer)
            
    def notify_save_filename_observers(self):
        for observer in self._save_filename_observers:
            observer.notify_save_filename()
    