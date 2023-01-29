# from typing import TextIO
#import os
#import cairo
import gettext  # The gettext module provides internationalization (I18N) and localization (L10N) services
                # for your Python modules and applications.

from PwdDialog import PwdDialog
from MessageDialogs import MessageDialogs
from Settings import Settings
from Encriptor import Encryptor
from TextViewHelper import TextViewHelper
import datetime
import gi
from gi.repository import Gtk, Pango, Gdk #, GtkSource
gi.require_version("Gtk", "3.0")

# internationalization and translation support with GNU gettext message catalog library


# I18N and L10N Gnu GetText Multilingual internationalization services
#pt = gettext.translation('base', localedir='locales', languages=['el'])
#pt.install()
#_ = gettext.gettext
#___ = gettext.ngettext  # plural sintax -> ngettext(singular: str, plural: str, n: int)
                        #  if n=1 singular, otherwise plural

  #  if n=1 singular, otherwise plural



def define_globals():
    global APP_NAME
    APP_NAME = 'Cryptedit'
    global builder
    builder = Gtk.Builder()
    builder.add_from_file("main_window.glade")
    global window
    window = builder.get_object("main_window")
    window.set_title(APP_NAME)
    window.set_icon_from_file("crypteditlogo.svg")

    # create icon object
    statusIcon = Gtk.StatusIcon()

    # load it
    statusIcon.set_from_file("crypteditlogo.svg")

    # show it
    statusIcon.set_visible(True)
    
    global app_creation_date
    app_creation_date = datetime.date(2022, 12, 1)
    global STATBAR_OPENFILE_ID
    STATBAR_OPENFILE_ID = 298
    global STATBAR_ENCRYPTED_ID
    STATBAR_ENCRYPTED_ID = 300
    global STATBAR_LOCKED_ID
    STATBAR_LOCKED_ID = 302
    global clipboard
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)



class Handler(object):
    # I18N and L10N Gnu GetText Multilingual internationalization services
    #pt = gettext.translation('base', localedir='locales', languages=['pt'])
    #[].append(Settings.idiom))
    # Settings.lang.install()
    _ = gettext.gettext
    ___ = gettext.ngettext  # plural sintax -> ngettext(singular: str, plural: str, n: int)

    PLAIN_TEXT_FILE_EXT: str = 'txt'
    ENC_TEXT_FILE_EXT: str = 'txt.encrypted'
    END_OF_LINE_MARK = '\n'  # Unix end of line mark

    @property
    def current_file(self):
        return self._current_file

    @current_file.setter
    def current_file(self, value: str):
        self._current_file = value

    @property
    def is_saved(self) -> bool:
        return self._is_saved

    @is_saved.setter
    def is_saved(self, value: bool):
        self._is_saved = value

    @property
    def is_encrypted(self) -> bool:
        return self._is_encrypted

    @is_encrypted.setter
    def is_encrypted(self, value: bool):
        self._is_encrypted = value
        self.textview.set_editable(not value)
        self.editmenuitem.set_sensitive(not value)
        self.mi_search_menuitem.set_sensitive(not value)
        self.decryptmenuitem.set_sensitive(value)
        if value:
            self.searchpanel.hide()
            self.clear_search_text()
            self.replacepanel.hide()
            # self.clear_search_text()

    @property
    def tabsize(self) -> int:
        return self.settings.tabsize

    @tabsize.setter
    def tabsize(self, value: int):
        self._currenttabsize = value
        self.set_mi_radio_tabsizes(self._currenttabsize)
        self.set_tab_size(self.textview, value)

    @property
    def insert_spaces_instead_of_tabs(self) -> bool:
        return self._insert_spaces_instead_of_tabs

    @insert_spaces_instead_of_tabs.setter
    def insert_spaces_instead_of_tabs(self, value: bool):
        self._insert_spaces_instead_of_tabs = value
        # self.settings.tabspaces = value

    @property
    def auto_indent(self) -> bool:
        return self._auto_indent

    @auto_indent.setter
    def auto_indent(self, value: bool):
        self._auto_indent = value

    def __init__(self, **kwargs):
        super(Handler, self).__init__(**kwargs)

        self._is_encrypted: bool = False
        self._is_saved: bool = False
        self._current_file: str = ""
        self._insert_spaces_instead_of_tabs = False
        self._auto_indent = False
        # settings widgets
        self.dlg_settings = builder.get_object("dlgsettings")

        self.textview = builder.get_object("textview1")

        ''' for line numbers. DOESN'T WORK
        
        long_text = u"0 Your Answer\n\
         1 Thanks for contributing an answer to Stack Overflow!\n\
         2   Please be sure to answer the question. Provide details and share your research!\n\
         3\n\
         4 But avoid …\n\
         5\n\
         6  Asking for help, clarification, or responding to other answers.\n\
         7  Making statements based on opinion; back them up with references or personal experience.\n\
         8\n\
         9To learn more, see our tips on writing great answers.\n\
        10 Your Answer\n\
        11Thanks for contributing an answer to Stack Overflow!\n\
        12    Please be sure to answer the question. Provide details and share your research!\n\
        13 \n\
        14 But avoid …\n\
        15\n\
        16   Asking for help, clarification, or responding to other answers.\n\
        17    Making statements based on opinion; back them up with references or personal experience.\n\
        18 \n\
        19 To learn more, see our tips on writing great answers.\n"

        tooltip = u'textview avec numérotation de ligne\n\
        <b>Warning</b> la numérotation ne fonctionne correctement que si on ne fait pas circuler le scrolling'

        
        self.textview.set_border_window_size(Gtk.TextWindowType.RIGHT, 54)
        self.textview.set_border_window_size(Gtk.TextWindowType.LEFT, 54)
        '''

        '''
        self.textview.modify_base(Gtk.StateType.NORMAL, Gdk.color_parse('light green'))  # non OK change marg like in gtk2
        self.textview.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('orange'))  # background text OK
        self.textview.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse('green'))  # modifie la couleur du texte OK
        self.textview.modify_font(Pango.FontDescription('Arial normal 10'))  # OK
        '''
        self.text_buffer = self.textview.get_buffer()
        # self.text_buffer.insert_at_cursor(long_text)  # sympath pour inserer la où est le curseur mais pas nécessaire ici

        self.settings: Settings = Settings(textview=self.textview, handler=self)

        # read settings from config file
        resreadsett = self.settings.read_ini()
        statusread = False
        msg = ""
        if resreadsett is not None:
            statusread = resreadsett[0]
            if not statusread:
                msg = resreadsett[1]
                MessageDialogs.show_messagebox_info(window, title=_("Config"), message=msg)

        if not statusread:
            # set default settings
            self.settings.set_defaults()


        # translate to current idiom
        self.translate()

        # Initialize settings dialog widgets
        self.initialize_settings_dialog()

        self.text_buffer.connect("changed", self.on_textbuffer_changed, None)

        # notify everytime cursor position changes
        self.text_buffer.connect("notify::cursor-position",
                            self.on_cursor_position_changed)

        self.tag_found = self.text_buffer.create_tag("found", background="yellow")
        self.start_search_iter = None
        self.end_search_iter = None

        #  search panel
        self.searchpanel = builder.get_object("searchpanel")
        self.searchentry = builder.get_object("searchentry")

        self.replacepanel = builder.get_object("replacepanel")
        self.replaceentry = builder.get_object("replaceentry")

        #  self.searchentry.set_buffer(self.text_buffer)

        self.is_saved = True

        # self.searchpanel.hide()

        self.statusbar: Gtk.Statusbar
        self.statusbar = builder.get_object("statusbar_main")

        #  self.searchbar = builder.get_object("searchbar")
        #  searchentry = Gtk.SearchEntry()
        #  self.searchbar.connect_entry(searchentry)
        #  self.searchbar.add(searchentry)

        #self.misave = builder.get_object("mi_save")
        # self._window = window
        # self.mi_quit = builder.get_object("mi_quit")
        # self.mi_quit.connect("activate", self.on_mi_quit_activate)

        # self.lb_texto.set_text('Alô mundo!')

    def translate(self):
        """
        Translates labels text to current selected idiom
        :return: None
        :rtype: Any
        """
        # Search menu
        self.mi_search_menuitem = builder.get_object("mi_search")
        self.mi_search_menuitem.set_label(_("_Search"))
        self.mi_find_menuitem = builder.get_object("mi_find")
        self.mi_find_menuitem.set_label(_("_Find"))
        self.mi_find_next_menuitem = builder.get_object("mi_find_next")
        self.mi_find_next_menuitem.set_label(_("_Find Next"))
        self.mi_find_previous_menuitem = builder.get_object("mi_find_previous")
        self.mi_find_previous_menuitem.set_label(_("_Find Previous"))
        self.mi_find_and_replace_menuitem = builder.get_object("mi_find_and_replace")
        self.mi_find_and_replace_menuitem.set_label(_("_Find And Replace"))
        self.mi_clearhighlights = builder.get_object("mi_clearhighlights")
        self.mi_clearhighlights.set_label(_("Clear Highlights"))

        # Document menu
        self.documentmenuitem = builder.get_object("mi_document")
        self.documentmenuitem.set_label(_("_Document"))
        self.encryptmenuitem = builder.get_object("mi_encrypt")
        self.encryptmenuitem.set_label(_("_Encrypt"))
        self.decryptmenuitem = builder.get_object("mi_decrypt")
        self.decryptmenuitem.set_label(_("_Decrypt"))
        self.autoindentmenuitem = builder.get_object("mi_autoindent")
        self.autoindentmenuitem.set_label(_("_Auto Indent"))
        self.tabsizemenuitem = builder.get_object("mi_tabsize")
        self.tabsizemenuitem.set_label(_("_Tab Size"))
        self.tabsizeothermenuitem = builder.get_object("mi_tabsize_other")
        self.tabsizeothermenuitem.set_label(_("_Other") + " ...")
        self.insertspacesmenuitem = builder.get_object("mi_insert_spaces")
        self.insertspacesmenuitem.set_label(_("_Insert Spaces"))

        # File menu
        self.mi_file_menuitem = builder.get_object("mi_file")
        self.mi_file_menuitem.set_label(_("_File"))
        self.mi_new_menuitem = builder.get_object("mi_new")
        self.mi_new_menuitem.set_label(_("_New"))
        self.mi_open_menuitem = builder.get_object("mi_open")
        self.mi_open_menuitem.set_label(_("_Open"))
        self.mi_open_encrypted_menuitem = builder.get_object("mi_open_encrypted")
        self.mi_open_encrypted_menuitem.set_label(_("_Open Encrypted Text"))
        self.mi_save_menuitem = builder.get_object("mi_save")
        self.mi_save_menuitem.set_label(_("_Save"))
        self.mi_saveas_menuitem = builder.get_object("mi_saveas")
        self.mi_saveas_menuitem.set_label(_("_Save As"))
        self.mi_quit_menuitem = builder.get_object("mi_quit")
        self.mi_quit_menuitem.set_label(_("_Quit"))

        # Edit menu
        self.editmenuitem = builder.get_object("mi_edit")
        self.editmenuitem.set_label(_("_Edit"))
        self.mi_cut_menuitem = builder.get_object("mi_cut")
        self.mi_cut_menuitem.set_label(_("_Cut"))
        self.mi_copy_menuitem = builder.get_object("mi_copy")
        self.mi_copy_menuitem.set_label(_("_Copy"))
        self.mi_paste_menuitem = builder.get_object("mi_paste")
        self.mi_paste_menuitem.set_label(_("_Paste"))
        self.mi_delete_menuitem = builder.get_object("mi_delete")
        self.mi_delete_menuitem.set_label(_("_Delete"))
        self.mi_select_all_menuitem = builder.get_object("mi_select_all")
        self.mi_select_all_menuitem.set_label(_("_Select All"))
        self.mi_preferences = builder.get_object("mi_preferences")
        self.mi_preferences.set_label(_("_Preferences"))

        # View menu
        self.viewmenuitem = builder.get_object("mi_view")
        self.viewmenuitem.set_label(_("_View"))
        self.mi_check_word_wrap_menuitem = builder.get_object("mi_check_word_wrap")
        self.mi_check_word_wrap_menuitem.set_label(_("_Word Wrap"))
        self.mi_select_font_menuitem = builder.get_object("mi_select_font")
        self.mi_select_font_menuitem.set_label(_("_Select Font"))

        self.helpmenuitem = builder.get_object("mi_help")
        self.helpmenuitem.set_label(_("_Help"))
        self.aboutmenuitem = builder.get_object("mi_about")
        self.aboutmenuitem.set_label(_("_About"))

        self.decryptmenuitem.set_sensitive(self.is_encrypted)
        self.editmenuitem.set_sensitive(not self.is_encrypted)

        # Search and replace panels
        self.btnclosesearchpanel = builder.get_object("btnclosesearchpanel")
        self.btnclosesearchpanel.set_label(_("Close"))

        self.btnReplace = builder.get_object("btnReplace")
        self.btnReplace.set_label(_("Replace"))

        self.btnreplaceall = builder.get_object("btnreplaceall")
        self.btnreplaceall.set_label(_("All"))

        # tab size dialog
        self.dialogscaletabsize: Gtk.Dialog
        self.dialogscaletabsize = builder.get_object("dlgtabsizechooser")
        self.scalertabsize = builder.get_object("scaletabsize")
        self.btncancelselecttabsize = builder.get_object("btncancelselecttabsize")
        self.btncancelselecttabsize.set_label(_("Cancel"))
        self.btnokselecttabsize = builder.get_object("btnokselecttabsize")
        self.btnokselecttabsize.set_label(_("OK"))

        self.dialogscaletabsize.set_title(_("Select Tab Size"))
        self.dialogscaletabsize.set_resizable(False)

        self.dlg_settings = builder.get_object("dlgsettings")
        self.dlg_settings.set_title(_("Preferences"))

        # preferences dialog
        self.labeldisplay = builder.get_object("labeldisplay")
        self.labeldisplay.set_label(_("Display"))

        self.checkbtnwrapword = builder.get_object("checkbtnwrapword")
        self.checkbtnwrapword.set_label(_("Wrap long lines"))

        self.labelfont = builder.get_object("labelfont")
        self.labelfont.set_label(_("Font"))

        #self.btnfont = builder.get_object("btnfont")
        #self.btnfont.set_label(_("No need"))

        self.labelidiom = builder.get_object("labelidiom")
        self.labelidiom.set_label(_("Idiom"))

        self.btnclosepref = builder.get_object("btnclosepref")
        self.btnclosepref.set_label(_("Close"))

        self.labelpageview = builder.get_object("labelpageview")
        self.labelpageview.set_label(_("View"))

        self.labelpageeditor = builder.get_object("labelpageeditor")
        self.labelpageeditor.set_label(_("Editor"))

        self.labelindentation = builder.get_object("labelindentation")
        self.labelindentation.set_label(_("Indentation"))

        self.label_tab_width = builder.get_object("label_tab_width")
        self.label_tab_width.set_label(_("Tab width:"))

        self.label_tab_mode = builder.get_object("label_tab_mode")
        self.label_tab_mode.set_label(_("Tab mode:"))

        self.checkbtnenableautoindent = builder.get_object("checkbtnenableautoindent")
        self.checkbtnenableautoindent.set_label(_("Enable automatic indentation"))

        self.cb_tab_mode: Gtk.ComboBox = builder.get_object("cbtabmode")
        idx = self.cb_tab_mode.get_active()
        self.cb_tab_mode.set_active(0)
        tree_iter = self.cb_tab_mode.get_active_iter()
        if tree_iter is not None:
            model = self.cb_tab_mode.get_model()
            model[tree_iter][1] = _("Insert Tabs")

        self.cb_tab_mode.set_active(1)
        tree_iter = self.cb_tab_mode.get_active_iter()
        if tree_iter is not None:
            model = self.cb_tab_mode.get_model()
            model[tree_iter][1] = _("Insert Spaces")

        self.cb_tab_mode.set_active(idx)


    def initialize_settings_dialog(self):
        """
        Initializes settings dialog widgets.
        :return: None
        :rtype: Any
        """
        # init tabmode combobox
        self.cb_tab_mode: Gtk.ComboBox = builder.get_object("cbtabmode")
        store = Gtk.ListStore(int, str)
        cell1 = Gtk.CellRendererText()
        cell2 = Gtk.CellRendererText()
        self.cb_tab_mode.pack_start(cell1, False)
        self.cb_tab_mode.pack_start(cell2, True)
        self.cb_tab_mode.add_attribute(cell1, 'int', 0)
        self.cb_tab_mode.add_attribute(cell2, 'text', 1)
        self.cb_tab_mode.set_id_column(0)
        store.append([0, _("Insert Tabs")])
        store.append([1, _("Insert Spaces")])
        self.cb_tab_mode.set_model(store)
        self.cb_tab_mode = builder.get_object("cbtabmode")
        if self.settings.tabspaces:
            self.cb_tab_mode.set_active(1)
        else:
            self.cb_tab_mode.set_active(0)

        # init idioms combobox
        self.cb_idioms: Gtk.ComboBox = builder.get_object("cbidioms")
        self.cb_idioms.set_active_id(self.settings.idiom)

        # word wrap
        self.checkbtnwrapword = builder.get_object("checkbtnwrapword")
        self.checkbtnwrapword.set_active(self.settings.word_wrap)

        # font button
        self.btnsettingsfont = builder.get_object("btnfont")
        self.btnsettingsfont.set_font_name(self.settings.font)

        # tab size
        self.spinbtntabsize = builder.get_object("spinbtntabsize")
        self.spinbtntabsize.set_value(self.settings.tabsize)

        # auto indentation
        self.checkbtnenableautoindent = builder.get_object("checkbtnenableautoindent")
        self.checkbtnenableautoindent.set_active(self.settings.auto_indent)

    def show_settings_dialog(self):
        dialog: Gtk.Dialog = self.dlg_settings  # builder.get_object("dlgsettings")
        dialog.set_title(_("Preferences"))
        dialog.run()
        #dialog.hide()
        #dialog.destroy()

    @staticmethod
    def get_password() -> str:
        """
        :return: Returns plain text password entered by the user if succeeded, empty string otherwise
        :rtype: String (str)
        """
        result = ""
        dialog = PwdDialog(parent=window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            # clean entry
            result = dialog.get_pwd_and_clear()
        else:
            pass

        dialog.destroy()
        return result

    def set_mi_radio_tabsizes(self, tabsize: int):
        mi_other = builder.get_object("mi_tabsize_other")
        otherstr = _("_Other")
        mi_other.set_label((otherstr + " {}").format("..."))
        if tabsize == 2:
            builder.get_object("mi_tabsize_2").set_active(True)
        elif tabsize == 3:
            builder.get_object("mi_tabsize_3").set_active(True)
        elif tabsize == 4:
            builder.get_object("mi_tabsize_4").set_active(True)
        elif tabsize == 8:
            builder.get_object("mi_tabsize_8").set_active(True)
        else:
            mi_other = builder.get_object("mi_tabsize_other")
            mi_other.set_active(True)
            strother = _("_Other")
            mi_other.set_label(strother + " (" + str(self.tabsize) + ")")

    def on_btnclosepref_clicked(self, widget):
        self.dlg_settings.hide()

    def on_btnfont_font_set(self, widget):
        font = widget.get_font_name()
        self.settings.font = font

    def on_checkbtnwrapword_toggled(self, widget):
        self.settings.word_wrap = widget.get_active()

    # handles text zoom in/out
    def on_textview1_scroll_event(self, widget, event):
        """ handles on scroll event"""
        zoom_incr = 2
        minsize = 3
        maxsize = 60

        # linevis = TextViewHelper.get_first_visible_line(self.textview)
        # print("First line visible = {}".format(linevis))

        # Handles zoom in / zoom out on Ctrl+mouse wheel
        accel_mask = Gtk.accelerator_get_default_mod_mask()
        if event.state & accel_mask == Gdk.ModifierType.CONTROL_MASK:
            direction = event.get_scroll_deltas()[2]
            size = self.settings.getfontsize()
            print("current size = {0}".format(size))
            new_size = size
            if direction > 0:  # scrolling down -> zoom out
                new_size -= zoom_incr
                #self.set_zoom_level(self.get_zoom_level() - 0.1)
            else:
                new_size += zoom_incr
                #  self.set_zoom_level(self.get_zoom_level() + 0.1)

            new_size = min(max(minsize, new_size), maxsize)
            self.settings.setfontsize(new_size)

    #  ------------ Line Numbers -------------
    # DOESN'T WORK
    '''
    def recup_lignes(self, textview: Gtk.TextView, premier_y, dernier_y, coords_buffer: [], numeros: []):
        # On recupere l'iterateur du premier y.
        iter, top = textview.get_line_at_y(premier_y)

        # On recupere la position de chaque iterateur et on l'ajoute
        # a la liste. On s'arrete apres dernier_y.
        nombre, taille = 0, 0
        while not iter.is_end():
            y, hauteur = textview.get_line_yrange(iter)  # textbuffer.get_line_yrange(iter)
            coords_buffer.append(y)
            num_ligne = iter.get_line()
            numeros.append(num_ligne)
            nombre += 1
            # suite nouvelle étude je le remet
            if (y + hauteur) >= dernier_y:
                break
            iter.forward_line()
        return nombre

    def on_textview1_draw(self, text_view: Gtk.TextView, cairo_context):
        text_buffer = text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        text = text_buffer.get_text(start, end, False)

        nlines = text.count("\n") + 1

        # collect size of visible part of window
        rectangle_visible = text_view.get_visible_rect()
        premier_y = rectangle_visible.y
        dernier_y = premier_y + rectangle_visible.height



        # collect numeros & pixels to be display
        numeros = []
        pixels = []
        nombre = self.recup_lignes(text_view, premier_y, dernier_y, pixels, numeros)
        # Affichage de numéros internationalises !
        layout: Pango.Layout = text_view.create_pango_layout("")

        pos_horizontal = 2
        for i in range(nombre):
            x, pos = text_view.buffer_to_window_coords(Gtk.TextWindowType., 0, pixels[i])
            chaine = "<span weight='bold' foreground='red'>%d </span>" % numeros[i]
            #layout.set_text(chaine)
            layout.set_markup(chaine, len(chaine))
            # met les numeros dans la zone texte

            Gtk.render_layout(text_view.get_style_context(), cairo_context, pos_horizontal, pos, layout)

    '''

    def on_textbuffer_changed(self, start, end):
        self.is_saved = False
        if self.start_search_iter is not None:
            self.clear_search_iters()

        self.update_statusbar(self.current_file, self.is_encrypted, not self.textview.get_editable())

        print("Text buffer changed.")

    def remove_tags(self):
        start = self.text_buffer.get_start_iter()
        end = self.text_buffer.get_end_iter()
        self.text_buffer.remove_all_tags(start, end)

    # clears text
    def clear_text(self):
        self.remove_tags()
        self.text_buffer.set_text("")
        #Handler.issaved = False;

    def get_text(self) -> str:
        startIter = self.text_buffer.get_start_iter()
        endIter = self.text_buffer.get_end_iter()
        text =  self.text_buffer.get_text(startIter, endIter, False)
        return text

    @staticmethod
    def ensure_extension(file_path: str, is_enc: bool) -> str:
        """
        Ensures that the file_path has the right extension.
        @param file_path: Full file path.
        @param is_enc: If True is an encrypted file, False otherwise.
        @return: Returns the file_path with right extension.
        """
        FResult: str = file_path
        if is_enc:
            # remove ".txt" suffix if exist
            if FResult.endswith('.' + Handler.PLAIN_TEXT_FILE_EXT):
                FResult.removesuffix('.' + Handler.PLAIN_TEXT_FILE_EXT)

            # add ".txt.encrypted" extension if not exist
            if not FResult.endswith(Handler.ENC_TEXT_FILE_EXT):
                FResult += '.' + Handler.ENC_TEXT_FILE_EXT
        else:
            # remove ".txt.encrypted" suffix if exist
            if FResult.endswith('.' + Handler.ENC_TEXT_FILE_EXT):
                FResult.removesuffix('.' + Handler.ENC_TEXT_FILE_EXT)

            # add ".txt" extension if not exist
            if not FResult.endswith(Handler.PLAIN_TEXT_FILE_EXT):
                FResult += '.' + Handler.PLAIN_TEXT_FILE_EXT

        return FResult

    def on_cursor_position_changed(self, buffer, data=None):
        self.update_statusbar(self.current_file, self.is_encrypted, not self.textview.get_editable())

    def update_statusbar(self, file_path: str, encrypted: bool, locked: bool):
        """
        :param file_path: Current open file path.
        :type file_path: str
        :param encrypted: True if is encrypted file, False otherwise.
        :type encrypted: bool
        :param locked: True if current file content is not editable, False otherwise.
        :type locked: bool
        """
        notif: str = ""
        sep: str = "  "
        result = TextViewHelper.get_line_col_from_cursor(buffer=self.text_buffer)
        if result is not None:
            # print(_("Line"))
            notif = str(_("Line") + ": {} " + _("Col") + ": {}").format(result[0], result[1])

        if len(file_path) > 0:
            # clear status bar
            # self.statusbar.push(STATBAR_OPENFILE_ID, notif)
            #self.statusbar.push(STATBAR_ENCRYPTED_ID, "")
            #self.statusbar.push(STATBAR_LOCKED_ID, "")
            # else:
            notif += sep + _("File") + ": " + file_path
            # self.statusbar.push(STATBAR_OPENFILE_ID, file_path)
        if encrypted:
            notif += " - " + _("Encrypted")
                # self.statusbar.push(STATBAR_ENCRYPTED_ID, "Encrypted")
            # else:
                # self.statusbar.push(STATBAR_ENCRYPTED_ID, "")

        if locked:
            notif += " - " + _("Locked")
                # self.statusbar.push(STATBAR_LOCKED_ID, "Locked")
            # else:
                # self.statusbar.push(STATBAR_LOCKED_ID, "")

        self.statusbar.push(STATBAR_OPENFILE_ID, notif)


    def open_file(self, encrypted: bool = False) -> str:
        """
        :param encrypted: True if it's an encrypted text file, False otherwise (default).
        :type encrypted: bool
        :return: Returns the selected file path if any, empty string otherwise.
        :rtype: string (str)
        """
        FResult = ""
        dialog = Gtk.FileChooserDialog(_("Please choose a file"), window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        btn_open = dialog.get_widget_for_response(Gtk.ResponseType.OK)
        btn_open.set_label(_("Open"))
        btn_cancel = dialog.get_widget_for_response(Gtk.ResponseType.CANCEL)
        btn_cancel.set_label(_("Cancel"))

        dfilter = Gtk.FileFilter()

        # all files fiter
        dfilter_all = Gtk.FileFilter()
        dfilter_all.set_name(_("All files (*.*)"))
        dfilter_all.add_pattern("*.*")

        if encrypted:
            dfilter.set_name(_("Encrypted text File (*.encrypted)"))
            dfilter.add_pattern("*.{}".format(Handler.ENC_TEXT_FILE_EXT))
            dialog.add_filter(dfilter)
            dialog.set_filter(dfilter)
        else:
            dfilter.set_name(_("Text file (*.txt)"))
            dfilter.add_pattern("*.{}".format(Handler.PLAIN_TEXT_FILE_EXT))
            dialog.add_filter(dfilter)
            dialog.set_filter(dfilter)

        dialog.add_filter(dfilter_all)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            self.current_file = file_path
            print("Open clicked")
            print("File selected: " + file_path)
            # self.labelframe.set_label(os.path.basename(file_path))
            # self.editor.open_file(file_path)
            f = open(file_path, "r")
            self.text_buffer.set_text(f.read())
            f.close()
            self.is_saved = True
            self.is_encrypted = encrypted
            FResult = file_path

        elif response == Gtk.ResponseType.CANCEL:
            FResult = ""
            print("Cancel clicked")

        dialog.destroy()
        return FResult

    # retrieves and stores the save file path in instance property (doesn't save content)
    def save_file(self, is_new: bool, is_enc: bool, filepath="newfile.txt") -> bool:
        """
        Saves current file content.

        :param is_new: True if saving a new file, False otherwise.
        :param is_enc: True if file or content is encrypted, False otherwise.
        :param filepath: The full file path.
        :return: Returns True if succeeded, False otherwise.
        """
        _exit = False
        title = "__untitled"
        return_value = True

        if is_new:
            title = _("Please enter new file name")
        else:
            title = _("Save as ...")

        while not _exit:
            dialog = Gtk.FileChooserDialog(title, window,
                                           Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

            btn_save = dialog.get_widget_for_response(Gtk.ResponseType.OK)
            btn_save.set_label(_("Save As"))
            btn_cancel = dialog.get_widget_for_response(Gtk.ResponseType.CANCEL)
            btn_cancel.set_label(_("Cancel"))

            if is_enc:
                dfilter2 = Gtk.FileFilter()
                dfilter2.set_name(_("Encrypted text File (*.encrypted)"))
                dfilter2.add_pattern("*.{}".format(Handler.ENC_TEXT_FILE_EXT))
                dialog.add_filter(dfilter2)
                dialog.set_filter(dfilter2)
            else:
                dfilter1 = Gtk.FileFilter()
                dfilter1.set_name(_("Text file (*.txt)"))
                dfilter1.add_pattern("*.{}".format(Handler.PLAIN_TEXT_FILE_EXT))
                dialog.add_filter(dfilter1)
                dialog.set_filter(dfilter1)

            '''
            dfilter3 = Gtk.FileFilter()
            dfilter3.set_name("All files (*.*)")
            dfilter3.add_pattern("*.*")

            dialog.add_filter(dfilter1)
            dialog.add_filter(dfilter2)
            dialog.add_filter(dfilter3)
            '''
            '''
            if self._is_encrypted:
                dialog.set_filter(dfilter2)
            else:
                dialog.set_filter(dfilter1)
            '''

            dialog.set_filename(self.current_file)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                file_path = dialog.get_filename()

                # append file extension in not exist
                file_path = Handler.ensure_extension(file_path=file_path, is_enc=is_enc)

                try:
                    # create new file only if doesn't exist yet
                    f = None
                    if is_new:
                        f = open(file_path, "x")
                    else:
                        f = open(file_path, "w")

                    self.current_file = file_path
                    f.close()

                    print("New clicked")
                    print("File selected: " + file_path)
                    # self.statusbar.push(STATBAR_OPENFILE_ID, file_path)
                    _exit = True
                    return_value = True

                except Exception as e:
                    if isinstance(e, FileExistsError):
                        MessageDialogs.show_messagebox_info(window, _("Warning message"), _("File already exists"),
                                                  _("Please choose another filename."))

                    print("Oops! ", e.__class__, " occurred.")

            elif response == Gtk.ResponseType.CANCEL:
                _exit = True
                print("Cancel clicked")
                return_value = False

            dialog.destroy()

        return return_value

    # ####################
    # Event Handlers
    # ###################

    def on_close_main_window(self):
        print("Caught a quitting event!!!\n")

        bInhibit = False
        if not self.is_saved:
            answer = MessageDialogs.show_messagebox_YesNo(window, _("Warning Message"),
                                                          _("Current file has changed. All changes will be lost!")
                                                          + "\n\n"
                                                          + _("Do you really want to close?"))

            if answer == Gtk.ResponseType.NO:
                bInhibit = True

        if not bInhibit:    # going to close
            # try to save settings
            saveres = self.settings.write_ini("")
            msg = ""
            saveok = False
            if saveres is None:
                msg = _("Unable to save current application settings!")
            else:
                saveok = saveres[0]

            if not saveok:
                msg = saveres[1]
                answer = MessageDialogs.show_messagebox_YesNo(window, _("Warning Message"),
                                                              msg
                                                              + "\n\n"
                                                              + _("Do you want to close anyway?"))
                if answer == Gtk.ResponseType.NO:
                    bInhibit = True

        return bInhibit  # return True prevents window from closing

    def on_main_window_delete_event(self, widget, event):
        return self.on_close_main_window()

    def on_main_window_destroy(self, window):
        Gtk.main_quit()

    def on_cbidioms_changed(self, widget):
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            langcode = model[tree_iter][0]
            self.settings.idiom = langcode
            print("Selected: lang=%s" % langcode)

    def on_cbtabmode_changed(self, widget):
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            tabmodeid = model[tree_iter][0]
            if tabmodeid == 0:
                # insert tabs
                self.settings.tabspaces = False
            else:
                # insert spaces
                self.settings.tabspaces = True

    def on_mi_quit_activate(self, widget):
        if not self.on_close_main_window():
            Gtk.main_quit()

    def on_mi_new_activate(self, widget):
        do_save = True
        # check if current content has changed
        if not self.is_saved:
            if Gtk.ResponseType.NO == MessageDialogs.show_messagebox_YesNo(window, _("Confirmation"), _("Your changes have not yet been saved.\n\n") + _("Are you sure you want to continue and lose all pending changes?")):
                return
            #else:
          #      do_save = False
        #else:
        #    do_save = False  # already saved

        # if do_save:
        #    if not self.save_file(True, self.is_encrypted, self.current_file):
        #        if Gtk.ResponseType.NO == MessageDialogs.show_messagebox_YesNo(window, _("Confirmation"),
        #                                    _("Pending changes were not saved.\nDo you want to continue anyway and "
        #                                      "lose all pending changes?")):
        #            return  # failed to save file

        self.clear_text()
        self.is_encrypted = False
        self.is_saved = True

    def on_mi_open_activate(self, widget):
        if not self.is_saved:
            title = _("Warning Message")
            response = MessageDialogs.show_messagebox_YesNo(window, title, _("There are pending changes that have not yet been saved.")
                        + "\n\n"
                        + _("Do you want to continue anyway and lose all pending changes?"))
            if response == Gtk.ResponseType.NO:
                return

        open_file_path: str = self.open_file(False)

        if len(open_file_path) > 0:
            self.update_statusbar(self.current_file, self.is_encrypted, not self.textview.get_editable())

    def on_mi_open_encrypted_activate(self, widget):
        if not self.is_saved:
            response = MessageDialogs.show_messagebox_YesNo(window, _("Warning Message"),
                      _("There are pending changes that have not yet been saved.")
                        + "\n\n"
                        + _("Do you want to continue anyway and lose all pending changes?"))
            if response == Gtk.ResponseType.NO:
                return

        open_file_path: str = self.open_file(True)
        if len(open_file_path) > 0:
            self.update_statusbar(self.current_file, self.is_encrypted, not self.textview.get_editable())

    def on_mi_save_activate(self, widget):
        if self.current_file == "":
            if self.save_file(True, self.is_encrypted, self.current_file):
                with open(self.current_file, 'w') as f:
                    f.write(self.get_text())

                self.is_saved = True
        else:
            with open(self.current_file, 'w') as f:
                f.write(self.get_text())

            self.is_saved = True

        self.update_statusbar(self.current_file, self.is_encrypted, not self.textview.get_editable())
        print("File saved successfully at {}".format(self.current_file))

    def on_mi_saveas_activate(self, widget):
        if self.save_file(True, self.is_encrypted):
            with open(self.current_file, 'w') as f:
                f.write(self.get_text())

            self.is_saved = True
            self.update_statusbar(self.current_file, self.is_encrypted, not self.textview.get_editable())

    # edit menu event handlers

    # cut selected text to clipboard
    def on_mi_cut_activate(self, widget):
        self.text_buffer.cut_clipboard(clipboard, True)

    # copy selected text to clipboard
    def on_mi_copy_activate(self, widget):
        self.text_buffer.copy_clipboard(clipboard)

    # paste text from clipboard
    def on_mi_paste_activate(self, widget):
        self.text_buffer.paste_clipboard(clipboard, None, True)

    # deletes selected text
    def on_mi_delete_activate(self, widget):
        if self.text_buffer.delete_selection(True, True):
            pass

    def on_mi_select_font_activate(self, widget):
        dlg = Gtk.FontSelectionDialog(title=_("Select Font"))
        dlg.set_modal(True)
        btnok = dlg.get_widget_for_response(Gtk.ResponseType.OK)
        btnok.set_label(_("OK"))
        btncancel = dlg.get_widget_for_response(Gtk.ResponseType.CANCEL)
        btncancel.set_label(_("Cancel"))
        response = dlg.run()

        if response == Gtk.ResponseType.OK:
            # font_description = dlg.get_font_map()
            fontname = dlg.get_font_name()
            print("You chose: " + fontname)
            self.settings.font = fontname
            #  self.textview.modify_font(Pango.FontDescription(fontname))

        elif response == Gtk.ResponseType.CANCEL:
            pass

        dlg.destroy()

    def on_mi_select_all_activate(self, widget):
        startiter, enditer = self.text_buffer.get_bounds()
        self.text_buffer.select_range(startiter, enditer)

    def Unselect_all(self):
        if self.text_buffer.get_has_selection():
            startiter, enditer = self.text_buffer.get_selection_bounds()
            if startiter is not None:
                enditer = startiter
                #self.text_buffer.insert(startiter, "", 0)


    def on_mi_check_word_wrap_toggled(self, widget):
        checked = widget.get_active()
        self.settings.word_wrap = checked

    def on_mi_about_activate(self, widget):
        about = Gtk.AboutDialog()
        about.set_program_name(APP_NAME) #  "Cryptedit")
        about.set_version("0.1")
        about.set_authors(['Tiago C. Teixeira'])
        image1 = Gtk.Image()
        image1.set_from_file("crypteditlogo.png")
        about.set_logo(image1.get_pixbuf())
        app_year = app_creation_date.year
        current_year = datetime.date.today().year
        cright_str: str = ""
        if app_year == current_year:
            cright_str = _("Copyright {} (c) Tiago C. Teixeira").format(app_year)
        else:
            cright_str = _("Copyright {}-{} (c) Tiago C. Teixeira").format(app_year, current_year)

        about.set_copyright(cright_str)
        about.set_comments(_("A simple editor that allows you to edit, encrypt and decrypt text files."))
        #  about.set_license('<a href="https://www.w3schools.com">Visit W3Schools.com!</a>')
        #  about.set_website("http://www.xpto.com")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.run()
        about.destroy()

    def on_mi_findandreplace_activate(self, widget):
        if not self.searchpanel.is_visible():
            self.searchpanel.show() # show_all() is disabled at startup. use show(9 instead
        #else:
        #    self.searchpanel.hide()

        if not self.replacepanel.is_visible():
            self.replacepanel.show() # show_all() is disabled at startup. use show(9 instead
        #else:
        #    self.replacepanel.hide()

    def on_mi_find_activate(self, widget):
        if not self.searchpanel.is_visible():
            self.searchpanel.show() # show_all() is disabled at startup. use show(9 instead
        """else:
            self.searchpanel.show()

            self.searchpanel.hide()
            if self.replacepanel.is_visible():
                self.replacepanel.hide()    # hide replace panel also
        """

    def on_mi_find_next_activate(self, widget):
        self.search_down()

    def on_mi_find_previous_activate(self, widget):
        self.search_up()

   # def on_mi_search_activate(self, widget):
        """
        Clears marked highlighted text.
        :param widget: Widget that raised event.
        :type widget:
        :return: None
        :rtype: Any
        """
    #    self.ClearHighlights()

    def on_btnclosesearchpanel_clicked(self, widget):
        self.searchpanel.hide()
        self.replacepanel.hide()
        print("Close search panel clicked")

    def on_btnclearreplacetext_clicked(self, widget):
        self.clear_replace_text()

    def on_btnclearsearchtext_clicked(self, widget):
        self.clear_search_text()

    def on_btnsearchdown_clicked(self, widget):
        self.search_down()

    def on_btnsearchup_clicked(self, widget):
        self.search_up()

    def clear_search_iters(self):
        self.start_search_iter = None
        self.end_search_iter = None

    def clear_search_text(self):
        self.searchentry.set_text("")
        self.remove_tags()
        self.start_search_iter = None
        self.end_search_iter = None

    def ClearHighlights(self):
        self.remove_tags()
        self.start_search_iter = None
        self.end_search_iter = None
        self.Unselect_all()

    def on_mi_clearhighlights_activate(self, widget):
        self.ClearHighlights()

    def clear_replace_text(self):
        self.replaceentry.set_text("")

    def search_down(self):
        search_text = self.searchentry.get_text()
        if len(search_text) == 0:
            return False

        self.prepare_search_iters(True)
        self.search_and_mark_forward(search_text, self.start_search_iter)

    def search_up(self):
        search_text = self.searchentry.get_text()
        if len(search_text) == 0:
            return False

        self.prepare_search_iters(False)
        self.search_and_mark_backward(search_text, self.start_search_iter)

    def prepare_search_iters(self, is_forward: bool):
        if self.start_search_iter is None:      #  search from cursor
            cursor_mark = self.text_buffer.get_insert()
            start = self.text_buffer.get_iter_at_mark(cursor_mark)
            self.start_search_iter = start
        else:
            # verify if TextIters are valid
            # self.start_search_iter.
            pass

         #   if is_forward:
          #      self.start_search_iter = self.end_search_iter

        # else:
        #    self.start_search_iter = self.earch_iter      # search from last search position

        #  if start.get_offset() == self.text_buffer.get_char_count():
        #    start = self.text_buffer.get_start_iter()
        #    self.start_search_iter = start

    def on_mi_autoindent_toggled(self, widget):
        self.auto_indent = widget.get_active()

    def on_textview1_key_press_event(self, widget, event):
        if self.auto_indent:
            if (event.keyval == Gdk.KEY_Return) or (event.keyval == Gdk.KEY_KP_Enter):
                cursor_mark = self.text_buffer.get_insert()
                end_iter = self.text_buffer.get_iter_at_mark(cursor_mark)
                result = end_iter.backward_search('\n', 0, self.text_buffer.get_start_iter())
                pos = 1
                if result is None:
                    start_iter = self.text_buffer.get_start_iter()
                    pos = 0
                else:
                    start_iter = result[0]
                
                line_text: str = self.text_buffer.get_text(start_iter, end_iter, True)
                indent_str: str = ""
                length = len(line_text)
                while (pos < length) and (line_text[pos] == ' ' or line_text[pos] == '\t'):
                    indent_str += line_text[pos]
                    pos += 1

                if len(indent_str) > 0:
                    self.text_buffer.insert_at_cursor(Handler.END_OF_LINE_MARK)
                    self.text_buffer.insert_at_cursor(indent_str)
                    return True

                return False

        if self.insert_spaces_instead_of_tabs:
            if event.keyval == Gdk.KEY_Tab:
                text: str = self.tabsize * ' '
                self.text_buffer.insert_at_cursor(text, -1)
                return True  # if True means key is already handled here

        return False

    def on_mi_insert_spaces_toggled(self, widget):
        is_on: bool = widget.get_active()
        self.insert_spaces_instead_of_tabs = is_on

    def search_and_mark_forward(self, text: str, start: Gtk.TextIter):
        # check if has text selected, otherwise get_selection_bounds() can not unpack values
        if self.text_buffer.get_has_selection():
            start_sel_iter, end_sel_iter = self.text_buffer.get_selection_bounds()
            if start_sel_iter is not None:
                start = end_sel_iter

        end_iter = self.text_buffer.get_end_iter()
        self.end_search_iter = end_iter
        match = start.forward_search(text, Gtk.TextSearchFlags.TEXT_ONLY, end_iter)

        if match is not None:
            match_start, match_end = match
            self.text_buffer.apply_tag(self.tag_found, match_start, match_end)
            self.start_search_iter = match_end
            self.text_buffer.select_range(match_start, match_end)


            #  self.search_and_mark(text, match_end)  # recursive call

    def search_and_mark_backward(self, text: str, start: Gtk.TextIter):
        end = self.text_buffer.get_start_iter()
        self.end_search_iter = end

        # check if has text selected, otherwise get_selection_bounds() can not unpack values
        if self.text_buffer.get_has_selection():
            start_sel_iter, end_sel_iter = self.text_buffer.get_selection_bounds()
            if start_sel_iter is not None:
                start = start_sel_iter

        match = start.backward_search(text, 0, end)

        if match is not None:
            match_start, match_end = match
            self.text_buffer.apply_tag(self.tag_found, match_start, match_end)
            self.start_search_iter = match_start
            self.text_buffer.select_range(match_start, match_end)


            #  self.search_and_mark(text, match_end)  # recursive call

    def search_and_mark_all(self, text: str, start: Gtk.TextIter):
        end = self.text_buffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match is not None:
            match_start, match_end = match
            self.text_buffer.apply_tag(self.tag_found, match_start, match_end)
            self.search_and_mark(text, match_end)   # recursive call

    @staticmethod
    def leninbytes(text: str):
        """
        Gets the text length in bytes
        :return: Returns the utf8 text length in bytes
        :rtype: int
        """
        return len(text.encode('utf-8'))

    def search_and_replace_all(self, start: Gtk.TextIter, searchtext: str, replacetext: str):
        if len(searchtext) > 0:
            if len(replacetext) > 0:
                if searchtext != replacetext:
                    end = self.text_buffer.get_end_iter()
                    match = start.forward_search(searchtext, 0, end)

                    if match is not None:
                        match_start, match_end = match
                        # self.text_buffer.select_range(match_start, match_end)
                        self.text_buffer.delete(match_start, match_end)
                        self.text_buffer.insert(match_start, replacetext, Handler.leninbytes(replacetext))
                        match_start.backward_chars(len(replacetext))
                        # replace_end = Gtk.TextIter()
                        replace_end = match_start.copy()
                        if replace_end.forward_chars(len(replacetext)):
                            self.text_buffer.apply_tag(self.tag_found, match_start, replace_end)

                        newstartiter = match_start  # self.text_buffer.get_iter_at_mark(self.text_buffer.get_insert())
                        self.search_and_replace_all(newstartiter, searchtext, replacetext)  #  recursive call

    def on_btnreplaceall_clicked(self, widget):
        stext = self.searchentry.get_text()
        rtext = self.replaceentry.get_text()
        self.search_and_replace_all(self.text_buffer.get_start_iter(), stext, rtext)


    def on_btnReplace_clicked(self, button):
        result = self.text_buffer.get_selection_bounds()
        if len(result) == 2:
            start_iter, end_iter = result[0], result[1]
            replace = self.replaceentry.get_text()
            length = len(replace)
            if length > 0:
                # self.text_buffer.move_mark(self.search_mark, end_iter)
                self.text_buffer.delete(start_iter, end_iter)
                self.text_buffer.insert(start_iter, replace, length)
                #  self.search_context.replace(start_iter, end_iter, replace, length)

                search_text = self.searchentry.get_text()
                if len(search_text) > 0:
                    self.prepare_search_iters(True)
                    self.search_and_mark_forward(search_text, self.start_search_iter)

    def on_btnReplace_activate(self, widget):
        pass

    def on_mi_encrypt_activate(self, widget):
        contentStr = self.get_text()
        if len(contentStr) > 0:
            pwd: str = Handler.get_password()
            if len(pwd) > 0:
                encStr = Encryptor.Encrypt(raw=contentStr, password=pwd)
                self.text_buffer.set_text(encStr)
                self.is_encrypted = True
                self.update_statusbar(self.current_file, self.is_encrypted, not self.textview.get_editable())

    def on_mi_decrypt_activate(self, widget):
        contentStr = self.get_text()
        if len(contentStr) > 0:
            pwd: str = Handler.get_password()
            if len(pwd) > 0:
                decStr, state = Encryptor.Decrypt(enc=contentStr, password=pwd)
                if state:
                    self.text_buffer.set_text(decStr)
                    self.is_encrypted = False
                    self.update_statusbar(self.current_file, self.is_encrypted, not self.textview.get_editable())
                else:
                    # failed to decrypt
                    MessageDialogs.show_messagebox_info(window, _("Failed to decrypt"), _("Invalid password!"))

    def on_mi_tab_size_toggled(self, widget):
        if widget.get_active():
            label = widget.get_label()[1:]
            self.tabsize = int(label)

    def on_mi_tabsize_other_activate(self, widget):
        if widget.get_active():
            self.dialogscaletabsize = builder.get_object("dlgtabsizechooser")
            dialog = self.dialogscaletabsize
            adj: Gtk.Adjustment
            adj = builder.get_object("adjustmenttabsize")
            adj.set_value(self.tabsize)
            #dialog.__setattr__("minimizable", False)
            dialog.run()
            #dialog.destroy()

    def on_btncancelselecttabsize_clicked(self, widget):
        self.dialogscaletabsize.hide()
        self.dialogscaletabsize = builder.get_object("dlgtabsizechooser")
        self.set_mi_radio_tabsizes(self.tabsize)

    def on_btnokselecttabsize_clicked(self, widget):
        adj: Gtk.Adjustment
        adj = builder.get_object("adjustmenttabsize")
        val: int = int(adj.get_value())
        self.tabsize = val
        dialog = self.dialogscaletabsize
        dialog.hide()  # destroy()
        self.dialogscaletabsize = builder.get_object("dlgtabsizechooser")

        print("OK button clicked")

    @staticmethod
    def set_tab_size(textview: Gtk.TextView, tab_width: int):
        tabs = Pango.TabArray(1, True)
        # tab_width = Pango.extents_to_pixels(tab_width)
        tabs.set_tab(0, Pango.TabAlign.LEFT, int(float(tab_width) * 8)) # tab width in pixels
        textview.set_tabs(tabs)

    def on_mi_preferences_activate(self, widget):
        self.show_settings_dialog()
        print("Preferences activated")


def main():
    """
    Application entry point
    :return: None
    :rtype: Any
    """

    define_globals()
    builder.connect_signals(Handler())
    window.show_all()
    Gtk.main()


