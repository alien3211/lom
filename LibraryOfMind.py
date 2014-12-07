#!/usr/bin/env python
#-*- coding: utf-8 -*-

import lomSQL
import re
import Tkinter as TK

def print_help():
    pass

def check_arguments():
    pass

class BaseLOMclass():

    def __init__(self):
        pass
    def makeARGV(self):
        pass

class tkWindow():
    def __init__(self,name):
        self.root = TK.Tk()
        self.root.title(name)
        TK.Label(text="Add or Edit record", fg="blue", font="Times 16").pack()
        TK.Label(text="Name", width=15, anchor='w').pack(side=TK.LEFT)
        self.ename = TK.Entry(self.root)
        self.ename.pack(side=TK.RIGHT, expand=TK.YES, fill=TK.X)



if __name__ == '__main__':
    
    import getopt
    import sys
    import os

    print '\n\n'

    operation = None

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],'aesh')
    except getopt.GetoptError:
        print_help()

    for opt, arg in opts:
        if opt in '-a':
            print 'add record'
            print args

        elif opt in '-e':
            print 'edit record'

        elif opt in '-s':
            print 'search record'
