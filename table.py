import wx.grid
from wx import *


class Table(wx.Panel):

    def __init__(self, parent, buttons):
        wx.Panel.__init__(self, parent=parent)

        self.upper_panel = parent

        self.grid = wx.grid.Grid(self, -1)
        wx.Accessible(self.grid)
        self.buttons = buttons
        self.grid.SetDefaultRowSize(75)
        self.grid.SetDefaultColSize(75)
        self.rows, self.columns = 2, 15
        self.pointer = -1
        self.grid.CreateGrid(self.rows, self.columns)
        self.grid.SetColLabelSize(0)
        self.grid.EnableGridLines(True)
        self.font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.get_text)
        self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.get_text)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
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

    def exit(self):
        self.buttons.getButtons()[0].SetFocus()

    def to_grid(self):
        if isinstance(self.FindFocus(), type(self.grid)):
            self.grid.SetGridCursor(0, 0)

    def resize(self, num):
        self.grid.AppendCols(num)
        self.columns += num

    def add(self, time, value):
        if self.pointer + 1 == self.columns:
            self.resize(1)
        self.pointer += 1

        self.grid.SetReadOnly(0, self.pointer)
        self.grid.SetReadOnly(1, self.pointer)
        self.grid.SetCellFont(0, self.pointer, self.font)
        self.grid.SetCellFont(1, self.pointer, self.font)
        self.grid.SetCellAlignment(0, self.pointer,
                                   wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.grid.SetCellAlignment(1, self.pointer,
                                   wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.grid.SetCellValue(0, self.pointer, str(time))
        self.grid.SetCellValue(1, self.pointer, str(value))

        # TODO updating possibly unnecessary
        self.Update()

    # TODO returns a constant
    def get_height(self):
        return self.rows * 75

    def get_text(self, event):
        row = event.GetRow()
        col = event.GetCol()
        return self.grid.GetCellValue(row, col)
