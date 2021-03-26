import gi
import gui
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

win = gui.MainWindow()
win.connect("destroy", win.on_cancel_clicked)
win.show_all()
Gtk.main()

