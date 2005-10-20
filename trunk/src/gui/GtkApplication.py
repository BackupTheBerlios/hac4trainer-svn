"""Application class for GTK"""

import gtk
from Application import ApplicationDispatcher

class GtkApplication(ApplicationDispatcher):
    """Application class for GTK"""
    def __init__(self, widgets):
        ApplicationDispatcher.__init__(self)
        self._widgets = widgets

    def getWidgets(self):
        return self._widgets

    def start(self):
        gtk.main()

    def quit(self):
        gtk.main_quit()
    
