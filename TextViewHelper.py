import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango


class TextViewHelper:

    def __init__(self):
        pass

    @staticmethod
    def get_line_col_from_cursor(buffer: Gtk.TextBuffer) -> tuple:  # row, col
        """
        Gets the row and column of current cursor position
        :param buffer: The TextBuffer.
        :type buffer: Gtk.TextBuffer.
        :return: Returns tuple with row and column of cursor position (int, int) if succeeded, None otherwise.
        :rtype: tuple
        """
        iter_at_cursor: Gtk.TextIter = buffer.get_iter_at_mark(buffer.get_insert())
        if iter_at_cursor is not None:
            row: int = iter_at_cursor.get_line()
            col: int = iter_at_cursor.get_line_offset()
            return row, col
        else:
            return None

"""
    @staticmethod
    def get_iter_of_start_visible_line(textview: Gtk.TextView) -> Gtk.Iter:
        FResult = -1;
        winX = 1
        winY = 1
        result_buf_coords = textview.window_to_buffer_coords(Gtk.TextWindowType.WIDGET, winX, winY)
        if result_buf_coords is not None:
            bufX = result_buf_coords[0]
            bufY = result_buf_coords[1]
            result = textview.get_iter_at_position(bufX, bufY)
            if result is not None:
                pos_overText = result[0]
                FResult = result[1]
                end_iter = Gtk.TextIter()

                while FResult.forward_visible_lines(1):
                    pass

                end_iter = FResult

        return FResult

"""

