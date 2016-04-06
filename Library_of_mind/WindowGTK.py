#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk as gtk
from gi.repository import Gdk
import log
from MySQL import ConMySQL
from AddRowWindowGTK import AddRowWindowGTK
import csv
import os

def css():
    css = b"""
* {
    transition-property: color, background-color, border-color, background-image, padding, border-width;
    transition-duration: 1s;
}
GtkLabel:hover{
color: yellow;
}
    """
    style_provider = gtk.CssProvider()
    style_provider.load_from_data(css)

    gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


WINDOW_WIDTH  = 460
WINDOW_HEIGHT = 244


class Window():

    def __init__(self, configData={}):

        log.LOG("START  __init__")

        css()

        self.configData = configData
        self.configData['history'] = "~/.lom_history"
        self.configData['short'] = ['id', 'type', 'name', 'key_list']
        self.configData['ip_MySQL'] = 'localhost'
        if not os.path.exists(self.configData['lomrc']):
            self.setConfig()

	self.getConfig()
        self.component = {}

	# Set MySQL IP
	ConMySQL.ip = self.configData['ip_MySQL']

        # Parse glade XML
        self.gladefile = os.path.dirname(os.path.abspath(__file__)) + "/Library_of_mind/MainWindow.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)

        # get object
        self.component['set'] = {}
        self.component['search'] = gtk.ListStore(int, str, str, str, str, str, str)
        self.component['update'] = gtk.ListStore(int, str, str, str)
        self.component['add'] = {}
        self.component['type'] = gtk.TreeStore(str, int)
        self.component['news'] = gtk.ListStore(int, str, str, str, str, str, str)
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

        log.LOG("END  __init__")

    def setConfig(self):

        log.LOG("START  setConfig")

        w = csv.writer(open(self.configData['lomrc'], 'w'))
        for key, val in self.configData.items():
            w.writerow([key,val])

        log.LOG("END  setConfig")

    def getConfig(self):

        log.LOG("START  getConfig")

        for key, val in csv.reader(open(self.configData['lomrc'])):
            self.configData[key] = val
            log.LOG("key['%s'] = %s" % (key, val))

        log.LOG("END  getConfig")

    def initialInfo(self):

        log.LOG("START  initialInfo")

        #get news
        rows = ConMySQL.getNews(self.configData['user'])

        if rows:
            self.print_error_message("%d news from last check" % len(rows))
            self.getNews()


        log.LOG("END  initialInfo")

    def initialWindow(self):

        log.LOG("START  initialWindow")

        self.window.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)

	self.window.set_gravity(Gdk.Gravity.SOUTH_EAST)
        self.window.set_keep_above(True)
        self.window.set_resizable(False)
        self.window.set_decorated(False)

        self.commonLayout()

        log.LOG("END  initialWindow")

    def __set_position(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):

        log.LOG("START  __set_position")
        (w, h) = width, height
        x = int(Gdk.Screen.get_default().get_width() * int(self.configData['x']))
        y = int(Gdk.Screen.get_default().get_height() * int(self.configData['y']))

        #Set position Left-Button
        log.LOG("(x,y) = (%s,%s)   (w,h) = (%s,%s)" % (x,y,w,h))
        self.window.move(x-w, y-h)

        log.LOG("END  __set_position")

    def print_error_message(self, text="fill all fields"):

        log.LOG("START  print_error_message")

        md = gtk.MessageDialog(self.window, type=gtk.MessageType.ERROR, buttons=gtk.ButtonsType.OK)
        md.set_markup(text)
        md.run()
        md.destroy()

        return None

        log.LOG("END  print_error_message")

    def main(self):

        log.LOG("START  main")
        "Run main loop"
        gtk.main()

        log.LOG("END  main")

    def deleteEvent(self, widget, event):

        log.LOG("START  deleteEvent")
        gtk.main_quit()

        log.LOG("END  deleteEvent")

    def parserArgs(self, widget):

        log.LOG("START  parserArgs")

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


        log.LOG("END  parserArgs")

    def commonLayout(self):

        log.LOG("START  commonLayout")
        self.window.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.entryCommandLine.set_text("")
        widget = self.gridMain.get_child_at(0,1)
        if widget != None:
            self.gridMain.remove(widget)

        widget = self.gridMain.get_child_at(0,2)
        if widget != None:
            self.gridMain.remove(widget)

        self.__set_position()


        log.LOG("END  commonLayout")

    def labelLayout(self, text):

        log.LOG("START  labelLayout")

        log.LOG("Create Scroll")
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.ShadowType.IN)
        sw.set_size_request(450, 200)
        sw.set_can_focus(True)
        sw.set_visible(True)
        sw.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)
        self.gridMain.attach(sw,0,2,1,1)
        log.LOG("(0,1): %s" % self.gridMain.get_child_at(0,1))


        self.labelText = gtk.Label("")
        self.labelText.set_markup(text)
        self.labelText.set_visible(True)
        self.labelText.set_line_wrap(True)
        self.labelText.props.valign = gtk.Align.START
        self.labelText.props.halign = gtk.Align.START

        sw.add(self.labelText)

        self.__set_position()


        log.LOG("END  labelLayout")

    def treeViewLayout(self, model, getSelectedRow):
        """
        Create treeView
        model -> GTK Storage
        """

        log.LOG("START  treeViewLayout")
	self.commonLayout()

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

        log.LOG("END  treeViewLayout")

    def getSelectedRow(self, widget, column, data):

        log.LOG("START  getSelectedRow")
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
	text_row ="""
<span>%d</span> <span color="#929287">Title: </span><span>%s</span>
<span color="#929287">Name: </span><span>%s</span>
<span color="#929287">Description:</span>\n
      %s\n
<span color="#929287">Keys: </span><span>%s</span>
<span weight="bold">%s</span><span>%s</span>
"""
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
            widget = self.gridMain.get_child_at(0,2)
            if widget != None:
                self.gridMain.remove(widget)
            self.labelLayout(text_row % tuple(model[iter][:]))
        self.__set_position(WINDOW_WIDTH, WINDOW_HEIGHT + 200)


        log.LOG("END  getSelectedRow")

    def getSelectedRowType(self, widget, column, data):

        log.LOG("START  getSelectedRowType")
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
            id_type = ["-it", '[[:<:]]' + str(model.get_value(iter, 1)) + '[[:>:]]']
            self.commonLayout()
            self.search(id_type)

        log.LOG("END  getSelectedRowType")

    def getSelectedRowKey(self, widget, column, data):

        log.LOG("START  getSelectedRowKey")
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
            id_type = ["-k", '[[:<:]]' + str(model.get_value(iter, 0)) + '[[:>:]]']
            self.commonLayout()
            self.search(id_type)


        log.LOG("END  getSelectedRowKey")

    def getHelp(self, com):

        log.LOG("START  getHelp")

        if com:
            helpList = ConMySQL.getHelp(' '.join(com))
            helpList = '<span color="red">INVALID SYNTAX</span>\n' + helpList[0]['description']
            log.LOG("#### %s" % helpList)
            self.labelLayout(helpList)
        else:
            helpList = ConMySQL.getHelp()
            helpList = helpList[0]['description']
            self.labelLayout(helpList)


        log.LOG("END  getHelp")

    def search(self, com):

        log.LOG("START  search")

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

        if com:
            if not com[0].startswith('-'):
                pattern = ' '.join(com)
                for name in ['name', 'type', 'description', 'key_list', 'name_a']:
                    dPattern[name] = pattern

            else:
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
                            checkRow(com, dPattern, 'id_type')
                    else:
                        return self.print_error_message("Invalid syntax")


        if dPattern:
            rows = ConMySQL.getLib(dPattern)
        else:
            rows = ConMySQL.getLib()

        for row in rows:
            toadd = [row['id'], row['type'], row['name'], row['key_list'], row['description'], row['name_a'], row['date_a'].strftime("%Y-%m-%d %T")]
            self.component['search'].append(toadd)


        # Create, TreeView Layout
        self.treeViewLayout(self.component['search'], self.getSelectedRow)

        # create columns
        self.createColumns(self.treeViewResult, ['ID', 'Title', 'Name', 'Keys'])

        log.LOG("END  search")


    def addRecord(self,com):

        log.LOG("START  addRecord")
        gtkWindowAddRow = AddRowWindowGTK('pi')
        gtkWindowAddRow.main()

        log.LOG("END  addRecord")

    def getTypeTree(self, com):

        log.LOG("START  getTypeTree")

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

        log.LOG("END  getTypeTree")

    def createColumns(self, treeView, listColumnName):

        log.LOG("START  createColumns")

        for i, name in enumerate(listColumnName):
            rendererText = gtk.CellRendererText()
            column = gtk.TreeViewColumn(name, rendererText, text=i)
            column.set_clickable(True)
            column.set_sort_indicator(True)
            column.set_sort_column_id(0)
            treeView.append_column(column)


        log.LOG("END  createColumns")

    def addRowToTreeView(self, typeData, parentName=('LOM', 1), parent=None):

        log.LOG("START  addRowToTreeView")

        if not typeData.get(parentName):
            return
        else:
            for child in typeData[parentName]:
                newParent = self.component['type'].append(parent, [child[0],child[1]])
                if typeData.get(child):
                    self.addRowToTreeView(typeData, child, newParent)


        log.LOG("END  addRowToTreeView")

    def getKeysList(self, com):

        log.LOG("START  getKeysList")

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

        log.LOG("END  getKeysList")

    def getNews(self):

        log.LOG("START  getNews")

        # clean TreeStore
        self.component['news'].clear()

        rows = ConMySQL.getNews(self.configData['user'])
        ConMySQL.updateUser(self.configData['user'])

        for row in rows:
            toadd = [row['id'], row['type'], row['name'], row['key_list'], row['description'], row['name_a'], row['date_a'].strftime("%Y-%m-%d %T")]
            self.component['news'].append(toadd)

        # Create, TreeView Layout
        self.treeViewLayout(self.component['news'], self.getSelectedRow)

        # create columns
        self.createColumns(self.treeViewResult, ['ID', 'Title', 'Name', 'Keys'])

        log.LOG("END  getNews")

    def getDigit(com):

        log.LOG("START  getDigit")
        pass

        log.LOG("END  getDigit")

    def setOption(self, com):

        log.LOG("START setOption")

        if len(com) >= 2 and com[0] in self.configData.keys():
            self.configData[com[0]] = ' '.join(com)
        elif not com:
            self.getConfig()
            message = ""
            for k, v in self.configData.items():
                message += "%s = %s\n" % (k, v)
            self.labelLayout(message)
        else:
            self.print_error_message('INVALID SYNTAX')
        self.setConfig()

        log.LOG("END setOption")
