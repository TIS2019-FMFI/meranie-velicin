import random

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from wx.lib.splitter import MultiSplitterWindow
import button_panel
from table import *


class MyGraph(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.axes.set_xlabel("ČAS")
        self.axes.set_ylabel("HODNOTA")

    def draw(self):
        x = []
        y = []
        for i in range(20):
            x.append(i * 4)
            y.append(random.randrange(10, 40))
        self.axes.plot(x, y)

    # TODO parameter names shadowing built-ins
    def change_axes(self, min, max):
        self.axes.set_ylim(float(min), float(max))
        self.canvas.draw()


class DrawGraph(wx.Frame):

    def __init__(self, handler):
        wx.Frame.__init__(self, parent=None, title='Po Merani', size=(1080, 720), pos=(243, 56))

        splitter = MultiSplitterWindow(self)
        self.buttons = button_panel.Buttons(handler, parent=splitter)

        x, y = 0, 0
        gap = 30

        for b in self.buttons.get_buttons():
            if b.GetLabel() not in ('Zastaviť meranie', 'Zobraziť graf', 'OK'):
                b.Show()
                b.SetPosition((x, y))
                x += b.GetTextExtent(b.GetLabel()).GetWidth() + gap
                # if b.GetLabel().startswith('Nov'):
                #     b.Bind(wx.EVT_BUTTON, self.new_measurement)

        splitter.AppendWindow(self.buttons)
        grid = Table(splitter, self.buttons)
        splitter.AppendWindow(grid, grid.get_height() + 20)

        graph = MyGraph(splitter)
        splitter.AppendWindow(graph)
        graph.draw()

        splitter.SetOrientation(wx.VERTICAL)
