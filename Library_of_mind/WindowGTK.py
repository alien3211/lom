#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk','3.0')

from gi.repository import Gtk as gtk
from gi.repository import Gdk
import log
from MySQL import ConMySQL
from AddRowWindowGTK import AddRowWindowGTK
import csv
import os
from collections import deque, defaultdict

def css():
    css = b"""
* {
    transition-property: color, background-color, border-color, background-image, padding, border-width;
    transition-duration: 1s;
  }
/* font operate on entire GtkTreeView not for selected row */
GtkTreeView {
text-shadow: 1px 1px 2px black, 0 0 1em blue, 0 0 0.2em blue;
color: white;
font: 1.5em Georgia, "Bitstream Charter", "URW Bookman L", "Century Schoolbook L", serif;
font-weight: bold;
font-style: italic;box-shadow: 5px 3px red;}
GtkTreeView row:nth-child(even) {
background-image: -gtk-gradient (linear,
left top,
left bottom,
from (#d0e4f7),
color-stop (0.5, darker (#d0e4f7)),
to (#fdffff));
}
GtkTreeView row:nth-child(odd) {
background-image: -gtk-gradient (linear,
left top,
left bottom,
from (yellow),
color-stop (0.5, darker (yellow)),
to (#fdffff));
}
/* next line only border action operate */
GtkTreeView:selected{color: white; background: green; border-width: 1px; border-color: black;}
/* next line for Gtk.TreeViewColumn */
column-header .button{color: white; background: purple;}

* {
    -GtkWindow-resize-grip-default: false;
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

        # set config data
        self.configData = configData
        self.configData['history_file'] = os.path.expanduser("~") + "/.lom_history"
        self.configData['history'] = 50
        self.configData['short'] = ['Title', 'Name', 'Keys']
        self.configData['ip_MySQL'] = '172.19.20.19'

        if not os.path.exists(self.configData['lomrc']):
            self.setConfig()

        if not os.path.exists(self.configData['history_file']):
            with open(self.configData['history_file'], 'wb') as f:
                f.write("")

	self.getConfig()

	# Set MySQL IP
	ConMySQL.ip = self.configData['ip_MySQL']

        # Parse glade XML
        self.gladefile = os.path.dirname(os.path.abspath(__file__)) + "/glade/MainWindow.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)

        # get object
        self.component = {}
        self.component['set'] = {}
        self.component['search'] = gtk.ListStore(int, str, str, str, str, str, str)
        self.component['update'] = gtk.ListStore(int, str, str, str)
        self.component['add'] = {}
        self.component['type'] = gtk.TreeStore(str, int)
        self.component['news'] = gtk.ListStore(int, str, str, str, str, str, str)
        self.component['keys'] = gtk.ListStore(str)
        self.component['history'] = gtk.ListStore(int, str)
        self.window = self.glade.get_object("window")
        self.gridMain = self.glade.get_object("gridMain")
        self.entryCommandLine = self.glade.get_object("entryCommandLine")
        self.labelTitle = self.glade.get_object("labelTitle")
        self.labelText = None
        self.treeViewResult = None

        # set up history command
        self.history = deque(maxlen=int(self.configData['history']))
        self.histpos = 0
        self.getHisoryFromFile()

        # initial window
        self.initialWindow()

        # show all object
        self.window.show_all()

        # check info
        self.initialInfo()

        log.LOG("END  __init__")

    def setConfig(self):

        log.LOG("START  setConfig")

	tmp = self.configData
	tmp['short'] = ' '.join(tmp['short'])
	with open(self.configData['lomrc'], 'wb') as csvfile:
	    writer = csv.DictWriter(csvfile, tmp.keys())
	    writer.writeheader()
	    writer.writerow(tmp)
	self.getConfig()

        log.LOG("END  setConfig")

    def getConfig(self):

        log.LOG("START  getConfig")

	with open(self.configData['lomrc']) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	      self.configData = row
	self.configData['short'] = self.configData['short'].split()

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

        self.entryCommandLine.connect('key_press_event', self.__key_function)

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

    def __key_function(self, entry, event):

        log.LOG("START __key_function")
        if event.keyval == Gdk.KEY_Return:

            self.entryCommandLine.emit_stop_by_name('key_press_event')

        elif event.keyval in (Gdk.KEY_KP_Up, Gdk.KEY_Up, Gdk.KEY_Page_Up):

            self.entryCommandLine.emit_stop_by_name('key_press_event')
            self.historyUp()

        elif event.keyval in (Gdk.KEY_KP_Down, Gdk.KEY_Down, Gdk.KEY_Page_Down):

            self.entryCommandLine.emit_stop_by_name('key_press_event')
            self.historyDown()

        elif event.keyval in (Gdk.KEY_D, Gdk.KEY_d) and\
                event.state & Gdk.ModifierType.CONTROL_MASK:

            self.entryCommandLine.emit_stop_by_name('key_press_event')
            self.setHisoryFile()
            gtk.main_quit()
            self.window.destroy()


        log.LOG("END __key_function")


    def historyDown(self):

        log.LOG("START historyUp")


        if self.histpos > 0:
            self.entryCommandLine.set_text(self.history[self.histpos])
            self.histpos = self.histpos - 1

        log.LOG("END historyUp")


    def historyUp(self):

        log.LOG("START historyDown")


        if self.histpos < len(self.history) - 1:
            self.entryCommandLine.set_text(self.history[self.histpos])
            self.histpos = self.histpos + 1

        log.LOG("END historyDown")


    def setHisoryFile(self):

        with open(self.configData['history_file'], 'w') as f:
            f.write('\n'.join(self.history))

    def getHisoryFromFile(self):

        with open(self.configData['history_file'], 'r') as f:
            self.history = deque(maxlen=int(self.configData['history']))
            for row in f.read().split('\n'):
                self.history.append(row)

    def print_error_message(self, text="fill all fields"):

        log.LOG("START  print_error_message")

        md = gtk.MessageDialog(self.window, type=gtk.MessageType.ERROR, buttons=gtk.ButtonsType.OK)
	md.set_position(gtk.WindowPosition.CENTER_ON_PARENT)
        md.set_markup(text)
        md.run()
        md.destroy()

        return None

        log.LOG("END  print_error_message")

    def entry_dialog(self, message):

        log.LOG("START entry_dialog")

	dialog = gtk.MessageDialog(self.window, type=gtk.MessageType.QUESTION, buttons=gtk.ButtonsType.OK)
	dialog.set_position(gtk.WindowPosition.CENTER_ON_PARENT)
	dialog.set_markup(message)

	dialogBox = dialog.get_content_area()
	entry = gtk.Entry()
	entry.set_size_request(200, 0)
	dialogBox.pack_end(entry, False, False, 0)

	dialog.show_all()
	response = dialog.run()
	text = entry.get_text() 
        dialog.destroy()
	if (response == gtk.ResponseType.OK) and (text != ''):
	    return text
	else:
	    return None

        log.LOG("END entry_dialog")

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

        arg = escapePattern(widget.get_text())
        rest = arg.split()
        self.histpos = 0
        if rest and '\n' not in rest:
            self.history.appendleft(arg)
        command = rest.pop(0) if rest else ""

        self.commonLayout()

        if command in ['help', 'h']:
            self.getHelp(rest)
        elif command in ['set']:
            self.setOption(rest)
        elif command in ['search', 's']:
            self.search(rest)
        elif command in ['add','a']:
            self.addParser(rest)
        elif command in ['update', 'u']:
            self.updateRecord(rest)
        elif command in ['type', 't']:
            self.getTypeTree(rest)
        elif command in ['key', 'k']:
            self.getKeysList(rest)
        elif command in ['news', 'n']:
            self.getNews()
        elif command in ['history', 'his']:
            self.getHisory()
        elif command in ['open', 'o']:
            self.openWebBrowser(rest)
        elif command in ['exit', 'bye']:
            self.setHisoryFile()
            gtk.main_quit()
            self.window.destroy()
        elif command.isdigit():
            self.getDigit(int(command))


        log.LOG("END  parserArgs")

    def commonLayout(self):

        log.LOG("START  commonLayout")
	self.labelTitle.set_text("Library Of Mind")

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
        sw.set_visible(True)
        sw.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)
        self.gridMain.attach(sw,0,2,1,1)
        log.LOG("(0,1): %s" % self.gridMain.get_child_at(0,1))


        self.labelText = gtk.Label()
        self.labelText.set_markup(escape(text))
        self.labelText.set_visible(True)
        self.labelText.set_selectable(True)
        self.labelText.props.valign = gtk.Align.START
        self.labelText.props.halign = gtk.Align.START

        sw.add(self.labelText)

        self.__set_position()


        log.LOG("END  labelLayout")

    def treeViewLayout(self, model, getSelectedRow, search_col=0):
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
        self.treeViewResult.set_search_column(search_col)
        self.treeViewResult.connect("row-activated", getSelectedRow)
        sw.add(self.treeViewResult)

        self.__set_position()

        log.LOG("END  treeViewLayout")

    def getSelectedRow(self, widget, column, data):

        log.LOG("START  getSelectedRow")
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
	text_row ="""
<span color="#929287">Title: </span><span>{1}</span>
<span color="#929287">Name: </span><span>{2}</span>
<span color="#929287">Description:</span>\n
<span>{4}</span>\n
<span color="#929287">Keys: </span><span>{3}</span>
<span color="#929287">Autor: </span><span weight="bold">{5}</span>\t<span color="#929287">Date: </span><span>{6}</span>
"""
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()

        if result:
            model, iter = result
            widget = self.gridMain.get_child_at(0,2)

            if widget != None:
                self.gridMain.remove(widget)
            self.labelLayout(text_row.format(*model[iter]))

        self.__set_position(WINDOW_WIDTH, WINDOW_HEIGHT)


	self.labelTitle.set_text("Search --> %s" % model[iter][2])
        log.LOG("END  getSelectedRow")

    def getSelectedRowType(self, widget, column, data):

        log.LOG("START  getSelectedRowType")
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
	    type_name = str(model.get_value(iter, 0))
	    type_id = model.get_value(iter, 1)

            typeData = ConMySQL.getTypeByTree()
	    child = (type_name, type_id)

            id_type = ["-it", '[[:<:]]' + str(type_id) + '[[:>:]]']

            for i in self.getIdFromTreeType(typeData, child):
	        id_type.extend(["-it", '[[:<:]]' + str(i) + '[[:>:]]'])
            self.commonLayout()
            self.search(id_type)

	self.labelTitle.set_text("Type select --> %s" % type_name)
        log.LOG("END  getSelectedRowType")

    def getIdFromTreeType(self, typeData, parentName=('LOM', 1)):

        log.LOG("START getIdFromTreeType")
	list_id = []

        if not typeData.get(parentName):
            return list_id
        else:
            for child in typeData[parentName]:
                list_id.append(child[1])
                if typeData.get(child):
                    list_id.extend(self.getIdFromTreeType(typeData, child))
        return list_id


        log.LOG("END getIdFromTreeType")

    def getSelectedRowKey(self, widget, column, data):

        log.LOG("START  getSelectedRowKey")
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
	    key_name = str(model.get_value(iter, 0))

            id_type = ["-k", '[[:<:]]' + key_name + '[[:>:]]']
            self.commonLayout()
            self.search(id_type)


	self.labelTitle.set_text("Key select --> %s" % key_name)
        log.LOG("END  getSelectedRowKey")

    def getSelectedHis(self, widget, column, data):

        log.LOG("START getSelectedHis")
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
            self.commonLayout()
            self.entryCommandLine.set_text(str(model.get_value(iter, 1)))
	    self.parserArgs(self.entryCommandLine)

        log.LOG("END getSelectedHis")

    def getSelectedUpdate(self, widget, column, data):

        log.LOG("START getSelectedUpdate")
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
	    id_row = model[iter][0]
            self.commonLayout()
            gtkWindowUpdateRow = AddRowWindowGTK(self.configData['user'], id_row)
            gtkWindowUpdateRow.main()

	self.labelTitle.set_text("Update select --> %s" % model[iter][1])
        log.LOG("END getSelectedUpdate")

    def getHelp(self, com):

        log.LOG("START  getHelp")

        if com:
            helpList = ConMySQL.getHelp(' '.join(com))[0]
	    if helpList['name'] == 'ALL':
                helpList = '<span color="red">INVALID SYNTAX</span>\n' + helpList['description']
            else:
                helpList = helpList['description']

            log.LOG("#### %s" % helpList)
            self.labelLayout(helpList)
        else:
            helpList = ConMySQL.getHelp()[0]
            helpList = helpList['description']
            self.labelLayout(helpList)


	self.labelTitle.set_text("Help --> %s" % ' '.join(com) or 'All')
        log.LOG("END  getHelp")

    def search(self, com):

        log.LOG("START  search")

        #helper fun
        def checkRow(l, d, n):

            log.LOG("%s %s %s" % (l,d,n))
            t = []
            while not l[0].startswith('-'):
                t.append(l.pop(0))
                if not l:
                    break

            if not t:
                return self.print_error_message("Invalid syntax")
            else:
                dPattern[n].append(' '.join(t))

        # clean TreeStore
        self.component['search'].clear()

        # Parse com
        dPattern = defaultdict(list)

        if com:
            if not com[0].startswith('-'):
                pattern = ' '.join(com)
                for name in ['name', 'type', 'description', 'key_list', 'name_a']:
                    dPattern[name].append(pattern)

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
            rows = ConMySQL.getLibDefaultDick(dPattern)
        else:
            rows = ConMySQL.getLib()

        for row in rows:
            toadd = [row['id'], row['type'], row['name'], row['key_list'], row['description'], row['name_a'], row['date_a'].strftime("%Y-%m-%d %T")]
            self.component['search'].append(toadd)


        # Create, TreeView Layout
        self.treeViewLayout(self.component['search'], self.getSelectedRow, 2)

        # create columns
        self.createColumns(self.treeViewResult, self.mapColumnNameToNumber(self.configData['short']))

	self.labelTitle.set_text("Search --> %s" % (' '.join(com) if com else "All"))
        log.LOG("END  search")


    def addRecord(self):

        log.LOG("START  addRecord")
        gtkWindowAddRow = AddRowWindowGTK(self.configData['user'])
        gtkWindowAddRow.main()

	self.labelTitle.set_text("Add record")
        log.LOG("END  addRecord")

    def addParser(self,com):

        log.LOG("START addParser")
        if com:
	    if com[0].startswith('-'):
	        if com[0] in ['-t', '-type']:
		    if len(com) == 2:
		        self.selectNewType(com[1])
		    else:
		        self.selectNewType()
		else:
	            self.print_error_message("Invalid syntax More in <tt>help add</tt>")
	    else:
	        self.print_error_message("Invalid syntax More in <tt>help add</tt>")
	else:
	    self.addRecord()

        log.LOG("END addParser")

    def selectNewType(self, new_type=None):

        log.LOG("START selectNewType")

        self.component['type'].clear()

        typeData = ConMySQL.getTypeByTree()

        # Show all type by pattern
        if new_type:
            types = ConMySQL.getType(new_type)
            for type in types:
                child = (type['type'], type['id_type'])

                parent = self.component['type'].append(None, child)
                self.addRowToTreeView(typeData, child, parent)

        else:
        # Show all type
            self.addRowToTreeView(typeData)

        # Create, TreeView Layout
        self.treeViewLayout(self.component['type'], self.addNewTypeToSelected)

        # create columns
        self.createColumns(self.treeViewResult, [(0, 'Type')])

	self.labelTitle.set_text("Add new type. Please select parent type")

        log.LOG("END selectNewType")

    def addNewTypeToSelected(self, widget, column, data):

        log.LOG("START addNewTypeToSelected")
        log.LOG("widget= %s path= %s column= %s data=%s" % (self, widget, column, data))
        selection = self.treeViewResult.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
	    type_name = str(model.get_value(iter, 0))
	    type_id = model.get_value(iter, 1)

            new_type = self.entry_dialog("Please entry new type to <tt>%s</tt>" % type_name)
	    if new_type:
	        ConMySQL.setType(new_type, type_id)
                self.commonLayout()
	        self.labelTitle.set_text("Add new type '%s' to '%s'" % (new_type, type_name))
	    else:
	        self.print_error_message("Name is empty More <tt>help add</tt>")

        log.LOG("END addNewTypeToSelected")

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
        self.createColumns(self.treeViewResult, [(0, 'Type')])


	self.labelTitle.set_text("Type --> %s" % (' '.join(com) if com else "All"))
        log.LOG("END getType")

        log.LOG("END  getTypeTree")


    def updateRecord(self, com):

        log.LOG("START updateRecord")

        # clean TreeStore
        self.component['search'].clear()

        # Parse com
        dPattern = defaultdict(list)

        if com:
            pattern = ' '.join(com)
            for name in ['name', 'type', 'description', 'key_list', 'name_a']:
                dPattern[name].append(pattern)

        if dPattern:
            rows = ConMySQL.getLibDefaultDick(dPattern)
        else:
            rows = ConMySQL.getLib()

        for row in rows:
            toadd = [row['id'], row['type'], row['name'], row['key_list'], row['description'], row['name_a'], row['date_a'].strftime("%Y-%m-%d %T")]
            self.component['search'].append(toadd)


        # Create, TreeView Layout
        self.treeViewLayout(self.component['search'], self.getSelectedUpdate, 2)

        # create columns
        self.createColumns(self.treeViewResult, self.mapColumnNameToNumber(self.configData['short']))

	self.labelTitle.set_text("Update --> %s" % (' '.join(com) if com else "All"))
        log.LOG("END updateRecord")


    def createColumns(self, treeView, listColumnName):

        log.LOG("START  createColumns")

        for i, name in listColumnName:
            rendererText = gtk.CellRendererText()
            column = gtk.TreeViewColumn(name, rendererText, text=i)
            column.set_clickable(True)
            column.set_sort_indicator(True)
            column.set_sort_column_id(0)
            treeView.append_column(column)
	    treeView.expand_all()


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
        self.createColumns(self.treeViewResult, [(0, 'keys')])

	self.labelTitle.set_text("Keys --> %s" % (' '.join(com) if com else "All"))
        log.LOG("END  getKeysList")

    def mapColumnNameToNumber(self, nameList):

        mapNumber = {
		'ID' : 0,
		'Title' : 1,
		'Name' : 2,
		'Keys' : 3,
		'Description' : 4,
		'name_a' : 5,
		'data_a' : 6}


	return [(mapNumber[x], x) for x in nameList if x in mapNumber.keys()]

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
        self.treeViewLayout(self.component['news'], self.getSelectedRow, 2)

        # create columns
        self.createColumns(self.treeViewResult, self.mapColumnNameToNumber(self.configData['short']))

	self.labelTitle.set_text("News")
        log.LOG("END  getNews")

    def getDigit(self):

        log.LOG("START  getDigit")
        pass

        log.LOG("END  getDigit")

    def getHisory(self):

        log.LOG("START  getDigit")

        # clean TreeStore
        self.component['history'].clear()

        for row in enumerate(self.history):
            self.component['history'].append(row)


        # Create, TreeView Layout
        self.treeViewLayout(self.component['history'], self.getSelectedHis, 1)

        # create columns
        self.createColumns(self.treeViewResult, [(0, 'ID'),(1, 'History')])

	self.labelTitle.set_text("History")
        log.LOG("END  getDigit")

    def setOption(self, com):

        log.LOG("START setOption")

        if len(com) >= 2 and com[0] in self.configData.keys():
            self.configData[com[0]] = ' '.join(com[1:])
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
    
    def openWebBrowser(self, com):
        log.LOG("START openWebBrowser")
	import webbrowser
	
	if len(com) >= 2 and com[0].startswith('-'):
	    option = com.pop(0)
	    if option in ['-s']:
	        url = "http://stackoverflow.com/search?q=" + '+'.join(com)
	    elif option in ['-u']:
	        url = "http://unix.stackexchange.com/search?q=" + '+'.join(com)
	    elif option in ['-g']:
	        url = "https://www.google.pl/search?q=" + '+'.join(com)
	    else:
	        print "error ifa"
	        return self.print_error_message('INVALID SYNTAX')

	    webbrowser.open_new(url)

	else:
            self.print_error_message('INVALID SYNTAX')

        log.LOG("END openWebBrowser")

def escape(s):
    "escape html markup"
    if isinstance(s, str):
        s = s.replace("&", "&amp;")
        s = s.replace("\<", "&lt;")
        s = s.replace("\>", "&gt;")

    return s
def escapePattern(s):
    "escape html markup"
    if isinstance(s, str):
        s = s.replace("\<", "[[:<:]]")
        s = s.replace("\>", "[[:>:]]")

    return s
