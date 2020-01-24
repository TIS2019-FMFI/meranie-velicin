from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from table import *


class Graph(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, wx.EXPAND)
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
