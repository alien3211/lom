#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk as gtk
import log
from MySQL import ConMySQL
import os

class AddRowWindowGTK:

    def __init__(self, user):

        self.user = user

        # Parse glade XML
        self.gladefile = os.path.dirname(os.path.abspath(__file__)) + "Library_of_mind/AddRowGladeWindow.glade"
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

        # initial text
        self.initialText()

        # show all object
        self.window.show_all()

    def initialText(self):

        # TreeViewType
        typeData = ConMySQL.getTypeByTree()
        self.addRowToTreeView(typeData)

        # TextView description
        self.addDescription()

        #ComboBoxKey
        keysData = ConMySQL.getUniqueKeys()
        self.addListKeyToComboBox(keysData)

    def addRowToTreeView(self, typeData, parentName=('LOM', 1), parent=None):

        if not typeData.get(parentName):
            return
        else:
            for child in typeData[parentName]:
                newParent = self.treeStoreType.append(parent, [child[0],child[1]])
                if typeData.get(child):
                    self.addRowToTreeView(typeData, child, newParent)

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

    def clickedButtonDone(self, button):

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

if __name__ == "__main__":
    try:
        gtkWindow = AddRowWindowGTK('pi')
        gtkWindow.main()
    except KeyboardInterrupt:
        pass
