#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk as gtk
import log
from MySQL import ConMySQL

class Window():

    def __init__(self, configData={}):

        self.configData = configData
        self.component = {}

        # Parse glade XML
        self.gladefile = "Library_of_mind/MainWindow.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)

        # get object
        self.component['help'] = ""
        self.component['set'] = {}
        self.component['search'] = gtk.ListStore(int, str, str, str)
        self.component['update'] = gtk.ListStore(int, str, str, str)
        self.component['add'] = {}
        self.component['type'] = gtk.TreeStore(str, int)
        self.component['news'] = gtk.ListStore(int, str, str, str)
        self.component['keys'] = gtk.ListStore(str, int) 
        self.window = self.glade.get_object("window")
        self.gridMain = self.glade.get_object("gridMain")
        self.entryCommandLine = self.glade.get_object("entryCommandLine")
        self.labelText = None
        self.treeViewResult = None

        # initial window
        self.initialWindow()

        # show all object
        self.window.show_all()

    def initialWindow(self):
        self.commonLayout()

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
        command = rest.pop(0)

        self.commonLayout()

        if command in ['help', 'h']:
            self.getHelp(rest)
        elif command in ['set']:
            self.setOption(rest)
        elif command in ['search', 's']:
            self.search(rest)
        elif command in ['add','a']:
            self.addRecord()
        elif command in ['update', 'u']:
            self.updateRecord(rest)
        elif command in ['type', 't']:
            log.LOG("GetType")
            self.getType(rest)
        elif command in ['key', 'k']:
            self.getKey(rest)
        elif command in ['news', 'n']:
            self.getNews(rest)
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


    def labelLayout(self):

        self.labelLayout = gtk.Label()
        self.labelLayout.set_size_request(450,200)
        self.gridMain.attach(self.labelLayout,0,1,1,1)


    def treeViewLayout(self, model, create_columns):
        """
        Create treeView
        model -> GTK Storage
        create_columns - > function to create columns
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
        sw.add(self.treeViewResult)
        create_columns(self.treeViewResult)

    def getHelp(com):

        return ConMySQL.getHelp(com)

    def search(com):
        pass

    def addRecord(com):
        pass

    def getType(self, com):

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
        self.treeViewLayout(self.component['type'], self.createTypeColumn)
        log.LOG("END getType")

    def createTypeColumn(self, treeView):

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Type", rendererText, text=0)
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


    def getKey(com):

        if com:
            return ConMySQL.getKey(com)
        else:
            return ConMySQL,getKey()

    def getNews(com):
        pass

    def getDigit(com):
        pass
