#!/usr/bin/env python
#-*- coding: utf-8 -*-

import getopt

from keycatch import *
from ThreadWindow import ThreadWindow
import log

list_keys = ['', 'left_shift', 'right_shift', 'left_ctrl', 'right_ctrl', 'left_alt', 'right_alt']

glkey = 'left_alt'
glchar = 'q'
glxx = 1
glyy = 1

def usage(res):
    out = ("""Usage:
  ./Library_of_mind.py <OPTS>
  -h         | --help           this help
  -k <key>   | --key <key>      keyboard shortcut
  -m <multi> | --move <multi>   position in window
  -d         | --debug          debug

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
        opts, args = getopt.getopt(sys.argv[1:], "hk:m:d",
                                   ["help","key=", "move=", "--debug"])
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
        elif opt in ("-d", "--debug"):
            log.debug = True




def startWindow(modifiers, keys):
    if (modifiers[glkey] == True) and (keys == glchar):
        args= {
               'x' : glxx,
               'y' : glyy}
        log.LOG("BEGIN Thread")
        thread = ThreadWindow(args)
        thread.start()
        log.LOG("RUN Thread")
        thread.join()
        log.LOG("END Thread")

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
