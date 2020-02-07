import wx.grid
from wx import *
from gtts import gTTS
from io import BytesIO
import pygame


class TablePanel(wx.Panel):

    def __init__(self, parent, buttons):
        wx.Panel.__init__(self, parent=parent)

        pygame.init()

        self.grid = wx.grid.Grid(self)
        self.grid.EnableEditing(False)
        self.grid.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)
        wx.Accessible(self.grid)
        self.buttons = buttons
        self.grid.SetDefaultRowSize(75)
        self.grid.SetDefaultColSize(125)
        self.rows, self.columns = 2, 8
        self.pointer = -1
        self.grid.CreateGrid(self.rows, self.columns)
        self.grid.SetColLabelSize(0)
        self.grid.EnableGridLines(True)
        self.font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.get_text)
        self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.get_text)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1)
        self.SetSizer(sizer)

        row_labels = ['Čas', 'Hodnota']
        for i in range(self.rows):
            self.grid.SetRowLabelValue(i, row_labels[i])

        self.last = None
        self.Bind(wx.EVT_KEY_DOWN, self.to_menu)

        self.last_time = None
        self.now_time = None
        self.after_measurement = False

    def to_menu(self, event):
        if event.GetUnicodeKey() == wx.WXK_TAB:
            self.buttons.get_visible()[0].SetFocus()
        else:
            event.Skip()

    def resize(self, num):
        self.grid.AppendCols(num)
        self.columns += num

    def add(self, time, value, load=False):
        if self.pointer + 1 == self.columns:
            self.resize(1)
        self.pointer += 1

        self.last = value

        try:
            if not load and self.pointer >= 7:
                self.scroll_table()
            self.grid.SetCellFont(0, self.pointer, self.font)
            self.grid.SetCellFont(1, self.pointer, self.font)
            self.grid.SetCellAlignment(0, self.pointer, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.grid.SetCellAlignment(1, self.pointer, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            time = (str(round(time, 2))).rstrip('0').rstrip('.')
            self.now_time = float(time)
            self.grid.SetCellValue(0, self.pointer, time)
            self.grid.SetCellValue(1, self.pointer, str(value))
            if not load:
                self.grid.SetGridCursor(1, self.pointer)
        except RuntimeError:
            return

    def scroll_table(self):
        self.grid.MoveCursorDown(False)
        self.grid.MoveCursorRight(False)

    def get_text(self, event):
        row = event.GetRow()
        col = event.GetCol()
        if self.grid.GetCellValue(row, col) == "":
            return
        self.speak(self.grid.GetCellValue(row, col))

    def speak(self, value, repeat=False):
        if ((self.last_time is None or (self.now_time - self.last_time) >= 5)
                or self.after_measurement or repeat):
            tts = gTTS(text=str(value), lang='sk')
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            self.last_time = self.now_time

    def read_last(self, event):
        if self.last is None:
            return
        self.speak(self.last, True)

    def show_scrollbar(self):
        self.grid.ShowScrollbars(wx.SHOW_SB_ALWAYS, wx.SHOW_SB_NEVER)

    def set_after_measurement(self):
        self.after_measurement = True
