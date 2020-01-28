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
        self.grid.SetDefaultColSize(75)
        self.rows, self.columns = 2, 13
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

        random_id = wx.ID_ANY
        self.Bind(wx.EVT_MENU, self.exit, id=random_id)

        button_list = self.buttons.get_buttons()
        button_list[-1].Bind(wx.EVT_KILL_FOCUS, self.to_grid())

        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('M'), random_id)])
        self.SetAcceleratorTable(accel_tbl)

        self.last = None

    def exit(self):
        self.buttons.getButtons()[0].SetFocus()

    def to_grid(self):
        if isinstance(self.FindFocus(), type(self.grid)):
            self.grid.SetGridCursor(0, 0)

    def resize(self, num):
        self.grid.AppendCols(num)
        self.columns += num

    def add(self, time, value, load=False):
        if self.pointer + 1 == self.columns:
            self.resize(1)
        self.pointer += 1

        self.last = value

        try:
            if not load and self.pointer >= 13:
                self.scroll_table()
            self.grid.SetCellFont(0, self.pointer, self.font)
            self.grid.SetCellFont(1, self.pointer, self.font)
            self.grid.SetCellAlignment(0, self.pointer, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.grid.SetCellAlignment(1, self.pointer, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.grid.SetCellValue(0, self.pointer, str(time))
            self.grid.SetCellValue(1, self.pointer, str(value))
            if not load:
                self.scroll_table()
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

    @staticmethod
    def speak(value):
        tts = gTTS(text=str(value), lang='sk')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()

    def read_last(self, event):
        if self.last is None:
            return
        self.speak(self.last)

    def show_scrollbar(self):
        self.grid.ShowScrollbars(wx.SHOW_SB_ALWAYS, wx.SHOW_SB_NEVER)
