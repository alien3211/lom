import time
import sys
from datetime import datetime

this = sys.modules[__name__]  

this.debug = False

def LOG(message):
    if this.debug:
        __log(message)

def __log(message):
        now = datetime.now().strftime("%H:%M:%S")
        print "%s %s" % (now, message)
