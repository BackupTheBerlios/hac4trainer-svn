import gtk
import gtk.glade
import gobject
import sys
sys.path.append("..")
from importer.HAC4USBImporter import HAC4USBImporter

DEFAULT_GLADE_FILE = 'USBImporter/usbimporter.glade'

class Controller:
    def __init__(self, glade_file = DEFAULT_GLADE_FILE):
        self.widgets = gtk.glade.XML(glade_file)
        self.init_widgets()
        
    def init_widgets(self):
        self._progress_bar = self.widgets.get_widget('progressbar1')
        self._progress_bar.set_fraction(0.0)
        self._go_button = self.widgets.get_widget('button1')
        self._go_button.connect("clicked", self.on_button1_clicked)
        
        
    def start(self):
        gtk.main()
    
    def on_button1_clicked(self, widget, data = None):
        """start "import" """
        self.importer = HAC4USBImporter()
        
        self._progress_bar.set_fraction(0.0)
        self._progress_bar.set_text('Waiting for data')
        
        # call self.update_import() every 100ms 
        gobject.timeout_add(100, self.update_import)
    
    def update_import(self):
        print 'attempting read'
        bytes_read = self.importer.attempt_read()
        
        if not self.importer.is_ready():
            if bytes_read == 0:
                progress_string = "Not receiving any data"
            else:
                progress_string = "Reading data (%d%%)" % (self.importer.get_progress() * 100)
            
            
            self._progress_bar.set_text(progress_string)    
            self._progress_bar.set_fraction(self.importer.get_progress())
            return True
        else:
            self._progress_bar.set_text('finished')
            self._progress_bar.set_fraction(1.0)
            print self.importer.get_data()
        
        
    
        
if __name__ == '__main__':
    
    c = Controller('usbimporter.glade')
    c.start()