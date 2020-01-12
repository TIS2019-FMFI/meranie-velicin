import time

from wx.lib.splitter import MultiSplitterWindow
from threading import Thread
import button_panel
from table import *


class Measurement(wx.Frame):

    def __init__(self, handler, measurement_data):

        wx.Frame.__init__(self, parent=None, title="Meranie", size=(1080, 720), pos=(243, 56))
        self.kill = False
        self.measurement_data = measurement_data
        self.thread = Thread(target=self.get_value, daemon=True)

        splitter = MultiSplitterWindow(self)
        self.buttons = button_panel.Buttons(handler, splitter)

        b = self.buttons.get_button('Zastaviť meranie')
        b.Show()
        b.Bind(wx.EVT_BUTTON, self.stop_click)

        splitter.AppendWindow(self.buttons)

        self.table_panel = Table(splitter, self.buttons)
        splitter.AppendWindow(self.table_panel, self.table_panel.get_height() + 20)
        splitter.SetOrientation(wx.VERTICAL)

    def stop_click(self, evt):
        self.Close()
        self.buttons.stop_click(evt)

    def get_value(self):
        while not self.kill:
            time.sleep(1)
            try:
                last_value = self.measurement_data.values[-1]
                print(last_value)
                self.table_panel.add(last_value[0], last_value[1][0])
            except IndexError:
                pass
