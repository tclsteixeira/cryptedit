import gettext
import gi
import os
import configparser
from gi.repository.GObject import Object

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk


# from main import Handler

class Settings:

    _ = gettext.gettext
    ___ = gettext.ngettext  # plural sintax -> ngettext(singular: str, plural: str, n: int)

    dir_path = ""
    file_name = "config.ini"
    secview = "view"
    seceditor = "editor"

    supported_idioms_keys = ['en', 'pt', 'el']
    supported_idioms = {'en': 'English', 'el': 'Greek', 'pt': 'Portuguese'}
    id_en = 0
    id_el = 1
    id_pt = 2

    # current_idiom: str = supported_idioms[iden]

    def __init__(self, textview: Gtk.TextView, handler):
        self.handler = handler
        self.textview = textview
        self.default_auto_indent = False
        self.default_tabsize = 8
        self.default_tabspaces = False
        self.default_font = 'Sans 10'
        self.default_word_wrap = True
        self.default_idiom = 'en'
        self._auto_indent = self.default_auto_indent
        self._tabsize = self.default_tabsize
        self._tabspaces = self.default_tabspaces
        self._selected_font = self.default_font
        self._word_wrap = True
        self._idiom = "pt"
        self._file_path = ""

    @staticmethod
    def default_file_path() -> str:
        """
        Gets the settings file path
        :return: Returns the settings file path.
        :rtype: str
        """
        if (Settings.dir_path is None) or (Settings.dir_path == ""):
            return f"{Settings.file_name}"
        else:
            return f"{Settings.dir_path}{os.path.sep}{Settings.file_name}"

    @property
    def auto_indent(self) -> int:
        return self._auto_indent

    @auto_indent.setter
    def auto_indent(self, value: int):
        self._auto_indent = value
        self.handler.auto_indent = value

    @property
    def tabsize(self) -> int:
        return self._tabsize

    @tabsize.setter
    def tabsize(self, value: int):
        self._tabsize = value
        self.handler.tabsize = value

    @property
    def tabspaces(self) -> bool:
        return self._tabspaces

    @tabspaces.setter
    def tabspaces(self, value: bool):
        self._tabspaces = value
        self.handler.insert_spaces_instead_of_tabs = value

    @property
    def idiom(self) -> str:
        return self._idiom

    @idiom.setter
    def idiom(self, value: str):
        self._idiom = value
        self.set_idiom(value)

    @property
    def word_wrap(self) -> bool:
        return self._word_wrap

    @word_wrap.setter
    def word_wrap(self, value: bool):
        self._word_wrap = value
        if value:
            self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        else:
            self.textview.set_wrap_mode(Gtk.WrapMode.NONE)

    @property
    def font(self) -> str:
        return self._selected_font

    @font.setter
    def font(self, value: str):
        if len(value) > 0:
            self._selected_font = value
            self.textview.modify_font(Pango.FontDescription(value))

    def set_idiom(self, idiom: str):
        """
        Sets app language translation idiom.
        :param idiom: Language idiom ex: en, pt, el, etc
        :type idiom: str
        :return: None
        :rtype: Any
        """
        if idiom in Settings.supported_idioms:
            lang = gettext.translation('base', localedir='locales', languages=[idiom])
            lang.install()
            self.handler.translate()
        else:
            print("Idiom '{}' is not supported!".format(idiom))

    # def set_tab_spaces(self):

    ''' INI file example
    [APP]
    ENVIRONMENT = test
    DEBUG = True
    # Only accept True or False
    
    [DATABASE]
    USERNAME = xiaoxu
    PASSWORD = xiaoxu
    HOST = 127.0.0.1
    PORT = 5432
    DB = xiaoxu_database
    '''

    def write_ini(self, file_path: str = '') -> (bool, str):
        """
        Writes settings values to config file.
        :param file_path: Settings file path.
        :type file_path: str
        :return: Returns True if succeeded, False with error message otherwise.
        :rtype: Tuple(bool, str)
        """
        msg = ""
        state = False
        try:
            if file_path == '':
                file_path = Settings.default_file_path()

            config = configparser.ConfigParser()
            config.add_section(Settings.secview)
            config[Settings.secview]["word_warp"] = str(self.word_wrap)
            config[Settings.secview]["font"] = self.font
            config[Settings.secview]["idiom"] = self.idiom

            config.add_section(Settings.seceditor)
            config[Settings.seceditor]["tabsize"] = str(self.tabsize)
            config[Settings.seceditor]["tabspaces"] = str(self.tabspaces)
            config[Settings.seceditor]["auto_indent"] = str(self.auto_indent)

            with open(file_path, 'w') as configfile:
                config.write(configfile)
        except:
            msg = gettext.gettext("An error occurred while writing config file.")
            return state, msg
        else:
            state = True
            return state, msg

    def read_ini(self, file_path: str = '') -> (bool, str):
        """
        Reads settings from config file.
        :param file_path: Settings file path.
        :type file_path: str
        :return: Returns True if succeeded, False with error message otherwise.
        :rtype: Tuple(bool, str)
        """
        msg = ""
        state = False
        try:
            if file_path == '':
                file_path = Settings.default_file_path()

            config = configparser.ConfigParser()
            config.read(file_path)

            self.word_wrap = bool(config[Settings.secview]["word_warp"])
            self.font = config[Settings.secview]["font"]
            self.idiom = config[Settings.secview]["idiom"]

            self.tabsize = int(config[Settings.seceditor]["tabsize"])
            self.tabspaces = bool(config[Settings.seceditor]["tabspaces"])
            self.auto_indent = bool(config[Settings.seceditor]["auto_indent"])

            # for section in config.sections():
            #    for key in config[section]:
            #        print((key, config[section][key]))
        except:
            msg = gettext.gettext("An error occurred while reading config file. Default values will be used.")
            return state, msg
        else:
            state = True
            return state, msg



    # read_ini("source/data/sample.ini")

    # ('environment', 'test')
    # ('debug', 'True')
    # ('username', 'xiaoxu')
    # ('password', 'xiaoxu')
    # ('host', '127.0.0.1')
    # ('port', '5432')
    # ('db', 'xiaoxu_database')

    '''
    def load_from_file(self):
        path = self.default_file_path
        datadict = dict()
        if len(path) == 0:
            return False, "File path is undefined!"
        else:
            if not os.path.exists(path):
                return False, "File not found at '{}'!".format(path)
            else:
                with open(file=path, mode='r', encoding='utf8') as f:
                    for line in f:
                        line = line.strip(' \t')
                        if line.startswith('#'):
                            continue  # ignore, it's a comment
                        else:
                            pairs = line.split('=')
                            if len(pairs != 2):
                                return False, "Settings file has an invalid format!\nExpected key=value pair in each line."
                            else:
                                key = pairs[0]
                                value = pairs[1]
                                # add to dict
                                datadict[key] = value

        if not datadict.get("idiom") is None:
            self.idiom = str(datadict.get("idiom"))
        else:
            return False, "Idiom setting missing."

        if not datadict.get("word_wrap") is None:
            self.word_wrap = str(datadict.get("word_wrap"))
        else:
            return False, "Word wrap setting missing."

        if not datadict.get("selected_font") is None:
            self.font = str(datadict.get("selected_font"))
        else:
            return False, "Selected font setting missing."

        return True, "OK"

    '''

    def setfontsize(self, size: int):
        """
        Sets current font size.
        :param size: Size in points.
        :type size: int
        :return: None
        :rtype: Any
        """
        result = ''
        font_str = self.font
        i = -1
        while not font_str[i].isspace():
            i -= 1

        if font_str[i].isspace():
            result = font_str[0:i] + ' ' + str(size)

        self.font = result

    def getfontsize(self) -> int:
        """
        Gets current font size.
        :return: Returns current font size.
        :rtype: int
        """
        font_str = self.font
        i = -1
        while not font_str[i].isspace():
            i -= 1

        if font_str[i].isspace():
            i += 1
            numstr = ''
            while i < 0 and font_str[i].isdigit():
                numstr += font_str[i]
                i += 1

            size = int(numstr)
            return size

        return 0

    # set default values
    def set_defaults(self):
        """
        Sets default values to all properties.
        :return: None
        :rtype: Any
        """
        self.word_wrap = True
        self.font = self.default_font
        self.idiom = self.default_idiom
        self.tabsize = self.default_tabsize
        self.tabspaces = self.default_tabspaces
        self.auto_indent = self.default_auto_indent

