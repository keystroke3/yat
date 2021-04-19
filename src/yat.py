import gi
import gui
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, WebKit2


win = Gtk.Window()
view = WebKit2.WebView()
print(view.__dir__())
# view.load_uri('result.html')
# win.add(view)
# win.show_all()
# Gtk.main()


# win = gui.MainWindow()
# win.connect("destroy", win.on_cancel_clicked)
# win.show_all()
# Gtk.main()

