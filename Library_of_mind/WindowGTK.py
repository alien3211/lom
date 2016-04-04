#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk as gtk
from gi.repository import Gdk
import log
from MySQL import ConMySQL
from AddRowWindowGTK import AddRowWindowGTK
import csv
import os

class Window():

    def __init__(self, configData={}):

            
        self.configData = configData
        self.configData['history'] = "~/.lom_history"
        self.configData['short'] = ['id', 'type', 'name', 'key_list']
        if not os.path.exists(self.configData['lomrc']):
            self.setConfig()
        self.component = {}

        # Parse glade XML
        self.gladefile = "Library_of_mind/MainWindow.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)

        # get object
        self.component['set'] = {}
        self.component['search'] = gtk.ListStore(int, str, str, str)
        self.component['update'] = gtk.ListStore(int, str, str, str)
        self.component['add'] = {}
        self.component['type'] = gtk.TreeStore(str, int)
        self.component['news'] = gtk.ListStore(int, str, str, str)
        self.component['keys'] = gtk.ListStore(str) 
        self.window = self.glade.get_object("window")
        self.gridMain = self.glade.get_object("gridMain")
        self.entryCommandLine = self.glade.get_object("entryCommandLine")
        self.labelText = None
        self.treeViewResult = None

        # initial window
        self.initialWindow()

        # show all object
        self.window.show_all()

        # check info
        self.initialInfo()

    def setConfig(self):

        w = csv.writer(open(self.configData['lomrc'], 'w'))
        for key, val in self.configData.items():
            w.writerow([key,val])

    def getConfig(self):
        
        for key, val in csv.reader(open(self.configData['lomrc'])):
            self.configData[key] = val

    def initialInfo(self):

        #get news
        rows = ConMySQL.getNews(self.configData['user'])

        if rows:
            self.print_error_message("%d news from last check" % len(rows))
            self.getNews()


    def initialWindow(self):

        self.window.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)

        self.window.set_size_request(460,244)
        self.window.set_keep_above(True)
        self.window.set_resizable(False)
        self.window.set_decorated(False)

        self.commonLayout()

    def __set_position(self):
        (w, h) = self.window.get_size()
        x = int(Gdk.Screen.get_default().get_width()*self.configData['x'])
        y = int(Gdk.Screen.get_default().get_height()*self.configData['y'])

        #Set position Left-Button
        self.window.move(x-w, y-h)
        log.LOG("(x,y) = (%s,%s)   (w,h) = (%s,%s)" % (x,y,w,h))

    def print_error_message(self, text="fill all fields"):

        md = gtk.MessageDialog(self.window, type=gtk.MessageType.ERROR, buttons=gtk.ButtonsType.OK)
        md.set_markup(text)
        md.run()
        md.destroy()

        return None

    def main(self):
        "Run main loop"
        gtk.main()

    def deleteEvent(self, widget, event):
        gtk.main_quit()

    def parserArgs(self, widget):

        arg = widget.get_text()
        rest = arg.split()
        command = rest.pop(0) if rest else ""

        self.commonLayout()

        if command in ['help', 'h']:
            self.getHelp(rest)
        elif command in ['set']:
            self.setOption(rest)
        elif command in ['search', 's']:
            self.search(rest)
        elif command in ['add','a']:
            self.addRecord(rest)
        elif command in ['update', 'u']:
            self.updateRecord(rest)
        elif command in ['type', 't']:
            log.LOG("GetType")
            self.getTypeTree(rest)
        elif command in ['key', 'k']:
            self.getKeysList(rest)
        elif command in ['news', 'n']:
            self.getNews()
        elif command in ['exit', 'bye']:
            gtk.main_quit()
            self.window.destroy()
        elif command.isdigit():
            self.getDigit(int(command))


    def commonLayout(self):

        self.entryCommandLine.set_text("")
        widget = self.gridMain.get_child_at(0,1)
        if widget != None:
            self.gridMain.remove(widget)

        self.__set_position()


    def labelLayout(self, text):

        log.LOG("Create Scroll")
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.ShadowType.IN)
        sw.set_size_request(450, 200)
        sw.set_can_focus(True)
        sw.set_visible(True)
        sw.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)
        self.gridMain.attach(sw,0,1,1,1)
        log.LOG("(0,1): %s" % self.gridMain.get_child_at(0,1))


        self.labelText = gtk.Label()
        self.labelText.set_size_request(450,200)
        self.labelText.set_text(text)
        self.labelText.set_visible(True)
        self.labelText.set_can_focus(True)
        sw.add(self.labelText)

        self.__set_position()


    def treeViewLayout(self, model, getSelectedRow):
        """
        Create treeView
        model -> GTK Storage
        """

        log.LOG("Create Scroll")
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.ShadowType.IN)
        sw.set_size_request(450, 200)
        sw.set_can_focus(True)
        sw.set_visible(True)
        sw.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)
        self.gridMain.attach(sw,0,1,1,1)
        log.LOG("(0,1): %s" % self.gridMain.get_child_at(0,1))

        self.treeViewResult = gtk.TreeView()
        self.treeViewResult.set_size_request(450, 200)
        self.treeViewResult.set_visible(True)
        self.treeViewResult.set_can_focus(True)
        self.treeViewResult.set_model(model)
        self.treeViewResult.set_search_column(0)
        self.treeViewResult.connect("row-activated", getSelectedRow)
        sw.add(self.treeViewResult)

        self.__set_position()

    def getSelectedRow(self, widget, column, data):
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))

    def getSelectedRowType(self, widget, column, data):
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
            id_type = ["-it", '[[:<:]]' + str(model.get_value(iter, 1)) + '[[:>:]]']
            self.commonLayout()
            self.search(id_type)
        
    def getSelectedRowKey(self, widget, column, data):
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
            id_type = ["-k", '[[:<:]]' + str(model.get_value(iter, 0)) + '[[:>:]]']
            self.commonLayout()
            self.search(id_type)


    def getHelp(self, com):

        if com:
            helpList = ConMySQL.getHelp(' '.join(com))
            helpList = "INVALID SYNTAX\n" + helpList[0]['description']
            log.LOG("#### %s" % helpList)
            self.labelLayout(helpList)
        else:
            helpList = ConMySQL.getHelp()
            helpList = helpList[0]['description']
            self.labelLayout(helpList)


    def search(self, com):
        log.LOG("START getKeys")

        #helper fun
        def checkRow(l, d, n):

            log.LOG("######33 %s %s %s" % (l,d,n))
            t = []
            while not l[0].startswith('-'):
                t.append(l.pop(0))
                if not l:
                    break

            if not t:
                return self.print_error_message("Invalid syntax")
            else:
                dPattern[n] = ' '.join(t)

        # clean TreeStore
        self.component['search'].clear()

        # Parse com
        dPattern = {}

        while com:
            k = com.pop(0)
            if com:
                if k.lower() in ['-id', '-i']:
                    checkRow(com, dPattern, 'id')

                elif k.lower() in ['-name','-n ']:
                    checkRow(com, dPattern, 'name')

                elif k.lower() in ['-type', '-t']:
                    checkRow(com, dPattern, 'type')

                elif k.lower() in ['-description', '-desc', '-d']:
                    checkRow(com, dPattern, 'description')

                elif k.lower() in ['-key', '-k']:
                    checkRow(com, dPattern, 'key_list')

                elif k.lower() in ['-autor', '-a']:
                    checkRow(com, dPattern, 'name_a')

                elif k.lower() in ['-id_type', '-it']:
                    log.LOG("in IF")
                    checkRow(com, dPattern, 'id_type')
            else:
                return self.print_error_message("Invalid syntax")


        if dPattern:
            rows = ConMySQL.getLib(dPattern)
        else:
            rows = ConMySQL.getLib()

        for row in rows:
            toadd = [row['id'], row['type'], row['name'], row['key_list']]
            self.component['search'].append(toadd)


        # Create, TreeView Layout
        self.treeViewLayout(self.component['search'], self.getSelectedRow)

        # create columns
        self.createColumns(self.treeViewResult, ['ID', 'Title', 'Name', 'Keys'])
        log.LOG("END getKeys")

    def addRecord(self,com):
        gtkWindowAddRow = AddRowWindowGTK('pi')
        gtkWindowAddRow.main()

    def getTypeTree(self, com):

        log.LOG("START getType")

        # clean TreeStore
        self.component['type'].clear()

        typeData = ConMySQL.getTypeByTree()

        # Show all type by pattern
        if com:
            types = ConMySQL.getType(' '.join(com))
            for type in types:
                child = (type['type'], type['id_type'])

                parent = self.component['type'].append(None, child)
                self.addRowToTreeView(typeData, child, parent)

        else:
        # Show all type
            self.addRowToTreeView(typeData)

        # Create, TreeView Layout
        self.treeViewLayout(self.component['type'], self.getSelectedRowType)

        # create columns
        self.createColumns(self.treeViewResult, ['Type'])

        log.LOG("END getType")

    def createColumns(self, treeView, listColumnName):

        for i, name in enumerate(listColumnName):
            rendererText = gtk.CellRendererText()
            column = gtk.TreeViewColumn(name, rendererText, text=i)
            column.set_clickable(True)
            column.set_sort_indicator(True)
            column.set_sort_column_id(0)
            treeView.append_column(column)


    def addRowToTreeView(self, typeData, parentName=('LOM', 1), parent=None):

        if not typeData.get(parentName):
            return
        else:
            for child in typeData[parentName]:
                newParent = self.component['type'].append(parent, [child[0],child[1]])
                if typeData.get(child):
                    self.addRowToTreeView(typeData, child, newParent)


    def getKeysList(self, com):

        log.LOG("START getKeys")

        # clean TreeStore
        self.component['keys'].clear()

        if com:
            keys = ConMySQL.getUniqueKeys(' '.join(com))
        else:
            keys = ConMySQL.getUniqueKeys()

        for key in keys:
            self.component['keys'].append([key['key_name']])


        # Create, TreeView Layout
        self.treeViewLayout(self.component['keys'], self.getSelectedRowKey)

        # create columns
        self.createColumns(self.treeViewResult, ['keys'])
        log.LOG("END getKeys")

    def getNews(self):
        log.LOG("START getNews")

        # clean TreeStore
        self.component['news'].clear()

        rows = ConMySQL.getNews(self.configData['user'])
        print "################# ",rows
        ConMySQL.updateUser(self.configData['user'])

        for row in rows:
            toadd = [row['id'], row['type'], row['name'], row['key_list']]
            self.component['news'].append(toadd)

        # Create, TreeView Layout
        self.treeViewLayout(self.component['news'], self.getSelectedRow)

        # create columns
        self.createColumns(self.treeViewResult, ['ID', 'Title', 'Name', 'Keys'])

        log.LOG("END getNews")

    def getDigit(com):
        pass

    def setOption(self, com):

        if len(com) >= 2 and com[0] in self.configData.keys():
            self.configData[com[0]] = ' '.join(com)
        else:
            self.print_error_message('INVALID SYNTAX')
        print "############## ",self.configData 
        self.setConfig()
