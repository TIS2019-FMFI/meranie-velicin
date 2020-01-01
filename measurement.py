from wx.lib.splitter import MultiSplitterWindow

import button_panel
from table import *


class Measurement(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Meranie", size=(1080, 720))

        splitter = MultiSplitterWindow(self)
        buttons = button_panel.Buttons(splitter)

        buttons.show_button('Zastaviť meranie')

        splitter.AppendWindow(buttons)
        grid = MyGrid(splitter, buttons)
        splitter.AppendWindow(grid, grid.get_height() + 20)
        splitter.SetOrientation(wx.VERTICAL)
