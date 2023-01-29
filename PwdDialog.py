import gettext
import gi
# from gi.repository.GObject import Object

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango  # , Pango, Gdk

class PwdDialog(Gtk.Dialog):
    # internationalization and translation support with GNU gettext message catalog library
    # pt = gettext.translation('base', localedir='locales', languages=['el'])
    # pt.install()
    _ = gettext.gettext
    ___ = gettext.ngettext  # plural sintax -> ngettext(singular: str, plural: str, n: int)

    #  if n=1 singular, otherwise plural

    def __init__(self, parent):
        super().__init__(transient_for=parent, modal=True)



        self.add_buttons(
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
        )
        self.set_title(_("Enter Password"))
        box = self.get_content_area()
        self.set_resizable(False)

        #label = Gtk.Label(label="Insert text you want to search for:")
        #box.add(label)


        self.entry = Gtk.Entry()
        self.entry.set_visibility(False)
        size = PwdDialog.get_pango_string_size("C").height
        self.entry.set_margin_top(size)
        self.entry.set_margin_bottom(size)
        box.add(self.entry)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.buttonok: Gtk.Button = self.get_widget_for_response(Gtk.ResponseType.OK)
        self.buttonok.set_label(_("OK"))
        self.buttoncancel: Gtk.Button = self.get_widget_for_response(Gtk.ResponseType.CANCEL)
        self.buttoncancel.set_label(_("Cancel"))
        self.show_all()
        self.entry.connect("changed", self.on_entry_text_changed)


        # self.buttonok: Gtk.Button = self.get_children()[0].get_children()[1].get_children()[0].get_children()[0]
        self.check_buttonok_enabled()

    def check_buttonok_enabled(self):
        self.buttonok.set_sensitive(len(self.entry.get_text()) > 0)

    def on_entry_text_changed(self, widget):
        self.check_buttonok_enabled()
        print("Text changed event!")

    def get_pwd_and_clear(self):
        """
        :return: Returns password text.
        :rtype: String (str)
        """
        pwd: str = self.entry.get_text()
        self.clear()
        return pwd

    def clear(self):
        """
        :return: Returns None
        :rtype: Any
        """
        self.entry.set_text("")

    @staticmethod
    def get_pango_string_size(txt: str, font_name="sans serif"):
        label = Gtk.Label()
        pango_layout = label.get_layout()
        pango_layout.set_markup(txt)
        pango_font_desc = Pango.FontDescription(font_name)
        pango_layout.set_font_description(pango_font_desc)
        return pango_layout.get_pixel_size()
