from wx.lib.splitter import MultiSplitterWindow
import button_panel
from table import *


class Measurement(wx.Frame):

    def __init__(self, handler, measurement_data):
        wx.Frame.__init__(self, parent=None, title="Meranie", size=(1080, 720), pos=(243, 56))
        self.kill = False
        self.handler = handler
        self.measurement_data = measurement_data

        splitter = MultiSplitterWindow(self)
        self.buttons = button_panel.Buttons(handler, splitter)

        splitter.AppendWindow(self.buttons)

        self.table_panel = Table(splitter, self.buttons)
        splitter.AppendWindow(self.table_panel, self.table_panel.get_height() + 20)
        splitter.SetOrientation(wx.VERTICAL)
