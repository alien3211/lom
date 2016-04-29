#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

	# change button Done signal if update
	if self.update_id:
	    self.buttonDone.connect('clicked', self.clickedButtonUpdateDone)

        # initial text
	if self.update_id:
            self.initialUpdateText()
	else:
            self.initialAddText()

        # show all object
        self.window.show_all()

    def initialAddText(self):

        # TreeViewType
        typeData = ConMySQL.getTypeByTree()
        self.addRowToTreeView(typeData)
	self.treeVType.expand_all()

        # TextView description
        self.addDescription()

        # ComboBoxKey
        keysData = ConMySQL.getUniqueKeys()
        self.addListKeyToComboBox(keysData)

        # TextBuffer
        self.textBuffer.connect("changed", self.textChanged)

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

    def clickedButtonAddDone(self, button):

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
            dataRow['idType'] = model.get_value(iter,1)

            if self.eType.get_text() != "":
                typeNameToRow = self.eType.get_text()
        else:
            dataRow['idType'] = 1
            if self.eType.get_text() != "":
                typeNameToRow = self.eType.get_text()

        if typeNameToRow and ConMySQL.getWhereTypeAndParent(typeNameToRow, dataRow['idType']):
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

        dataRow['keys'] = ",".join(text).replace(' ', '_')

        self.addWaitingRow(dataRow)


    def clickedButtonUpdateDone(self, button):

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
            dataRow['idType'] = model.get_value(iter,1)

            if self.eType.get_text() != "":
                typeNameToRow = self.eType.get_text()
        else:
            dataRow['idType'] = 1
            if self.eType.get_text() != "":
                typeNameToRow = self.eType.get_text()

        if typeNameToRow and ConMySQL.getWhereTypeAndParent(typeNameToRow, dataRow['idType']):
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

        dataRow['keys'] = ",".join(text).replace(' ', '_')

        self.addWaitingRow(dataRow)


    def addWaitingRow(self, dataRow):

        if dataRow['nameType']:
            ConMySQL.setType(dataRow['nameType'], dataRow['idType'])
	    idNewType = ConMySQL.getWhereTypeAndParent(dataRow['nameType'], dataRow['idType'])[0]['id_type']

            ConMySQL.setRow(dataRow['name'], idNewType, dataRow['description'], dataRow['keys'], self.user)
	else:
            ConMySQL.setRow(dataRow['name'], dataRow['idType'], dataRow['description'], dataRow['keys'], self.user)

        gtk.main_quit()
        self.window.destroy()

    def print_error_message(self, text="fill all fields"):

        md = gtk.MessageDialog(self.window, type=gtk.MessageType.ERROR, buttons=gtk.ButtonsType.OK)
        md.set_markup(text)
        md.run()
        md.destroy()

        return None

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
