import gettext
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango  # , Pango, Gdk
# _ = gettext.gettext


class MessageDialogs:
    # internationalization and translation support with GNU gettext message catalog library
    _ = gettext.gettext
    ___ = gettext.ngettext  # plural sintax -> ngettext(singular: str, plural: str, n: int)

    #  if n=1 singular, otherwise plural

    @staticmethod
    def show_messagebox_info(win: Gtk.Window, title: str = gettext.gettext("Title"), message: str = "", sec_message: str = ""):
        """
        Shows an information message dialog box.

        :param win:
        :type win:
        :param title:
        :type title:
        :param message:
        :type message:
        :param sec_message:
        :type sec_message:
        :return:
        :rtype:
        """
        msgdialog = Gtk.MessageDialog(message_format=message)
        msgdialog.set_modal(True)
        msgdialog.set_transient_for(win)
        msgdialog.set_title(title)
        msgdialog.add_button(_("Close"), Gtk.ResponseType.CLOSE)
        #btnclose = msgdialog.get_widget_for_response(Gtk.ResponseType.CLOSE)
        #btnclose.set_label(_("Close"))
        if len(sec_message) == 0:
            msgdialog.format_secondary_text(sec_message)

        msgdialog.run()
        msgdialog.destroy()

    @staticmethod
    def show_messagebox_YesNo(win: Gtk.Window, title: str = gettext.gettext("Title"), message: str = "") -> Gtk.ResponseType:
        """
        Shows an information message dialog box.

        :param win:
        :type win:
        :param title:
        :type title:
        :param message:
        :type message:
        :param sec_message:
        :type sec_message:
        :return:
        :rtype:
        """
        result: Gtk.ResponseType = Gtk.ResponseType.NO
        dialog = Gtk.MessageDialog(parent=win,  # parent=self.__getRootWindow(),
                                   flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                   type=Gtk.MessageType.QUESTION,
                                   buttons=Gtk.ButtonsType.YES_NO,
                                   title=title,
                                   message_format=message)

        btnyes = dialog.get_widget_for_response(Gtk.ResponseType.YES)
        btnyes.set_label(_("Yes"))
        btnno = dialog.get_widget_for_response(Gtk.ResponseType.NO)
        btnno.set_label(_("No"))
        result = dialog.run()
        dialog.destroy()
        return result
