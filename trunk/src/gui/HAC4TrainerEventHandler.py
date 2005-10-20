class HAC4TrainerEventHandler:
    """Main event handler. Serves mainly as a way for all 
    event handlers to get the application context
    """
    
    def __init__(self, application, widgets):
        """Create a new HAC4TrainerEventHandler. This also calls
        the signal_connect() function for all subclasses"""
        self._application = application
        self._widgets = widgets
        self.signals_connect(widgets)

    def getApplication(self):
        """return the application"""
        return self._application
    
    def getWidgets(self):
        return self._widgets

