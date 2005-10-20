"""Implements the GUI class for HAC4 Trainer"""

import gtk
import gtk.glade

from GtkApplication import GtkApplication
from MainWindowEventHandler import MainWindowEventHandler
from TreeViewEventHandler import TreeViewEventHandler

import logging
DEFAULT_GLADE_FILENAME = 'hac4trainer.glade'

class Controller:
    def __init__(self, xmlFileName = DEFAULT_GLADE_FILENAME):
        self.widgets = gtk.glade.XML(xmlFileName)
        self.application = GtkApplication(self.widgets)
        mainWindowHandler = MainWindowEventHandler(self.application, self.widgets)
        treeViewEventHandler = TreeViewEventHandler(self.application, self.widgets)
        
    def run(self):
    	self.application.start()

if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG)
    sys.path.append('..')
    controller = Controller()
    controller.run()
