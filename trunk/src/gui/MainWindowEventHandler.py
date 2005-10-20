"""MainWindowEventHandler

author: Ilja Booij (ibooij@gmail.com)
date: 30-09-2005


handles all events sent at the main window. This mostly has to 
do with stuff like the closing of the window.
"""
from HAC4TrainerEventHandler import HAC4TrainerEventHandler
import gtk
import logging


class MainWindowEventHandler(HAC4TrainerEventHandler):
    """implements event handlers for mainWindow gtk events
    
    This class subclasses HAC4TrainerEventHandler which it
    uses to get the application context etc"""
    
    def __init__(self, application, widgets):
    	"""Create a new event handling class for the Main Window,
    	and connect the signals"""
        HAC4TrainerEventHandler.__init__(self, application, widgets)
        self._widgets = widgets
        self._window = widgets.get_widget("mainWindow")
        self._window.set_title("BLA")

    def signals_connect(self, widgets):
        widgets.signal_connect("on_mainWindow_destroy_event", 
		    self.on_mainWindow_destroy_event)
        widgets.signal_connect("on_import_from_file_activate",
            self.on_import_from_file_activate)                   
         
    def on_mainWindow_delete_event(self, window, event):
        self.getApplication().quit()
   
    def on_mainWindow_destroy_event(self,window, event):
       	self.getApplication().quit() 

    def on_import_from_file_activate(self, window, data = None):
        file_chooser = self._widgets.get_widget('dialog_import_from_file')
        
        filter = gtk.FileFilter()
        filter.set_name('All Files')
        filter.add_pattern('*')
        file_chooser.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name('HAC4 data files')
        filter.add_pattern('*.dat')
        file_chooser.add_filter(filter)
        
        response = file_chooser.run()
        if response == gtk.RESPONSE_OK:
            logging.debug(file_chooser.get_filename() + ' selected')
            self.getApplication().import_from_file(file_chooser.get_filename())
        else:
            logging.debug('no filename selected')
        #file_chooser.destroy()
        file_chooser.hide()

