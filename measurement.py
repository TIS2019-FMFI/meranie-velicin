import time

from wx.lib.splitter import MultiSplitterWindow
from threading import Thread
import button_panel
from table import *


class Measurement(wx.Frame):

    def __init__(self, handler, measurement_data):

        wx.Frame.__init__(self, parent=None, title="Meranie", size=(1080, 720))

        self.kill = False
        self.measurement_data = measurement_data
        self.thread = Thread(target=self.get_value)

        splitter = MultiSplitterWindow(self)
        buttons = button_panel.Buttons(handler, splitter)

        buttons.show_button('Zastaviť meranie')

        splitter.AppendWindow(buttons)

        self.table_panel = Table(splitter, buttons)
        splitter.AppendWindow(self.table_panel, self.table_panel.get_height() + 20)
        splitter.SetOrientation(wx.VERTICAL)

    def get_value(self):
        while not self.kill:
            time.sleep(1)
            try:
                last_value = self.measurement_data.values[-1]
                self.table_panel.add(last_value[0], last_value[1][0])
            except IndexError:
                pass
