# -*- coding: utf-8 -*-
import threading
import logging

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kargs):
        threading.Thread.__init__(self, *args, **kargs)
        logging.warn('%s will init', self.name)
        self.stop_event = threading.Event()

    def stop(self):
        logging.warn('%s will stop', self.name)
        if self.isAlive():
            self.stop_event.set()
            self.join()
