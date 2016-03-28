#!/usr/bin/env python
#-*- coding: utf-8 -*-

import log

import pygtk
pygtk.require('2.0')
import gtk
import pango

class Window(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("Library Of Mind")

        #initialization window
        self.set_border_width(10)
        self.set_size_request(500,750)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("delete-event", gtk.main_quit)
        self.show_all()

    def main(self):
        "Run main loop"
        gtk.main()

    def gtk_quit(self):
        "Terminate Window"
        gtk.main_quit()

    def parserArgs(args):

        rest = arg.split()
        command = rest.pop(-1)

        if command in ['help', 'h']:
            return getHelp(rest)
        elif command in ['set']:
            return setOption(rest)
        elif command in ['search', 's']:
            return search(rest)
        elif command in ['add','a']:
            return addRecord()
        elif command in ['update', 'u']:
            return updateRecord(rest)
        elif command in ['type', 't']:
            return getType(rest)
        elif command in ['key', 'k']:
            return getKey(rest)
        elif command in ['news', 'n']:
            return getNews(rest)
        elif command.isdigit():
            return getDigit(int(command))

    def getHelp(com):

        return ConMySQL.getHelp(com)

    def search(com):
        pass

    def addRecord(com):
        pass

    def getType(com):

        if com:
            return ConMySQL.getType(com)
        else:
            return ConMySQL,getType()

    def getKey(com):

        if com:
            return ConMySQL.getKey(com)
        else:
            return ConMySQL,getKey()

    def getNews(com):
        pass

    def getDigit(com):
        pass
