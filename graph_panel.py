from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import wx
import threading
from pipigraph import PipiGraph


class GraphPanel(wx.Panel):

    def __init__(self, parent, values):
        wx.Panel.__init__(self, parent=parent)
        self.figure = Figure()
        self.values = values
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.axes.set_xlabel("ČAS")
        self.axes.set_ylabel("HODNOTA")
        self.draw()

        self.thread = threading.Thread(target=self.beep)
        self.thread.start()

    def draw(self):
        x = []
        y = []
        for i in self.values:
            x.append(i[0])
            y.append(i[1][0])
        self.axes.plot(x, y)

    def beep(self):
        ppg = PipiGraph(self.values)
        ppg.read_values()
