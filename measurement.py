import time

from wx.lib.splitter import MultiSplitterWindow
from threading import Thread
import button_panel
from table import *


class Measurement(wx.Frame):

    kill = False

    def __init__(self, handler, measurement_data):

        wx.Frame.__init__(self, parent=None, title="Meranie", size=(1080, 720), pos=(243, 56))

        self.measurement_data = measurement_data
        self.thread = Thread(target=self.get_value)

        splitter = MultiSplitterWindow(self)
        self.buttons = button_panel.Buttons(handler, splitter)

        b = self.buttons.get_button('Zastaviť meranie')
        b.Show()
        b.Bind(wx.EVT_BUTTON, self.stop_click)

        splitter.AppendWindow(self.buttons)
        grid = MyGrid(splitter, self.buttons)
        splitter.AppendWindow(grid, grid.get_height() + 20)
        splitter.SetOrientation(wx.VERTICAL)

    def stop_click(self, evt):
        self.Close()
        self.buttons.stop_click(evt)

    def get_value(self):
        while not self.kill:
            time.sleep(1)
            try:
                print(self.measurement_data.values[-1])
            except IndexError:
                pass
