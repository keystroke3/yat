import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, Gdk, WebKit2

with open('template.html', 'r') as html:
    html = html.read()

#langs = ('english', 'spanish', 'russian', 'italian', 'portugues','greek','polish', 'swidish', 'armanian','german')
langs = ('english', 'spanish', 'russian')
selected_langs = []

body_font = '15px roboto'
body_bg = '#1E1C31'
body_fg = '#E5C07B'

word_fg = '#E06C75'
word_bg = '#1E1C31'
word_font = '15px comfortaa'

lang_fg = '#61AFEF'
lang_bg = '#1E1C31'
lang_font = '15px comfortaa'

okay_fg = '#98C379'
okay_bg = '#1E1C31'
okay_font = '15px comfortaa'

style = f"""
<style>
body{{
    font: {body_font};
    background-color: {body_bg};
    color: {body_fg};
    overflow: scroll;
}}
word{{
    color: {word_fg};
    background-color: {word_bg};
    font: {word_font};
}}
lang{{
    color: {lang_fg};
    background-color: {lang_bg};
    font: {lang_font};
}}
trans{{
    color: {okay_fg};
    background-color: {okay_bg};
    font: {okay_font};
}}
</style>
"""


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="YAT")

        self.set_default_size(300, 250)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.MOUSE)
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(5)
        self.add(self.grid)
        self.create_btns()
        self.create_view()

    def create_view(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, len(langs), 1)
        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolledwindow.add(self.textview)
        self.create_checks()

    def create_checks(self):
        btns = 0
        v = 2
        for lang in langs:
            btns += 1
            check_lang = Gtk.CheckButton(label=lang)
            check_lang.set_active(False)
            check_lang.connect("toggled", self.on_lang_selected, lang)
            if btns > 3:
                v += 1
                btns = 1
            self.grid.attach(check_lang, btns-1, v, 1, 1)

    def create_btns(self, lbl1='Okay', lbl2='Cancel'):
        okay_btn = Gtk.Button.new_with_label(lbl1)
        okay_btn.connect("clicked", self.on_okay_clicked)
        self.grid.attach(okay_btn, 2, 99, 1, 1)

        cancel_btn = Gtk.Button.new_with_label(lbl2)
        cancel_btn.connect("clicked", self.on_cancel_clicked)
        self.grid.attach_next_to(cancel_btn, okay_btn,
                                 Gtk.PositionType.LEFT, 1, 1)

    def on_lang_selected(self, widget, language):
        if widget.get_active():
            selected_langs.append(language)
        else:
            selected_langs.remove(language)

    def on_cancel_clicked(self, cancel_btn):
        print("input cancelled")
        Gtk.main_quit()

    def on_okay_clicked(self, okay_btn):
        self.buffer = self.textview.get_buffer()
        begining, end = self.buffer.get_bounds()
        payload = self.buffer.get_text(begining, end, False)
        output = AnswerWindow(payload)
        output.show_all()
        self.hide()


class AnswerWindow(MainWindow):
    def __init__(self, payload):
        print(payload)
        Gtk.Window.__init__(self, title="yes")
        self.payload = payload
        self.set_default_size(300, 250)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.MOUSE)
        self.create_view()

    def create_view(self):
        html = f"""
        <!DOCTYPE html><html><head>{style}</head><body>{self.payload}</body>
        """
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(5)
        self.grid.set_row_homogeneous(True)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        webview = WebKit2.WebView()
        vbox.pack_start(webview, True, True, 0)
        hbox = Gtk.Box(spacing=0)
        vbox.pack_end(hbox, False, True, 5)
        hbox.pack_end(self.grid, False, True, 5)
        self.create_btns('Go Back', 'Exit')
        webview.load_html(html)
        webview.show()

    def on_okay_clicked(self, okay_btn):
        back = MainWindow()
        back.show_all()
        self.hide()


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.create_checks()
win.create_view()
win.show_all()
# web = AnswerWindow()
# web.connect("destroy", Gtk.main_quit)
# web.create_view()
# web.show_all()

Gtk.main()
