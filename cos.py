#!/usr/bin/env python

try:
  import pygtk
  pygtk.require('2.0')
except:
  pass
try:
  import gtk
except:
  print('GTK not available')
  sys.exit(1)

class Buglump:

  def __init__(self):

    # the liststore
    self.liststore = gtk.ListStore(int,str)
    self.liststore.append([0,"Select an Item:"])
    self.liststore.append([1,"Row 1"])
    self.liststore.append([2,"Row 2"])
    self.liststore.append([3,"Row 3"])
    self.liststore.append([4,"Row 4"])
    self.liststore.append([5,"Row 5"])

    # the combobox
    self.combobox = gtk.ComboBox()
    self.combobox.set_model(self.liststore)
    self.cell = gtk.CellRendererText()
    self.combobox.pack_start(self.cell, True)
    self.combobox.add_attribute(self.cell, 'text', 1)
    self.combobox.connect('changed', self.on_combobox1_changed)
    self.combobox.set_active(0)

    self.window = gtk.Window()
    self.window.add(self.combobox)
    self.window.show_all()

  def on_combobox1_changed(self, widget, data=None):
    self.index = widget.get_active()
    self.model = widget.get_model()
    self.item = self.model[self.index][1]
    print "ComboBox Active Text is", self.item
    print "ComboBox Active Index is", self.index

  def on_window1_destroy(self, object, data=None):
    print "quit with cancel"
    gtk.main_quit()

if __name__ == "__main__":
  main = Buglump()
  gtk.main()
