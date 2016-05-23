#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk','3.0')

from gi.repository import Gtk as gtk
from gi.repository import Gdk, Pango, Gio, GLib
import log
from MySQL import ConMySQL
import os

class AddRowWindowGTK:

    def __init__(self, user, update=None):

        self.user = user
	self.update_id = update
	self.selected_type_iter = None

        # Parse glade XML
        self.gladefile = os.path.dirname(os.path.abspath(__file__)) + "/glade/AddRowGladeWindow.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)

        # initial object
        self.window = self.glade.get_object("window")
        self.eName = self.glade.get_object("entryName")
        self.eType = self.glade.get_object("entryType")
        self.treeVType = self.glade.get_object("treeviewType")
        self.treeStoreType = self.glade.get_object("treestoreType")
        self.textView = self.glade.get_object("textView")
        self.textBuffer = self.textView.get_buffer()
        self.comboBKey = self.glade.get_object("comboBoxKey")
        self.comboBStoreKey = self.glade.get_object("liststoreKey")
        self.treeVKeys = self.glade.get_object("treeviewKeys")
        self.treeVStoreKeys = self.glade.get_object("liststoreTreeKeys")
        self.labelInfoMarkup = self.glade.get_object("labelInfo")
        self.buttonDone = self.glade.get_object("buttonDone")


        self.treeVType.connect("row-activated", self.unselectedRow)

        # initial text
	if self.update_id:
            self.initialUpdateText()
	    self.buttonDone.connect('clicked', self.clickedButtonDone, self.updateWaitingRow)
	else:
            self.initialAddText()
	    self.buttonDone.connect('clicked', self.clickedButtonDone, self.addWaitingRow)

        # show all object
        self.window.show_all()

    def unselectedRow(self, widget, column, data):
        selection = widget.get_selection()
	selection.unselect_all()

    def initialAddText(self):


        # TreeViewType
        typeData = ConMySQL.getTypeByTree()
        self.addRowToTreeView(typeData)
        self.treeVType.connect("cursor-changed", self.getExpandRow)

        # ComboBoxKey
        keysData = ConMySQL.getUniqueKeys()
        self.addListKeyToComboBox(keysData)

        # TextBuffer
        self.textBuffer.connect("changed", self.textChanged)

        # TextView description
	text = """\<b><b>Bold</b>\<b>
\<i><i>Italic</i>\</i>
\<u><u>Underline</u>\</u>
\<small><small>Small</small>\</small>
\<big><big>Big</big>\</big>
\<tt><tt>Monospace font</tt>\</tt>
\<span color="red"><span color="red">Red color</span>\</span>
\<a href="url"><a href="url">URL</a>\</a>"""
        self.addDescription(text)

    def textChanged(self, buffer):

        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        buffer.remove_all_tags(start, end)

        text = buffer.get_text(start, end, False).encode('utf-8')
        self.labelInfoMarkup.set_markup(escape(text))


        gtk.StyleContext.reset_widgets(Gdk.Screen.get_default())

    def initialUpdateText(self):

	row = ConMySQL.getLib({'id': '[[:<:]]' + str(self.update_id) + '[[:>:]]'})[0]

	# set entryName
	self.eName.set_text(row['name'])

        # TreeViewType
        typeData = ConMySQL.getTypeByTree()
        self.addRowToTreeView(typeData, row['id_type'])
	self.treeVType.expand_all()
        selection = self.treeVType.get_selection()
	selection.select_iter(self.selected_type_iter)

        # treeviewType scroll to selected row
        tm, tree_iter = selection.get_selected()
        path = tm.get_path(tree_iter)
        self.treeVType.scroll_to_cell(path)

        # ComboBoxKey
        keysData = ConMySQL.getUniqueKeys()
        self.addListKeyToComboBox(keysData)

	# keyList
	for x in row['key_list'].split(','):
            self.treeVStoreKeys.append([x])

        # TextBuffer
        self.textBuffer.connect("changed", self.textChanged)

        # TextView description
        self.addDescription(row['description'])

    def addRowToTreeView(self, typeData, update_id=None, parentName=('LOM', 1), parent=None):

        if not typeData.get(parentName):
            return
        else:
            for child in typeData[parentName]:
                newParent = self.treeStoreType.append(parent, [child[0],child[1]])
		if update_id == child[1]:
		    self.selected_type_iter = newParent
                if typeData.get(child):
                    self.addRowToTreeView(typeData, update_id, child, newParent)

    def addDescription(self, desc = ""):

        self.textBuffer.set_text(desc)

    def addListKeyToComboBox(self, keysData):

        for key in keysData:
            self.comboBStoreKey.append([key['key_name']])

    def deleteEvent(self, widget, event):
        gtk.main_quit()

    def clickedButtonAddKey(self, button):

        tree_iter = self.comboBKey.get_active_iter()
        if tree_iter != None:
            model = self.comboBKey.get_model()
            name = model[tree_iter][0]
            self.treeVStoreKeys.append([name])
        else:
            entry = self.comboBKey.get_child()
            if entry.get_text() != "":
                self.treeVStoreKeys.append([entry.get_text()])

    def clickedButtonDeleteKey(self, button):

        selection = self.treeVKeys.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
            try:
                model.remove(iter)
            except:
                pass

    def clickedButtonDone(self, button, waitingRow):

        dataRow = {}

        #check entry name
        if self.eName.get_text() in ["", "Unique name"]:
            return self.print_error_message()

        dataRow['name'] = self.eName.get_text()


        #check select or add type
        selection = self.treeVType.get_selection()
        model, iter = selection.get_selected()

        typeNameToRow = None

        if iter:
            dataRow['id_type'] = model.get_value(iter,1)

            if self.eType.get_text() != "":
                typeNameToRow = self.eType.get_text()
        else:
            dataRow['id_type'] = 1
            if self.eType.get_text() != "":
                typeNameToRow = self.eType.get_text()

        if typeNameToRow and ConMySQL.getWhereTypeAndParent(typeNameToRow, dataRow['id_type']):
            return self.print_error_message("NOT Unique Type!!")

        dataRow['nameType'] = typeNameToRow

        #check description
        if self.textBuffer.get_text(*self.textBuffer.get_bounds(), include_hidden_chars=True) == "":
            return self.print_error_message("Fill in the description")

        start_iter = self.textBuffer.get_start_iter()
        end_iter   = self.textBuffer.get_end_iter()
        dataRow['description'] = self.textBuffer.get_text(start_iter, end_iter, True)

        #check add key
        text = set()
        item = self.treeVStoreKeys.get_iter_first()

        while item != None:
            text.add(self.treeVStoreKeys.get_value(item,0))
            item = self.treeVStoreKeys.iter_next(item)

        if len(text) == 0:
            return self.print_error_message("Add at least one key")

        dataRow['key_list'] = ",".join(text).replace(' ', '_')

        waitingRow(dataRow)


    def addWaitingRow(self, dataRow):

        if dataRow['nameType']:
            ConMySQL.setType(dataRow['nameType'], dataRow['id_type'])
	    idNewType = ConMySQL.getWhereTypeAndParent(dataRow['nameType'], dataRow['id_type'])[0]['id_type']

            ConMySQL.setRow(dataRow['name'], idNewType, dataRow['description'], dataRow['key_list'], self.user)
	else:
            ConMySQL.setRow(dataRow['name'], dataRow['id_type'], dataRow['description'], dataRow['key_list'], self.user)

        gtk.main_quit()
        self.window.destroy()

    def updateWaitingRow(self, dataRow):

        if dataRow['nameType']:
            ConMySQL.setType(dataRow['nameType'], dataRow['idType'])
            dataRow['id_type'] = ConMySQL.getWhereTypeAndParent(dataRow['nameType'], dataRow['idType'])[0]['id_type']

	ConMySQL.UpdateLib(dataRow['name'], dataRow['id_type'], dataRow['description'], dataRow['key_list'], self.update_id, self.user)

        gtk.main_quit()
        self.window.destroy()

    def getExpandRow(self, widget):
        log.LOG("START getExpandRow")

        selection = widget.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
	    path = model.get_path(iter)
            widget.expand_to_path(path)

        log.LOG("END getExpandRow")

    def print_error_message(self, text="fill all fields"):

        log.LOG("START  print_error_message")

        md = gtk.MessageDialog(self.window, type=gtk.MessageType.ERROR, buttons=gtk.ButtonsType.OK)
	md.set_position(gtk.WindowPosition.CENTER_ON_PARENT)
        md.set_markup(text)
        md.run()
        md.destroy()

        return None

        log.LOG("END  print_error_message")

    def main(self):
        gtk.main()

def escape(s):
    "escape html markup"
    if isinstance(s, str):
        s = s.replace("&", "&amp;")
        s = s.replace("\<", "&lt;")
        s = s.replace("\>", "&gt;")

    return s

if __name__ == "__main__":
    try:

	ConMySQL.ip = '172.19.20.19'
        gtkWindow = AddRowWindowGTK('pi')
        gtkWindow.main()
    except KeyboardInterrupt:
        pass
