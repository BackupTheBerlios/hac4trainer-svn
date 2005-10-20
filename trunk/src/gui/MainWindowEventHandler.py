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

