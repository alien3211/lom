#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import getopt
from time import sleep
from threading import Thread

from keycatch import *

list_keys = ['', 'left_shift', 'right_shift', 'left_ctrl', 'right_ctrl', 'left_alt', 'right_alt']

glkey = 'left_alt'
glchar = 'q'
glxx = 1
glyy = 1

def usage(res):
    out = ("""Usage:
  ./Library_of_mind.py <OPTS>
  -h         | --help           this help
  -f <from>  | --from <from>    original language
  -t <to>    | --to <to>        destination language
  -l         | --list           list language
  -k <key>   | --key <key>      keyboard shortcut
  -c <time>  | --count <time>   long the active window (s)
  -m <multi> | --move <multi>   position in window

  Example:
  ./translateTool.py -f en -t pl

  Example change key:
  [key+char] default 'left_alt+q'
  ./translateTool.py -f en -t pl -k 'left_alt+q'

  Example position:
  'x:y' default rigth button window '1:1'
  left top window     '0:0'
  right top window    '1:0'
  left button window  '0:1'
  rigth button window '1:1'

  2 window:
  	firts window
  left top window     '0:0'
  right top window    '0.5:0'
  left button window  '0:1'
  rigth button window '0.5:1'

  	secend window
  left top window     '0:0'
  right top window    '1:0'
  left button window  '0:1'
  rigth button window '1:1'

  ./translateTool.py -m 1:1

  All key: """)
    print out
    print '\n  '.join(list_keys)
    sys.exit(res)


def parseKey(arg):
    global glkey, glchar
    arg = arg.split('+')
    if len(arg) == 2:
        if arg[0] in list_keys:
            glkey, glchar = arg
        else:
            usage(2)
    else:
        usage(2)


def parseMove(arg):
    global glxx, glyy
    glxx, glyy = arg.split(':')


def parseArgs():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hk:m:",
                                   ["help","key=", "move="])
    except getopt.GetoptError, err:
        usage(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(0)
            sys.exit()
        elif opt in ("-k", "--key"):
            parseKey(arg)
        elif opt in ("-m", "--move"):
            parseMove(arg)

class ThreadWindow(Thread):
    def __init__(self, x):
        Thread.__init__(self)
        self.x = x
    
    def run(self):
        sleep(self.x)
        print "WATEK RUSZONY %d -> %d" % (self.x, self.x**2)



def startWindow(modifiers, keys):
    if (modifiers[glkey] == True) and (keys == glchar):
        thread = ThreadWindow(2)
        thread.start()
        thread.join()
        print "ZACZYNA SIE!!!!" 

def main():
    parseArgs()

    sleep_interval=.005
    while True:
        sleep(sleep_interval)
        changed, modifiers, keys = fetch_keys()
        if changed:
            startWindow(modifiers, keys)



if __name__ == '__main__':
    main()
