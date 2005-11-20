#!/usr/bin/env python

print "starting"
import logging
logging.basicConfig(level=logging.DEBUG)

from gui.MainGui import Controller
controller = Controller()
controller.run()