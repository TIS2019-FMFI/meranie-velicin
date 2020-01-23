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

    def draw(self, values):
        # tuple in form: (time, (value, unit))
        x = []
        y = []
        for i in values:
            x.append(i[0])
            y.append(i[1][0])
        self.axes.plot(x, y)

    # TODO parameter names shadowing built-ins
    def change_axes(self, min, max):
        self.axes.set_ylim(float(min), float(max))
        self.canvas.draw()


class DrawGraph:

    def __init__(self, handler, parent):
        parent.panelHandler.clear()
        self.parent = parent
        self.buttons = button_panel.Buttons(handler, parent.splitter)
        self.grid = Table(parent.splitter, self.buttons)
        self.graph = MyGraph(parent.splitter)
        parent.panelHandler.add(self.buttons)
        parent.panelHandler.add(self.grid, self.grid.get_height() + 20)
        parent.panelHandler.add(self.graph)
        self.graph.draw()
