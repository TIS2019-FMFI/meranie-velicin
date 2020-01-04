from wx.lib.splitter import MultiSplitterWindow

import button_panel
from table import *


class AfterMeasurement(wx.Frame):

    def __init__(self, handler):
        wx.Frame.__init__(self, parent=None, title='Po Merani', size=(1080, 720), pos=(243, 56))

        splitter = MultiSplitterWindow(self)
        self.buttons = button_panel.Buttons(handler, parent=splitter)

        x, y = 0, 0
        gap = 30

        for b in self.buttons.get_buttons():
            if b.GetLabel() not in ('Zastaviť meranie', 'OK'):
                b.Show()
                b.SetPosition((x, y))
                x += b.GetTextExtent(b.GetLabel()).GetWidth() + gap
                if b.GetLabel().startswith('Nov'):
                    b.Bind(wx.EVT_BUTTON, self.new_meas)
                elif b.GetLabel().startswith('Zobraz'):
                    b.Bind(wx.EVT_BUTTON, self.graph)

        splitter.AppendWindow(self.buttons)
        grid = MyGrid(splitter, self.buttons)
        splitter.AppendWindow(grid, grid.get_height() + 20)

        splitter.SetOrientation(wx.VERTICAL)

    def new_meas(self, event):
        self.Close()
        self.buttons.new_meas(event)

    def graph(self, event):
        self.Close()
        self.buttons.display_graph(event)
