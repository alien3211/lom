#!/usr/bin/env python
import gtk, gobject
from math import pi

class Canvas(gtk.DrawingArea):
    def __init__(self):
        super(Canvas, self).__init__()
        self.connect("expose_event", self.expose)
        self.set_size_request(400,400)

        self.x = 20
        self.y = 20

        self.counter = 0

    def movealittle(self):
        self.x += 1
        self.counter += 1
        self.queue_draw()
        if self.counter <= 20:
            return True
        elif self.counter > 20:
            self.counter = 0
            return False

    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        rect = self.get_allocation()

        w = rect.width
        h = rect.height

        cr.arc(self.x, self.y, 10, 0, 2*pi)
        cr.fill()

def runanimation(widget):
    gobject.timeout_add(5, canvas.movealittle)
    print "runanimation call"

button = gtk.Button("Move")
button.connect("clicked", runanimation)

window = gtk.Window()
canvas = Canvas()
panel = gtk.VBox()
window.add(panel)
panel.pack_start(canvas)
panel.pack_start(button)
window.set_position(gtk.WIN_POS_CENTER)
window.show_all()
gtk.main()
