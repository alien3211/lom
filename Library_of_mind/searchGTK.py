from gi.repository import Gtk, Gio

HEIGHT = 500
WIDTH = 800

class MainWindow(Gtk.Window):

 def __init__(self):

    Gtk.Window.__init__(self, title="Resolution")
    self.set_border_width(0)
    self.set_default_size(WIDTH, HEIGHT)

    hb = Gtk.HeaderBar()
    hb.props.show_close_button = True
    hb.props.title = "Resolution"
    self.set_titlebar(hb)

    button = Gtk.Button()
    icon = Gio.ThemedIcon(name="emblem-system-symbolic")
    image = Gtk.Image.new_from_gicon(icon, 1)
    button.add(image)
    button.connect("clicked", self.sidebarShowHide)
    button.set_focus_on_click(False)
    hb.pack_start(button)

    sidebarbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    toplevelbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

    self.add(toplevelbox)

    self.sidebar = Gtk.Box()
    toplevelbox.pack_start(self.sidebar, False, False, 0)
    self.sidebar.add(sidebarbox)

    self.searchentry = Gtk.SearchEntry()
    self.searchentry.connect("search-changed", self.search_changed)
    sidebarbox.pack_start(self.searchentry, False, False, 0)

    label = Gtk.Label("Contents Selector")
    sidebarbox.pack_start(label, True, True, 0)

    scroller = Gtk.ScrolledWindow()
    toplevelbox.pack_start(scroller, True, True, 0)


 def sidebarShowHide(self, button):
    if self.sidebar.get_visible():
        self.sidebar.hide ()
    else:
        self.sidebar.show ()

 def search_changed(self, searchentry):
    pass




win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
