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

from HAC4TrainerEventHandler import HAC4TrainerEventHandler

import gtk
import logging
from time import strftime

class TreeViewEventHandler(HAC4TrainerEventHandler):
    
    def __init__(self, application, widgets):
        self._treeView = None
        self._tourIterMap = {}
        HAC4TrainerEventHandler.__init__(self, application, widgets)
       
    def signals_connect(self, widgets):
        selection = self.get_selection().connect("changed", self.on_selection)
        
    def get_view(self):
        if self._treeView == None:
            self.init_tree_view()
        return self._treeView
    
    def get_store(self):
        return self.get_view().get_model()
    
    def get_selection(self):
        return self.get_view().get_selection()
    
    def init_tree_view(self):
        self._treeView = self.getWidgets().get_widget('date_tree_view')
        
        treeStore = gtk.TreeStore(str)
        self.get_view().set_model(treeStore)
        
        treeViewColumn = gtk.TreeViewColumn('Date')
        self.get_view().append_column(treeViewColumn)
        
        cellRenderer = gtk.CellRendererText()
        treeViewColumn.pack_start(cellRenderer, True)
        treeViewColumn.add_attribute(cellRenderer, 'text', 0)
    
        # init the tree selection stuff
        self.init_tree_selection()
        
        self.getApplication().add_tour_list_observer(self)
    
    def init_tree_selection(self):
        treeSelection = self.get_view().get_selection()
        treeSelection.set_mode(gtk.SELECTION_SINGLE)
        
    def notify_tour_list(self):
        """After a change in the tour list, we have to redraw the tour tree
        view"""
        
        # clear the tree and get the new tours
        treeStore = self.get_view().get_model()
        treeStore.clear()
        tours = self.getApplication().getTours()
        
        years_iter = {}
        months_iter = {}
        
        for tour in tours:
            # add year nodes
            startTime = tour.getStartTime()
            year = startTime.year
            if year not in years_iter.keys():
                iterator = treeStore.append(None, [repr(year)])
                years_iter[year] = iterator
            # add month nodes
            month = startTime.month
            if "%d/%d" % (year, month) not in months_iter.keys():
                month_str = strftime("%B", startTime.timetuple())
                iterator = treeStore.append(years_iter[year],
                        [month_str])
                months_iter["%d/%d" % (year, month)] = iterator
            
            
            startTime_str = strftime("%A, %d, %H:%M", startTime.timetuple())
            iter = treeStore.append(months_iter["%d/%d" % (year, month)],
                                         [startTime_str])
            self._tourIterMap[iter] = tour
            print self.get_store().get_path(iter), iter
    
    def on_selection(self, selection):
        logging.debug("made a selection in the treeView")
        (model, iter) = selection.get_selected()
        for (key, value) in self._tourIterMap.items():
            print value, key
            
        print self._tourIterMap[iter]
        print self.get_store().get_path(iter)
        print self.get_store().get_path(self.get_store().iter_parent(iter))
        print self.get_store().get(iter, 0)
#        print 'selected tour = %s' % (repr(self._tourIterMap[iter]))