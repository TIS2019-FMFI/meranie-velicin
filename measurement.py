import time

from wx.lib.splitter import MultiSplitterWindow
from threading import Thread
import button_panel
from table import *


class Measurement(wx.Frame):

    kill = False

    def __init__(self, measurement_data):
        wx.Frame.__init__(self, parent=None, title="Meranie", size=(1080, 720))

        self.measurement_data = measurement_data
        self.thread = Thread(target=self.get_value)

        splitter = MultiSplitterWindow(self)
        buttons = button_panel.Buttons(splitter)

        buttons.show_button('Zastaviť meranie')

        splitter.AppendWindow(buttons)
        grid = MyGrid(splitter, buttons)
        splitter.AppendWindow(grid, grid.get_height() + 20)
        splitter.SetOrientation(wx.VERTICAL)

    def get_value(self):
        while not self.kill:
            time.sleep(1)
            try:
                print(self.measurement_data.values[-1])
            except IndexError:
                pass
