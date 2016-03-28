from threading import Thread

from IWindow import getWindow
import log

class ThreadWindow(Thread):
    def __init__(self, args):
        Thread.__init__(self)
        self.args = args

    def run(self):
        log.LOG("IN thread window")
        self.window = getWindow(self.args)
        self.window.main()
