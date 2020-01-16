import button_panel
import wx
from wx.lib.splitter import MultiSplitterWindow

from handler import Handler


class PanelSwitchingHandler:
    def __init__(self, frame, splitter):
        self.frame = frame
        self.splitter = splitter

    def replace(self, index, oldPanel, newPanel):
        self.splitter.ReplaceWindow(oldPanel, newPanel)
        oldPanel.Destroy()
        if index == 1:
            self.frame.p1 = newPanel
        elif index == 2:
            self.frame.p2 = newPanel
        elif index == 3:
            self.frame.p3 = newPanel


class Start(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Start', size=(1080, 720), pos=(243, 56))
        self.splitter = MultiSplitterWindow(self)

        self.p1 = wx.Panel(self)
        self.p2 = wx.Panel(self)
        self.p3 = wx.Panel(self)

        self.splitter.AppendWindow(self.p1, 720)
        self.splitter.AppendWindow(self.p2)
        self.splitter.AppendWindow(self.p3)

        self.splitter.SetOrientation(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.splitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(main_sizer)

        self.splitter.SetOrientation(wx.VERTICAL)

        self.handler = Handler()
        self.handler.parent_window = self
        self.buttons = button_panel.Buttons(self.handler, self.splitter)

        self.panelSwitcher = PanelSwitchingHandler(self, self.splitter)
        self.panelSwitcher.replace(1, self.p1, self.buttons)

        self.buttons.button_handler('start')


if __name__ == "__main__":
    app = wx.App()
    start = Start()
    start.Show()
    app.MainLoop()
