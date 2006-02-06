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
"""MainWindowEventHandler

author: Ilja Booij (ibooij@gmail.com)
date: 30-09-2005


handles all events sent at the main window. This mostly has to 
do with stuff like the closing of the window.
"""
from HAC4TrainerEventHandler import HAC4TrainerEventHandler
import gtk
import gobject
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
        self._set_title()
        self.get_application().add_save_filename_observer(self)

    def signals_connect(self, widgets):
        widgets.signal_connect("on_mainWindow_destroy_event", 
		    self.on_mainWindow_destroy_event)
        widgets.signal_connect("on_import_from_file_activate",
            self.on_import_from_file_activate)
        widgets.signal_connect("on_save_as_tour_list_activate",
            self.on_save_as_tour_list_activate)
        widgets.signal_connect("on_save_tour_list_activate",
            self.on_save_tour_list_activate)
        widgets.signal_connect("on_open_tour_list_activate",
            self.on_open_tour_list_activate)
        widgets.signal_connect("on_export_to_tur_activate",
            self.on_export_to_tur_activate)
        widgets.signal_connect("on_import_from_watch_activate",
            self.on_import_from_watch_activate)
         
    def on_mainWindow_delete_event(self, window, event):
        self.get_application().quit()
   
    def on_mainWindow_destroy_event(self,window, event):
       	self.get_application().quit() 

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
            self.get_application().import_from_file(file_chooser.get_filename())
        else:
            logging.debug('no filename selected')
        #file_chooser.destroy()
        file_chooser.hide()
    
    def on_import_from_watch_activate(self, window, data = None):
        """start import from watch"""
        status_window = self._widgets.get_widget('window_import_from_watch')
        
        status_label = self._widgets.get_widget('label_import_from_watch')
        status_label.set_text('Waiting for data')
        progress_bar = self._widgets.get_widget('progress_bar_import_from_watch')
        progress_bar.set_fraction(0.0)
        
        status_window.show()
        
        self.get_application().start_import_from_watch()
        self.import_usb_timer = gobject.timeout_add(100, self.get_application().monitor_import_from_watch, self.import_from_watch_update)
    
    def import_from_watch_update(self, is_receiving, progress):
        """this is to be called by the function that is importing from
        the watch"""
        progress_bar = self._widgets.get_widget('progress_bar_import_from_watch')
        progress_bar.set_fraction(0.0)
        
        if is_receiving:
            status_label = self._widgets.get_widget('label_import_from_watch')
            status_label.set_text('Receiving data')
        

    def on_save_as_tour_list_activate(self, window, data = None):
        file_chooser = self._widgets.get_widget('dialog_save_tour_list')
      
        response = file_chooser.run()
        file_chooser.hide()
        if response == gtk.RESPONSE_OK:
            logging.debug(file_chooser.get_filename() + ' selected')
            self.get_application().set_save_filename(file_chooser.get_filename())
            self.get_application().save_tour_list()

        else:
            logging.debug('no filename selected')
        #file_chooser.destroy()
        
    def on_export_to_tur_activate(self, window, data = None):
        file_chooser = self._widgets.get_widget('dialog_export_tur')
        
        # set filename standard to date.tur
        tour = self._application.get_selected_tour()
        date = tour.getStartTime()
        filename = "%4d-%02d-%02d_%02d:%02d.tur" % (date.year, date.month, date.day, date.hour, date.minute)
        file_chooser.set_current_name(filename)
        response = file_chooser.run()
        file_chooser.hide()
        if response == gtk.RESPONSE_OK:
            logging.debug(file_chooser.get_filename() + ' selected')
            self.get_application().export_tour(file_chooser.get_filename())
        else:
            logging.debug('no filename selected')
            
    def on_save_tour_list_activate(self, window, data = None):
        if self.get_application().get_save_filename() == None:
            self.on_save_as_tour_list_activate(window, data)
        else:
            self.get_application().save_tour_list()
    
    def on_open_tour_list_activate(self, window, data = None):
        file_chooser = self._widgets.get_widget('dialog_open_tour_list')
        
        filter = gtk.FileFilter()
        filter.set_name('HAC4Trainer files')
        filter.add_pattern('*.hdf')
        file_chooser.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name('All Files')
        filter.add_pattern('*')
        file_chooser.add_filter(filter)
        
        is_file_opened_succesfully = 1
        response = file_chooser.run()
        if response == gtk.RESPONSE_OK:
            logging.debug(file_chooser.get_filename() + ' selected')
            self.get_application().set_save_filename(file_chooser.get_filename())
            is_file_opened_succesfully = self.get_application().open_tour_list()
                
        else:
            logging.debug('no filename selected')
        #file_chooser.destroy()
        file_chooser.hide()

        if not is_file_opened_succesfully:
            dialog = self._widgets.get_widget('dialog_error_opening_file')
            response = dialog.run()
            dialog.hide()
    
    def _set_title(self):
        filename = self.get_application().get_save_filename()
        if filename == None:
            filename = 'None'
        self._window.set_title('HAC4Trainer - ' + filename)
        
    def notify_save_filename(self):
        self._set_title()
