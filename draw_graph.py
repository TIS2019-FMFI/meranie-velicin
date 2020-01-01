from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from wx.lib.splitter import MultiSplitterWindow

import button_panel
from table import *


class MyGraph(wx.Panel):
    # ....................................Rebeka........................................#
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

    def change_axes(self, min, max):
        self.axes.set_ylim(float(min), float(max))
        self.canvas.draw()


class DrawGraph(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Po Merani', size=(1080, 720))

        splitter = MultiSplitterWindow(self)
        self.buttons = button_panel.Buttons(splitter)

        for b in self.buttons.get_buttons():
            if b.GetLabel() not in ('Zastaviť meranie', 'Zobraziť graf', 'OK'):
                b.Show()

        splitter.AppendWindow(self.buttons)
        grid = MyGrid(splitter, self.buttons)
        splitter.AppendWindow(grid, grid.get_height() + 20)

        graph = MyGraph(splitter)
        splitter.AppendWindow(graph)
        graph.draw()

        splitter.SetOrientation(wx.VERTICAL)
