import pygtk
pygtk.require('2.0')
import gtk

class Basewindow:

    def delete_event(self, widget, event, data=None):
        print "delete event"
        return False

    def main(self):
        gtk.main()

    def entry_callback(self, widget, entry):
        entry_text = entry.get_text()
        print "Entry Text", entry_text

    def setCombolist(self, request, combobox):
        name_store = gtk.ListStore(int, str)

        for l, row in enumerate(request):
            name_store.append([l+1, row])

        combobox.set_model(name_store)


    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.set_title("Library Of Mind")
        self.window.set_size_request(800,600)
        self.window.set_position(gtk.WIN_POS_CENTER)

        title = gtk.Label()
        title.set_markup('<span size="large" color="red">Add/Edit record in database\nname</span>')
        title.set_justify(gtk.JUSTIFY_LEFT)

        name = gtk.Label("Name")
        self.ename = gtk.Entry()
        self.ename.set_max_length(100)
        #self.ename.connect("activate", self.entry_callback, self.ename)
        self.ename.set_text("np. GIT Workflow")
        self.ename.select_region(0, len(self.ename.get_text()))

        self.access = gtk.ComboBox()
        self.setCombolist(['alan','cos'],self.access)
        self.cell = gtk.CellRendererText()
        self.access.pack_start(self.cell, True)
        self.access.add_attribute(self.cell, 'text', 1)
        #self.access.connect('changed', self.changeCombo)
        self.access.set_active(0)


        self.window.add(self.access)
        self.window.show_all()

if __name__ == '__main__':
    window = Basewindow()
    window.main()
