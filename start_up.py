import button_panel
import wx
from wx.lib.splitter import MultiSplitterWindow

from handler import Handler


class PanelHandler:
    def __init__(self, frame, splitter):
        self.frame = frame
        self.splitter = splitter
        self.windows = []

    def clear(self):
        for w in self.windows:
            self.splitter.DetachWindow(w)
            w.Destroy()
        self.windows.clear()

    def add(self, panel, sash_pos=-1):
        self.windows.append(panel)
        self.splitter.AppendWindow(panel, sash_pos)
        print(panel.GetPosition())


class Start(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Multimeter', size=(1080, 720), pos=(243, 56))
        self.splitter = MultiSplitterWindow(self)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.splitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(main_sizer)
        self.splitter.SetOrientation(wx.VERTICAL)

        self.handler = Handler()
        self.handler.parent_window = self
        self.buttons = button_panel.Buttons(self.handler, self.splitter)

        self.panelHandler = PanelHandler(self, self.splitter)
        self.panelHandler.add(self.buttons)

        self.buttons.button_handler('start')


if __name__ == "__main__":
    app = wx.App()
    start = Start()
    start.Show()
    app.MainLoop()
