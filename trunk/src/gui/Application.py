"""Main application."""
import logging

class ApplicationDispatcher:
    """Main application class. This is used to dispatch from the GUI to
    the backend application (and back in some cases)"""
    def __init__(self):
        self._tours = []
        self._tour_list_listeners = []
    
    def import_from_file(self, filename):
        import importer.HAC4FileImporter# import HAC4Fileimporter
        try:
            fileImporter = importer.HAC4FileImporter.HAC4FileImporter(filename)
            self._tours += fileImporter.doImport()
            self.notify_tour_list_observers()
        except importer.HAC4Importer.HAC4DataLengthError, e:
            return "error, wrong datalength"
        except Exception, e:
            print e
    
    def getTours(self):
        return self._tours
        
    def add_tour_list_observer(self, listener):    
        if listener not in self._tour_list_listeners:
            self._tour_list_listeners.append(listener)
    
    def notify_tour_list_observers(self):
        for listener in self._tour_list_listeners:
            listener.notify_tour_list()
    