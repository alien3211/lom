#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import pango

class MainWindow(gtk.Window):

    def __init__(self, function):

        self.outdoor_check_function = function
        gtk.Window.__init__(self)
        self.set_title("Library Of Mind")

        #initialization window
        self.set_border_width(10)
        self.set_size_request(500,750)
        self.set_position(gtk.WIN_POS_CENTER)

        fix = gtk.Fixed()

        #Window name label
        label = gtk.Label("Add/Update record")
        label.modify_font(pango.FontDescription("sans 28"))
        fix.put(label, 10, 10)

        #Box to name 
        hbox = gtk.HBox(spacing=6)
        fix.put(hbox, 10, 75)

        label = gtk.Label("Name:")
        hbox.pack_start(label, True, True, 0)
        
        self.e_name = gtk.Entry()
        self.e_name.set_text("Unique name")
        hbox.pack_start(self.e_name, True, True, 0)

        #Box to type
        hbox = gtk.HBox(spacing=6)
        fix.put(hbox, 10, 120)

        label = gtk.Label("Type:")
        hbox.pack_start(label, True, True, 0)

        #list type name
        self.name_store = gtk.ListStore(int, str)
        
        #add/selected type
        self.type_combo = gtk.ComboBoxEntry(self.name_store, 1)
        hbox.pack_start(self.type_combo, False, False, True)

        #list parent name
        self.parent_store = gtk.ListStore(str)

        #parent type
        self.parent_combo = gtk.ComboBox(self.parent_store)
        renderer_text = gtk.CellRendererText()
        self.parent_combo.pack_start(renderer_text, True)
        self.parent_combo.add_attribute(renderer_text, "text", 0)
        hbox.pack_start(self.parent_combo, False, False, True)


        #label to description
        label = gtk.Label("Description:")
        fix.put(label, 10, 180)
        
        #Box to description
        hbox = gtk.HBox(spacing=6)
        fix.put(hbox, 10, 210)

        #scrolled to TextView
        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_size_request(200,200)
        scrolledwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        hbox.pack_start(scrolledwindow, False, False, 0)

        self.textview = gtk.TextView()
        self.textview.set_size_request(350, 250)
        self.textview.set_wrap_mode(gtk.WRAP_WORD) # wrap text by WORD
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("This is some text inside of a gtk.TextView\n. "
            + "Select text and click one of the buttons 'bold', 'italic', "
            + "or 'underline' to modify the text accordingly.")
        scrolledwindow.add(self.textview)

        #Help to Text view
        label = gtk.Label("cos tam cos tam")
        hbox.pack_start(label, False, False, 0)

        #label to key
        label = gtk.Label("keys:")
        fix.put(label, 10, 425)

        #Box to keys
        hbox = gtk.HBox(spacing=6)
        fix.put(hbox, 10, 440)

        #list type key
        self.key_store = gtk.ListStore(int, str)
        
        #add/selected key
        self.key_combo = gtk.ComboBoxEntry(self.key_store, 1)
        hbox.pack_start(self.key_combo, False, False, True)

        #add key 
        self.key_button = gtk.Button("Add Key")
        self.key_button.connect("clicked", self.on_add_key)
        hbox.pack_start(self.key_button, True, True, 0)


        #delete key 
        self.delete_button = gtk.Button("Delete")
        self.delete_button.connect("clicked", self.delete_key)
        fix.put(self.delete_button, 220, 650)

        #List add key
        self.listkey = gtk.ListStore(str)

        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_size_request(200,200)
        scrolledwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        fix.put(scrolledwindow, 10, 480)

        self.treeview = gtk.TreeView(model=self.listkey)

        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn("Key", renderer_text, text=0)
        self.treeview.append_column(column_text)
        scrolledwindow.add(self.treeview)


        #Done button
        self.done_button = gtk.Button("DANE")
        self.done_button.connect("clicked", self.done_add_record)
        fix.put(self.done_button, 450, 700)

        self.add(fix)
        self.connect("delete-event", gtk.main_quit)
        self.show_all()

    def on_add_key(self, button):
        tree_iter = self.key_combo.get_active_iter()
        if tree_iter != None:
            model = self.key_combo.get_model()
            print model[tree_iter]
            name = model[tree_iter][1]
            self.listkey.append([name])
        else:
            entry = self.key_combo.get_child()
            if entry.get_text() != "":
                self.listkey.append([entry.get_text()])

    
    def delete_key(self, button):
        selection = self.treeview.get_selection()
        result = selection.get_selected()
        if result:
            model, iter = result
        try:
            model.remove(iter)
        except:
            pass

    def add_type(self, type_list):
        
        for i, row in enumerate(type_list):
            self.name_store.append([i, row])
            self.parent_store.append([row])

    def add_key(self, type_list):
        for i, row in enumerate(type_list):
            self.key_store.append([i, row])

    def done_add_record(self, button):

        #check entry name
        if self.e_name.get_text() in ["", "Unique name"]:
            return self.print_error_message()
        
        #check select or add type
        tree_iter = self.type_combo.get_active_iter()
        if tree_iter == None:
            if self.type_combo.get_child().get_text() == "":
                return self.print_error_message("DUPA")
            else:
                parent_iter = self.parent_combo.get_active_iter()
                if parent_iter == None:
                    return self.print_error_message("Select parent type")

        #check description
        if self.textbuffer.get_text(*self.textbuffer.get_bounds(), include_hidden_chars=True) == "":
            return self.print_error_message("Fill in the description")


        #check add key
        text = set()
        item = self.listkey.get_iter_first()

        while item != None:
            text.add(self.listkey.get_value(item,0))
            item = self.listkey.iter_next(item)
            
        if len(text) == 0:
            return self.print_error_message("Add at least one key")


        print self.get_data()

        #check in databases
        self.outdoor_check_function(self)

    def get_data(self):

        record = []
        record.append(self.e_name.get_text())

        #get select type 
        tree_iter_type = self.type_combo.get_active_iter()
        tree_iter_parent = self.parent_combo.get_active_iter()
        if tree_iter_type != None:
            model = self.type_combo.get_model()
            record.append(model[tree_iter_type][1])
            record.append("")
        else:
            model = self.parent_combo.get_model()
            record.append(self.type_combo.get_child().get_text())
            record.append(model[tree_iter_parent][0])

        record.append(self.textbuffer.get_text(*self.textbuffer.get_bounds(), include_hidden_chars=True))

        text = set()
        item = self.listkey.get_iter_first()

        while item != None:
            text.add(self.listkey.get_value(item,0))
            item = self.listkey.iter_next(item)

        record.append(', '.join(text))

        return record

    def print_error_message(self, text="fill all fields"):

        md = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
        md.run()
        md.destroy()

        return None
        

    def main_loop(self):
        gtk.main()

    def gtk_quit(self):
        gtk.main_quit()


if __name__ == '__main__':
    win = MainWindow(lambda x : x)
    win.main_loop()

