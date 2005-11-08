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
"""Implements the GUI class for HAC4 Trainer"""

# make sure we can import our own packages
import sys
sys.path.append('..')

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
        self.mainWindowHandler = MainWindowEventHandler(self.application, self.widgets)
        self.treeViewEventHandler = TreeViewEventHandler(self.application, self.widgets)
        
    def run(self):
    	self.application.start()

if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG)
    sys.path.append('..')
    controller = Controller()
    controller.run()
