import gi
import pickle
import json
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, Gdk, WebKit2, Gio

try:
    with open('../cache/state.p') as p:
        state = pickle.load(p)
except FileNotFoundError:
    state = {
        'langs': ['it', 'es', 'ru', 'ja']
    }

with open('../lib/names', 'rb') as n:
    lang_names = pickle.load(n)

with open('../lib/native_names', 'rb') as n:
    lang_n_names = pickle.load(n)

langs_codes = state['langs']
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
        self.set_position(Gtk.WindowPosition.CENTER)
        self.main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0)
        self.add(self.main_box)
        self.create_view()

    def create_view(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.main_box.pack_start(scrolledwindow, True, True, 0)
        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolledwindow.add(self.textview)
        self.textview.set_indent(5)
        self.textview.is_focus()

        self.grid = Gtk.Grid()
        self.grid_box = Gtk.Box()
        self.grid.set_column_spacing(0)
        self.grid.set_row_spacing(3)
        self.main_box.pack_start(self.grid_box, False, True, 0)
        self.grid_box.pack_end(self.grid, False, True, 0)
        self.create_btns()
        self.create_checks()
        self.create_drop()

    def create_checks(self):
        btns = 0
        v = 2
        for code in langs_codes:
            btns += 1
            self.lang_btn_box = Gtk.Box(spacing=0)
            lang = lang_names[code]
            check_lang = Gtk.CheckButton(label=lang)
            check_lang.set_active(False)
            check_lang.connect("toggled", self.on_lang_checked, lang)
            self.lang_btn_box.pack_start(check_lang, False, True, 0)

            remove_btn = Gtk.Button()
            icon = Gio.ThemedIcon(name="list-remove-symbolic")
            image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
            remove_btn.add(image)
            remove_btn.connect("clicked", self.remove_lang, self.lang_btn_box, code)
            self.lang_btn_box.pack_end(remove_btn, False, True, 5)
            if btns > 3:
                v += 1
                btns = 1
            self.grid.attach(self.lang_btn_box, btns-1, v, 1, 1)

    def create_btns(self, lbl1='Okay', lbl2='Cancel'):
        btns_box = Gtk.Box()
        self.main_box.pack_end(btns_box, False, False, 5)

        okay_btn = Gtk.Button.new_with_label(lbl1)
        okay_btn.connect("clicked", self.on_okay_clicked)
        btns_box.pack_end(okay_btn, False, False, 5)

        cancel_btn = Gtk.Button.new_with_label(lbl2)
        cancel_btn.connect("clicked", self.on_cancel_clicked)
        btns_box.pack_end(cancel_btn, False, False, 1)

    def create_drop(self):
        
        combo_list = Gtk.ListStore(str, str)
        for code in lang_names:
            combo_list.append([code, lang_names[code]])

        lang_combo = Gtk.ComboBox.new_with_model(combo_list)
        lang_combo.set_entry_text_column(1)
        lang_combo.set_wrap_width(5)
        renderer_text = Gtk.CellRendererText()
        lang_combo.pack_start(renderer_text, True)
        lang_combo.add_attribute(renderer_text, "text", 1)
        print('create_drop')
        lang_combo.connect("changed", self.on_lang_combo_changed)
        self.grid_box.pack_start(lang_combo, False, False, 0)

    def on_cancel_clicked(self, cancel_btn):
        print("Quitting")
        Gtk.main_quit()

    def on_okay_clicked(self, okay_btn):
        self.buffer = self.textview.get_buffer()
        begining, end = self.buffer.get_bounds()
        payload = self.buffer.get_text(begining, end, False)
        output = AnswerWindow(payload)
        output.connect("destroy", self.on_cancel_clicked)
        output.show_all()
        self.hide()

    def on_lang_checked(self, widget, language):
        if widget.get_active():
            selected_langs.append(language)
            print(f'{language} checked')
        else:
            selected_langs.remove(language)
            print(f'{language} unchecked')
    
    def on_lang_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            lang_code, lang_name = model[tree_iter][:2]
            print(f"{(lang_code, lang_name)}")
        
    def remove_lang(self, remove_btn, lang_btn, lang):
        langs_codes.remove(lang)
        self.grid.remove(lang_btn)



class AnswerWindow(MainWindow):
    def __init__(self, payload):
        self.payload = payload
        super().__init__()

    def create_view(self):
        html = f"""
        <!DOCTYPE html><html><head>{style}</head><body>{self.payload}</body>
        """
        webview = WebKit2.WebView()
        self.main_box.pack_start(webview, True, True, 5)
        self.create_btns('Go Back', 'Exit')
        webview.load_html(html)
        webview.show()

    def on_okay_clicked(self, okay_btn):
        back = MainWindow()
        back.show_all()
        back.connect("destroy", self.on_cancel_clicked)
        self.hide()


win = MainWindow()
win.connect("destroy", win.on_cancel_clicked)
win.show_all()


Gtk.main()
