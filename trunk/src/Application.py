#Copyright (c) 2005, Ilja Booij (ibooij@gmail.com)
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or 
#without modification, are permitted provided that the following 
#conditions are met:
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
__revision__ = "$Rev$"
import logging
from model.HAC4TourList import HAC4TourList

class ApplicationDispatcher:
    """Main application class. This is used to dispatch from the GUI to
    the backend application (and back in some cases)"""
    def __init__(self):
        self._tours = HAC4TourList()
        self._tours_changed = 0
        self._tour_list_observers = []
        self._save_filename_observers = []
        self._selected_tour_observers = []
        self._save_filename = None
        self._selected_tour = None
    
    def import_from_file(self, filename):
        """import new tours from a raw data file

        return 1 if successfull
        return 0 if not successfull"""
        import importer.HAC4FileImporter# import HAC4Fileimporter
        try:
            file_importer = importer.HAC4FileImporter.HAC4FileImporter(filename)
            nr_tours_changed = self._tours.merge_tours(file_importer.do_import())
            if nr_tours_changed > 0:
                self.notify_tour_list_observers()
                self._tours_changed = 1 
            
        except importer.HAC4Importer.HAC4DataLengthError, exception:
            return 0 
         
        except Exception, exception:
            logging.error(repr(exception))
        return 1
    
    def get_tour_list(self):
        """get the current tours list, which is of type model.HAC4TourList"""
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
        self._tours_changed = 0
    
    def open_tour_list(self):
        """save the tour list to a file
    
        return 1 if succesful
        return 0 if not succesful"""
        from fileops.PickleTourListIO import PickleTourListIO, TourLoadingError
        file_reader = PickleTourListIO()
        try:
            self._tours = file_reader.read_tour_list(self.get_save_filename())
        except TourLoadingError:
            return 0
        self.notify_tour_list_observers()
        self._tours_changed = 0
        return 1
        
    def add_tour_list_observer(self, observer):    
        """add an observer for the tour list"""
        if observer not in self._tour_list_observers:
            self._tour_list_observers.append(observer)
    
    def notify_tour_list_observers(self):
        """notify all tour list observers of a change"""
        for listener in self._tour_list_observers:
            listener.notify_tour_list()
    
    def add_save_filename_observer(self, observer):
        """add an observer for the name of the current save file"""
        if observer not in self._save_filename_observers:
            self._save_filename_observers.append(observer)
            
    def notify_save_filename_observers(self):
        """notify all observers of the current save filename"""
        for observer in self._save_filename_observers:
            observer.notify_save_filename()
    
    def add_selected_tour_observer(self, observer):
        """add_selected_tour_observer(observer) -> void
        
        add an observer for the selected tour"""
        if observer not in self._selected_tour_observers:
            self._selected_tour_observers.append(observer)
    
    def notify_selected_tour_observers(self):
        """notify_selected_tour_observers()
        
        notify all observers of the selected tour of a change"""
        for observer in self._selected_tour_observers:
            observer.notify_selected_tour()
            
    def set_selected_tour(self, tour):
        """set_selected_tour(tour) -> void
        
        set which tour is selected"""
        self._selected_tour = tour
        self.notify_selected_tour_observers()
    
    def get_selected_tour(self):
        """get the currently selected tour"""
        return self._selected_tour
    
    def is_tours_changed(self):
        """is_tours_changed() -> boolean"""
        return self._tours_changed == 1 
