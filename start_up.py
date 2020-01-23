import button_panel
import wx
from wx.lib.splitter import MultiSplitterWindow
from panel_handler import PanelHandler


class Start(wx.Frame):

    def __init__(self, handler):
        wx.Frame.__init__(self, parent=None, title='Multimeter', size=(1080, 720), pos=(243, 56))
        self.splitter = MultiSplitterWindow(self)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.splitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(main_sizer)
        self.splitter.SetOrientation(wx.VERTICAL)

        self.handler = handler
        self.handler.window = self
        self.buttons = button_panel.Buttons(self.handler, self.splitter)

        self.table_panel = None
        self.panel_handler = PanelHandler(self, self.splitter)
        self.panel_handler.handle('start')
