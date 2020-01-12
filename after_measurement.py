from wx.lib.splitter import MultiSplitterWindow

import button_panel
from table import *


class AfterMeasurement(wx.Frame):

    def __init__(self, handler):
        wx.Frame.__init__(self, parent=None, title='Po Merani', size=(1080, 720))

        splitter = MultiSplitterWindow(self)
        buttons = button_panel.Buttons(handler, parent=splitter)

        for b in buttons.get_buttons():
            if b.GetLabel() not in ('Zastaviť meranie', 'OK'):
                b.Show()

        splitter.AppendWindow(buttons)
        grid = Table(splitter, buttons)
        splitter.AppendWindow(grid, grid.get_height() + 20)
        splitter.SetOrientation(wx.VERTICAL)
