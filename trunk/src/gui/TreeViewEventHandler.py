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
import gobject
import logging
from time import strftime

class TreeViewEventHandler(HAC4TrainerEventHandler):
    
    def __init__(self, application, widgets):
        self._treeView = None
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
        self._treeView = self.get_widgets().get_widget('date_tree_view')
        
        treeStore = gtk.TreeStore(gobject.TYPE_PYOBJECT, 
             gobject.TYPE_STRING, # date string
             gobject.TYPE_STRING, # type of tour
             gobject.TYPE_STRING, # distance
             gobject.TYPE_STRING, # time
             gobject.TYPE_STRING, # moving time
             gobject.TYPE_STRING  # speed
        )
        self.get_view().set_model(treeStore)
        
        # Add Date column (1st)
        dateColumn = gtk.TreeViewColumn('Date')
        self.get_view().append_column(dateColumn)
        date_renderer = gtk.CellRendererText()
        dateColumn.pack_start(date_renderer, True)
        dateColumn.add_attribute(date_renderer, 'text', 1)
        # Add Type column (2nd)
        typeColumn = gtk.TreeViewColumn('Type')
        self.get_view().append_column(typeColumn)
        type_renderer = gtk.CellRendererText()
        typeColumn.pack_start(type_renderer, True)
        typeColumn.add_attribute(type_renderer, 'text', 2)
        # Add Distance column (3rd)
        distanceColumn = gtk.TreeViewColumn('Distance')
        self.get_view().append_column(distanceColumn)
        distance_renderer = gtk.CellRendererText()
        distanceColumn.pack_start(distance_renderer, True)
        distanceColumn.add_attribute(distance_renderer, 'text', 3)
        # Add Time column (4rd)
        timeColumn = gtk.TreeViewColumn('Recording Time')
        self.get_view().append_column(timeColumn)
        time_renderer = gtk.CellRendererText()
        timeColumn.pack_start(time_renderer, True)
        timeColumn.add_attribute(time_renderer, 'text', 4)
        # Add Moving Time column (4rd)
        movingTimeColumn = gtk.TreeViewColumn('Moving Time')
        self.get_view().append_column(movingTimeColumn)
        time_renderer = gtk.CellRendererText()
        movingTimeColumn.pack_start(time_renderer, True)
        movingTimeColumn.add_attribute(time_renderer, 'text', 5)
         # Add Speed column (5th)
        speedColumn = gtk.TreeViewColumn('Speed')
        self.get_view().append_column(speedColumn)
        speed_renderer = gtk.CellRendererText()
        speedColumn.pack_start(speed_renderer, True)
        speedColumn.add_attribute(speed_renderer, 'text', 6)
        # init the tree selection stuff
        self.init_tree_selection()
        
        self.get_application().add_tour_list_observer(self)
    
    def init_tree_selection(self):
        treeSelection = self.get_view().get_selection()
        treeSelection.set_mode(gtk.SELECTION_SINGLE)
        
    def notify_tour_list(self):
        """After a change in the tour list, we have to redraw the tour tree
        view"""
        
        # clear the tree and get the new tours
        treeStore = self.get_view().get_model()
        treeStore.clear()
        tours= self.get_application().get_tour_list().get_tours()
        
        years_iter = {}
        months_iter = {}
        
        for tour in tours:
            try:
                row = [None, None, None, None, None, None, None]
                # add year nodes
                startTime = tour.getStartTime()
                year = startTime.year
                if year not in years_iter.keys():
                    row[1] = repr(year)
                    iterator = treeStore.append(None, row)
                    years_iter[year] = iterator
                # add month nodes
                month = startTime.month
                if "%d/%d" % (year, month) not in months_iter.keys():
                    month_str = strftime("%B", startTime.timetuple())
                    row[1] = month_str
                    iterator = treeStore.append(years_iter[year], row)
                    months_iter["%d/%d" % (year, month)] = iterator
                
                row[0] = tour
                row[1] = strftime("%A, %d, %H:%M", startTime.timetuple())
                row[2] = tour.getTypeString()
                row[3] = "%.1f km" % (tour.getTotalDistance())
                row[4] = str(tour.getRecordingTime())
                row[5] = str(tour.getMovingRecordingTime())
                row[6] = "%.1f km/h" % (tour.getAverageSpeedCorrected())
    
                treeStore.append(months_iter["%d/%d" % (year, month)],
                                             row)
            except Exception, e:
                 print e
        self._treeView.expand_all()
    
    def on_selection(self, selection):
        logging.debug("made a selection in the treeView")
        (model, iter) = selection.get_selected()
        try:
            selected_tour = self.get_view().get_model().get_value(iter, 0)
            if selected_tour != None:
                self.get_application().set_selected_tour(selected_tour)
                print self.get_application().get_selected_tour()
        except IndexError, e:
            # non-leaf node selected.
            pass
       
#        print 'selected tour = %s' % (repr(self._tourIterMap[iter]))